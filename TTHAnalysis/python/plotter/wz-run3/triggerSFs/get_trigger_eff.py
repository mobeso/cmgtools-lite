""" Small piece of code to compute trigger efficiencies on data and MC"""
import ROOT as r
import os, sys
from copy import deepcopy
from optparse import OptionParser
import array
sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
from functions import color_msg
import scripts.canvas as cv 
from logistics.make_latex_table import dict_to_latex_table

r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)


mode = sys.argv[1]

def get_pais_fail(path, files, num, den, name):
    hPass = r.TH1D(name, "", 1, 0, 1)
    hFail = r.TH1D(name, "", 1, 0, 1)
    totPass = 0
    totFail = 0
    entries = 0
    for file_ in files:
        # --------- Open the file and add friends ---------   
        print(" >> Opening file: {}/{}".format(path, file_))
        rf = r.TFile.Open( os.path.join(path, file_+".root"))
        # Get the tree and add the friend trees
        tree = rf.Get("Events")
        
        
        for friend in ["leptonJetRecleaning", "leptonBuilder"]:
            friendpath = os.path.join(path, friend, file_+"_Friend.root")
            print("   + Adding friend: %s"%friendpath)
            friendfile = r.TFile( friendpath )
            tree.AddFriend("Friends", friendfile)
        # -------------------------------------------------
        tree.Draw("1 >> hPasst", num, "hist")
        tree.Draw("1 >> hFailt", den, "hist")
        hPasst  = r.gDirectory.Get("hPasst")
        hFailt = r.gDirectory.Get("hFailt")
        
        totPass += hPasst.Integral()
        totFail += hFailt.Integral()
        
        rf.Close()
    
    hPass.SetBinContent(1, totPass)
    hFail.SetBinContent(1, totFail)
        
    return hPass, hFail

