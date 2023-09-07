# Config file with processes. Used to create MCAs mostly
from cfgs.samplepaths import samplepaths as paths
from cfgs.datasets_cfg import dataset, datasets
from functions import color_msg
import sys
import os
import re


def get_local_files(name, isData, year = "2022EE"):
    inpath = os.path.join(paths["processed"], "data" if isData else "mc", year)
    files = list(filter(lambda element: name in element, os.listdir(inpath)))
    files = [file_.replace(".root", "") for file_ in files]
    return files

template_line = '{procname}: {files}: {norm} ;FillColor=ROOT.{fc}, Label="{label}", genSumWeightName="genEventSumw"\n'
template_line_data = '{procname}: {files}; Label="data"\n'

ftotal = open("mca/mca_wz_3l.txt", "w")
ftotal.write("# vim: syntax=sh\n")
for tier in ["data", "mc"]:
    for samplegroup, samples in datasets[tier].items():
        line = template_line if tier != "data" else template_line_data
        color_msg(" >> Writing MCA Sample: %s"%samplegroup, "green")
        outpath = os.path.join("mca/includes/mca-%s.txt"%(samplegroup))
        f = open(outpath, "w")
        # Header for the include file
        f.write("# vim: syntax=sh\n\n")
        
        # Add entry to the file that points to all includes
        ftotal.write("## %s\n"%samplegroup)
        ftotal.write('incl_%s : + ; IncludeMca="wz-run3/mca/includes/mca-%s.txt"\n\n'%(samplegroup, samplegroup))
        for samplename, sample in samples.items():
            color_msg("    * Adding %s"%samplename, "blue")
            f.write("# ---- %s ----\n"%samplename)
            for subsample in sample:
                color_msg("      + Name: %s - xsec: %s - label: %s"%(subsample.name, subsample.xsec, subsample.name), "none")
                files = subsample.get_processed_files()
                procname = samplename
                if samplegroup == "signal":
                    procname += "+"
                elif samplegroup == "data":
                    procname = "data"
                f.write(line.format(procname = procname,
                                    files = "+".join(files),
                                    norm = subsample.xsec,
                                    fc = subsample.fC,
                                    label = subsample.label))
            f.write("\n\n")
        f.close()
    ftotal.close()
