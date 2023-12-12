import ROOT as r
import os
from copy import deepcopy
r.gROOT.SetBatch(1)
files = {  
          "muonEG" :   ["/beegfs/data/nanoAODv11/30march2023/data/2022PostEE/MuonEG/dataRun3_PostEE_april2023_MuonEG_Run2022F-PromptNanoAODv11_v1-v2/230425_133253/0000/", 2],
          "muon" :   ["/beegfs/data/nanoAODv11/30march2023/data/2022PostEE/Muon/dataRun3_PostEE_april2023_Muon_Run2022F-PromptNanoAODv11_v1-v2/230404_161330/0000/", 3],
}


# Create a chain
#stack = r.THStack()
l = r.TLegend(0.1, 0.7, 0.5, 0.88)
histos = {}
for dataset in files:
  chain = r.TChain("Events", "chain")
  chain.Add(files[dataset][0] + "tree*.root")

  c = r.TCanvas("c_%s"%dataset, "", 800, 800)
  chain.Draw("run")
  h = chain.GetHistogram() 
  h.Scale(1/h.Integral())
  hcopy = deepcopy(h.Clone("h_%s"%dataset))
  hcopy.SetLineColor(files[dataset][1])
  hcopy.SetLineWidth(3)
#  hcopy.Scale(1/hcopy.Integral())
  hcopy.Draw("hist")
  histos[dataset] = hcopy
  l.AddEntry(hcopy, dataset, "l")
  c.SaveAs("%s.png"%dataset)

c = r.TCanvas("c", "", 800, 800)

histos["muon"].Draw("hist same")
histos["muonEG"].Draw("hist same")
l.Draw("same")
c.SaveAs("stack.png")
