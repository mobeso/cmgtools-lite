'''
Modules used for the WZ-Run3 Analysis.
'''
import os
import ROOT 
# ---------------------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON MERGER+SKIM+LABELTAGGERS    -------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------------------- #
from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
from CMGTools.TTHAnalysis.tools.nanoAOD.skimNRecoLeps import SkimRecoLeps
from CMGTools.TTHAnalysis.tools.nanoAOD.DatasetTagger import datasetTagger
from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
from CMGTools.TTHAnalysis.tools.nanoAOD.applyPuWeights import puWeighter 

# --- Lepton minimum cuts 
# Muons 
min_mu_pt = 10
max_mu_eta = 2.4

# Electrons    
min_el_pt = 10
max_el_eta = 2.5
etaLeak = 1.56

# Common
relIso = 0.4
dxy = 0.05
dz = 0.1
sip3d = 8

# --- Minimum selection --- #
# + Minimum ISO and promptness
isoAndIPCuts  = lambda l : l.miniPFRelIso_all < relIso and abs(l.dxy) < dxy and abs(l.dz) < dz and l.sip3d < sip3d 


# + Muons
muonSelection = lambda l : ((abs(l.eta) < max_mu_eta) and (l.pt > min_mu_pt)
                            and isoAndIPCuts(l) 
                            and l.mediumId 
                            and (l.isGlobal or l.isTracker) 
                            and l.isPFcand)

# + Electrons
elecSelection = lambda l : (
    ( abs(l.eta) < max_el_eta) and (l.pt > min_el_pt)
    and (abs(l.eta+l.deltaEtaSC) < 1.4442 or abs(l.eta+l.deltaEtaSC) > 1.566)
    and isoAndIPCuts(l) and l.lostHits < 2
)
# + Electrons: postEE+ leak
elecSelection_EE = lambda l : (
    elecSelection(l) 
    and not( (l.eta+l.deltaEtaSC) > etaLeak and int(l.seediEtaOriX) < 45 and l.seediPhiOriY > 72)
)

lepMerge = collectionMerger(
    input = ["Electron", "Muon"], 
    output = "LepGood",
    selector = dict(Muon = muonSelection, Electron = elecSelection)
)

lepMerge_EE = collectionMerger(
    input = ["Electron", "Muon"], 
    output = "LepGood",
    selector = dict(Muon = muonSelection, Electron = elecSelection_EE)
)

# --- Electron Scale/Smearing corrections
from CMGTools.TTHAnalysis.tools.nanoAOD.applyElectronSS import applyElectronSS 
elecScaleRes2022_data = lambda: applyElectronSS(os.environ["CMSSW_BASE"] + "/src/CMGTools/TTHAnalysis/data/WZRun3/EGM/2022/", isData = True, file = "electronSS.json.gz")
elecScaleRes2022_mc = lambda: applyElectronSS(os.environ["CMSSW_BASE"] + "/src/CMGTools/TTHAnalysis/data/WZRun3/EGM/2022/", isData = False, file = "electronSS.json.gz")
elecScaleRes2022EE_data = lambda: applyElectronSS(os.environ["CMSSW_BASE"] + "/src/CMGTools/TTHAnalysis/data/WZRun3/EGM/2022EE/", isData = True, file = "electronSS.json.gz")
elecScaleRes2022EE_mc = lambda: applyElectronSS(os.environ["CMSSW_BASE"] + "/src/CMGTools/TTHAnalysis/data/WZRun3/EGM/2022EE/", isData = False, file = "electronSS.json.gz")


# --- Skimming and label tagger --- #
lepSkim = SkimRecoLeps() # Skim configuration: at least 2 leptons
tagger  = lambda : datasetTagger()

