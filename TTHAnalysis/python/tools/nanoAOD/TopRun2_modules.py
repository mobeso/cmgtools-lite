import os, sys, enum
import ROOT as r
from copy import deepcopy

class ch(enum.IntEnum):
    NoChan = 0
    ElMu   = 1
    Muon   = 2
    Elec   = 3
    ElMuFromTaus = 4
    MuonFromTaus = 5
    ElecFromTaus = 6
    ElMuMixedFromTaus = 7
    MuonMixedFromTaus = 8
    ElecMixedFromTaus = 9


class tags(enum.IntEnum):
    NoTag      = 0
    mc         = 1
    singlemuon = 2
    singleelec = 3
    doublemuon = 4
    doubleeg   = 5
    muoneg     = 6

emass = 0.0005109989461

# =========================================================================================================================
# ============================================================================================ TRIGGER
# =========================================================================================================================
def _fires(ev, path):
    if "/hasfiredtriggers_cc.so" not in r.gSystem.GetLibraries():
        r.gROOT.ProcessLine(".L %s/src/CMGTools/Production/src/hasfiredtriggers.cc+" % os.environ['CMSSW_BASE'])
    if not hasattr(ev, path): return False

    if ev.run == 1:  # is MC
        return getattr(ev, path)
    else :
        return getattr(r, 'fires_%s_%d'%(path, ev.year))( ev.run, getattr(ev, path) )

#### Old, pre 2021-01
#triggerGroups = dict(
    #Trigger_1e = {
        #2016 : lambda ev : _fires(ev, 'HLT_Ele27_WPTight_Gsf'),
        #2017 : lambda ev : _fires(ev, 'HLT_Ele35_WPTight_Gsf'),
        #2018 : lambda ev : _fires(ev, 'HLT_Ele32_WPTight_Gsf'),
    #},
    #Trigger_1m = {
        #2016 : lambda ev : (   _fires(ev, 'HLT_IsoMu24')
                            #or _fires(ev, 'HLT_IsoTkMu24')),
        #2017 : lambda ev :     _fires(ev, 'HLT_IsoMu27'),
        #2018 : lambda ev :     _fires(ev, 'HLT_IsoMu24'),
    #},
    #Trigger_2e = {
        #2016 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ'),
        #2017 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
        #2018 : lambda ev : _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL'),
    #},
    #Trigger_2m = {
        #2016 : lambda ev : ((   _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL')
                             #or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'))
                            #if (ev.datatag == tags.mc or ev.run <= 280385) else

                            #(  _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ')
                            #or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'))),
        #2017 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'),
        #2018 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    #},
    #Trigger_em = {
        #2016 : lambda ev : ((  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL')
                            #or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"))
                            #if (ev.datatag == tags.mc or ev.run <= 280385) else

                            #(  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            #or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"))),
        #2017 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            #or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
        #2018 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            #or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
    #},
#)

