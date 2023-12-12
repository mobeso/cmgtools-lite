import ROOT 
import os, sys, re
from optparse import OptionParser
import json

'''
This script writes a json file with runs and lumisections from a given dataset.
You can also filter by a goldenJson to check only certified runs and lumisections
'''


default_datasets = ["EGamma", "SingleMuon", "DoubleMuon", "Muon", "JetHT", "MET", "MuonEG", "JetMET"]


def add_parsing_options():
  ''' Parsing arguments '''
  parser = OptionParser(usage = "python buildJSONfromNano.py [options]")
  parser.add_option("--inpath", dest = "inpath",  
                    help = "input path where datasets are stored.")
  parser.add_option("--outpath", dest = "outpath",  default = "jsonfiles",
                    help = "input path where datasets are stored.")
  parser.add_option("--datasets", dest = "datasets", action="append",
                    help = "Datasets to process from the input folder. By default it searches for %s."%default_datasets)
  parser.add_option("--filterjson", dest = "filterjson", default = None, 
                    help = "Parse a golden json to filter certified lumisections.")
  parser.add_option("--filter-by-era",  dest = "filter_era",
                    help = "Search for datasets in a given era only. Format: Run2022X, X has to be the era identifier.")
  parser.add_option("--filter-by-version",  dest = "filter_version",
                    help = "Search for datasets of a given version (v1, v1-v1, v2...)")
  parser.add_option("--verbose", dest = "verbose", action = "store_true", default = True,
                    help = "Add verbosity.")
  return parser.parse_args()

def load_json(jsonfile):
  with open(jsonfile, "r") as jsondata:
    data = json.load(jsondata)
  return data

def check_match(matchstring, string, makeSure = ""):
  ''' Function to match strings and return true if matching exists '''
  matches = True
  try:
    re.match(matchstring, string).groups()
  except AttributeError: # It does not match
    matches = False
  return matches

if __name__ == "__main__":
  # -- Unpack arguments and options -- #
  opts, args     = add_parsing_options()
  mainDir         = opts.inpath
  outpath        = opts.outpath
  datasets       = opts.datasets
  if datasets == None: datasets = default_datasets
  goldenJson     = opts.filterjson
  filter_era     = opts.filter_era
  filter_version = opts.filter_version
  verbosity      = opts.verbose

  certifiedRuns = None  # By default, do not filter with goldenJson
  outname = "lumi" # Default_name

  # -- Remove the last "/" --> regexp matching is sensitive to this
  if mainDir[-1] == "/": mainDir = mainDir[:-1]
  if filter_era:
    print((" Filtering by era: %s"%filter_era))
    outname += "_Era%s"%filter_era
  if filter_version:
    print((" Filtering by version: %s"%filter_version))
    outname += "_%s"%filter_version

  outname += ".json"
  # -- Fetch the files from where to extract runs and lumi blocks -- #
  files_per_dataset = { d : [] for d in datasets }
  ## Do a recursive search to find the rootfiles
  ## this should work for any given format of the input path.
  for root, dirs, files in os.walk(mainDir): 
    inputFiles = [file_ for file_ in files if (".root" in file_ and "log" not in root)]
    if len(inputFiles) == 0: continue
    dataset = re.match("%s/(.*)"%mainDir, root).groups()[0].split("/")[0] # Get the name of the dataset 
    print(dataset)
    if dataset not in datasets: continue
    filters = []
    if filter_era: 
      filters.append( check_match(".*(%s).*"%filter_era, root) )
    if filter_version:
      filters.append( check_match(".*(-|_)(%s)\/.*"%filter_version, root, filter_version) )
      # Extra care:
      if filter_version == "v1" and ("v1-v1" in root or "v1_v1" in root or "v1-v2" in root or "v1-v3" in root): continue
    print("hola", (filters, root, dataset)) 
    if not all(filters): continue
    
    print((" >> Getting files for dataset %s (folder: %s)"%(dataset, root)))
    for file_ in inputFiles:
      files_per_dataset[dataset].append(root + "/%s"%file_)

  # -- Write the json files -- #
  for d in datasets:
    inputFiles = files_per_dataset[d]
    if len(inputFiles) == 0:
      continue
    print((" >> Writing json for dataset %s"%d))
    
    if goldenJson != None:
      certifiedRuns = load_json(goldenJson)
      begin_run, end_run = re.match(".*_.*_(.*)_(.*)_.*", goldenJson).groups()
      outname = outname.replace(".json", "_filteredGolden%s_%s.json"%(begin_run, end_run))
    
    ## Get runs and lumiblocks (and filter by goldenJson if needed)
    runs = {}
    minrun = 99999999999999
    maxrun = 0
    print((" ----- There are %d datasets"%len(inputFiles)))    
    for f in inputFiles:
      if verbosity: print(("   * Reading %s"%f))
      ff    = ROOT.TFile(f, "READ")
      lumis = ff.Get("LuminosityBlocks")
      if type(lumis) == ROOT.TObject:
        print(("File %s could not be read"%f))
        continue
 
     
      for ev in lumis:
        run       = ev.run
        lumiblock = ev.luminosityBlock
        if run < minrun: minrun = run
        if run > maxrun: maxrun = run
        
        ## Check if it is need to filter by the goldenJson
        if certifiedRuns != None:
          runstring = str(run) # To read the keys in the goldenJson, which are unicode.

          ## Filter by run
          if runstring not in list(certifiedRuns.keys()): continue # If the run is not in the golden json just skip it
          
          ## Filter by lumisection/lumiblock
          validLumis = certifiedRuns[runstring] 
          not_certified = []
          #print("\t- Checking lumi: %s"%lumiblock) 
          for lumi_low, lumi_hi in validLumis:
              ## Check if current LS is contained within each of the lumi ranges in the goldenJson
              isNotValid = not(lumi_low <= lumiblock and lumiblock <= lumi_hi)
              #print("\t >> Is it between %d and %d? %s"%(lumi_low, lumi_hi, not isNotValid))
              not_certified.append( isNotValid )
          ## If the current lumiblock is not in any of the goldenJson ranges for this run, then discard the event.
          if all(not_certified): 
            #print("\t >>> LS: %d not valid"%lumiblock)
            continue

        ## Save run and lumiblock 
    
        if run in list(runs.keys()): 
          runs[run].append(lumiblock)
        else: 
          runs[run] = [lumiblock]
      # -- Build the output json -- #
      forjson = {}
      for key in list(runs.keys()):
        forjson[str(key)] = []
        templist = runs[key] 
        templist.sort() 
        saving = False
        start  = 0 
        end    = 0
        for t in templist:
          if not saving:
            saving = True
            start = t
            end = t
          elif t == end +1:
            end = t 
          else:
            forjson[str(key)].append([start, end])
            start = t
            end = t
        forjson[str(key)].append([start,end])

      if not (os.path.exists("%s/%s"%(outpath, d))): os.system("mkdir -p %s/%s"%(outpath, d))
      json.dump(forjson, open("%s/%s/%s"%(outpath, d, outname),"w"), sort_keys=True)
    print(("min range: %d"%min(runs.keys())))
    print(("max range: %d"%max(runs.keys())))
    print(("min range 2: %d"%minrun))
    print(("max range 2: %d"%maxrun))