# --- Trigger sequence --- #
# Define different trigger strategies in this dictionary
# to target different topologies.
triggerGroups = dict(
    # Single lepton triggers
    triggers_se    = { 2022 : lambda ev: ev.HLT_Ele32_WPTight_Gsf},
    triggers_sm    = { 2022 : lambda ev: ev.HLT_IsoMu24},
    
    # Double lepton triggers
    triggers_ee    = { 2022 : lambda ev: ev.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL},
    triggers_mm    = { 2022 : lambda ev: ev.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8},
    triggers_em    = { 2022 : lambda ev: ev.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ \
                                         or ev.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL},
    # Tri-lepton triggers
    triggers_mmm = { 2022 : lambda ev: ev.HLT_TripleMu_12_10_5 or ev.HLT_TripleMu_10_5_5_DZ},
    triggers_eee = { 2022 : lambda ev: 0 }, # Only one is prescaled in some of the data
    triggers_mme = { 2022: lambda ev : ev.HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ},
    triggers_mee = { 2022: lambda ev : ev.HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ},
    
    # MET triggers
    triggers_met = { 2022 : lambda ev: ev.HLT_PFMETNoMu120_PFMHTNoMu120_IDTight or ev.HLT_PFMETNoMu110_PFMHTNoMu110_IDTight},

    # Fake rate triggers
    triggers_fr = { 2022 : lambda ev: ev.HLT_Ele8_CaloIdM_TrackIdM_PFJet30 \
                                or ev.HLT_Ele17_CaloIdM_TrackIdM_PFJet30 \
                                or ev.HLT_Ele23_CaloIdM_TrackIdM_PFJet30 \
                                or ev.HLT_Mu3_PFJet40 \
                                or ev.HLT_Mu8 \
                                or ev.HLT_Mu17 \
                                or ev.HLT_Mu20 \
                                or ev.HLT_Mu27},
    # Combinations
    triggers_2lss = { 2022 : lambda ev: ev.Trigger_se or ev.Trigger_sm or ev.Trigger_mm or ev.Trigger_ee or ev.Trigger_em },
    triggers_3l   = { 2022 : lambda ev: ev.Trigger_2lss or ev.Trigger_eee or ev.Trigger_mee or ev.Trigger_mme or ev.Trigger_mmm},
    triggers_jme  = { 2022 : lambda ev: ev.Trigger_jetmet or ev.Trigger_met or ev.Trigger_jetht }
)

# Prompt triggers
Trigger_sm     = lambda : EvtTagger('Trigger_sm',   [lambda ev : triggerGroups['triggers_sm'][2022](ev)])
Trigger_se     = lambda : EvtTagger('Trigger_se',   [lambda ev : triggerGroups['triggers_se'][2022](ev)])
Trigger_mm     = lambda : EvtTagger('Trigger_mm',   [lambda ev : triggerGroups['triggers_mm'][2022](ev)])
Trigger_ee     = lambda : EvtTagger('Trigger_ee',   [lambda ev : triggerGroups['triggers_ee'][2022](ev)])
Trigger_em     = lambda : EvtTagger('Trigger_em',   [lambda ev : triggerGroups['triggers_em'][2022](ev)])
Trigger_eee    = lambda : EvtTagger('Trigger_eee',  [lambda ev : triggerGroups['triggers_eee'][2022](ev)])
Trigger_mee    = lambda : EvtTagger('Trigger_mee',  [lambda ev : triggerGroups['triggers_mee'][2022](ev)])
Trigger_mme    = lambda : EvtTagger('Trigger_mme',  [lambda ev : triggerGroups['triggers_mme'][2022](ev)])
Trigger_mmm    = lambda : EvtTagger('Trigger_mmm',  [lambda ev : triggerGroups['triggers_mmm'][2022](ev)])
Trigger_2lss   = lambda : EvtTagger('Trigger_2lss', [lambda ev : triggerGroups['triggers_2lss'][2022](ev)])
Trigger_3l     = lambda : EvtTagger('Trigger_3l',   [lambda ev : triggerGroups['triggers_3l'][2022](ev)])
Trigger_met    = lambda : EvtTagger('Trigger_met',  [lambda ev : triggerGroups['triggers_met'][2022](ev)])

triggerSequence = [Trigger_sm, Trigger_se, Trigger_mm, Trigger_ee, Trigger_em, Trigger_eee, Trigger_mee, Trigger_mme, Trigger_mmm, Trigger_2lss, Trigger_3l, Trigger_met]