triggerGroups = dict(
    Trigger_1e = {
        2016 : lambda ev : _fires(ev, 'HLT_Ele27_WPTight_Gsf'),
        2017 : lambda ev : _fires(ev, 'HLT_Ele35_WPTight_Gsf'),
        2018 : lambda ev : _fires(ev, 'HLT_Ele32_WPTight_Gsf'),
    },
    Trigger_1m = {
        2016 : lambda ev : (   _fires(ev, 'HLT_IsoMu24')
                            or _fires(ev, 'HLT_IsoTkMu24')),
        2017 : lambda ev :     _fires(ev, 'HLT_IsoMu27'),
        2018 : lambda ev :     _fires(ev, 'HLT_IsoMu24'),
    },
    Trigger_2e = {
        2016 : lambda ev : (   _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, 'HLT_DoubleEle33_CaloIdL_MW')
                            or _fires(ev, 'HLT_DoubleEle33_CaloIdL_GsfTrkIdVL')),
        2017 : lambda ev : (   _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_DoubleEle33_CaloIdL_MW')),
        2018 : lambda ev : (   _fires(ev, 'HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_DoubleEle25_CaloIdL_MW')),
    },
    Trigger_2m = {
        2016 : lambda ev : ((   _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL')
                             or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL'))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else

                            (  _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ')
                            or _fires(ev, 'HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ'))),
        2017 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8'),
        2018 : lambda ev :     _fires(ev, 'HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8'),
    },
    Trigger_em = {
        2016 : lambda ev : ((  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL"))
                            if (ev.datatag == tags.mc or ev.run <= 280385) else

                            (  _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')
                            or _fires(ev, "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"))),
        2017 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
        2018 : lambda ev : (   _fires(ev, 'HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL')
                            or _fires(ev, 'HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ')),
    },
)

from CMGTools.TTHAnalysis.tools.evtTagger import EvtTagger
Trigger_1e = lambda : EvtTagger('Trigger_1e',  [ lambda ev : triggerGroups['Trigger_1e'][ev.year](ev) ])
Trigger_1m = lambda : EvtTagger('Trigger_1m',  [ lambda ev : triggerGroups['Trigger_1m'][ev.year](ev) ])
Trigger_2e = lambda : EvtTagger('Trigger_2e',  [ lambda ev : triggerGroups['Trigger_2e'][ev.year](ev) ])
Trigger_2m = lambda : EvtTagger('Trigger_2m',  [ lambda ev : triggerGroups['Trigger_2m'][ev.year](ev) ])
Trigger_em = lambda : EvtTagger('Trigger_em',  [ lambda ev : triggerGroups['Trigger_em'][ev.year](ev) ])

remove_overlap_booleans = [ lambda ev : (
                            (  (ev.channel == ch.ElMu and (ev.Trigger_em or ev.Trigger_1m or ev.Trigger_1e))
                            or (ev.channel == ch.Muon and (ev.Trigger_1m or ev.Trigger_2m))
                            or (ev.channel == ch.Elec and (ev.Trigger_1e or ev.Trigger_2e)) )
                            if ev.datatag == tags.mc else

                            (  (ev.channel == ch.ElMu and (not ev.Trigger_em) and ev.Trigger_1m)
                            or (ev.channel == ch.Muon and (not ev.Trigger_2m) and ev.Trigger_1m))
                            if ev.datatag == tags.singlemuon else

                            (   ev.channel == ch.ElMu and (not ev.Trigger_em) and (not ev.Trigger_1m) and ev.Trigger_1e)
                            or (ev.channel == ch.Elec and (not ev.Trigger_2e) and ev.Trigger_1e)
                            if (ev.datatag == tags.singleelec and not ev.year == 2018) else

                            (   ev.channel == ch.ElMu and (not ev.Trigger_em) and (not ev.Trigger_1m) and ev.Trigger_1e)
                            or (ev.channel == ch.Elec and (ev.Trigger_2e or ev.Trigger_1e))
                            if (ev.datatag == tags.singleelec and ev.year == 2018) else
                            
                            (   ev.channel == ch.Muon and ev.Trigger_2m)
                            if ev.datatag == tags.doublemuon else

                            (  ev.channel == ch.Elec and ev.Trigger_2e)
                            if ev.datatag == tags.doubleeg else

                            (  ev.channel == ch.ElMu and ev.Trigger_em)
                            if ev.datatag == tags.muoneg else

                            (False)
                        )]

remove_overlap = lambda : EvtTagger('pass_trigger', remove_overlap_booleans)

triggerSeq = [Trigger_1e, Trigger_1m, Trigger_2e, Trigger_2m, Trigger_em, remove_overlap]

# =========================================================================================================================
# ============================================================================================ OTHER GENERAL MODULES
# =========================================================================================================================



# =========================================================================================================================
# ============================================================================================ ANALYSIS MODULES & SETTINGS
# =========================================================================================================================

# %%%%%%%%%%%%%%%%%%%%%%%%%% tW full Run 2 inclusive & differential
#### LEPTON TREATMENTS ###
IDDict = {}
IDDict["muons"] = {
    "pt"       : 20,
    #"pt"       : 18, # Lo del stop
    "eta"      : 2.4,
    "isorelpf" : 0.15,
}

IDDict["elecs"] = {
    "pt"   : 20,
    #"pt"   : 18, # Lo del stop
    "eta0" : 1.4442,
    "eta1" : 1.566,
    "eta2" : 2.4,
    "dxy_b" : 0.05,
    "dz_b"  : 0.10,
    "dxy_e" : 0.10,
    "dz_e"  : 0.20,
    "etasc_be" : 1.479,
}

IDDict["jets"] = {
    "pt"      : 30,
    "pt2"     : 20,
    "ptmin"   : 15,
    "ptfwdnoise" : 60,
    "eta"     : 2.4,
    "etafwd"  : 5.0,
    "etafwdnoise0" : 2.7,
    "etafwdnoise1" : 3.0,
    "jetid_2016" : 0,  # > X
    #"jetid_2016" : 1,  # > X Lo del stop
    "jetid_2017" : 1,  # > X
    "jetid_2018" : 1,  # > X
}

#muonID = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      #and l.tightId == 1 )
muonID = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.corrected_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

elecID = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       #and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (l.eta <= IDDict["elecs"]["etasc_be"])   #### COMOL STOP
                       #else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )
                       #and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.deltaEtaSC - l.eta) <= IDDict["elecs"]["etasc_be"]) ### COMO IGUAL ES
                       #else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )


muonID_lepenUp = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedUp_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

# TODO: esto de aqui ponerlo bien
elecID_lepenUp = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )

muonID_lepenDn = lambda l : ( abs(l.eta) < IDDict["muons"]["eta"] and l.correctedDown_pt > IDDict["muons"]["pt"] and l.pfRelIso04_all < IDDict["muons"]["isorelpf"]
                      and l.tightId == 1 )

# TODO: esto de aqui ponerlo bien
elecID_lepenDn = lambda l : ( (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"]) )
                       and l.pt > IDDict["elecs"]["pt"] and l.cutBased >= 4 and l.lostHits <= 1
                       and ((abs(l.dxy) < IDDict["elecs"]["dxy_b"] and abs(l.dz) < IDDict["elecs"]["dz_b"]) if (abs(l.eta) <= IDDict["elecs"]["etasc_be"])     ### COMO CREIA QUE ERA
                       else (abs(l.dxy) < IDDict["elecs"]["dxy_e"] and abs(l.dz) < IDDict["elecs"]["dz_e"])) )



dresslepID         = lambda l : ( (abs(l.eta) < IDDict["muons"]["eta"] and l.pt > IDDict["muons"]["pt"]) if (abs(l.pdgId) == 13) else
                                  (abs(l.eta) < IDDict["elecs"]["eta2"] and (abs(l.eta) < IDDict["elecs"]["eta0"] or abs(l.eta) > IDDict["elecs"]["eta1"])
                                   and l.pt > IDDict["elecs"]["pt"]) if (abs(l.pdgId) == 11) else False )
dressjetID         = lambda j : ( abs(j.eta) < 2.4 and j.pt > IDDict["jets"]["pt"] )
dressloosejetID    = lambda j : ( abs(j.eta) < 2.4 and j.pt > IDDict["jets"]["pt2"] and j.pt < IDDict["jets"]["pt"] )
dressfwdjetID      = lambda j : ( abs(j.eta) >= 2.4 and abs(j.eta) < 5.0 and
                                  ( ((abs(j.eta) < 2.7 or abs(j.eta) >= 3.0) and j.pt > IDDict["jets"]["pt"]) or
                                    ((abs(j.eta) >= 2.7 or abs(j.eta) < 3.0) and j.pt > IDDict["jets"]["ptfwdnoise"]) ) )
dressfwdloosejetID = lambda j : ( abs(j.eta) >= 2.4 and abs(j.eta) < 5.0 and (abs(j.eta) < 2.7 or abs(j.eta) >= 3.0) and j.pt > IDDict["jets"]["pt2"] )



from PhysicsTools.NanoAODTools.postprocessing.modules.common.collectionMerger import collectionMerger
lepMerge = lambda : collectionMerger(input = ["Electron", "Muon"],
                                     output = "LepGood",
                                     selector = dict(Muon = muonID, Electron = elecID))

lepMerge_muenUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuUp",
                                            selector = dict(Muon = muonID_lepenUp, Electron = elecID))
lepMerge_muenDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodmuDown",
                                            selector = dict(Muon = muonID_lepenDn, Electron = elecID))

