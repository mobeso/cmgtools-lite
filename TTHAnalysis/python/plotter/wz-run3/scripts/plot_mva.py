""" Script to plot MVA performance plots """

import ROOT as r
from copy import deepcopy
import os,sys
from optparse import OptionParser
import canvas as cv
import array as ar
import numpy as np
from array import array

r.gROOT.SetBatch(1)
r.gStyle.SetOptStat(0)


sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
from functions import color_msg


def add_parsing_opts():
    ''' Function with base parsing arguments used by any script '''
    parser = OptionParser(usage = "python plot_triggerSF.py [options]", 
                                    description = "Main options for running WZ trigger SF") 
    parser.add_option("--file", dest = "file_", default = None,
                help = "Path to the file with the numerator histograms.")
    return parser.parse_args()

def get_yields(h, name):
    """ Returns the number of anything per MVA score in a TGraph. """
    gr = r.TGraph()
    nbins = h.GetNbinsX() 
    for bini in range(1, 1+nbins):
        x_point = h.GetBinLowEdge(bini)
        yields = h.Integral(bini, 1+nbins)
        eff = yields/h.Integral()
        gr.SetPoint(bini-1, x_point, eff)
    gr.SetName(name)
    return gr

def get_eff(h, wp):
    """ Function to integrate and get overall efficiencies """
    # The working point is the cut on discriminant in the X axis.
    # But the integral has to be done using the bin number
    bini = h.FindBin(wp)
    nbins = h.GetNbinsX()
    eff = h.Integral(bini, nbins+1) / h.Integral()
    return eff

def cut_on_graph(gr, thr):
    """ 
        This function returns the GRAPH POINT above which the associated value 
        (point content) is below a given threshold
    """
    npoints = gr.GetN() 
    correct_WP = 0
    for i in range(npoints):
        # Get the value for this point
        current_value = gr.GetPointY(i)

        # Find the point at which the value you obtain
        # is <= the threshold you set.
        if (current_value  <= thr):
            x_value = gr.GetPointX(i)
            y_value = gr.GetPointY(i)
            return (i, x_value, y_value) 

def cut_on_hist(h, thr):
    """ 
        This function returns the HIST BIN above which the INTEGRAL value 
        is below a given threshold
    """
    nbins = h.GetNbinsX()

    for bini in range(1, nbins+1):
      current_val = h.Integral(bini, nbins+1)/h.Integral()
      if current_val <= thr:
          return (bini, h.GetBinLowEdge(bini))

def ROC_curve(sig, bkg, name):
    """ Returns a ROC curve: 
    That is the integral for a given range of bins (WP)
    of signal over background 
    """
    integral_sig = sig.Integral()
    integral_bkg = bkg.Integral()
    eff_s = 0
    eff_b = 0
    
    roc = r.TGraph()
    nbins = sig.GetNbinsX()
    for b in range(1, 1+nbins):
        S = sig.Integral(b, nbins+1)
        B = bkg.Integral(b, nbins+1)
        eff_sig = S / integral_sig
        eff_bkg = B / integral_bkg
        roc.SetPoint(b-1, eff_bkg, eff_sig)
 
    roc.SetName(name)
    return roc

def get_siginificance(h_sig, h_bkg, name, kind):
    """ Function to get a significant curve of different kinds:
        kind=1: S/B
        kind=2: S/sqrt(B)
        kind=3: S/sqrt(S+B)
    """

    gr = r.TGraph()
    nbins = h_sig.GetNbinsX() 
    for i in range(1, 1+nbins):
        S = h_sig.Integral(i, nbins+1)
        B = h_bkg.Integral(i, nbins+1)

        #x = -1 + i*0.002
        x = h_sig.GetBinCenter(i)
        if B != 0:
            if kind == 0:
                gr.SetPoint(i-1, x, S/B)
            elif kind == 1:
                gr.SetPoint(i-1, x, S/np.sqrt(B))
            elif kind == 2:
                gr.SetPoint(i-1, x, S/np.sqrt(S+B))
            else:
                color_msg("Wrong kind of significance. Choose 0, 1 or 2.", "red")
                sys.exist()
        else:
            gr.SetPoint(i-1, x, 0)
    gr.SetName(name)
    return gr

