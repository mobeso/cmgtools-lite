""" Define your selections here """
from copy import deepcopy
from collections import OrderedDict

always = OrderedDict()
always.update ({
    "alwaystrue" :  "1"
})

data_flags = ['Flag_eeBadScFilter', 'Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter']
mc_flags = ['Flag_eeBadScFilter', 'Flag_goodVertices', 'Flag_globalSuperTightHalo2016Filter', 'Flag_HBHENoiseFilter', 'Flag_HBHENoiseIsoFilter', 'Flag_EcalDeadCellTriggerPrimitiveFilter', 'Flag_BadPFMuonFilter']


# -------------------- Baseline selection criteria for the analysis -------------------- #
baseline = {
    # Some baseline cuts used in all SRs and CRs
    "filters" : "$DATA{%s} $MC{%s}"%( " && ".join(data_flags), " && ".join(mc_flags)),
    "trigger" : "Trigger_3l",
    "lowmass"    : "minMllSFOS_Mini > 4 || minMllSFOS_Mini == -1",
}

# -------------------- To select 3l -------------------- #
AtLeastThreeLeptons = {
    "3l"         : "nLepSel >= 3",
    "AllTight"   : "allTight(LepSel_isTight[0], LepSel_isTight[1], LepSel_isTight[2])",
    "lepPt"      : "LepZ1_pt >= 25 && LepZ2_pt >= 10 && LepW_pt >= 25",
    "BRevent"    : "abs(LepSel_pdgId[0]) < 15 && abs(LepSel_pdgId[1]) < 15 && abs(LepSel_pdgId[2]) < 15 && nOSSF_3l >= 1",
    "m3l"        : "m3L >= 100",
}

ExactlyThreeLeptons = deepcopy(AtLeastThreeLeptons)
ExactlyThreeLeptons.update({
    "exactly3L"  : "nLepGood < 4"
})

# -------------------- To select 4l -------------------- #
ExactlyFourLeptons = {
    "4l"         : "nLepSel == 4",
    "AllTight"   : "allTight(LepSel_isTight[0], LepSel_isTight[1], LepSel_isTight[2], LepSel_isTight[3])",
    "lepPt"      : "LepZ1_pt >= 25 && LepZ2_pt >= 10 && LepW_pt >= 25 && LepSel_pt[3] > 10",
    "BRevent"    : "abs(LepSel_pdgId[0]) < 15 && abs(LepSel_pdgId[1]) < 15 && abs(LepSel_pdgId[2]) < 15 && nOSSF_3l >= 1",
    "m3l"        : "m3L >= 100",
}

flavor_splits = {
    "flav_eee"    : "(abs(LepZ1_pdgId)+abs(LepZ2_pdgId)+abs(LepW_pdgId)-33)/2 == 0; Disable=True",
    "flav_eem"    : "(abs(LepZ1_pdgId)+abs(LepZ2_pdgId)+abs(LepW_pdgId)-33)/2 == 1; Disable=True",
    "flav_mme"    : "(abs(LepZ1_pdgId)+abs(LepZ2_pdgId)+abs(LepW_pdgId)-33)/2 == 2; Disable=True",
    "flav_mmm"    : "(abs(LepZ1_pdgId)+abs(LepZ2_pdgId)+abs(LepW_pdgId)-33)/2 == 3; Disable=True",
    "chargeplus"  : "LepW_pdgId < 0 ; Disable=True",
    "chargeminus" : "LepW_pdgId > 0 ; Disable=True",
    "m3lmetblind" : "$DATA{m3Lmet <= 400} $MC{1} $FASTSIM{1}; Disable=True",
    "Cha_Tight"   : "LepGood_tightCharge[0]==2 && LepGood_tightCharge[1]==2 &&  LepGood_tightCharge[2]==2; Disable= True",
    "cha3_Tight"  : "LepGood_tightCharge[iW]==2; Disable= True"
}


    
baseline_wz = always
baseline_wz.update(baseline)