lepMerge_elenUp = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodelUp",
                                            selector = dict(Muon = muonID, Electron = elecID_lepenUp))
lepMerge_elenDn = lambda : collectionMerger(input = ["Electron", "Muon"],
                                            output = "LepGoodelDown",
                                            selector = dict(Muon = muonID, Electron = elecID_lepenDn))
# Lepton & trigger SF
from CMGTools.TTHAnalysis.tools.nanoAOD.lepScaleFactors_TopRun2 import lepScaleFactors_TopRun2
leptrigSFs = lambda : lepScaleFactors_TopRun2()


#### JET TREATMENTS ###

jecGroups = {'HF'                 : ['PileUpPtHF', 'RelativeJERHF', 'RelativePtHF'],
             'BBEC1_year'         : ['RelativeJEREC1', 'RelativePtEC1', 'RelativeStatEC'],
             'FlavorQCD'          : ['FlavorQCD'],
             'RelativeSample_year': ['RelativeSample'],
             'EC2'                : ['PileUpPtEC2'],
             'HF_year'            : ['RelativeStatHF'],
             'RelativeBal'        : ['RelativeBal'],
             'Absolute_year'      : ['AbsoluteStat', 'RelativeStatFSR', 'TimePtEta'],
             'BBEC1'              : ['PileUpPtBB', 'PileUpPtEC1', 'RelativePtBB'],
             'EC2_year'           : ['RelativeJEREC2', 'RelativePtEC2'],
             'Absolute'           : ['AbsoluteMPFBias', 'AbsoluteScale', 'Fragmentation', 'PileUpDataMC',
                                     'PileUpPtRef', 'RelativeFSR', 'SinglePionECAL', 'SinglePionHCAL'],
}