def rebin_histo(nquant, h, firstBin = [-1.0]):

    #h = get_histos(var, path, someProcess = "background")

    xquant = array('d')
    yquant = array('d', [0.] * nquant)
    init = array('d', firstBin) #min bin

    for q in range(0, nquant):
            xquant.append(float((q+1))/nquant)

    h.GetQuantiles(nquant, yquant, xquant) # Use background to rebin


    rebining = init + yquant
    rebining = rebining.tolist()

    return rebining

if __name__ == "__main__":
    opts, _ = add_parsing_opts()
    
    file_ = opts.file_
    outpath = opts.file_.split("/")[0]
    
    # Get the important histograms. This is an specific
    # code for plotting 4 (3 atm) different MVAs.
    f = r.TFile.Open(file_)
    
    h_signal_legacy_total = deepcopy(f.Get("h_signal_legacy_total"))
    h_signal_tth_total = deepcopy(f.Get("h_signal_tth_total"))
    h_signal_ttw_total = deepcopy(f.Get("h_signal_ttw_total"))
    h_bkg_legacy_total = deepcopy(f.Get("h_bkg_legacy_total"))
    h_bkg_tth_total = deepcopy(f.Get("h_bkg_tth_total"))
    h_bkg_ttw_total = deepcopy(f.Get("h_bkg_ttw_total"))
    h_signal_legacy = deepcopy(f.Get("h_signal_legacy"))
    h_signal_tth = deepcopy(f.Get("h_signal_tth"))
    h_signal_ttw = deepcopy(f.Get("h_signal_ttw"))
    h_bkg_legacy = deepcopy(f.Get("h_bkg_legacy"))
    h_bkg_tth = deepcopy(f.Get("h_bkg_tth"))
    h_bkg_ttw = deepcopy(f.Get("h_bkg_ttw")) 
    
    f.Close()
    
    """ Now start plotting stuff """
    # ----------------- Fake lepton yields ----------------- #
    cFakes = cv.new_canvas(nPads = 1, name = "fakeYields")
    cFakes.SetLogy()
    lFakes = cv.new_legend((0.15, 0.3, 0.35, 0.45))
    lFakes.SetTextSize(0.03)
    
    ## Legacy
    gr_legacy_fakeLeps = get_yields(h_bkg_legacy, "Fake yielsds legacy")
    gr_legacy_fakeLeps.SetLineColor(r.kBlack)
    gr_legacy_fakeLeps.SetLineWidth(2)
    
    # Get NFakes at legacy WP
    legacy_nFakes_wp = gr_legacy_fakeLeps.Eval(0.8)
    legacy_nFakes_point = r.TGraph()
    legacy_nFakes_point.SetPoint(0, 0.8, legacy_nFakes_wp)
    legacy_nFakes_point.SetMarkerStyle(20)
    legacy_nFakes_point.SetMarkerSize(2)
    legacy_nFakes_point.SetMarkerColor(r.kBlack)
    legacy_signal_eff = get_eff(h_signal_legacy, 0.8)
    
    ## Run3 (ttH)
    gr_tth_fakeLeps = get_yields(h_bkg_tth, "Fake yields run3 (ttH-like)")
    gr_tth_fakeLeps.SetLineColor(r.kRed)
    gr_tth_fakeLeps.SetLineWidth(2)
    
    # Get WP in new training to match legacy FR
    _, wp_tth, _ = cut_on_graph(gr_tth_fakeLeps, legacy_nFakes_wp )
    nFakes_tth =  gr_tth_fakeLeps.Eval(wp_tth)
    
    tth_nFakes_point = r.TGraph()
    tth_nFakes_point.SetPoint(0, wp_tth, nFakes_tth )
    tth_nFakes_point.SetMarkerStyle(20)
    tth_nFakes_point.SetMarkerSize(2)
    tth_nFakes_point.SetMarkerColor(r.kRed)
    tth_signal_eff = get_eff(h_signal_tth, wp_tth)
    
    ## Run3 (ttW)
    gr_ttw_fakeLeps = get_yields(h_bkg_ttw, "Fake yields run3 (ttW-like)")
    gr_ttw_fakeLeps.SetLineColor(r.kAzure+7)
    gr_ttw_fakeLeps.SetLineWidth(2)
    
    # Get WP in new training to match legacy FR
    _, wp_ttw, _ = cut_on_graph(gr_ttw_fakeLeps, legacy_nFakes_wp )
    nFakes_ttw =  gr_ttw_fakeLeps.Eval(wp_ttw)

    ttw_nFakes_point = r.TGraph()
    ttw_nFakes_point.SetPoint(0, wp_ttw, nFakes_ttw )
    ttw_nFakes_point.SetMarkerStyle(20)
    ttw_nFakes_point.SetMarkerSize(2)
    ttw_nFakes_point.SetMarkerColor(r.kAzure+7)
    ttw_signal_eff = get_eff(h_signal_ttw, wp_ttw)

    # Add some labels for the legend
    legacy_leg = "Legacy (#epsilon_{s} = %3.2f, %3.2f) "%(legacy_signal_eff, 0.8)
    tth_leg = "ttH (#epsilon_{s} = %3.2f, %3.2f) "%(tth_signal_eff, wp_tth)
    ttw_leg = "ttW (#epsilon_{s} = %3.2f, %3.2f) "%(ttw_signal_eff, wp_ttw)
    lFakes.SetHeader("f_{R} = %3.4f"%legacy_nFakes_wp, "C")
    
    lFakes.AddEntry(gr_legacy_fakeLeps, legacy_leg)
    lFakes.AddEntry(gr_tth_fakeLeps, tth_leg)
    lFakes.AddEntry(gr_ttw_fakeLeps, ttw_leg)

    # Draw canvas
    gr_legacy_fakeLeps.GetXaxis().SetTitle("BDT Discriminant")
    gr_legacy_fakeLeps.GetYaxis().SetTitle("Number of fakes")
    gr_legacy_fakeLeps.Draw("AL")
    gr_tth_fakeLeps.Draw("L same")
    gr_ttw_fakeLeps.Draw("L same")
    legacy_nFakes_point.Draw("P same")
    tth_nFakes_point.Draw("P same")
    ttw_nFakes_point.Draw("P same")
    lFakes.Draw("same")
    
    cFakes.SaveAs( os.path.join(outpath, "nfakes_%s.png"%("muon" if "mu" in file_ else "el")))
    cFakes.SaveAs( os.path.join(outpath, "nfakes_%s.pdf"%("muon" if "mu" in file_ else "el")))

    # ------------------------------------------------------- #

    
    # ----------------- ROC curves ----------------- #
    cRoc = cv.new_canvas(nPads = 1, name = "ROC")
    cRoc.SetLogx()
    lRoc = cv.new_legend((0.2, 0.65, 0.6, 0.85))
    lRoc.SetTextSize(0.03)
    
    ## Legacy
    ROC_legacy = ROC_curve(h_signal_legacy, h_bkg_legacy, "legacy")
    ROC_legacy.SetLineColor(r.kBlack)
    ROC_legacy.SetLineWidth(2)
    fr_legacy = get_eff(h_bkg_legacy, 0.8) # FR for tight legacy WP
    _, wp_legacy = cut_on_hist(h_bkg_legacy, fr_legacy) # "Exact" WP
    signalEff_legacy = get_eff(h_signal_legacy, 0.8) # Signal efficiency
    gr_legacy_wp = r.TGraph()
    gr_legacy_wp.SetPoint(0, fr_legacy, signalEff_legacy)  
    gr_legacy_wp.SetMarkerSize(2)
    gr_legacy_wp.SetMarkerStyle(20)
    gr_legacy_wp.SetMarkerColor(r.kBlack)
    
    ## ttH run3
    ROC_tth = ROC_curve(h_signal_tth, h_bkg_tth, "tth-like")
    ROC_tth.SetLineColor(r.kRed)
    ROC_tth.SetLineWidth(2)
    _, wp_tth = cut_on_hist(h_bkg_tth, fr_legacy) # Get WP for same legacy FR
    fr_tth = get_eff(h_bkg_tth, wp_tth) # Get FR at that WP
    signalEff_tth = get_eff(h_signal_tth, wp_tth) # Get Signal Eff at that wp
    gr_tth_wp = r.TGraph()
    gr_tth_wp.SetPoint(0, fr_tth, signalEff_tth)  
    gr_tth_wp.SetMarkerSize(2)
    gr_tth_wp.SetMarkerStyle(20)
    gr_tth_wp.SetMarkerColor(r.kRed)
    
    ## ttW run3
    ROC_ttw = ROC_curve(h_signal_ttw, h_bkg_ttw, "ttw-like")
    ROC_ttw.SetLineColor(r.kAzure+7)
    ROC_ttw.SetLineWidth(2)
    _, wp_ttw = cut_on_hist(h_bkg_ttw, fr_legacy)
    fr_ttw = get_eff(h_bkg_ttw, wp_ttw)
    signalEff_ttw = get_eff(h_signal_ttw, wp_ttw)
    gr_ttw_wp = r.TGraph()
    gr_ttw_wp.SetPoint(0, fr_ttw, signalEff_ttw)  
    gr_ttw_wp.SetMarkerSize(2)
    gr_ttw_wp.SetMarkerStyle(20)
    gr_ttw_wp.SetMarkerColor(r.kAzure+1)
    
    
    # Add some labels for the legend

    legacy_leg = "Legacy (#epsilon_{s} = %3.2f, %3.2f) "%(signalEff_legacy, 0.8)
    tth_leg = "ttH (#epsilon_{s} = %3.2f, %3.2f) "%(signalEff_tth, wp_tth)
    ttw_leg = "ttW (#epsilon_{s} = %3.2f, %3.2f) "%(signalEff_ttw, wp_ttw)
    lRoc.SetHeader("f_{R} = %3.4f"%fr_ttw, "C") 
    lRoc.AddEntry(ROC_legacy, legacy_leg)
    lRoc.AddEntry(ROC_tth, tth_leg)
    lRoc.AddEntry(ROC_ttw, ttw_leg)

    # Draw canvas
    ROC_legacy.GetXaxis().SetRangeUser(1e-4, 1)
    ROC_legacy.GetYaxis().SetTitle("Signal efficiency")
    ROC_legacy.GetXaxis().SetTitle("Bkg efficiency")
    ROC_legacy.Draw("AL")
    ROC_tth.Draw("L same")
    ROC_ttw.Draw("L same")
    gr_legacy_wp.Draw("P same")
    gr_tth_wp.Draw("P same")
    gr_ttw_wp.Draw("P same")
    lRoc.Draw("same")
    
    cRoc.SaveAs( os.path.join(outpath, "roc_curve_%s.png"%("muon" if "mu" in file_ else "el")))
    cRoc.SaveAs( os.path.join(outpath, "roc_curve_%s.pdf"%("muon" if "mu" in file_ else "el")))
    # ------------------------------------------------------- #
    
    # ----------------- Significance curves ----------------- #
    cSignificance = cv.new_canvas(nPads = 1, name = "significance")
    lSignificance = cv.new_legend((0.24, 0.25, 0.65, 0.45))
    lSignificance.SetTextSize(0.03)
    
    ## Legacy
    Significance_legacy = get_siginificance(h_signal_legacy, h_bkg_legacy, "legacy_sign", 2)
    Significance_legacy.SetLineColor(r.kBlack)
    Significance_legacy.SetLineWidth(2)

    ## ttH run3
    Significance_tth = get_siginificance(h_signal_tth, h_bkg_tth, "tth-like_sign", 2)
    Significance_tth.SetLineColor(r.kRed)
    Significance_tth.SetLineWidth(2)
    
    ## ttW run3
    Significance_ttw = get_siginificance(h_signal_ttw, h_bkg_ttw, "ttw-like_sign", 2)
    Significance_ttw.SetLineColor(r.kAzure+7)
    Significance_ttw.SetLineWidth(2)
    
    
    # Add some labels for the legend
    legacy_leg = "Legacy"
    tth_leg = "ttH-like"
    ttw_leg = "ttW-like"
    
    lSignificance.AddEntry(ROC_legacy, legacy_leg)
    lSignificance.AddEntry(ROC_tth, tth_leg)
    lSignificance.AddEntry(ROC_ttw, ttw_leg)

    # Draw canvas

    Significance_legacy.GetXaxis().SetTitle("BDT Discriminant")
    #Significance_legacy.GetYaxis().SetTitle("#frac{S}{#sqrt{S+B}}")
    Significance_legacy.GetYaxis().SetTitle("S/(S+B)")
    Significance_legacy.GetYaxis().SetLabelSize(0.025)
    Significance_legacy.Draw("AL")
    Significance_legacy.GetXaxis().SetRangeUser(-1, 1)
    Significance_legacy.GetYaxis().SetRangeUser(1600, 1888)
    Significance_tth.Draw("L same")
    Significance_ttw.Draw("L same")
    lSignificance.Draw("same")
    
    cSignificance.SaveAs( os.path.join(outpath, "significance_curve_%s.png"%("muon" if "mu" in file_ else "el")))
    cSignificance.SaveAs( os.path.join(outpath, "significance_curve_%s.pdf"%("muon" if "mu" in file_ else "el")))
    # ------------------------------------------------------- #
    
    
    # ----------------- Compute quantiles ----------------- #
    nq = 4 

    cQuantiles = cv.new_canvas(nPads = 1, name = "quantiles")
    lQuantiles = cv.new_legend((0.24, 0.25, 0.65, 0.45))
    lQuantiles.SetTextSize(0.03)
 
    # Legacy
    rebin_legacy = rebin_histo(nq, h_signal_legacy)
    print(rebin_legacy)
    bkg_legacy= deepcopy(h_bkg_legacy)
    sig_legacy = deepcopy(h_signal_legacy)
    norm = sig_legacy.Integral() + bkg_legacy.Integral()
    sig_legacy_rebin = sig_legacy.Rebin(nq, "sig_legacy", xbins = np.array(rebin_legacy))
    bkg_legacy_rebin = bkg_legacy.Rebin(nq, "bkg_legacy", xbins = np.array(rebin_legacy))
    sig_legacy_rebin.Scale(1/norm)
    bkg_legacy_rebin.Scale(1/norm)
    sig_legacy_rebin.SetLineColor(r.kBlack)
    sig_legacy_rebin.SetLineWidth(2)

    # ttH
    rebin_tth = rebin_histo(nq, h_signal_tth)
    bkg_tth= deepcopy(h_bkg_tth)
    sig_tth= deepcopy(h_signal_tth)
    norm = sig_tth.Integral() + bkg_tth.Integral()
    sig_tth_rebin = sig_tth.Rebin(nq, "sig_tth", xbins = np.array(rebin_tth))
    bkg_tth_rebin = bkg_tth.Rebin(nq, "bkg_tth", xbins = np.array(rebin_tth))
    sig_tth_rebin.Scale(1/norm)
    bkg_tth_rebin.Scale(1/norm)
    sig_tth_rebin.SetLineColor(r.kRed)
    sig_tth_rebin.SetLineWidth(2)
 
    # ttW 
    rebin_ttw = rebin_histo(nq, h_signal_ttw)
    bkg_ttw= deepcopy(h_bkg_ttw)
    sig_ttw= deepcopy(h_signal_ttw)
    norm = sig_ttw.Integral() + bkg_ttw.Integral()
    sig_ttw_rebin = sig_ttw.Rebin(nq, "sig_ttw", xbins = np.array(rebin_ttw))
    bkg_ttw_rebin = bkg_ttw.Rebin(nq, "bkg_ttw", xbins = np.array(rebin_ttw))
    sig_ttw_rebin.Scale(1/norm)
    bkg_ttw_rebin.Scale(1/norm)
    sig_ttw_rebin.SetLineColor(r.kAzure+7)
    sig_ttw_rebin.SetLineWidth(2)

    lQuantiles.AddEntry(sig_legacy_rebin, legacy_leg)
    lQuantiles.AddEntry(sig_tth_rebin, tth_leg)
    lQuantiles.AddEntry(sig_ttw_rebin, ttw_leg)



    # Draw canvas
    sig_legacy_rebin.GetXaxis().SetTitle("BDT Discriminant")
    sig_legacy_rebin.GetYaxis().SetTitle("#frac{S}{#sqrt{S+B}}")
    sig_legacy_rebin.GetYaxis().SetTitle("S/(S+B)")
    sig_legacy_rebin.GetYaxis().SetLabelSize(0.025)
    sig_legacy_rebin.Draw("hist")
    sig_legacy_rebin.GetXaxis().SetRangeUser(-1, 1)
    sig_tth_rebin.Draw("hist same")
    sig_ttw_rebin.Draw("hist same")
    lQuantiles.Draw("same")

    cQuantiles.SaveAs( os.path.join(outpath, "quantiles_%s.png"%("muon" if "mu" in file_ else "el")))

    cQuantiles.SaveAs( os.path.join(outpath, "quantiles_%s.pdf"%("muon" if "mu" in file_ else "el")))