# --- PU weights --- #
from CMGTools.TTHAnalysis.tools.nanoAOD.puWeightProducer_run3 import puAutoWeight_2022PostEE

lepCollector         = [lepMerge, elecScaleRes2022_mc, lepSkim]  + [tagger, puAutoWeight_2022PostEE] + triggerSequence
lepCollector_data    = [lepMerge, elecScaleRes2022_data, lepSkim]  + [tagger] + triggerSequence
lepCollector_EE      = [lepMerge_EE, elecScaleRes2022EE_mc, lepSkim] + [tagger, puAutoWeight_2022PostEE] + triggerSequence
lepCollector_EE_data = [lepMerge_EE, elecScaleRes2022EE_data, lepSkim] + [tagger] + triggerSequence

# --------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- JET CORRECTIONS ------------------------------------------------------ # 
# --------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.jetMetGrouper_wzRun3 import jetMetCorrelate2022, groups

# To use nanoAODtools implementation
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

# To be used when json files are available for JER/JEC corrections
from CMGTools.TTHAnalysis.tools.nanoAOD.calculateJECS import JetEnergyCorrector
from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import createJMECorrector

addJECs_2022_mc = lambda : JetEnergyCorrector(
    year = 2022, era = "CD", jec = "Winter22Run3", isMC = True,
    algo = "AK4PFPuppi", metbranchname = "PuppiMET", rhoBranchName = "Rho_fixedGridRhoFastjetAll",
    hjetvetomap = "jetvetomap",
    unc = "Total", saveMETUncs = ["T1", "T1Smear"], 
    splitJers = False, applyVetoMaps = True 
)

# In reality this only runs the jet vetos (for data)
addJECs_2022_data = lambda : JetEnergyCorrector(
    year = 2022, era = "CD", jec = "Winter22Run3", isMC = False,
    algo = "AK4PFPuppi", metbranchname = "PuppiMET", rhoBranchName = "Rho_fixedGridRhoFastjetAll",
    hjetvetomap = "jetvetomap",
    unc = "Total", saveMETUncs = ["T1", "T1Smear"], 
    splitJers = False, applyVetoMaps = True
)

addJECs_2022EE_mc = lambda : JetEnergyCorrector(
    year = 2022, era = "E", jec = "Summer22EEPrompt22", isMC = True,
    algo = "AK4PFPuppi", metbranchname = "PuppiMET", rhoBranchName = "Rho_fixedGridRhoFastjetAll",
    hjetvetomap = "jetvetomap",
    unc = "Total", saveMETUncs = ["T1", "T1Smear"], 
    splitJers = False, applyVetoMaps = True 
)

# In reality this only runs the jet vetos (for data)
addJECs_2022EE_data = lambda : JetEnergyCorrector(
    year = 2022, era = "E", jec = "Summer22EEPrompt22", isMC = False,
    algo = "AK4PFPuppi", metbranchname = "PuppiMET", rhoBranchName = "Rho_fixedGridRhoFastjetAll",
    hjetvetomap = "jetvetomap",
    unc = "Total", saveMETUncs = ["T1", "T1Smear"],
    splitJers = False, applyVetoMaps = True 
)

# --- 2022: Add JECs (+ correlate in case of MC) --- #
jmeCorrections_mc   = [addJECs_2022_mc, jetMetCorrelate2022]
jmeCorrections_data = [addJECs_2022_data]


# --- 2022EE: Add JECs (+ correlate in case of MC) --- #
jmeCorrections_mc_EE   = [addJECs_2022EE_mc, jetMetCorrelate2022]
jmeCorrections_data_EE   = [addJECs_2022EE_data]
#jmeCorrections_data_EE_eraF = [addJECs_2022EE_data_eraF]
#jmeCorrections_data_EE_eraG = [addJECs_2022EE_data_eraG]

# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON MVA ----------------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------------------- #
# --- lepton MVA identification --- #
weightspath_2022   = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/")
weightspath_2022EE = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/")

