import ROOT
import os, re, sys
from copy import deepcopy
import json
import argparse
import numpy as np
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
    if not nominal_hist:
        print("Nominal histogram not found!")
        return None, []

    # Iterate over keys in file and find the up/down variations
    ratio_histograms = []
    key_list = root_file.GetListOfKeys()
    for key in key_list:
        hist_name = key.GetName()
        if "scale" not in hist_name: continue
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

    canvas = ROOT.TCanvas("c1", "Histogram ratios for {}".format(process), 800, 600)

    # Create a legend
    legend = ROOT.TLegend(0.12, 0.65, 0.9, 0.88)
    legend.SetNColumns(4)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.025)

    # Use the first ratio histogram to set the range, title, etc.
    first_hist = ratio_histograms[0]
    first_hist.SetTitle("")
    first_hist.SetMarkerSize(0)
    first_hist.GetYaxis().SetRangeUser(0.9, 1.25)
    first_hist.SetLineColor(ROOT.kBlack)
    first_hist.SetTitle("Variation/Nominal")
    first_hist.GetYaxis().SetTitle("Ratio")
    first_hist.GetXaxis().SetTitle(nominal_hist.GetXaxis().GetTitle())
    first_hist.Draw()
    name = first_hist.GetName().split("_")[-1] if "scale" not in first_hist.GetName() else "_".join(first_hist.GetName().split("_")[-2:])
    legend.AddEntry(first_hist, name, "l")

    # Iterate over other histograms and plot them
    for i, hist in enumerate(ratio_histograms[1:], 1):
        color = i + 1  # ROOT colors start from 1 (kBlack)
        hist.SetLineColor(color)
        hist.Draw("same")  # Draw on the same canvas
        hist.SetMarkerSize(0)
        name = hist.GetName().split("_")[-1] if "scale" not in hist.GetName() else "_".join(hist.GetName().split("_")[-2:])
        legend.AddEntry(hist, name, "l")

    legend.Draw("same")  # Draw the legend on the canvas

    canvas.Update()
    canvas.Print("{}_ratio_variations.png".format(process))
    canvas.Print("{}_ratio_variations.pdf".format(process))

    
if __name__ == "__main__":
    opts = add_parsing_options()
    file_name = opts.infile
    process = "x_prompt_WZ"

    nominal_hist, ratio_histograms = retrieve_histograms(file_name, process)
    plot_histograms(nominal_hist, ratio_histograms, process)
