""" Script to compute trigger SFs in WZ analysis """

import ROOT as r
from copy import deepcopy
import canvas as cv
import os,sys
from optparse import OptionParser

from make_latex_table import dict_to_latex_table
sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
from functions import color_msg
r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)


outpath = "trigger_efficiencies/results/"

def add_parsing_opts():
    ''' Function with base parsing arguments used by any script '''
    parser = OptionParser(usage = "python plot_triggerSF.py [options]", 
                                    description = "Main options for running WZ trigger SF") 
    parser.add_option("--numpath", dest = "numpath", default = "trigger_efficiencies/numerator",
                help = "Path to the file with the numerator histograms.")
    parser.add_option("--denpath", dest = "denpath", default = "trigger_efficiencies/denominator",
                help = "Path to the file with the denominator histograms.")
    parser.add_option("--var", dest = "var", default = "tot_weight",  
                help = "Variable to compute eff with.")
    return parser.parse_args()

def plot_eff(h_num, h_den, eff, name):
    # Canvas    
    c, p1, p2 = cv.new_canvas("trigger_eff")
    l = cv.new_legend()

    # Plot things
    h_num.GetXaxis().SetTitle("")
    h_num.SetTitle(name)
    h_num.GetXaxis().SetTitleSize(0.04)
    h_num.GetXaxis().SetLabelSize(0)
    h_num.GetYaxis().SetTitle("Events")
    h_num.GetYaxis().SetTitleSize(0.04)
    h_num.GetYaxis().SetTitleOffset(1.2)
    h_num.GetYaxis().SetNdivisions(510)
    h_num.GetYaxis().SetLabelSize(0.06)
    h_num.SetLineColor(r.kGreen)
    h_den.SetLineColor(r.kRed)
    h_num.SetFillColor(0)
    h_den.SetFillColor(0)

    l.AddEntry(h_num, "Num.", "l")
    l.AddEntry(h_den, "Den.", "l")


    # -- Work on the second pad -- #
    p1.cd()
    h_num.Draw("hist")
    h_den.Draw("hist same")
    l.Draw("same")

    # -- Work on the second pad -- #
    p2.cd()
    h_aux = cv.get_aux_histo(h_den)
    
    # -- Now draw -- #
    h_aux.Draw()
    eff.Draw("same")
    h_aux.SetTitle("")
    h_aux.GetYaxis().SetRangeUser(0.985, 1.005)
    h_aux.GetYaxis().SetNdivisions(505)
    h_aux.GetYaxis().SetTitle("Efficiency")
    h_aux.GetYaxis().SetLabelSize(0.1)
    h_aux.GetXaxis().SetLabelSize(0.12)
    h_aux.GetXaxis().SetTitleSize(0.12)

    if not os.path.exists(outpath): 
        os.system("mkdir -p %s"%outpath)
    c.SaveAs( os.path.join(outpath, name + ".png") )
    c.SaveAs( os.path.join(outpath, name + ".pdf") )

    return

def get_eff(typ, numpath, denpath, var, name):
    path_num = numpath
    path_den = denpath
    var = var

    # Open files
    f_num  = r.TFile.Open(path_num)
    f_den = r.TFile.Open(path_den)

    # Get histograms
    h_num  = f_num.Get("{var}_{typ}".format(var = var, typ = typ))
    h_den = f_den.Get("{var}_{typ}".format(var = var, typ = typ))
    eff = r.TEfficiency(h_num, h_den)

    plot_eff(h_num, h_den, eff, name)
    
    return eff.GetEfficiency(1), eff.GetEfficiencyErrorLow(1), eff.GetEfficiencyErrorUp(1)

if __name__ == "__main__":
    regions = ["Inclusive", "barrel0", "barrel1", "barrel2", "barrel3"]
    # Unpack opts
    opts, _ = add_parsing_opts()

    effs = {
            "year" : [("2022",5)],
            "Region" : regions,
            "$\epsilon_{MC}$" : [],
            "$\epsilon_{Data}$" : []
    }
    
    for region in regions:
        #color_msg(" >> Printing table for region %s"%region, "green")        
        numpath = os.path.join(opts.numpath, region, "srwz", "plots_wz.root")
        denpath = os.path.join(opts.denpath, region, "srwz", "plots_wz.root")
        eff_s, errDn_s, errUp_s = get_eff("signal", numpath, denpath, opts.var, name="eff_{}_signal".format(region))
        eff_d, errDn_d, errUp_d = get_eff("data", numpath, denpath, opts.var, name="eff_{}_data".format(region))
        effs["$\epsilon_{MC}$"].append("$%3.2f^{%3.4f}_{%3.4f}$"%(eff_s, errUp_s, errDn_s))
        effs["$\epsilon_{Data}$"].append("$%3.2f^{%3.4f}_{%3.4f}$"%(eff_d, errUp_d, errDn_d))

    table = dict_to_latex_table(effs)
    print(table)