from CMGTools.TTHAnalysis.tools.nanoAOD.apply_json import apply_json
pathtojsons = "/nfs/fanae/user/vrbouza/Proyectos/produccciones_nanoAOD/2021_04_05_postprocesadoRERECOtWRun2/CMSSW_10_2_22/src/PhysicsTools/NanoAODTools/macros/lumijson/"

json2016 = "Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
json2017 = "Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON_v1.txt"
json2018 = "Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt"

apply_json_2016 = lambda : apply_json(pathtojsons + "/" + json2016)
apply_json_2017 = lambda : apply_json(pathtojsons + "/" + json2017)
apply_json_2018 = lambda : apply_json(pathtojsons + "/" + json2018)



from CMGTools.TTHAnalysis.tools.nanoAOD.btag_weighter               import btag_weighter
## b-tagging
# Old (pre-new correlations)
#btagEffpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/TopRun2/btagging/"
#btagSFpath  = os.environ['CMSSW_BASE'] + "/src/PhysicsTools/NanoAODTools/data/btagSF/"

#btagWeights_2016 = lambda : btag_weighter(btagSFpath + "DeepJet_2016LegacySF_V1.csv",  btagEffpath + "BtagMCSF.root", 'deepjet', year = 2016)
#btagWeights_2017 = lambda : btag_weighter(btagSFpath + "DeepFlavour_94XSF_V3_B_F.csv", btagEffpath + "BtagMCSF.root", 'deepjet', year = 2017)
#btagWeights_2018 = lambda : btag_weighter(btagSFpath + "DeepJet_102XSF_V1.csv",        btagEffpath + "BtagMCSF.root", 'deepjet', year = 2018)

# New
btagpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/TopRun2/btagging"
btagWeights_2016 = lambda : btag_weighter(btagpath + "/" + "DeepJet_2016LegacySF_V1_YearCorrelation-V1.csv",
#btagWeights_2016 = lambda : btag_weighter(btagpath + "/" + "DeepCSV_2016LegacySF_V1_YearCorrelation-V1.csv",
                                          btagpath + "/" + "BtagMCSF.root",
#                                          btagpath + "/" + "btagEffs_2022_01_29.root",
                                          'deepjet',
                                          #'deepcsv',
                                          jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                          splitCorrelations = True,
                                          year = 2016)
