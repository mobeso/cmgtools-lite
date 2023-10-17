""" Script to evaluate MVA trainings """

import ROOT as r
from copy import deepcopy
import os,sys
from optparse import OptionParser
import array as ar
import numpy as np

sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
from functions import color_msg

sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/PhysicsTools/NanoAODTools/python/postprocessing/framework/"))
from datamodel import Collection as Collection

r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)
outpath = "lepmva_results"

h_signal_legacy_total = r.TH1F("h_signal_legacy_total", "h_signal_legacy", 1000, -1., 1.)
h_signal_ul_total = r.TH1F("h_signal_ul_total", "h_signal_ul", 1000, -1., 1.)
h_signal_tth_total = r.TH1F("h_signal_tth_total", "h_signal_tth", 1000, -1., 1.)
h_signal_ttw_total = r.TH1F("h_signal_ttw_total", "h_signal_ttw", 1000, -1., 1.)

h_bkg_legacy_total = r.TH1F("h_bkg_legacy_total", "h_bkg_legacy", 1000, -1., 1.)
h_bkg_ul_total = r.TH1F("h_bkg_ul_total", "h_bkg_ul", 1000, -1., 1.)
h_bkg_tth_total = r.TH1F("h_bkg_tth_total", "h_bkg_tth", 1000, -1., 1.)
h_bkg_ttw_total = r.TH1F("h_bkg_ttw_total", "h_bkg_ttw", 1000, -1., 1.)

h_signal_legacy = r.TH1F("h_signal_legacy", "h_signal_legacy", 1000, -1., 1.)
h_signal_ul = r.TH1F("h_signal_ul", "h_signal_ul", 1000, -1., 1.)
h_signal_tth = r.TH1F("h_signal_tth", "h_signal_tth", 1000, -1., 1.)
h_signal_ttw = r.TH1F("h_signal_ttw", "h_signal_ttw", 1000, -1., 1.)

h_bkg_legacy = r.TH1F("h_bkg_legacy", "h_bkg_legacy", 1000, -1., 1.)
h_bkg_ul = r.TH1F("h_bkg_ul", "h_bkg_ul", 1000, -1., 1.)
h_bkg_tth = r.TH1F("h_bkg_tth", "h_bkg_tth", 1000, -1., 1.)
h_bkg_ttw = r.TH1F("h_bkg_ttw", "h_bkg_ttw", 1000, -1., 1.)

class MVAvar:
    def __init__(self, name):
        self.name = name
        self.var = ar.array('f', [0.])

    def set(self, val):
        self.var[0] = val
    
def add_parsing_opts():
    ''' Function with base parsing arguments used by any script '''
    parser = OptionParser(usage = "python plot_triggerSF.py [options]", 
                                    description = "Main options for running WZ trigger SF") 
    parser.add_option("--inpath", dest = "inpath", default = None,
                help = "Path to the folder with the files used to evaluate performance")
    parser.add_option("--nfiles", dest = "nfiles", type = int, default = -1,
            help = "Number of files to be iterated over.")
    parser.add_option("--mode", dest = "mode", default = "muon",
        help = "Produce results for muons or electrons.")
    return parser.parse_args()

def open_model(modelname, modelpath, vars_):
    reader = r.TMVA.Reader()
    for vname, v in vars_.items():
            color_msg("    + Adding variable: %s "%vname) 
            reader.AddVariable(v.name, v.var)
    reader.BookMVA(modelname, modelpath)
    return reader

