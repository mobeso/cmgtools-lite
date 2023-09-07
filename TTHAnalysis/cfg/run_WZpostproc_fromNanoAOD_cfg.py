'''
Based on @cericeci's postprocessor
-----------------------------------
Config file defines two things: POSTPROCESSOR and selectedComponents. 
 * selectedComponents is read by the submitter to configure the different samples. 
 * POSTPROCESSOR is read at running time, and configures the modules to run 
   using the json file produced.
-----------------------------------
'''

# -- Import libraries -- #
### Main
import re, os, sys
from copy import deepcopy
### CMGTools
from CMGTools.RootTools.samples.configTools import printSummary, mergeExtensions, doTestN, configureSplittingFromTime, cropToLumi
from CMGTools.RootTools.samples.autoAAAconfig import autoAAA
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

### For crab submission
from PhysicsTools.HeppyCore.framework.heppy_loop import getHeppyOption


def byCompName(components, regexps):
  return [ c for c in components if any(re.match(r, c.name) for r in regexps) ]


# -- Unpack submission configurations  -- #
year              = getHeppyOption("year", "2022")    
analysis          = getHeppyOption("analysis", "main") 
selectComponents  = getHeppyOption('selectComponents')
justSummary       = getHeppyOption("justSummary")
test              = getHeppyOption("test")
preprocessor      = 0
quiet             = not(getHeppyOption("verboseAAA", False))
applyTriggersInMC = getHeppyOption('applyTriggersInMC')

### Prepare samples for submission 
doData = (selectComponents == "DATA")

# -- Import sample configuration files -- #
### THESE FILES NEED TO BE UPDATED ONCE RUN3 DATASETS ARE MADE PUBLIC


# -- From prenano 2022 -- september (nanoAOD for ttrun3)
#from CMGTools.RootTools.samples.samples_13p6TeV_2022_preNanoAODv10     import samples as mcSamples_
#from CMGTools.RootTools.samples.samples_13p6TeV_DATA2022_preNanoAODv10 import dataSamples as allData

# -- From 13.5fb-1 (november 2022 -- BCDE)
#from CMGTools.RootTools.samples.samples_13p6TeV_mc2022_nanoAODv10_fromLocal   import mcSamples_toImport   as mcSamples_
#from CMGTools.RootTools.samples.samples_13p6TeV_data2022_nanoAODv10_fromLocal import dataSamples_toImport as allData

# -- From ~10 fb-1 (preEE)
if year == "2022":
  from CMGTools.RootTools.samples.samples_13p6TeV_mc2022_nanoAODv11_fromLocal   import mcSamples_toImport   as mcSamples_
  allData = []
#  from CMGTools.RootTools.samples.samples_13p6TeV_data2022_nanoAODv11_fromLocal import dataSamples_toImport as allData

# -- From 20.06 fb-1 (March 2023 -- FG -- postEE)
elif year == "2022EE":
  from CMGTools.RootTools.samples.samples_13p6TeV_mc2022EE_nanoAODv11_fromLocal   import mcSamples_toImport   as mcSamples_
  from CMGTools.RootTools.samples.samples_13p6TeV_data2022EE_nanoAODv11_fromLocal import dataSamples_toImport as allData

# -- From 2018 UL: to do preliminary studies before having all the MC ready
elif year == "2018":
  from CMGTools.RootTools.samples.samples_13p6TeV_mc2018_nanoAODv11_fromLocal   import mcSamples_toImport   as mcSamples_
  from CMGTools.RootTools.samples.samples_13p6TeV_data2022EE_nanoAODv11_fromLocal import dataSamples_toImport as allData
  if doData:
    print(" ERROR: Cannot use 2018 data for Run3 processing!!!! Only MC")
    sys.exit()
  yearstr = "2022EE"
  year = 2022 # Effectively this is used for 2022

autoAAA(mcSamples_ + allData, 
        quiet         = quiet, 
        redirectorAAA = "xrootd-cms.infn.it",
        node          = 'T2_ES_IFCA') 
mcSamples_, _ = mergeExtensions(mcSamples_) ### autoAAA must be created before call mergeExtensions

# From now on, just use 2022 for everything
if year == "2022EE" or year == "2022": 
  yearstr = year
  year = 2022

### Set up trigger paths 
if year == 2022:
  from CMGTools.TTHAnalysis.tools.nanoAOD.triggers_13p6TeV_DATA2022 import triggerGroups_dict

DatasetsAndTriggers = {}; DatasetsAndVetos = {} 

### Double muon
DatasetsAndTriggers["DoubleMuon"] = triggerGroups_dict["triggers_mumu_iso"][year]
DatasetsAndTriggers["DoubleMuon"].extend(triggerGroups_dict["triggers_3mu"][year])