btagWeights_2017 = lambda : btag_weighter(btagpath + "/" + "DeepJet_DeepFlavour2017_mujets_YearCorrelation-V1.csv",
#btagWeights_2017 = lambda : btag_weighter(btagpath + "/" + "DeepCSV_102XSF_V1_YearCorrelation-V1.csv",
                                          btagpath + "/" + "BtagMCSF.root",
                                          #btagpath + "/" + "btagEffs_2022_01_29.root",
                                          'deepjet',
                                           #'deepcsv',
                                          jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                          splitCorrelations = True,
                                          year = 2017)
btagWeights_2018 = lambda : btag_weighter(btagpath + "/" + "DeepJet_102XSF_V1_YearCorrelation-V1.csv",
#btagWeights_2018 = lambda : btag_weighter(btagpath + "/" + "DeepCSV_94XSF_V4_B_F_YearCorrelation-V1.csv",
                                          btagpath + "/" + "BtagMCSF.root",
                                          #btagpath + "/" + "btagEffs_2022_01_29.root",
                                          'deepjet',
                                          #'deepcsv',
                                          jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                          splitCorrelations = True,
                                          year = 2018)


# Cleaning
#from CMGTools.TTHAnalysis.tools.combinedObjectTaggerForCleaningTopRun2     import CombinedObjectTaggerForCleaningTopRun2
#from CMGTools.TTHAnalysis.tools.nanoAOD.fastCombinedObjectRecleanerTopRun2 import fastCombinedObjectRecleanerTopRun2
#from CMGTools.TTHAnalysis.tools.nanoAOD.cleaningTopRun2 import cleaningTopRun2
from CMGTools.TTHAnalysis.tools.nanoAOD.pythonCleaningTopRun2 import pythonCleaningTopRun2

#cleaning_mc = lambda : cleaningTopRun2(label = "Recl",
                                       #jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                       #jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"], isMC = True,
                                       #jecvars   = ['jesTotal', 'jer'],
                                       #lepenvars = ["mu"],
                                       ##variations = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups]
#)

#cleaning_data = lambda : cleaningTopRun2(label = "Recl",
                                         #jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                         #jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"], isMC = False,
                                         #jecvars   = [],
                                         #lepenvars = [],
#)


cleaning_mc_mod2016 = lambda : pythonCleaningTopRun2(label  = "Recl",
                                             jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                             jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                             jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                             lepenvars = ["mu"],
                                             isMC      = True,
                                             #debug     = True,
                                             year_     = 2016,
#                                             algo      = "DeepCSV",
)
cleaning_mc_mod2017 = lambda : pythonCleaningTopRun2(label  = "Recl",
                                             jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                             jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                             jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                             lepenvars = ["mu"],
                                             isMC      = True,
                                             #debug     = True,
                                             year_     = 2017,
#                                             algo      = "DeepCSV",
)
cleaning_mc_mod2018 = lambda : pythonCleaningTopRun2(label  = "Recl",
                                             jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                             jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                             jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                             lepenvars = ["mu"],
                                             isMC      = True,
                                             year_     = 2018,
                                             #debug     = True,
#                                             algo      = "DeepCSV",
)

cleaning_data_mod2016 = lambda : pythonCleaningTopRun2(label = "Recl",
                                               jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                               jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                               jecvars   = [], lepenvars = [], isMC = False,
                                               year_     = 2016,
#                                               algo      = "DeepCSV",
)
cleaning_data_mod2017 = lambda : pythonCleaningTopRun2(label = "Recl",
                                               jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                               jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                               jecvars   = [], lepenvars = [], isMC = False,
                                               year_     = 2017,
#                                               algo      = "DeepCSV",
)
cleaning_data_mod2018 = lambda : pythonCleaningTopRun2(label = "Recl",
                                               jetPts = [IDDict["jets"]["pt"], IDDict["jets"]["pt2"]],
                                               jetPtNoisyFwd = IDDict["jets"]["ptfwdnoise"],
                                               jecvars   = [], lepenvars = [], isMC = False,
                                               year_     = 2018,
#                                               algo      = "DeepCSV",
)

