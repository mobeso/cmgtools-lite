from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import numpy as np
import ROOT
#import numpy as np
import array as ar

class MVAvar:
    def __init__(self, name):
        self.name = name
        self.var = ar.array('f', [0.])
    
    def set(self, val):
        self.var[0] = val

class lepMVAWZ_run3(Module):
    def __init__(self, inputpath, modelname = "BDTGttw_vetoLeak", isMC = True):
        
        self.branches = [
            ("LepGood_mvaTTH_run3", "F", 20, "nLepGood"),
            ("LepGood_miniRelIsoNeutral", "F", 20, "nLepGood"),
            ("LepGood_miniRelIsoCharged", "F", 20, "nLepGood"),
            ("LepGood_jetNDauChargedMVASel", "F", 20, "nLepGood"),
            ("LepGood_jetPtRatio", "F", 20, "nLepGood"),
            ("LepGood_jetDF", "F", 20, "nLepGood"),
            ("LepGood_absLogDxy", "F", 20, "nLepGood"),
            ("LepGood_absLogDz", "F", 20, "nLepGood"), 
        ]
        
        self.inputpath = inputpath
        self.modelname = modelname
        self.isMC = isMC       
        
        self.inputVars = {
            "electrons" : {
                "specs" : {
#                    "event" : MVAvar("event"),
#                    "mvaTTH" : MVAvar("Electron_mvaTTH"),
#                    "miniPFRelIso_all" : MVAvar("Electron_miniPFRelIso_all"),
#                    "mvaNoIso_Fall17V2_WPL" : MVAvar("Electron_mvaNoIso_Fall17V2_WPL"), 
#                    "lostHits" : MVAvar("Electron_lostHits"),
#                    "genPartFlav" : MVAvar("Electron_genPartFlav"),
#                    "dxy" : MVAvar("Electron_dxy"),
#                    "dz" : MVAvar("Electron_dz")},
                },
                "vars" : {
                    "LepGood_pt" : MVAvar("Electron_LepGood_pt"),
                    "LepGood_eta" : MVAvar("Electron_LepGood_eta"),
                    "LepGood_miniRelIsoCharged" : MVAvar("Electron_LepGood_miniRelIsoCharged"),
                    "LepGood_miniRelIsoNeutral" : MVAvar("Electron_LepGood_miniRelIsoNeutral"),
                    "LepGood_jetNDauChargedMVASel" : MVAvar("Electron_LepGood_jetNDauChargedMVASel"), 
                    "LepGood_jetPtRelv2" : MVAvar("Electron_LepGood_jetPtRelv2"), 
                    "LepGood_jetPtRatio" : MVAvar("Electron_LepGood_jetPtRatio"), 
                    "LepGood_jetDF" : MVAvar("Electron_LepGood_jetDF"),
                    "LepGood_sip3d" : MVAvar("Electron_LepGood_sip3d"), 
                    "LepGood_dxy" : MVAvar("Electron_LepGood_dxy"), 
                    "LepGood_dz" : MVAvar("Electron_LepGood_dz"), 
                    "LepGood_mvaFall17V2noIso" : MVAvar("Electron_LepGood_mvaFall17V2noIso")}
            },
            "muons" : {
                "specs" : {
#                    "event" : MVAvar("event"),
#                    "mvaTTH" : MVAvar("Muon_mvaTTH"),
#                    "miniPFRelIso_all" : MVAvar("Muon_miniPFRelIso_all"),
#                    "looseId" : MVAvar("Muon_looseId"),
#                    "genPartFlav" : MVAvar("Muon_genPartFlav"),
#                    "isGlobal" : MVAvar("Muon_isGlobal"),
#                    "isTracker" : MVAvar("Muon_isTracker"),
#                    "isPFcand" : MVAvar("Muon_isPFcand"),
#                    "mediumId" : MVAvar("Muon_mediumId"),
#                    "looseId_2" : MVAvar("Muon_looseId"),
#                    "dxy" : MVAvar("Muon_dxy"),
#                    "dz" : MVAvar("Muon_dz")},
                },
                "vars" : {
                    "LepGood_pt" : MVAvar("Muon_LepGood_pt"),
                    "LepGood_eta" : MVAvar("Muon_LepGood_eta"),
                    "LepGood_miniRelIsoCharged" : MVAvar("Muon_LepGood_miniRelIsoCharged"), 
                    "LepGood_miniRelIsoNeutral" : MVAvar("Muon_LepGood_miniRelIsoNeutral"),
                    "LepGood_jetNDauChargedMVASel" : MVAvar("Muon_LepGood_jetNDauChargedMVASel"), 
                    "LepGood_jetPtRelv2" : MVAvar("Muon_LepGood_jetPtRelv2"), 
                    "LepGood_jetPtRatio" : MVAvar("Muon_LepGood_jetPtRatio"), 
                    "LepGood_jetDF" : MVAvar("Muon_LepGood_jetDF"),
                    "LepGood_sip3d" : MVAvar("Muon_LepGood_sip3d"), 
                    "LepGood_dxy" : MVAvar("Muon_LepGood_dxy"), 
                    "LepGood_dz" : MVAvar("Muon_LepGood_dz"), 
                    "LepGood_segmentComp" : MVAvar("Muon_LepGood_segmentComp")}
            }
        }
        self.mva_electrons = self.open_model(inputpath + "el_ttw_vetoLeak_BDTG.weights.xml", modelname, "electrons")
        self.mva_muons     = self.open_model(inputpath + "mu_ttw_vetoLeak_BDTG.weights.xml", modelname, "muons")
        return

    def open_model(self, modelpath, modelname, whichones):
        """ Code extracted from MVATool.py """
        self.name = modelname
        print("> Loading %s from %s" % (modelname, modelpath))
        
        # Create the reader
        reader = ROOT.TMVA.Reader()
        self.vars  = [var for varkey, var in self.inputVars[whichones]["vars"].items()]