### MuonEG
DatasetsAndTriggers["MuonEG"] = triggerGroups_dict["triggers_2mu1e"][year]
DatasetsAndTriggers["MuonEG"].extend(triggerGroups_dict["triggers_mue"][year])
DatasetsAndTriggers["MuonEG"].extend(triggerGroups_dict["triggers_2e1mu"][year])
DatasetsAndTriggers["MuonEG"].extend(triggerGroups_dict["triggers_mue_noiso"][year])

### E-Gamma
DatasetsAndTriggers["EGamma"] = triggerGroups_dict["triggers_3e"][year] 
DatasetsAndTriggers["EGamma"].extend(triggerGroups_dict["triggers_ee"][year])
DatasetsAndTriggers["EGamma"].extend(triggerGroups_dict["triggers_ee_noniso"][year])
DatasetsAndTriggers["EGamma"].extend(triggerGroups_dict["triggers_1e_iso"][year])
#DatasetsAndTriggers["EGamma"].extend(deepcopy(triggerGroups_dict["triggers_etau"])

### SingleMuon
DatasetsAndTriggers["SingleMuon"] = triggerGroups_dict["triggers_1mu_iso"][year]
#DatasetsAndTriggers["SingleMuon"].extend(deepcopy(triggerGroups_dict["triggers_mutau"])

### Muon dataset = DoubleMuon + SingleMuon (from era D onwards)
DatasetsAndTriggers["Muon"] = deepcopy(DatasetsAndTriggers["DoubleMuon"])
DatasetsAndTriggers["Muon"].extend(deepcopy(DatasetsAndTriggers["SingleMuon"]))

### MET
DatasetsAndTriggers["JetMET"] = triggerGroups_dict["triggers_met"][year]
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_htmet"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_metNoMu100_mhtNoMu100"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_pfht"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_pfht1050"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_pfht800_mass50"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_pfjet500"][year])
DatasetsAndTriggers["JetMET"].extend(triggerGroups_dict["triggers_pfjet400_mass30"][year])


### TRIGGER OVERLAP REMOVAL: inherited from tt-run3 analysis
# -- Do not veto MuonEG datasets
DatasetsAndVetos["MuonEG"]     = [] 

# -- Veto DoubleMuon with MuonEG
DatasetsAndVetos["DoubleMuon"] = deepcopy(DatasetsAndTriggers["MuonEG"])

# -- Same for Muon
DatasetsAndVetos["Muon"]       = deepcopy(DatasetsAndTriggers["MuonEG"])

# -- Veto EGamma with the remaining datasets
DatasetsAndVetos["EGamma"]     = deepcopy(DatasetsAndTriggers["MuonEG"])
DatasetsAndVetos["EGamma"].extend(deepcopy(DatasetsAndTriggers["DoubleMuon"])) 
DatasetsAndVetos["EGamma"].extend(deepcopy(DatasetsAndTriggers["Muon"])) 

# -- Same for SingleMuon
DatasetsAndVetos["SingleMuon"] = deepcopy(DatasetsAndTriggers["MuonEG"])
DatasetsAndVetos["SingleMuon"].extend(deepcopy(DatasetsAndTriggers["DoubleMuon"]))
DatasetsAndVetos["SingleMuon"].extend(deepcopy(DatasetsAndTriggers["EGamma"]))

# -- Do not veto MET triggers with lepton triggers. That way we can use JetMET samples
#    to measure trigger efficiencies. 
DatasetsAndVetos["JetMET"] = []

selectedComponents = []

if doData:
  dataSamples = []
  for pd, trigs in DatasetsAndTriggers.items():
    if not trigs: continue
    for comp in byCompName(allData, [pd+"_"]):
      print("---")
      print(("Adding to %s dataset"%comp.name))
      comp.triggers = trigs[:]
      print((" >> triggers %s"%trigs[:]))
      comp.vetoTriggers = DatasetsAndVetos[pd][:]
      print((" >> vetoTriggers %s"%DatasetsAndVetos[pd][:]))
      dataSamples.append(comp)
  selectedComponents = dataSamples 