#### Add year
from CMGTools.TTHAnalysis.tools.addYear import addYear
addYear_2016 = lambda : addYear(2016)
addYear_2017 = lambda : addYear(2017)
addYear_2018 = lambda : addYear(2018)  #### NOTE: this also adds the PrefireWeight as a branch for this year

#### FIX PORQUE SOY FATISIMU
cleaning_mc_2016   = [cleaning_mc_mod2016,   addYear_2016]
cleaning_mc_2017   = [cleaning_mc_mod2017,   addYear_2017]
cleaning_mc_2018   = [cleaning_mc_mod2018,   addYear_2018]
cleaning_data_2016 = [cleaning_data_mod2016, addYear_2016]
cleaning_data_2017 = [cleaning_data_mod2017, addYear_2017]
cleaning_data_2018 = [cleaning_data_mod2018, addYear_2018]



#### EVENT VARIABLES ###
from CMGTools.TTHAnalysis.tools.eventVars_tWRun2 import EventVars_tWRun2
eventVars_mc = lambda : EventVars_tWRun2('', 'Recl',
                                         jecvars = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)] + ["unclustEn"],
                                         #jecvars = ['jesTotal', 'jer'],
                                         lepvars = ['mu'])
eventVars_data = lambda : EventVars_tWRun2('', 'Recl', isMC = False,
                                           jecvars = [],
                                           lepvars = [])

from CMGTools.TTHAnalysis.tools.nanoAOD.altHEMcheck import altHEMcheck
HEMcheck = lambda : altHEMcheck('', 'Recl')

#### Add data tag
from CMGTools.TTHAnalysis.tools.addDataTag import addDataTag
addMuonEG     = lambda : addDataTag(tags.muoneg)
addDoubleMuon = lambda : addDataTag(tags.doublemuon)
addDoubleEG   = lambda : addDataTag(tags.doubleeg)
addSingleMuon = lambda : addDataTag(tags.singlemuon)
addSingleElec = lambda : addDataTag(tags.singleelec)
addMC         = lambda : addDataTag(tags.mc)
addMC_ttbar   = lambda : addDataTag(tags.mc, isTop = True)

from CMGTools.TTHAnalysis.tools.addJetPtCorr import addJetPtCorr
addJetPtCorrAll = lambda : addJetPtCorr()

