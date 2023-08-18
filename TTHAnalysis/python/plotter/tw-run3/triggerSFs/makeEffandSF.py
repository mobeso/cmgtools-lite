import ROOT as r
import os
import sys
import argparse
import math

r.gROOT.SetBatch(True)
r.gStyle.SetOptStat(0)
# Axis ticks in all sides of the plot
r.gStyle.SetPadTickX(1)
r.gStyle.SetPadTickY(1)

# limit the decimals in SetPaintTextFormat
r.gStyle.SetPaintTextFormat(".3f")

'''
Theory: https://indico.cern.ch/event/731987/contributions/3252702/attachments/1785783/2908948/tutorial_trigeff.pdf
'''

# Some dictionaries
xAxisTitles = { "trigger" : "Electron p_{T} (GeV)",
                "trigger-ee" : "Leading electron p_{T} (GeV)",
                "trigger-mm" : "Leading muon p_{T} (GeV)" }

yAxisTitles = { "trigger" : "Muon p_{T} (GeV)",
                "trigger-ee" : "Subleading electron p_{T} (GeV)",
                "trigger-mm" : "Subleading muon p_{T} (GeV)" }

savingNames = { "trigger" : "h2D_SF_emu_lepABpt_FullError",
                "trigger-ee" : "h2D_SF_ee_lepABpt_FullError",
                "trigger-mm" : "h2D_SF_mumu_lepABpt_FullError" }

histoNames = { "trigger" : "ept_mpt",
                "trigger-ee" : "lep1pt_lep2pt",
                "trigger-mm" : "lep1pt_lep2pt" }

def avoidUnconsistentEff(passed, total):
    '''
    In MC there is the posibility that if the eff is close to 1, some events
    from the pass with negative weights are removed.
    The result is some bins of pass are bigger than the total.

    This function redifines the histograms by taking the value passed = total
    '''
    for i in range(1, passed.GetNbinsX() + 1):
        for j in range(1, passed.GetNbinsY() + 1):
            if passed.GetBinContent(i, j) > total.GetBinContent(i, j):
                passed.SetBinContent(i, j, total.GetBinContent(i, j))