else:
  mcSamples = byCompName(mcSamples_, ["%s(|_PS)$"%dset for dset in [
      # ----------------- Single boson
      "WtoLnu_2jets",
      # ----------------- Drell Yan
      "DYJetsToLL_M50",
      "DYJetsToLL_M10to50",
      # ----------------- ttbar
      "TTTo2L2Nu",
      "TTTo2J1L1Nu",
      # ----------------- single top + tW
      "TbarBQ_t",
      "TBbarQ_t",
      "TbarWplus",
      "TWminus",
      # ----------------- conversions
      #"TTGJets",
      #"TTGJets_ext", 
      #"TGJets_lep",
      #"WGToLNuG_01J",
      #"WGToLNuG", 
      #"ZGTo2LG",
      # ----------------- ttV
      #"TTWToLNu_fxfx", 
      #"TTZToLLNuNu", 
      #"TTZToLLNuNu_m1to10",
      #'TTWToLNu', 
      #"TTWToLNu_EWK",
      # ----------------- ttH + tHq/tHW
      #"TTHnobb_pow",
      #"THQ", 
      #"THW", 
      #"TTH_ctcvcp",
      #'TTH_pow',
      # ----------------- Top + V rare processes
      #"TZQToLL",
      #"tWll",
      # "TTWW","TTWW_LO",
      #'TTTT_P8M2T4','TTTT',
      #'tZq_ll_1','tZq_ll_2',
      # ----------------- Diboson
      "WZto3LNu",
      "ZZto4l",
      "ZZto2L2Nu",
      "ZZto2L2Q",
      "WW",
      #"WWTo2L2Nu"
      #"WW_DPS", 
      #"WpWpJJ",
      #"WWTo2L2Nu_DPS",
      # ----------------- TRIBOSON  
      "WWW",
      "WWZ",
      "WZZ", 
      "ZZZ",
      "WZG",
      # ----------------- Other Higgs processes
      "ggHtoZZto4L",
      #"qqHZZ4L", 
      #"VHToNonbb", 
      #"VHToNonbb_ll", 
      #"ZHTobb_ll", 
      #"ZHToTauTau", 
      #"TTWH", 
      #"TTZH",
  ]])

  # -- Apply trigger in MC -- # 
  mcTriggers = sum((trigs for (pd,trigs) in DatasetsAndTriggers.items() if trigs), [])
  if applyTriggersInMC :
      for comp in mcSamples:
          comp.triggers = mcTriggers
  selectedComponents = mcSamples 

# -- Create the submitter -- #
autoAAA(selectedComponents, 
        quiet=quiet, 
        redirectorAAA="xrootd-cms.infn.it")

### Configure for efficient processing
if not doData:
  if year==2022:
      configureSplittingFromTime(byCompName(mcSamples,['^(?!(TTJets_Single|T_|TBar_)).*']),150 if preprocessor else 10,12)
      configureSplittingFromTime(byCompName(mcSamples,['^(TTJets_Single|T_|TBar_).*']),70 if preprocessor else 10,12)
      #configureSplittingFromTime(dataSamples,50 if preprocessor else 5,12)
  else: # rerunning deepFlavor can take up to twice the time, some samples take up to 400 ms per event
      configureSplittingFromTime(byCompName(mcSamples,['^(?!(TTJets_Single|T_|TBar_)).*']),300 if preprocessor else 10,12)
      configureSplittingFromTime(byCompName(mcSamples,['^(TTJets_Single|T_|TBar_).*']),150 if preprocessor else 10,12)
      #configureSplittingFromTime(dataSamples,100 if preprocessor else 5,12)
      #configureSplittingFromTime(byCompName(dataSamples,['Single']),50 if preprocessor else 5,12)
selectedComponents, _ = mergeExtensions(selectedComponents)


if analysis == "main" and not doData:
    cropToLumi(byCompName(selectedComponents, ["^(?!.*(TTH|TTW|TTZ)).*"]),1000.)
    cropToLumi(byCompName(selectedComponents, ["T_","TBar_"]),100.)
    cropToLumi(byCompName(selectedComponents, ["DYJetsToLL"]),2.)


# print summary of components to process
if justSummary: 
    printSummary(selectedComponents)
    sys.exit(0)


from CMGTools.TTHAnalysis.tools.nanoAOD.wzsm_modules import lepCollector,lepCollector_EE,lepCollector_data, lepCollector_EE_data
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

# in the cut string, keep only the main cuts to have it simpler
modules = []
if yearstr == "2022":
  if doData:
    modules = lepCollector_data 
  else:
    modules = lepCollector
elif yearstr == "2022EE":
  if doData:
    modules = lepCollector_EE_data 
  else:
    modules = lepCollector_EE

if (doData):
  from CMGTools.TTHAnalysis.tools.nanoAOD.remove_overlap import OverlapRemover
  modules.extend( [lambda : OverlapRemover()] ) 

cut = "1" 
compression = "ZLIB:3" #"LZ4:4" #"LZMA:9"
branchsel_out = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/tools/nanoAOD/OutputSlim_wz.txt"
branchsel_in  = os.environ['CMSSW_BASE']+"/src/CMGTools/TTHAnalysis/python/tools/nanoAOD/InputSlim_wz.txt"


# -- Finally create the postprocessor
POSTPROCESSOR = PostProcessor(None, [], modules = modules,
        cut = cut, prefetch = False, longTermCache = False,
        branchsel = branchsel_in, outputbranchsel = None, compression = compression)