if __name__ == "__main__":

 
    # --------- Make a TTree::Draw with numerator and denominator selection
    years = ["2022", "2022EE"]
    effs = {
            "Year" : [],
            "Sample" : ["Data (JetMET)", "WZ", "WZ (no ref trigger)"]*len(years),
            "Pass PR" : [],
            "Pass PR and HLT" : [],
            "$\epsilon$(HLT)" : []
    }
    for year in years:
        datapath = f"/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees_v2/data/{year}/"
        mcpath = f"/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees_v2/mc/{year}/"
        mcfiles = ["WZto3LNu"]
        datafiles = ["JetMET_Run2022E" , "JetMET_Run2022F", "JetMET_Run2022G"] if year == "2022EE" else ["JetMET_Run2022C" , "JetMET_Run2022D"]
        if mode == "inclusive":
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt > 15 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s"%(baseline, reftrigger)
            hDenVar = "%s && %s"%(baseline, reftrigger)
            hNumVar_bias = "Trigger_3l && %s"%baseline
            hDenVar_bias = baseline
        
        elif mode == "barrel0":     
            extra = "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 0"
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt > 15 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s && %s"%(baseline, reftrigger, extra)
            hDenVar = "%s && %s && %s"%(baseline, reftrigger, extra)
            hNumVar_bias = "Trigger_3l && %s && %s"%(baseline, extra)
            hDenVar_bias = "%s && %s"%(baseline, extra)
            
        elif mode == "barrel1":      
            extra = "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 1"
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt > 15 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s && %s"%(baseline, reftrigger, extra)
            hDenVar = "%s && %s && %s"%(baseline, reftrigger, extra)
            hNumVar_bias = "Trigger_3l && %s && %s"%(baseline, extra)
            hDenVar_bias = "%s && %s"%(baseline, extra)
            
        elif mode == "barrel2":  
            extra = "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 2"
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt > 15 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s && %s"%(baseline, reftrigger, extra)
            hDenVar = "%s && %s && %s"%(baseline, reftrigger, extra)
            hNumVar_bias = "Trigger_3l && %s && %s"%(baseline, extra)
            hDenVar_bias = "%s && %s"%(baseline, extra)
        
        elif mode == "barrel3":
            extra = "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 3"
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt > 15 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s && %s"%(baseline, reftrigger, extra)
            hDenVar = "%s && %s && %s"%(baseline, reftrigger, extra)
            hNumVar_bias = "Trigger_3l && %s && %s"%(baseline, extra)
            hDenVar_bias = "%s && %s"%(baseline, extra)
            
        elif mode == "lowpt":
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt >= 15 && LepZ2_pt <= 25 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s"%(baseline, reftrigger)
            hDenVar = "%s && %s"%(baseline, reftrigger)
            hNumVar_bias = "Trigger_3l && %s"%baseline
            hDenVar_bias = baseline
            
        elif mode == "highpt":
            baseline = "nLepSel >= 3 && MET_pt_central > 120 && LepZ1_pt > 25 && LepZ2_pt >= 25 && LepW_pt > 25 "
            reftrigger = "(HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight)" # reference triggers
            
            hNumVar = "Trigger_3l && %s && %s"%(baseline, reftrigger)
            hDenVar = "%s && %s"%(baseline, reftrigger)
            hNumVar_bias = "Trigger_3l && %s"%baseline
            hDenVar_bias = baseline
        
        
        pass_data, fail_data = get_pais_fail(datapath, datafiles, hNumVar, hDenVar, name = "inclusive_data")
        pass_mc, fail_mc = get_pais_fail(mcpath, mcfiles, hNumVar, hDenVar, name = "inclusive_mc")
        pass_mc_bias, fail_mc_bias = get_pais_fail(mcpath, mcfiles, hNumVar_bias, hDenVar_bias, name = "inclusive_mc_bias")
    
        eff_data = r.TEfficiency(pass_data, fail_data)
        eff_mc = r.TEfficiency(pass_mc, fail_mc)
        eff_mc_bias = r.TEfficiency(pass_mc_bias, fail_mc_bias)
    
        pass_pr_s = fail_mc.GetBinContent(1)
        pass_pr_and_hlt_s = pass_mc.GetBinContent(1)
        eff_s, errUp_s, errDn_s = eff_mc.GetEfficiency(1), eff_mc.GetEfficiencyErrorUp(1), eff_mc.GetEfficiencyErrorLow(1)
    
        pass_pr_d = fail_data.GetBinContent(1)
        pass_pr_and_hlt_d = pass_data.GetBinContent(1)
        eff_d, errUp_d, errDn_d = eff_data.GetEfficiency(1), eff_data.GetEfficiencyErrorUp(1), eff_data.GetEfficiencyErrorLow(1)
    
        pass_pr_s_bias = fail_mc_bias.GetBinContent(1)
        pass_pr_and_hlt_s_bias = pass_mc_bias.GetBinContent(1)
        eff_s_bias, errUp_s_bias, errDn_s_bias = eff_mc_bias.GetEfficiency(1), eff_mc_bias.GetEfficiencyErrorUp(1), eff_mc_bias.GetEfficiencyErrorLow(1)
    
        print(" >> Table for mode: %s"%mode)
        
        
        # Add for Data
        effs["Year"].append( (year, 3) )
        effs["Year"].append( "{}" )
        effs["Year"].append( "{}" )
        effs["Pass PR"].append("%3.3f"%pass_pr_d)
        effs["Pass PR and HLT"].append("%3.3f"%pass_pr_and_hlt_d)
        effs["$\epsilon$(HLT)"].append("$%3.3f^{+%3.3f}_{-%3.3f}$"%(eff_d, errUp_d, errDn_d))
    
    
        # Add for MC
        effs["Pass PR"].append("%3.3f"%pass_pr_s)
        effs["Pass PR and HLT"].append("%3.3f"%pass_pr_and_hlt_s)
        effs["$\epsilon$(HLT)"].append("$%3.3f^{+%3.3f}_{-%3.3f}$"%(eff_s, errUp_s, errDn_s ))
        
        # Add for MC (bias)
        effs["Pass PR"].append("%3.3f"%pass_pr_s_bias)
        effs["Pass PR and HLT"].append("%3.3f"%pass_pr_and_hlt_s_bias)
        effs["$\epsilon$(HLT)"].append("$%3.3f^{%3.3f}_{%3.3f}$"%(eff_s_bias, errUp_s_bias, errDn_s_bias))
        

    table = dict_to_latex_table(effs, caption = "", label = "")
    print(table)
    
    
    
    
    
    
    