def create_muon_rootfiles(inpath, files):
    """ Evaluate MVA for muons """
    chain = r.TChain("Events", "chain")
    for file in files:
        chain.AddFile(os.path.join(inpath, file))
        
    color_msg(" >> Evaluating Muon MVA", "green")
    color_msg("    * Number of events: %d "%chain.GetEntries())
    
    # Register the MVAs: semi-hardcoded :)
    tth_like = os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/muonMVA_tth-like.xml")
    ttw_like = os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/muonMVA_ttw-like.xml") 
    
    vars_ = {
        "LepGood_pt" : MVAvar("Muon_LepGood_pt"),
        "LepGood_eta" : MVAvar("Muon_LepGood_eta"),
        "LepGood_miniRelIsoCharged" : MVAvar("Muon_LepGood_miniRelIsoCharged"), 
        "LepGood_miniRelIsoNeutral" : MVAvar("Muon_LepGood_miniRelIsoNeutral"),
        "LepGood_jetNDauChargedMVASel" : MVAvar("Muon_LepGood_jetNDauChargedMVASel"), 
        "LepGood_jetPtRelv2" : MVAvar("Muon_LepGood_jetPtRelv2"), 
        "LepGood_jetPtRatio" : MVAvar("Muon_LepGood_jetPtRatio"), 
        "LepGood_jetDF" : MVAvar("Muon_LepGood_jetDF"),
        "LepGood_sip3d" : MVAvar("Muon_LepGood_sip3d"), 
        "LepGood_dxy" : MVAvar("Muon_LepGood_dxy"), 
        "LepGood_dz" : MVAvar("Muon_LepGood_dz"), 
        "LepGood_segmentComp" : MVAvar("Muon_LepGood_segmentComp")
    }

    mva_tth = open_model("BDTGtth", tth_like, vars_)
    mva_ttw = open_model("BDTGttw", ttw_like, vars_)

    # Selections
    
    presel = lambda lep: (lep.pt > 5 and
                          abs(lep.eta) < 2.4 and
                          (lep.isGlobal == 1 or lep.isTracker == 1) and
                          lep.isPFcand and
                          lep.looseId == 1)
                                   
    for ievent, event in enumerate(chain):
        
        jets = Collection(event, "Jet", "nJet")
        leps = Collection(event, "Muon","nMuon")

        for ilep, lep in enumerate(leps):
            # Fill the histograms
            if (lep.jetIdx > 40): continue # Sometimes the branch appears not to be filled and it crashes 

            # -- Training variables
            vars_["LepGood_pt"].set(lep.pt)
            vars_["LepGood_eta"].set(lep.eta)
            vars_["LepGood_miniRelIsoNeutral"].set(lep.miniPFRelIso_all - lep.miniPFRelIso_chg)
            vars_["LepGood_miniRelIsoCharged"].set(lep.miniPFRelIso_chg)
            vars_["LepGood_jetNDauChargedMVASel"].set(lep.jetNDauCharged)
            vars_["LepGood_jetPtRelv2"].set(lep.jetPtRelv2)
            vars_["LepGood_jetPtRatio"].set(min(1. / (1. + lep.jetRelIso), 1.5))
            vars_["LepGood_jetDF"].set(jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0)
            vars_["LepGood_sip3d"].set(lep.sip3d)
            vars_["LepGood_dxy"].set(np.log(abs(lep.dxy)))
            vars_["LepGood_dz"].set(np.log(abs(lep.dz)))
            vars_["LepGood_segmentComp"].set(lep.segmentComp)
            
            # -- Truth level
            genPartFlav = lep.genPartFlav
            
            # -- Evaluate
            legacy_score = lep.mvaTTH
            tth_score = mva_tth.EvaluateMVA("BDTGtth")
            ttw_score = mva_ttw.EvaluateMVA("BDTGttw")
            
            # -- Fill the total histograms 
            ## Signal
            if (genPartFlav == 1 or genPartFlav == 15):
                h_signal_legacy_total.Fill(legacy_score)
                h_signal_tth_total.Fill(tth_score)
                h_signal_ttw_total.Fill(ttw_score)
            ## Background
            elif (genPartFlav != 1 or genPartFlav != 15):
                h_bkg_legacy_total.Fill(legacy_score)
                h_bkg_tth_total.Fill(tth_score)
                h_bkg_ttw_total.Fill(ttw_score)
            
            # -- Now fill the selected histograms
            # basic common preselection
            if (lep.miniPFRelIso_all > 0.4): continue
            if (lep.sip3d > 8): continue
            if (abs(lep.dxy) > 0.05): continue
            if (abs(lep.dz) > 0.1): continue
 
            # Ask the lepton to at least pass loose selection: for muons this is
            # the ttH preselection.
            if not presel(lep): continue


            # -- Fill the filtered histograms 
            ## Signal 
            if (genPartFlav == 1 or genPartFlav == 15):
                h_signal_legacy.Fill(legacy_score)
                h_signal_tth.Fill(tth_score)
                # For ttW evaluation, since it is trained in a tighter preselection, by
                # construction if we just evaluate in its own preselection region, we don't
                # take into account the fact that ttH MVA must work in a harsher environment.
                # So the most fair way to evaluate the MVA is to penalize ttW events.
                h_signal_ttw.Fill( (-1)*(lep.mediumId == 0) + (lep.mediumId == 1)*ttw_score )

            elif (genPartFlav != 1 or genPartFlav != 15):
                h_bkg_legacy.Fill(legacy_score)
                h_bkg_tth.Fill(tth_score)
                h_bkg_ttw.Fill( (-1)*(lep.mediumId == 0) + (lep.mediumId == 1)*ttw_score )
    
    print(" ---------------------------------------------------------------- ")        
    print("    * Finished iterating over events. Results:")
    print(" ---------------------------------------------------------------- ")
    print("         + Signal: legacy (total) -> %3.2f"%h_signal_legacy_total.Integral())
    print("         + Signal: ttH (total) -> %3.2f"%h_signal_tth_total.Integral())
    print("         + Signal: ttW (total) -> %3.2f"%h_signal_ttw_total.Integral())
    print("         + Bkg: legacy (total) -> %3.2f"%h_bkg_legacy_total.Integral())
    print("         + Bkg: ttH (total) -> %3.2f"%h_bkg_tth_total.Integral())
    print("         + Bkg: ttW (total) -> %3.2f"%h_bkg_ttw_total.Integral())
    print(" ---------------------------------------------------------------- ")
    print("         + Signal: legacy -> %3.2f"%h_signal_legacy.Integral())
    print("         + Signal: ttH -> %3.2f"%h_signal_tth.Integral())
    print("         + Signal: ttW -> %3.2f"%h_signal_ttw.Integral())
    print("         + Bkg: legacy -> %3.2f"%h_bkg_legacy.Integral())
    print("         + Bkg: ttH -> %3.2f"%h_bkg_tth.Integral())
    print("         + Bkg: ttW -> %3.2f"%h_bkg_ttw.Integral())
    print(" ---------------------------------------------------------------- ")

    f_out = r.TFile(os.path.join(outpath, "muon_mvaEvaluate.root"), "recreate");
    
    h_signal_legacy_total.Write()
    h_signal_tth_total.Write()
    h_signal_ttw_total.Write()
    h_bkg_legacy_total.Write()
    h_bkg_tth_total.Write()
    h_bkg_ttw_total.Write()
    h_signal_legacy.Write()
    h_signal_tth.Write()
    h_signal_ttw.Write()
    h_bkg_legacy.Write()
    h_bkg_tth.Write()
    h_bkg_ttw.Write()
    
    f_out.Close()
    return

