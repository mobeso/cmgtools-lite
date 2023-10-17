""" Script to plot a table with all sample metadata in LaTeX format """

import ROOT as r
from copy import deepcopy
import canvas as cv
import os,sys
from optparse import OptionParser

from make_latex_table import dict_to_latex_table
sys.path.append( os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3"))
from functions import color_msg
from cfgs.datasets_cfg import datasets

if __name__ == "__main__":
    table_mc = {
            "Short name" : [],
            "DAS" : [],
            "$\sigma$" : [],
            "Plotting group" : []
    }
    
    donelabels = []
    for biggroup, dset in datasets["mc"].items():
        for subgroup, samples in dset.items():
            for sample in samples:
                table_mc["Short name"].append(sample.name.replace("_","\_"))
                table_mc["DAS"].append("/%s/"%sample.dbspath.split("/")[1].replace("_", "\_"))
                table_mc["$\sigma$"].append("%3.2f"%sample.xsec)
                table_mc["Plotting group"].append(sample.label)

    # Rearrange plotting group to show just one cell
    
    table = dict_to_latex_table(table_mc)
    print(table)  