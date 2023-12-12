import os, sys, re
import pandas as pd
from copy import deepcopy
inpath = sys.argv[1]

folders = os.listdir(inpath)
#goldenjson="Cert_Collisions2022_355100_357900_Golden.json" # eras CD
goldenjson="Cert_Collisions2022_355100_362760_Golden.json" # eras CDEFG

table = {}
expected_folders = ["EGamma", "SingleMuon", "DoubleMuon", "Muon", "JetHT", "MET", "MuonEG", "JetMET"]
for fold in folders:
  table[fold] = {"v1 (C)" : "-", "v2 (C)" : "-", "v1 (D)" : "-", "v1-v1 (D)" : "-", "v2 (D)" : "-", "v1-v2 (E)" : "", "v1-v3 (E)" : "-", "v1-v2 (F)" : "-", "v1-v1 (G)" : "-" }
  total_c = 0
  total_d = 0
  total_e = 0
  total_f = 0
  total_g = 0
  for lumitxt in os.listdir( os.path.join(inpath, fold) ):
    if "txt" not in lumitxt: continue
    # Find out which entry should we fill
  
    era, version = re.match("lumi_EraRun2022(.)_(.*)filtered.*", lumitxt).groups()
  
    if version == "": 
      version = "v1"
    else:
      version = version[:-1] # so it does not match one _ in the names...
  
    entry = "%s (%s)"%(version, era)
  
    print("era: %s"%era, "version: %s"%version, "entry: %s"%entry, lumitxt)
    # Read the file
    print(" >> Reading file %s"%(inpath+"/%s/%s"%(fold, lumitxt)))
    f = open(os.path.join(inpath, fold, lumitxt), "r") 
  
    # Find the nfill line
    text = f.readlines()    
    for iline, line in enumerate(text):
      if "nfill | nrun" in line: 
        header_i = iline
        break
   
    header = text[header_i]
    info   = text[header_i+2]
    
    # Apply a factor to always express in fb-1 
    factor = 1
    if "ub" in header: factor = 1e-9
    if "nb" in header: factor = 1e-6
    if "pb" in header: factor = 1e-3
      
    lumi = float(info.strip().split("|")[-2])*factor
    if era == "C": total_c += lumi
    if era == "D": total_d += lumi
    if era == "E": total_e += lumi
    if era == "F": total_f += lumi
    if era == "G": total_g += lumi
  
    f.close()
    table[fold][entry]       = "%3.2f"%(lumi)
  #table[fold]["total (D)"]   = "%3.2f"%total_d
  table[fold]["total"]       = "%3.2f"%(total_c+total_d+total_e+total_f+total_g)

  

print("\n\n -- Golden JSON: %s"%goldenjson)
df = pd.DataFrame(table, index = ["v1 (C)", "v2 (C)", "v1-v1 (D)", "v1 (D)", "v2 (D)", "total (D)", "v1-v2 (E)", "v1-v3 (E)", "v1-v2 (F)", "v1-v1 (G)", "total"],
                         columns = ["DoubleMuon", "SingleMuon", "Muon", "JetHT", "MET", "JetMET", "EGamma", "MuonEG"])
df = df.fillna("-")
df = df.transpose()
df.to_latex('table.tex', header = "Golden JSON -- %s"%goldenjson)
print(df)
print("\n\n")