#        self.specs = [spec for speckey, spec in self.inputVars[whichones]["specs"].items()]
        
        print(">> Initialising variables")
#        for s in self.specs:
#            print("  + Adding spectator: ", s.name) 
#            reader.AddSpectator(s.name, s.var)
            
        for v in self.vars:
            print("  + Adding variable: ", v.name) 
            reader.AddVariable(v.name, v.var)
        
        # Book MVA
        print(">> Booking MVA")
        reader.BookMVA(modelname, modelpath)
        return reader
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
        return

    def analyze(self, event):
        """ All the magic happens here """
        ret = {
            "LepGood_mvaTTH_run3" : [],
            "LepGood_miniRelIsoNeutral" : [],
            "LepGood_miniRelIsoCharged" : [],
            "LepGood_jetNDauChargedMVASel" : [],
            "LepGood_jetPtRatio" : [],
            "LepGood_jetDF" : [],
            "LepGood_absLogDxy" : [],
            "LepGood_absLogDz" : []
        }
        
        jets = Collection(event, "Jet", "nJet")

        for ilep, lep in enumerate(Collection(event, "LepGood","nLepGood")):
            if abs(lep.pdgId) == 11: # Electrons
#                # -- Spectators
#                self.inputVars["electrons"]["specs"]["event"].set(event.event)
#                self.inputVars["electrons"]["specs"]["mvaTTH"].set(lep.mvaTTH)
#                self.inputVars["electrons"]["specs"]["miniPFRelIso_all"].set(lep.miniPFRelIso_all)
#                self.inputVars["electrons"]["specs"]["mvaNoIso_Fall17V2_WPL"].set(lep.mvaFall17V2noIso_WPL) # 2018
##                self.inputVars["electrons"]["specs"]["mvaNoIso_Fall17V2_WPL"].set(lep.mvaNoIso_Fall17V2_WPL)
#                self.inputVars["electrons"]["specs"]["lostHits"].set(lep.lostHits)
#                
#                if self.isMC:
#                    self.inputVars["electrons"]["specs"]["genPartFlav"].set(lep.genPartFlav)
#                else:
#                    self.inputVars["electrons"]["specs"]["genPartFlav"].set(-1)
#             
#                self.inputVars["electrons"]["specs"]["dxy"].set(lep.dxy)
#                self.inputVars["electrons"]["specs"]["dz"].set(lep.dz)

                
                # -- Training variables
                self.inputVars["electrons"]["vars"]["LepGood_pt"].set(lep.pt)
                self.inputVars["electrons"]["vars"]["LepGood_eta"].set(lep.eta)
                self.inputVars["electrons"]["vars"]["LepGood_miniRelIsoNeutral"].set(lep.miniPFRelIso_all - lep.miniPFRelIso_chg)
                self.inputVars["electrons"]["vars"]["LepGood_miniRelIsoCharged"].set(lep.miniPFRelIso_chg)
                self.inputVars["electrons"]["vars"]["LepGood_jetNDauChargedMVASel"].set(lep.jetNDauCharged)
                self.inputVars["electrons"]["vars"]["LepGood_jetPtRelv2"].set(lep.jetPtRelv2)
                self.inputVars["electrons"]["vars"]["LepGood_jetPtRatio"].set(min(1. / (1. + lep.jetRelIso), 1.5) )
                self.inputVars["electrons"]["vars"]["LepGood_jetDF"].set(jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0)
                self.inputVars["electrons"]["vars"]["LepGood_sip3d"].set(lep.sip3d)
                self.inputVars["electrons"]["vars"]["LepGood_dxy"].set(np.log(abs(lep.dxy)))
                self.inputVars["electrons"]["vars"]["LepGood_dz"].set(np.log(abs(lep.dz)))
                self.inputVars["electrons"]["vars"]["LepGood_mvaFall17V2noIso"].set(lep.mvaNoIso_Fall17V2)
                 
                 # Now that all variables have been updated in memory, evaluate the MVA
                
                mva = self.mva_electrons.EvaluateMVA(self.name)
                setattr(lep, "mvaTTH_run3", mva)
                ret["LepGood_mvaTTH_run3"].append(mva)
            elif abs(lep.pdgId) == 13: # Muons
                # -- Spectators