def create_electron_rootfiles(inpath, files):
    """ Evaluate MVA for electrons """
    chain = r.TChain("Events", "chain")
    for file in files:
        chain.AddFile(os.path.join(inpath, file))
        
    color_msg(" >> Evaluating Electron MVA", "green")
    color_msg("    * Number of events: %d "%chain.GetEntries())
    
    # Register the MVAs: semi-hardcoded :)
    tth_like = os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/electronMVA_tth-like.xml")
    ttw_like = os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/electronMVA_ttw-like.xml") 
    
    vars_ = {
            "LepGood_pt" : MVAvar("Electron_LepGood_pt"),
            "LepGood_eta" : MVAvar("Electron_LepGood_eta"),
            "LepGood_miniRelIsoCharged" : MVAvar("Electron_LepGood_miniRelIsoCharged"),
            "LepGood_miniRelIsoNeutral" : MVAvar("Electron_LepGood_miniRelIsoNeutral"),
            "LepGood_jetNDauChargedMVASel" : MVAvar("Electron_LepGood_jetNDauChargedMVASel"), 
            "LepGood_jetPtRelv2" : MVAvar("Electron_LepGood_jetPtRelv2"), 
            "LepGood_jetPtRatio" : MVAvar("Electron_LepGood_jetPtRatio"), 
            "LepGood_jetDF" : MVAvar("Electron_LepGood_jetDF"),
            "LepGood_sip3d" : MVAvar("Electron_LepGood_sip3d"), 
            "LepGood_dxy" : MVAvar("Electron_LepGood_dxy"), 
            "LepGood_dz" : MVAvar("Electron_LepGood_dz"), 
            "LepGood_mvaFall17V2noIso" : MVAvar("Electron_LepGood_mvaFall17V2noIso")
    }

    mva_tth = open_model("BDTGtth", tth_like, vars_)
    mva_ttw = open_model("BDTGttw", ttw_like, vars_)

    presel = lambda lep: (lep.pt > 5 and
                          abs(lep.eta) < 2.5 and
                          lep.lostHits < 2)
    
    for ievent, event in enumerate(chain):
        
        jets = Collection(event, "Jet", "nJet")
        leps = Collection(event, "Electron","nElectron")

        for ilep, lep in enumerate(leps):
            # Fill the histograms
            if (lep.jetIdx > 40): continue # Sometimes the branch appears not to be filled and it crashes 


            # -- Training variables
            vars_["LepGood_pt"].set(lep.pt)
            vars_["LepGood_eta"].set(lep.eta)
            vars_["LepGood_miniRelIsoNeutral"].set(lep.miniPFRelIso_all - lep.miniPFRelIso_chg)
            vars_["LepGood_miniRelIsoCharged"].set(lep.miniPFRelIso_chg)
            vars_["LepGood_jetNDauChargedMVASel"].set(lep.jetNDauCharged)
            vars_["LepGood_jetPtRelv2"].set(lep.jetPtRelv2)
            vars_["LepGood_jetPtRatio"].set(min(1. / (1. + lep.jetRelIso), 1.5) )
            vars_["LepGood_jetDF"].set(jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0)
            vars_["LepGood_sip3d"].set(lep.sip3d)
            vars_["LepGood_dxy"].set(np.log(abs(lep.dxy)))
            vars_["LepGood_dz"].set(np.log(abs(lep.dz)))
            vars_["LepGood_mvaFall17V2noIso"].set(lep.mvaNoIso_Fall17V2)
           
            # -- Truth level
            genPartFlav = lep.genPartFlav
            
            # -- Evaluate
            legacy_score = lep.mvaTTH
            tth_score = mva_tth.EvaluateMVA("BDTGtth")
            ttw_score = mva_ttw.EvaluateMVA("BDTGttw")
            
            # -- Fill the total histograms 
            ## Signal
            if (genPartFlav == 1 or genPartFlav == 15):
                h_signal_legacy_total.Fill(legacy_score)
                h_signal_tth_total.Fill(tth_score)
                h_signal_ttw_total.Fill(ttw_score)
            ## Background
            elif (genPartFlav != 1 or genPartFlav != 15):
                h_bkg_legacy_total.Fill(legacy_score)
                h_bkg_tth_total.Fill(tth_score)
                h_bkg_ttw_total.Fill(ttw_score)
            
            # -- Now fill the selected histograms
            ## Baseline selection
            if (lep.miniPFRelIso_all > 0.4): continue
            if (lep.sip3d > 8): continue
            if (abs(lep.dxy) > 0.05): continue
            if (abs(lep.dz) > 0.1): continue

            # Ask the lepton to at least pass loose selection: for muons this is
            # the ttH preselection.
            if not presel(lep): continue
            
            # -- Fill the filtered histograms 
            ## Signal 
            if (genPartFlav == 1 or genPartFlav == 15):
                h_signal_legacy.Fill(legacy_score)
                h_signal_tth.Fill(tth_score)
                h_signal_ttw.Fill((-1)*(lep.mvaNoIso_Fall17V2_WPL == 0) + ttw_score * (lep.mvaNoIso_Fall17V2_WPL == 1))

            elif (genPartFlav != 1 or genPartFlav != 15):
                h_bkg_legacy.Fill(legacy_score)
                h_bkg_tth.Fill(tth_score)
                h_bkg_ttw.Fill((-1)*(lep.mvaNoIso_Fall17V2_WPL == 0) + ttw_score * (lep.mvaNoIso_Fall17V2_WPL == 1))
    
    print(" ---------------------------------------------------------------- ")        
    print("    * Finished iterating over events. Results:")
    print(" ---------------------------------------------------------------- ")
    print("         + Signal: legacy (total) -> %3.2f"%h_signal_legacy_total.Integral())
    print("         + Signal: ttH (total) -> %3.2f"%h_signal_tth_total.Integral())
    print("         + Signal: ttW (total) -> %3.2f"%h_signal_ttw_total.Integral())
    print("         + Bkg: legacy (total) -> %3.2f"%h_bkg_legacy_total.Integral())
    print("         + Bkg: ttH (total) -> %3.2f"%h_bkg_tth_total.Integral())
    print("         + Bkg: ttW (total) -> %3.2f"%h_bkg_ttw_total.Integral())
    print(" ---------------------------------------------------------------- ")
    print("         + Signal: legacy -> %3.2f"%h_signal_legacy.Integral())
    print("         + Signal: ttH -> %3.2f"%h_signal_tth.Integral())
    print("         + Signal: ttW -> %3.2f"%h_signal_ttw.Integral())
    print("         + Bkg: legacy -> %3.2f"%h_bkg_legacy.Integral())
    print("         + Bkg: ttH -> %3.2f"%h_bkg_tth.Integral())
    print("         + Bkg: ttW -> %3.2f"%h_bkg_ttw.Integral())
    print(" ---------------------------------------------------------------- ")

    f_out = r.TFile(os.path.join(outpath, "electron_mvaEvaluate.root"), "recreate")
    
    h_signal_legacy_total.Write()
    h_signal_tth_total.Write()
    h_signal_ttw_total.Write()
    h_bkg_legacy_total.Write()
    h_bkg_tth_total.Write()
    h_bkg_ttw_total.Write()
    h_signal_legacy.Write()
    h_signal_tth.Write()
    h_signal_ttw.Write()
    h_bkg_legacy.Write()
    h_bkg_tth.Write()
    h_bkg_ttw.Write()
    
    f_out.Close()
    return
    
if __name__ == "__main__":
    opts, _ = add_parsing_opts()
    
    inpath = opts.inpath
    if not inpath: color_msg("Wrong path: %s"%inpath, "red")
    nfiles = opts.nfiles
    mode = opts.mode
    
    if not os.path.exists(outpath): 
        os.system("mkdir -p %s"%outpath)
        
    # Get files for input
    files = os.listdir(inpath)[:nfiles]
    
    if "mu" in mode.lower():
        create_muon_rootfiles(inpath, files)
    elif "el" in mode.lower():
        create_electron_rootfiles(inpath, files)