if __name__=="__main__":
    parser = argparse.ArgumentParser(usage = "python3 plotterHelper.py [options]", description = "Helper for plotting.", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inpath',   '-i', metavar = 'inpath',   dest = "inpath", required = False, default = "./temp/varplots")
    parser.add_argument('--channel',    '-c', metavar = 'channel',    dest = "channel",  required = False, default = "mu")
    parser.add_argument('--outpath',  '-o', metavar = 'outpath',  dest = "outpath",  required = False, default = "./temp/varplots")


    args     = parser.parse_args()
    inpath  = args.inpath
    channel   = args.channel # Can be: trigger, trigger-ee, trigger-mm
    outpath = args.outpath

    # Create the output directory if it doesn't exist
    if not os.path.exists(outpath):
        os.makedirs(outpath)

    metOnlyFolder = "METTrig"
    metLepFolder = "METandLeptonTrig"

    plotsRoot = "plots-tw-{channel}.root".format(channel = channel)

    # Get the histograms
    metOnly   = r.TFile.Open(inpath + "/" + channel + "/" + metOnlyFolder + "/" + plotsRoot, "READ")
    metLepton = r.TFile.Open(inpath + "/" + channel + "/" + metLepFolder + "/" + plotsRoot, "READ")

    # Get the 2D histograms data and MC
    histoName = histoNames[channel]
    metOnlyData   = metOnly.Get("{name}_data".format(name = histoName))
    metOnlyMC     = metOnly.Get("{name}_ttbar".format(name = histoName))

    metLeptonData = metLepton.Get("{name}_data".format(name = histoName))
    metLeptonMC   = metLepton.Get("{name}_ttbar".format(name = histoName))

    avoidUnconsistentEff(metLeptonMC, metOnlyMC)
    # Efficiency histograms (ratio of metLeptonData to metOnlyData)
    effData = metLeptonData.Clone("effData")
    effData.Divide(metOnlyData)

    effMC = metLeptonMC.Clone("effMC")
    effMC.Divide(metOnlyMC)

    # Compute the scale factors (ratio of effData to effMC)
    sf = effData.Clone("sf")
    sf.Divide(effMC)

    # Plot the scale factors and efficiencies
    c = r.TCanvas("c", "c", 1400, 900)
    # Set margins
    c.SetBottomMargin(0.15)
    c.SetLeftMargin(0.2)
    c.SetRightMargin(0.15)
    c.cd()

    # Scale factors
    sf.SetTitle("Scale Factors")
    sf.GetXaxis().SetTitle(xAxisTitles[channel])
    sf.GetYaxis().SetTitle(yAxisTitles[channel])
    #sf.GetZaxis().SetRangeUser(0.5, 1.)
    sf.Draw("colz TEXT45")
    c.SaveAs(outpath + "/sf_" + channel + ".pdf")
    c.SaveAs(outpath + "/sf_" + channel + ".png")

    # Efficiencies
    effData.SetTitle("Efficiencies")
    effData.GetXaxis().SetTitle(xAxisTitles[channel])
    effData.GetYaxis().SetTitle(yAxisTitles[channel])
    #effData.GetZaxis().SetRangeUser(0.5, 1.5)
    effData.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effData_" + channel + ".pdf")
    c.SaveAs(outpath + "/effData_" + channel + ".png")

    effMC.SetTitle("Efficiencies")
    effMC.GetXaxis().SetTitle(xAxisTitles[channel])
    effMC.GetYaxis().SetTitle(yAxisTitles[channel])
    #effMC.GetZaxis().SetRangeUser(0.5, 1.5)
    effMC.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effMC_" + channel + ".pdf")
    c.SaveAs(outpath + "/effMC_" + channel + ".png")

    # Now plot the uncertainties of the scale factors and efficiencies
    # Get the uncertainties
    # Scale factors
    sfUnc = sf.Clone("sfUnc")
    for i in range(1, sfUnc.GetNbinsX()+1):
        for j in range(1, sfUnc.GetNbinsY()+1):
            sfUnc.SetBinContent(i, j, sf.GetBinError(i, j))
    
    # Efficiencies
    effDataUnc = effData.Clone("effDataUnc")
    for i in range(1, effDataUnc.GetNbinsX()+1):
        for j in range(1, effDataUnc.GetNbinsY()+1):
            effDataUnc.SetBinContent(i, j, effData.GetBinError(i, j))
    
    effMCUnc = effMC.Clone("effMCUnc")
    for i in range(1, effMCUnc.GetNbinsX()+1):
        for j in range(1, effMCUnc.GetNbinsY()+1):
            effMCUnc.SetBinContent(i, j, effMC.GetBinError(i, j))

    # Scale factors
    sfUnc.SetTitle("Scale Factor Uncertainties")
    sfUnc.GetXaxis().SetTitle(xAxisTitles[channel])
    sfUnc.GetYaxis().SetTitle(yAxisTitles[channel])
    sfUnc.GetZaxis().SetRangeUser(0., 0.2)
    sfUnc.Draw("colz TEXT45")
    c.SaveAs(outpath + "/sfUnc_" + channel + ".pdf")
    c.SaveAs(outpath + "/sfUnc_" + channel + ".png")

    # Efficiencies
    effDataUnc.SetTitle("Efficiency Uncertainties")
    effDataUnc.GetXaxis().SetTitle(xAxisTitles[channel])
    effDataUnc.GetYaxis().SetTitle(yAxisTitles[channel])
    effDataUnc.GetZaxis().SetRangeUser(0., 0.2)
    effDataUnc.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effDataUnc_" + channel + ".pdf")
    c.SaveAs(outpath + "/effDataUnc_" + channel + ".png")

    effMCUnc.SetTitle("Efficiency Uncertainties")
    effMCUnc.GetXaxis().SetTitle(xAxisTitles[channel])
    effMCUnc.GetYaxis().SetTitle(yAxisTitles[channel])
    effMCUnc.GetZaxis().SetRangeUser(0., 0.2)
    effMCUnc.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effMCUnc_" + channel + ".pdf")
    c.SaveAs(outpath + "/effMCUnc_" + channel + ".png")

    # Now compute the scale factor uncertainties but using the Clopper-Pearson method
    efficiencyDataCP = r.TEfficiency(metLeptonData, metOnlyData)
    efficiencyMCCP = r.TEfficiency(metLeptonMC, metOnlyMC)

    # Create a clone of the eff histograms to store the uncertainties from TEfficiency
    effDataUncCP = effData.Clone("effDataUncCP")
    effMCUncCP = effMC.Clone("effMCUncCP")
    for i in range(1, efficiencyDataCP.GetPassedHistogram().GetNbinsX()+1):
        for j in range(1, efficiencyDataCP.GetPassedHistogram().GetNbinsY()+1):
            dataUnc = (efficiencyDataCP.GetEfficiencyErrorLow(efficiencyDataCP.GetGlobalBin(i, j)) + efficiencyDataCP.GetEfficiencyErrorUp(efficiencyDataCP.GetGlobalBin(i, j))) / 2.
            mcUnc = (efficiencyMCCP.GetEfficiencyErrorLow(efficiencyMCCP.GetGlobalBin(i, j)) + efficiencyMCCP.GetEfficiencyErrorUp(efficiencyMCCP.GetGlobalBin(i, j))) / 2.
            effDataUncCP.SetBinContent(i, j, dataUnc)
            effMCUncCP.SetBinContent(i, j, mcUnc)
    
    # Efficiencies
    effDataUncCP.SetTitle("Efficiency Uncertainties (CP)")
    effDataUncCP.GetXaxis().SetTitle(xAxisTitles[channel])
    effDataUncCP.GetYaxis().SetTitle(yAxisTitles[channel])
    effDataUncCP.GetZaxis().SetRangeUser(0., 0.2)
    effDataUncCP.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effDataUncCP_" + channel + ".pdf")
    c.SaveAs(outpath + "/effDataUncCP_" + channel + ".png")

    effMCUncCP.SetTitle("Efficiency Uncertainties (CP)")
    effMCUncCP.GetXaxis().SetTitle(xAxisTitles[channel])
    effMCUncCP.GetYaxis().SetTitle(yAxisTitles[channel])
    effMCUncCP.GetZaxis().SetRangeUser(0., 0.2)
    effMCUncCP.Draw("colz TEXT45")
    c.SaveAs(outpath + "/effMCUncCP_" + channel + ".pdf")
    c.SaveAs(outpath + "/effMCUncCP_" + channel + ".png")

    # Propagate the uncertainties to the scale factors, we have efficiencyDataCP, efficiencyMCCP and their uncertainties
    # We apply the formula: SF = effDataCP / effMCCP and propagate the uncertainties

    # Scale factors
    sfUncCP = sf.Clone("sfUncCP")
    for i in range(1, sfUncCP.GetNbinsX()+1):
        for j in range(1, sfUncCP.GetNbinsY()+1):
            # Check if the denominator is zero
            if effMC.GetBinContent(i, j) == 0. or effData.GetBinContent(i, j) == 0.:
                sfUncCP.SetBinContent(i, j, 0.)
            else:
                sfUncCP.SetBinContent(i, j, sf.GetBinContent(i, j) * math.sqrt((effDataUncCP.GetBinContent(i, j) / effData.GetBinContent(i, j))**2 + (effMCUncCP.GetBinContent(i, j) / effMC.GetBinContent(i, j))**2))
    
    # Scale factors
    sfUncCP.SetTitle("Scale Factor Uncertainties (CP)")
    sfUncCP.GetXaxis().SetTitle(xAxisTitles[channel])
    sfUncCP.GetYaxis().SetTitle(yAxisTitles[channel])
    #sfUncCP.GetZaxis().SetRangeUser(0., 0.2)
    sfUncCP.Draw("colz TEXT45")
    c.SaveAs(outpath + "/sfUncCP_" + channel + ".pdf")
    c.SaveAs(outpath + "/sfUncCP_" + channel + ".png")

    # Output root file with the histos (append if it exists)
    outroot = r.TFile.Open(outpath + "/triggerSFs.root", "UPDATE")
    # We will only write the sf but we have to update the bin errors to the ones from the CP method
    for i in range(1, sf.GetNbinsX()+1):
        for j in range(1, sf.GetNbinsY()+1):
            sf.SetBinError(i, j, sfUncCP.GetBinContent(i, j))
    
    # Save the sf with savingNames[channel]
    sf.SetName(savingNames[channel])
    sf.Write()
    outroot.Close()