addYearTag_2016_mc         = [addYear_2016, addMC        ]#, addJetPtCorrAll]
addYearTag_2016_mc_ttbar   = [addYear_2016, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2016_singlemuon = [addYear_2016, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2016_singleelec = [addYear_2016, addSingleElec]#, addJetPtCorrAll]
addYearTag_2016_doublemuon = [addYear_2016, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2016_doubleeg   = [addYear_2016, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2016_muoneg     = [addYear_2016, addMuonEG    ]#, addJetPtCorrAll]

addYearTag_2017_mc         = [addYear_2017, addMC        ]#, addJetPtCorrAll]
addYearTag_2017_mc_ttbar   = [addYear_2017, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2017_singlemuon = [addYear_2017, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2017_singleelec = [addYear_2017, addSingleElec]#, addJetPtCorrAll]
addYearTag_2017_doublemuon = [addYear_2017, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2017_doubleeg   = [addYear_2017, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2017_muoneg     = [addYear_2017, addMuonEG    ]#, addJetPtCorrAll]

addYearTag_2018_mc         = [addYear_2018, addMC        ]#, addJetPtCorrAll]
addYearTag_2018_mc_ttbar   = [addYear_2018, addMC_ttbar  ]#, addJetPtCorrAll]
addYearTag_2018_singlemuon = [addYear_2018, addSingleMuon]#, addJetPtCorrAll]
addYearTag_2018_singleelec = [addYear_2018, addSingleElec]#, addJetPtCorrAll]
addYearTag_2018_doublemuon = [addYear_2018, addDoubleMuon]#, addJetPtCorrAll]
addYearTag_2018_doubleeg   = [addYear_2018, addDoubleEG  ]#, addJetPtCorrAll]
addYearTag_2018_muoneg     = [addYear_2018, addMuonEG    ]#, addJetPtCorrAll]


#### Add Rochester corrections
from CMGTools.TTHAnalysis.tools.addRochester import addRochester
#from CMGTools.TTHAnalysis.tools.addRochesterValid import addRochesterValid
addRoch_mc = lambda : addRochester()
addRoch_data = lambda : addRochester(isMC = False)

from CMGTools.TTHAnalysis.tools.nanoAOD.selectParticleAndPartonInfo import selectParticleAndPartonInfo
theDressAndPartInfo = lambda : selectParticleAndPartonInfo(dresslepSel_         = dresslepID,
                                                           dressjetSel_         = dressjetID,
                                                           dressloosejetSel_    = dressloosejetID,
                                                           dressfwdjetSel_      = dressfwdjetID,
                                                           dressfwdloosejetSel_ = dressfwdloosejetID)

#lepMerge_roch_mc   = [lepMerge, lepMerge_muenUp, lepMerge_muenDn, lepMerge_elenUp, lepMerge_elenDn, addRoch_mc, theDressAndPartInfo] ### FIXME: este es el "bueno"
lepMerge_roch_mc   = [lepMerge, lepMerge_muenUp, lepMerge_muenDn, addRoch_mc, theDressAndPartInfo]
lepMerge_roch_data = [lepMerge, addRoch_data]


#### BDT
from CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2 import MVA_tWRun2
MVAProc_mc   = lambda : MVA_tWRun2(jecvars = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)])
MVAProc_data = lambda : MVA_tWRun2(isData = True)

mvas_mc   = [MVAProc_mc]
mvas_data = [MVAProc_data]



from CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_pruebas import MVA_tWRun2_pruebas
MVAProc_mc_pruebas   = lambda : MVA_tWRun2_pruebas(isData = True, jecvars = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)])
MVAProc_data_pruebas = lambda : MVA_tWRun2_pruebas(isData = True)


#from CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_new import MVA_tWRun2_new
# Standard import
import importlib

mvas_mc_pruebas = [lambda : getattr(importlib.import_module("CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_new"), "MVA_tWRun2_new_")()]

tmpstr = """mvas_mc_pruebas.append(lambda : getattr(importlib.import_module("CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_new"), "MVA_tWRun2_new_{v}{sv}")() )"""

for v in (['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)] + ["mu"] + ["unclustEn"]):
    for sv in ["Up", "Down"]:
        eval(tmpstr.format(v = v, sv = sv))
        #mvas_mc_pruebas.append(  getattr(importlib.import_module("CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_new"), "MVA_tWRun2_new_" + v + sv)() )
#print "aqui", mvas_mc_pruebas
mvas_data_pruebas = lambda : getattr(importlib.import_module("CMGTools.TTHAnalysis.tools.nanoAOD.MVA_tWRun2_new"), "MVA_tWRun2_new_")()



from CMGTools.TTHAnalysis.tools.nanoAOD.createTrainingMiniTree_tWRun2 import createTrainingMiniTree_tWRun2

createMVAMiniTree = lambda : createTrainingMiniTree_tWRun2()


from CMGTools.TTHAnalysis.tools.particleAndPartonVars_tWRun2 import particleAndPartonVars_tWRun2
from CMGTools.TTHAnalysis.tools.nanoAOD.jetMetGrouper_TopRun2 import jetMetCorrelate2016_TopRun2,jetMetCorrelate2017_TopRun2,jetMetCorrelate2018_TopRun2
theDressAndPartVars = lambda : particleAndPartonVars_tWRun2()

varstrigger_mc_2016 = [jetMetCorrelate2016_TopRun2, eventVars_mc, theDressAndPartVars] + triggerSeq
varstrigger_mc_2017 = [jetMetCorrelate2017_TopRun2, eventVars_mc, theDressAndPartVars] + triggerSeq
varstrigger_mc_2018 = [jetMetCorrelate2018_TopRun2, eventVars_mc, theDressAndPartVars] + triggerSeq
varstrigger_data    = [eventVars_data] + triggerSeq


from CMGTools.TTHAnalysis.tools.nanoAOD.TopPtWeight import TopPtWeight
addTopPtWeight = lambda : TopPtWeight()

from CMGTools.TTHAnalysis.tools.addSeparationIndex import addSeparationIndex

applicationProportion = 0.6

addSeparationIndex_nomva   = lambda : addSeparationIndex(isThisSampleForMVA = False, applicationProp = applicationProportion)
addSeparationIndex_mva     = lambda : addSeparationIndex(isThisSampleForMVA = True, applicationProp = applicationProportion)
addSeparationIndex_mva_ent = lambda : addSeparationIndex(isThisSampleForMVA = True, isEntire = True, applicationProp = applicationProportion)

#sfSeq_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_nomva]
#sfSeq_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_nomva]
#sfSeq_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_nomva]

from CMGTools.TTHAnalysis.tools.nanoAOD.jetPUid_weighter import jetPUid_weighter
jetpuidpath = os.environ['CMSSW_BASE'] + "/src/CMGTools/TTHAnalysis/data/TopRun2/jetPUid"
addjetPUidMod = lambda : jetPUid_weighter(jetpuidpath + "/" + "scalefactorsPUID_81Xtraining.root",
                                          jetpuidpath + "/" + "effcyPUID_81Xtraining.root",
                                          wp = "T",
                                          jecvars   = ['jesTotal', 'jer'] + ['jes%s'%v for v in jecGroups] + ["jer%i"%i for i in range(6)],
                                          #year = 2016, debug = True)
                                          year = 2016)

#sfSeq_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addjetPUidMod]   ### COSINA
sfSeq_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight]
sfSeq_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight]
sfSeq_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight]

sfSeq_mvatrain_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_mva]
sfSeq_mvatrain_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_mva]
sfSeq_mvatrain_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_mva]

