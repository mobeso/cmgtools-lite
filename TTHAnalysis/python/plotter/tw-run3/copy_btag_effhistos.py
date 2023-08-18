import ROOT as r
from copy import deepcopy
import os

tmpfil   = "./temp_Run3_plots/2023_06_06_btaggingEff/2022PostEE/eff/"
savepath = "{cmsswpath}/src/CMGTools/TTHAnalysis/data/TopRun2UL/btagging/".format(cmsswpath = os.environ['CMSSW_BASE'])

xuandict = {"deepcsv" : "DeepCSV",
            "deepjet" : "DeepFlav"}
wp = "M"
writethings = []
for y in ["2022"]:
    tmpf = r.TFile(tmpfil + "/output.root", "READ")
    for algo in ["deepjet", "deepcsv"]:
        for el in ["B", "C", "L"]:
            print("btageff_{a}_{t}_btag_{t}_tw".format(t = el, a = algo))
            writethings.append(deepcopy(tmpf.Get("btageff_{a}_{t}_btag_{t}_tw".format(t = el, a = algo)).Clone("BtagSF{t}_{a}{w}_{y}".format(t = el, a = xuandict[algo], w = wp, y = y))))
    tmpf.Close()


outF = r.TFile(savepath + "/btagEffs_2023_06_06.root", "RECREATE")
for el in writethings: el.Write()
outF.Close()
