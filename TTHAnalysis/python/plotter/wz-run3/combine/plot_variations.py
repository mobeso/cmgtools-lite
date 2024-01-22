import ROOT
import os, re, sys
from copy import deepcopy
import json
import argparse
import numpy as np
sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
import scripts.canvas as cv 

ROOT.gROOT.SetBatch(1)
ROOT.gStyle.SetOptStat(0)

def add_parsing_options():
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', '-i', metavar = "infile", default = None, dest = "infile", 
                     help = "path to the input file that contain the histograms and the variations.")
    return parser.parse_args()

def retrieve_histograms(file_name, process):
    """
    Retrieves histograms from the file based on the process.
    Returns a list of histograms corresponding to variations.
    """
    histograms = []
    root_file = ROOT.TFile.Open(file_name)
    # Check if the nominal histogram exists
    nominal_hist = deepcopy(root_file.Get("{}".format(process)))
    for bini in range(1, nominal_hist.GetNbinsX()):
        nominal_hist.SetBinError(bini, 0)
    if not nominal_hist:
        print("Nominal histogram not found!")
        return None, []

    # Iterate over keys in file and find the up/down variations
    ratio_histograms = []
    key_list = root_file.GetListOfKeys()
    for key in key_list:
        hist_name = key.GetName()
        if "nonfid" in hist_name:continue
        if "smear" not in hist_name: continue
        if hist_name.startswith("{}_".format(process)) and ("Up" in hist_name or "Down" in hist_name):
            variated_hist = root_file.Get(hist_name).Clone()
            variated_hist.Divide(nominal_hist)
            ratio_histograms.append(deepcopy(variated_hist))
    return nominal_hist, ratio_histograms

def plot_histograms(nominal_hist, ratio_histograms, process):
    """
    Plot the ratio histograms on a single canvas.
    """
    if not ratio_histograms:
        print("No histograms to plot!")
        return

    canvas = cv.new_canvas(nPads = 1, name = "variations")
    text = "#bf{CMS} Simulation"
    cmsprel = cv.add_text("#bf{CMS} Simulation", (.08, .91, .5, .97))

    legend_updn = ROOT.TLegend(0.62, 0.91, 0.9, 0.96)
    legend_updn.SetNColumns(2)
    legend_updn.SetBorderSize(0)
    legend_updn.SetTextSize(0.055)


    # Create a legend
    legend = ROOT.TLegend(0.12, 0.55, 0.9, 0.88)
    legend.SetNColumns(4)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.025)

    # Use the first ratio histogram to set the range, title, etc.
    first_hist = ratio_histograms[0]
    first_hist.SetTitle("")
    first_hist.SetMarkerSize(0)
    first_hist.GetYaxis().SetRangeUser(0.9, 1.15)
    first_hist.SetLineColor(ROOT.kBlack)
    first_hist.SetTitle("")
    first_hist.GetYaxis().SetTitle("Ratio")
    first_hist.GetXaxis().SetTitle(nominal_hist.GetXaxis().GetTitle())
    first_hist.Draw()
    first_hist.SetMarkerSize(0)
    if "scale" in first_hist.GetName() or "ID" in first_hist.GetName():
        name = "_".join(first_hist.GetName().split("_")[-2:])
    elif "year" in first_hist.GetName():
        name = "_".join(first_hist.GetName().split("_")[-2:])
    else:
        name = first_hist.GetName().split("_")[-1] 
    legend.AddEntry(first_hist, name, "l")

    up_example = deepcopy(first_hist)
    dn_example = deepcopy(first_hist)

    up_example.SetMarkerSize(0)
    up_example.SetLineColor(ROOT.kBlack)
    dn_example.SetMarkerSize(0)
    dn_example.SetLineColor(ROOT.kBlack)
    dn_example.SetLineStyle(2)

    legend_updn.AddEntry(up_example, "Up", "l")
    legend_updn.AddEntry(dn_example, "Down", "l")
   
    first_hist.GetXaxis().SetLabelSize(0.07)
    first_hist.GetXaxis().SetTitle("Channel flavor")
    for ibin in range(1, first_hist.GetNbinsX()+1):
        if ibin == 1:
            first_hist.GetXaxis().SetBinLabel(ibin, "eee") 
        if ibin == 2:
            first_hist.GetXaxis().SetBinLabel(ibin, "ee\\mu")
        if ibin == 3:
            first_hist.GetXaxis().SetBinLabel(ibin, "e\\mu\\mu")
        if ibin == 4:
            first_hist.GetXaxis().SetBinLabel(ibin, "\\mu\\mu\\mu")

    # Iterate over other histograms and plot them
    counter = 1
    color = 1
    for i, hist in enumerate(ratio_histograms[1:], 1):
        if counter%2 == 0:
            color = color + 1  # ROOT colors start from 1 (kBlack)
        hist.SetLineColor(color)
        hist.SetMarkerSize(0)
        hist.Draw("same")  # Draw on the same canvas

        if "scale" in hist.GetName() or "ID" in hist.GetName():
            name = "_".join(hist.GetName().split("_")[-2:])
        elif "year" in hist.GetName():
            name = "_".join(hist.GetName().split("_")[-2:])
        else:
            name = hist.GetName().split("_")[-1] 
       
        if "Up" not in hist.GetName():
          hist.SetLineStyle(9)
        else:
          legend.AddEntry(hist, name.replace("Up",""), "l")

        counter += 1 

    legend.Draw("same")  # Draw the legend on the canvas
    legend_updn.Draw("same")  # Draw the legend on the canvas
    cmsprel.Draw("same")
    canvas.Update()
    canvas.Print("{}_ratio_variations.png".format(process))
    canvas.Print("{}_ratio_variations.pdf".format(process))

    
if __name__ == "__main__":
    opts = add_parsing_options()
    file_name = opts.infile
    process = "x_prompt_WZ"

    nominal_hist, ratio_histograms = retrieve_histograms(file_name, process)
    plot_histograms(nominal_hist, ratio_histograms, process)