import CMGTools.TTHAnalysis.tools.nanoAOD.mvaTTH_vars_run3 as mvatth_cfg
from CMGTools.TTHAnalysis.tools.nanoAOD.lepMVAWZ_run3 import lepMVAWZ_run3

lepmvas_2022 = [
    lambda : lepMVAWZ_run3(
        weightspath_2022, 
        elxmlpath = "EGM/Electron-mvaTTH.2022EE.weights_mvaISO.xml", 
        muxmlpath = "MUO/Muon-mvaTTH.2022EE.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df_wIso("2022")}
    ),
]

lepmvas_2022EE = [
    lambda : lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "EGM/Electron-mvaTTH.2022EE.weights_mvaISO.xml", 
        muxmlpath = "MUO/Muon-mvaTTH.2022EE.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022EE"), "electrons" : mvatth_cfg.electron_df_wIso("2022EE")}
    ),
]

"""
lepmvas_2022 = [
    lambda : lepMVAWZ_run3(
        weightspath_2022, 
        elxmlpath = "el_ttw_df_useIso_2022_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022_BDTG.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df_wIso("2022")}
    ),
    lambda : lepMVAWZ_run3(
        weightspath_2022, 
        elxmlpath = "el_ttw_df_useNoIso_2022_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022_BDTG.weights.xml", 
        suffix = "_run3_withDF_withNoISO",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df_wNoIso("2022")}
    ),
    lambda : lepMVAWZ_run3(
        weightspath_2022, 
        elxmlpath = "el_ttw_df_2022_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022_BDTG.weights.xml", 
        suffix = "_run3_noMVA",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df("2022")}
    ),
]

lepmvas_2022EE = [
    lambda : lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "el_ttw_df_useIso_2022EE_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022EE_BDTG.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022EE"), "electrons" : mvatth_cfg.electron_df_wIso("2022EE")}
    ),
    lambda : lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "el_ttw_df_useNoIso_2022EE_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022EE_BDTG.weights.xml", 
        suffix = "_run3_withDF_withNoISO",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022EE"), "electrons" : mvatth_cfg.electron_df_wNoIso("2022EE")}
    ),
    lambda : lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "el_ttw_df_2022EE_BDTG.weights.xml", 
        muxmlpath = "mu_ttw_df_2022EE_BDTG.weights.xml", 
        suffix = "_run3_noMVA",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022EE"), "electrons" : mvatth_cfg.electron_df("2022EE")}
    ),
]
"""


# --------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON RECLEANER ----------------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------------------------- #

from CMGTools.TTHAnalysis.tools.nanoAOD.leptonJetRecleanerWZSM import LeptonJetRecleanerWZSM

## Loose selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _loose_lepton

## Fakeable selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _fO_lepton

## Tight selections
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_muon
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_electron
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import _tight_lepton

from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import conept

# --- b tagging working points from 2022EE
btag_wps = {
    "2022" : {
        "btagDeepFlavB" : {
            "L" : 0.0583,
            "M" : 0.3086,
            "T" : 0.7183
        },
        "btagRobustParTAK4B" : {
            "L" : 0.0849,
            "M" : 0.4319,
            "T" : 0.8482
        },
        "btagPNetB" : {
            "L" : 0.047,
            "M" : 0.245,
            "T" : 0.6734
        }
    },
    "2022EE" : {
        "btagDeepFlavB" : {
            "L" : 0.0614,
            "M" : 0.3196,
            "T" : 0.73
        },
        "btagRobustParTAK4B" : {
            "L" : 0.0897,
            "M" : 0.451,
            "T" : 0.8604
        },
        "btagPNetB" : {
            "L" : 0.0499,
            "M" : 0.2605,
            "T" : 0.6915
        }
    }
}

looseDeepFlavB = btag_wps["2022EE"]["btagDeepFlavB"]["L"]
mediumDeepFlavB = btag_wps["2022EE"]["btagDeepFlavB"]["M"]

looselep = lambda lep          : _loose_lepton(lep, looseDeepFlavB, mediumDeepFlavB)
cleanlep = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
folep    = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
tightlep = lambda lep, jetlist : _tight_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)


