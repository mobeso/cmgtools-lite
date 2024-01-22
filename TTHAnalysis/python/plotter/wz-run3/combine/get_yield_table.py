""" Read input cards and provide a table """
import ROOT as r
import sys, os
import math
from make_latex_table import dict_to_latex_table

# Get the fitDiagnostics
f = r.TFile.Open("inclusiveFlavorFit/fitDiagnosticsTest.root")

dire = f.Get("shapes_prefit")

data = {'Process': [], 'eee': [], 'eem': [], 'mme': [], 'mmm': [], 'Inclusive': []}

totals = {}
totals_errs = {}
for ich, ch in enumerate(["ch1", "ch2", "ch3", "ch4"]):
    direch = dire.Get(ch)
    for hkey in direch.GetListOfKeys():
        if hkey.GetName() in ["data", "total", "prompt_WZ", "prompt_WZ_nonfiducial", "total_covar"]: continue
        h = direch.Get(hkey.GetName())
        
        
        if hkey.GetName() not in data["Process"]: 
            data["Process"].append(hkey.GetName())
            totals[hkey.GetName()] = 0
            totals_errs[hkey.GetName()] = 0
        
        if ch == "ch1": ret = "eee"    
        if ch == "ch2": ret = "eem"
        if ch == "ch3": ret = "mme"
        if ch == "ch4": ret = "mmm"
        
        totals[hkey.GetName()] += h.GetBinContent(ich+1)
        totals_errs[hkey.GetName()] += h.GetBinError(ich+1)*h.GetBinError(ich+1)
        
        if h.GetBinContent(1) > 1:
            data[ret].append("%d $\\pm$ %d"%(h.GetBinContent(ich+1), h.GetBinError(ich+1)))
        else:
            data[ret].append("%3.2f $\\pm$ %3.2f"%(h.GetBinContent(ich+1), h.GetBinError(ich+1)))

        


for proc, values in totals.items():
    if totals[proc] > 1:
        data["Inclusive"].append("%d $\\pm$ %d"%(totals[proc], math.sqrt(totals_errs[proc])))
    else:
        data["Inclusive"].append("%3.2f $\\pm$ %3.2f"%(totals[proc], math.sqrt(totals_errs[proc])))
    
        
# Print the processed data
caption="""Expected (pre-fit) yields (by flavor channel) for the relevant processes in the signal 
region of the analysis. All analysis uncertainties but the $(\mu_r, \mu_F)$ and PDFs are included."""




table = dict_to_latex_table(data, caption, "yields_prefit2022PostEE")
print(table)