#                self.inputVars["muons"]["specs"]["event"].set(event.event)
#                self.inputVars["muons"]["specs"]["mvaTTH"].set(lep.mvaTTH)
#                self.inputVars["muons"]["specs"]["miniPFRelIso_all"].set(lep.miniPFRelIso_all)
#                self.inputVars["muons"]["specs"]["looseId"].set(lep.looseId)
#                
#                if self.isMC:
#                    self.inputVars["muons"]["specs"]["genPartFlav"].set(lep.genPartFlav)
#                else:
#                    self.inputVars["muons"]["specs"]["genPartFlav"].set(-1)
#             
#                self.inputVars["muons"]["specs"]["isGlobal"].set(lep.isGlobal)
#                self.inputVars["muons"]["specs"]["isTracker"].set(lep.isTracker)
#                self.inputVars["muons"]["specs"]["isPFcand"].set(lep.isPFcand)
#                self.inputVars["muons"]["specs"]["mediumId"].set(lep.mediumId)
#                self.inputVars["muons"]["specs"]["looseId_2"].set(lep.looseId)
#                self.inputVars["muons"]["specs"]["dxy"].set(lep.dxy)
#                self.inputVars["muons"]["specs"]["dz"].set(lep.dz)
                
                # -- Training variables
                self.inputVars["muons"]["vars"]["LepGood_pt"].set(lep.pt)
                self.inputVars["muons"]["vars"]["LepGood_eta"].set(lep.eta)
                self.inputVars["muons"]["vars"]["LepGood_miniRelIsoNeutral"].set(lep.miniPFRelIso_all - lep.miniPFRelIso_chg)
                self.inputVars["muons"]["vars"]["LepGood_miniRelIsoCharged"].set(lep.miniPFRelIso_chg)
                self.inputVars["muons"]["vars"]["LepGood_jetNDauChargedMVASel"].set(lep.jetNDauCharged)
                self.inputVars["muons"]["vars"]["LepGood_jetPtRelv2"].set(lep.jetPtRelv2)
                self.inputVars["muons"]["vars"]["LepGood_jetPtRatio"].set(min(1. / (1. + lep.jetRelIso), 1.5))
                self.inputVars["muons"]["vars"]["LepGood_jetDF"].set(jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0)
                self.inputVars["muons"]["vars"]["LepGood_sip3d"].set(lep.sip3d)
                self.inputVars["muons"]["vars"]["LepGood_dxy"].set(np.log(abs(lep.dxy)))
                self.inputVars["muons"]["vars"]["LepGood_dz"].set(np.log(abs(lep.dz)))
                self.inputVars["muons"]["vars"]["LepGood_segmentComp"].set(lep.segmentComp)
                 
                 # Now that all variables have been updated in memory, evaluate the MVA
                
                mva = self.mva_muons.EvaluateMVA(self.name)
                ret["LepGood_mvaTTH_run3"].append(mva)
                setattr(lep, "mvaTTH_run3", mva)
            else:
                ret["LepGood_mvaTTH_run3"].append(-1)
            
            # Store also these input variables for later studies
            ret["LepGood_miniRelIsoNeutral"].append(lep.miniPFRelIso_all - lep.miniPFRelIso_chg)
            ret["LepGood_miniRelIsoCharged"].append(lep.miniPFRelIso_chg)
            ret["LepGood_jetNDauChargedMVASel"].append(lep.jetNDauCharged)
            ret["LepGood_jetPtRatio"].append(min(1. / (1. + lep.jetRelIso), 1.5) )
            ret["LepGood_jetDF"].append(jets[lep.jetIdx].btagDeepFlavB if lep.jetIdx > -1 else 0)
            ret["LepGood_absLogDxy"].append(np.log(abs(lep.dxy)))
            ret["LepGood_absLogDz"].append(np.log(abs(lep.dz)))
            
        writeOutput(self, ret)
        return True