# --- Groups of systematics
leptongroups = []#["elScaleUp", "muScaleUp", "elScaleDown", "muScaleDown"]
jecgroups = [ "jes%s%s"%(jecgroup, sign) for jecgroup in groups for sign in ["Up", "Down"] ] 

recleaner_2022 = lambda : LeptonJetRecleanerWZSM(
    "Mini",
    # Lepton selectors
    looseLeptonSel    = looselep, # Loose selection 
    cleaningLeptonSel = cleanlep, # Clean on FO
    FOLeptonSel       = folep,    # FO selection
    tightLeptonSel    = tightlep, # Tight selection
    coneptdef = lambda lep: conept(lep),
    # Lepton jet cleaner functions
    jetPt = 30,
    bJetPt = 25,
    cleanJet  = lambda lep, jet, dr : dr < 0.4,
    selectJet = lambda jet: abs(jet.eta) < 4.7 and (jet.jetId & 2), 
    # For taus (used in EWKino)
    cleanTau  = lambda lep, tau, dr: True, 
    looseTau  = lambda tau: True, # Used in cleaning
    tightTau  = lambda tau: True, # On top of loose
    cleanJetsWithTaus = False,
    cleanTausWithLoose = False,
    # For systematics
    systsJEC = jecgroups,
    systsLepScale = leptongroups,
    # These are used for EWKino as well
    doVetoZ   = False,
    doVetoLMf = False,
    doVetoLMt = True,
    # ------------------------------------- #
    year  = "2022EE",
    btag_wps = btag_wps,
    bAlgo = "btagDeepFlavB"
)

leptonJetRecleaning = [recleaner_2022]

# ------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------- BTAGGING EFFICIENCIES --------------------------------------------------- # 
# ------------------------------------------------------------------------------------------------------------------------------ #
from CMGTools.TTHAnalysis.tools.nanoAOD.btagEffCount_wzRun3 import bTagEffCount
btagEffDeepjet_2022EE                   = [lambda : bTagEffCount( tagger = "btagDeepFlavB", year = "2022EE" )]
btagEffrobustParticleTransformer_2022EE = [lambda : bTagEffCount( tagger = "btagDeepFlavB", year = "2022EE" )]
btagEffrobustParticleNet_2022EE         = [lambda : bTagEffCount( tagger = "btagPNetB",     year = "2022EE" )]

# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON BUILDER    ----------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.leptonBuilderWZSM import leptonBuilderWZSM
leptonBuilderWZSM_2022 = lambda : leptonBuilderWZSM(
    "Mini", 
    metbranch="PuppiMET",
    systsJEC  = jecgroups,
    lepScaleSysts = leptongroups 
)
leptonBuilder = [leptonBuilderWZSM_2022]

# ------------------------------------------------------------------------------------------------------------------------------ #
# ---------------------------------------------------- SCALE FACTORS ----------------------------------------------------------- # 
# ------------------------------------------------------------------------------------------------------------------------------ #
# Lepton Scale factors
from CMGTools.TTHAnalysis.tools.nanoAOD.lepScaleFactors_wzRun3 import lepScaleFactors_wzrun3
lepscalefactors_2022EE = lambda: lepScaleFactors_wzrun3( "2022EE", keepOutput = 2, summary = False ) 

# bTag scale factors
from CMGTools.TTHAnalysis.tools.nanoAOD.btag_weighterRun3 import btag_weighterRun3
btagpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/WZRun3/btagging"
btagWeights_2022EE = lambda : btag_weighterRun3(btagpath + "/" + "btagging.json.gz",
                                            btagpath + "/btagEff_DeepJet_2022EE.root",
                                            'deepJet',
                                            branchJet = "iJ",
                                            labelJet = "Mini",
                                            jecvars   = [ "jes%s"%(jecgroup) for jecgroup in groups ],
                                            lepenvars = [],
                                            splitCorrelations = True,
                                            year = "2022EE")

scalefactors_2022EE = [lepscalefactors_2022EE]#, btagWeights_2022EE]


