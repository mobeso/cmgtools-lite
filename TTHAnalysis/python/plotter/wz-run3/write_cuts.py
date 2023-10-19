# Config file with processes. Used to create CUT files mostly
from cfgs.samplepaths import samplepaths as paths
from cfgs.selections_cfg import *
from functions import color_msg
from copy import deepcopy
from collections import OrderedDict
import sys
import os
import re


# -------------------- Cut in met (to be optimized) -------------------- #
met = {
    "met_10" : "MET_pt_central > 10; Disable=True",
    "met_15" : "MET_pt_central > 15; Disable=True",
    "met_20" : "MET_pt_central > 20; Disable=True",
    "met_25" : "MET_pt_central > 25; Disable=True",
    "met_30" : "MET_pt_central > 30; Disable=True",
    "met_35" : "MET_pt_central > 35; Disable=True",
    "met_40" : "MET_pt_central > 40; Disable=True",
}

## Define the cut files here
# --- Signal region --- #
srwz = deepcopy(baseline_wz)
srwz.update(ExactlyThreeLeptons)
srwz.update({
    "btag" : "nBJetTight25_Mini == 0",
    "zPeak" : "abs(mll_3l - 91.16) < 15"
})
srwz.update(met)


# --- ZZ Control region --- #
crzz = deepcopy(baseline_wz)
crzz.update(ExactlyFourLeptons)
crzz.update({
    "btag" : "nBJetTight25_Mini == 0",
    "zPeak" : "abs(mll_3l - 91.16) < 15",
    "noTau" : "((abs(LepSel_pdgId[0]) + abs(LepSel_pdgId[1]) + abs(LepSel_pdgId[2]) + abs(LepSel_pdgId[3]) - 44)/2)%2 == 0"
})
crzz.update(met)


# --- CR Nonprompt (DY) Control region --- #
crnpdy = deepcopy(baseline_wz)
crnpdy.update(ExactlyThreeLeptons)
crnpdy.update({
    "btag" : "nBJetTight25_Mini == 0",
    "zPeak" : "abs(mll_3l - 91.16) < 15",
    "met" : "MET_pt_central < 30"
})

# --- CR Nonprompt (TT) Control region --- #
crnptt = deepcopy(baseline_wz)
crnptt.update(ExactlyThreeLeptons)
crnptt.update(met)
crnptt.update({
    "btag" : "nBJetTight25_Mini > 0",
    "zPeak" : "abs(mll_3l - 91.16) > 15",
})

# --- For trigger SF measurement --- #
AtLeastThreeLeptons_forTrigger = deepcopy(AtLeastThreeLeptons)
AtLeastThreeLeptons_forTrigger.pop("m3l", None)
trigger = deepcopy(always)
trigger.update({
    "filters" : baseline["filters"],
    "reftrigger": "HLT_PFMETNoMu110_PFMHTNoMu110_IDTight || HLT_PFMETNoMu120_PFMHTNoMu120_IDTight",
    "trigger"   : "Trigger_3l; Disable=True",
    "met"       : "MET_pt_central > 120",
    "barrel3"   : "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 3 ; Disable=True",
    "barrel2"   : "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 2 ; Disable=True",
    "barrel1"   : "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 1 ; Disable=True",
    "barrel0"   : "(abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) + (abs(LepSel_eta[1]) < (1.2+0.245*(abs(LepSel_pdgId[1])==11))) + (abs(LepSel_eta[0]) < (1.2+0.245*(abs(LepSel_pdgId[0])==11))) == 0 ; Disable=True"
})
trigger.update(AtLeastThreeLeptons_forTrigger)


selections = [
    ("srwz", srwz),
    ("crzz", crzz),
    ("trigger", trigger)
    #("crnpdy", crnpdy),
    #("crnptt", crnptt)
]

if __name__ == "__main__":
    for selname, selection in selections:
        color_msg(" >> Writing cut file for: %s "%selname, "green")
        outf = "common/cuts-%s.txt"%selname
        f = open(outf, "w")
        f.write("# vim: syntax=sh\n")
        f.write("# Cuts for %s\n\n"%selname)
        for cutid, cut in selection.items():
            f.write("%s: %s\n"%(cutid, cut))
        
        f.write("\n\n# Flavor split\n")
        for flavcut, cut in flavor_splits.items():
            f.write("%s: %s\n"%(flavcut, cut))
        f.close()