sfSeq_mvatrain_ent_2016 = [leptrigSFs, btagWeights_2016, addTopPtWeight, addSeparationIndex_mva_ent]
sfSeq_mvatrain_ent_2017 = [leptrigSFs, btagWeights_2017, addTopPtWeight, addSeparationIndex_mva_ent]
sfSeq_mvatrain_ent_2018 = [leptrigSFs, btagWeights_2018, addTopPtWeight, addSeparationIndex_mva_ent]


##### HEM16/17 Issue
#from PhysicsTools.NanoAODTools.postprocessing.modules.jme.jetmetHelperRun2 import *
#HEMuncsMod = createJMECorrector(dataYear      = 2018,
#                                       jesUncert     = "Total",
#                                       metBranchName = "MET",
#                                       applyHEMfix   = True,
#                                       saveMETUncs = [],)
#
#hemunc_mc_2018 = [HEMuncsMod]


###### b-tagging efficiencies
from CMGTools.TTHAnalysis.tools.btageffVars_tWRun2 import btageffVars_tWRun2
btagEffFtree_2016 = lambda : btageffVars_tWRun2(wp_   = 1,
                                                algo_ = ['deepjet',
                                                         "deepcsv"],
                                                csv_  = [btagpath + "/DeepJet_2016LegacySF_V1_YearCorrelation-V1.csv",
                                                         btagpath + "/DeepCSV_2016LegacySF_V1_YearCorrelation-V1.csv"],
                                                year_ = 2016)

btagEffFtree_2017 = lambda : btageffVars_tWRun2(wp_   = 1,
                                                algo_ = ['deepjet',
                                                         "deepcsv"],
                                                csv_  = [btagpath + "/DeepJet_DeepFlavour2017_mujets_YearCorrelation-V1.csv",
                                                         btagpath + "/DeepCSV_94XSF_V4_B_F_YearCorrelation-V1.csv"],
                                                year_ = 2017)

btagEffFtree_2018 = lambda : btageffVars_tWRun2(wp_   = 1,
                                                algo_ = ['deepjet',
                                                         "deepcsv"],
                                                csv_  = [btagpath + "/DeepJet_102XSF_V1_YearCorrelation-V1.csv",
                                                         btagpath + "/DeepCSV_102XSF_V1_YearCorrelation-V1.csv"],
                                                year_ = 2018)


# %%%%%%%%%%%%%%%%%%%%%%%%%% WWbb
# TODO


# %%%%%%%%%%%%%%%%%%%%%%%%%% tW+/tW-
# TODO