#from CMGTools.TTHAnalysis.tools.nanoAOD.mvasergio import LepMVAFriend 
#mvasergio = [lambda : LepMVAFriend(18, separateCollections = 1)]


# -------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- MODULES FOR FR ------------------------------------------------------ # 
# -------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagDeepFlav
from CMGTools.TTHAnalysis.tools.nanoAOD.ttHLepQCDFakeRateAnalyzer import ttHLepQCDFakeRateAnalyzer
from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import deltaR


from CMGTools.TTHAnalysis.tools.nanoAOD.nBJetCounter import nBJetCounter
centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 4.7 and (j.jetId & 2)
nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

lepFR = lambda : ttHLepQCDFakeRateAnalyzer(jetSel = centralJetSel,
                                  pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
                                  maxLeptons = 1, 
                                  requirePair = True)

lepCollector_FR = [m for m in lepCollector if m != lepSkim]
lepCollector_data_FR = [m for m in lepCollector_data if m != lepSkim]

lepCollector_EE_FR = [m for m in lepCollector_EE if m != lepSkim]
lepCollector_EE_data_FR = [m for m in lepCollector_EE_data if m != lepSkim]

frUtils = [ lepJetBTagDeepFlav, lepFR, nBJetDeepFlav25NoRecl ]

# ---------------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- LEPTON MC MATCHER    -------------------------------------------------- # 
# ---------------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.leptonMatcher import leptonMatcher
from CMGTools.TTHAnalysis.tools.nanoAOD.lepgenVarsWZSM import lepgenVarsWZSM
from CMGTools.TTHAnalysis.tools.nanoAOD.lepgenVarsWZSM_nondressed_withtaus import lepgenVarsWZSM_nondressed_withtaus

leptonMCMatcher =  lambda: leptonMatcher("Mini")
leptonMCBuilder = lambda : lepgenVarsWZSM("Mini")
leptonGENBuilder = [leptonMCMatcher, leptonMCBuilder]
lepGENBuilder_withtaus = lambda : lepgenVarsWZSM_nondressed_withtaus("Mini")

# ---- These are used for fiducial analysis
lepMerge_fiducial = collectionMerger(
    input = ["Electron", "Muon"], 
    output = "LepGood",
    selector = dict(Muon = lambda l: 1, Electron = lambda l: 1)
)

lepCollector_fiducial = [lepGENBuilder_withtaus]


# --------------------------------------------------------------------------------------------------------------------- #
# ---------------------------------------------------- MODULES FOR TNP SFS -------------------------------------------- # 
# --------------------------------------------------------------------------------------------------------------------- #
from CMGTools.TTHAnalysis.tools.nanoAOD.addTnpTree import Electron_2022, Muon_2022
from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagAdder

# Merge lepton collections without applying selections
remove_ecalDeadZones = lambda l: not( (l.eta+l.deltaEtaSC) > etaLeak and int(l.seediEtaOriX) < 45 and l.seediPhiOriY > 72) and (abs(l.eta + l.deltaEtaSC) < 1.4442 or abs(l.eta + l.deltaEtaSC) > 1.566)

lepMerge_forTnP = collectionMerger(
    input = ["Electron", "Muon"], 
    output = "LepGood",
    selector = dict(Muon = lambda l: 1, Electron = remove_ecalDeadZones )
)

addBtag = lepJetBTagAdder("btagDeepFlavB", "jetBTagDeepFlav")

leptonSFs_muon_2022EE     = [lepMerge_forTnP, puAutoWeight_2022PostEE, addBtag, lepmvas_2022EE[0], Muon_2022] 
leptonSFs_electron_2022EE = [lepMerge_forTnP, puAutoWeight_2022PostEE, addBtag, lepmvas_2022EE[0], Electron_2022] 
leptonSFs_muon_2022EE_data  = [lepMerge_forTnP, addBtag, lepmvas_2022EE[0], Muon_2022] 
leptonSFs_electron_2022EE_data = [lepMerge_forTnP, addBtag, lepmvas_2022EE[0], Electron_2022]
