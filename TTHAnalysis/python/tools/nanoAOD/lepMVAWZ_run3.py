from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection as Collection
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import numpy as np
import ROOT
import os
import array as ar


class lepMVAWZ_run3(Module):
    def __init__(self, inputpath, elxmlpath, muxmlpath, inputVars, suffix = "run3"):
            
        self.branches = [
            ("LepGood_mvaTTH%s"%suffix, "F", 20, "nLepGood"),
        ]
        modelname = "BDTG"
        
        self.inputpath = inputpath
        self.elxmlpath = elxmlpath
        self.muxmlpath = muxmlpath
        self.suffix = suffix
        
        self.inputVars = inputVars
        
        self.mva_electrons = self.open_model(os.path.join(inputpath, elxmlpath), self.inputVars["electrons"], "electrons")
        self.mva_muons     = self.open_model(os.path.join(inputpath, muxmlpath), self.inputVars["muons"],  "muons")
        return
    
    def open_model(self, xmlpath, vars, modelname):
        """ Method to open a model a load variables """
        print(" >> Opening model: %s"%xmlpath)
        reader = ROOT.TMVA.Reader()
        for vname, v in vars.items():
                print("  + Adding variable: ", v[0].name) 
                reader.AddVariable(v[0].name, v[0].var)
        print(">> Booking MVA")
        reader.BookMVA(modelname, xmlpath)
        return reader

    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
        return

    def set_vars(self, vars, lep, jets):
        """ Set the values of the variables before evaluating MVA """
        for vname, v in vars.items():
            lambda_func = v[1]
            v[0].set( lambda_func(lep, jets) )
        return
    
    def evaluate(self, mva, name):
        return mva.EvaluateMVA(name)
    
    def analyze(self, event):
        """ All the magic happens here """
        ret = {
            "LepGood_mvaTTH%s"%self.suffix : [],
        }
        
        jets = Collection(event, "Jet", "nJet")

        for ilep, lep in enumerate(Collection(event, "LepGood","nLepGood")):
            if abs(lep.pdgId) == 11: # Electrons                
                # Set the values of the input variables
                self.set_vars(self.inputVars["electrons"], lep, jets)
                
                # Evaluate the MVA
                mva = self.evaluate(self.mva_electrons, "electrons")
                
                # Save it
                ret["LepGood_mvaTTH%s"%self.suffix].append(mva)
                setattr(lep, "mvaTTH%s"%self.suffix, mva)
            elif abs(lep.pdgId) == 13: # Muons         
                # Set the values of the input variables
                self.set_vars(self.inputVars["muons"], lep, jets)
                
                # Evaluate the MVA
                mva = self.evaluate(self.mva_muons, "muons")
                
                # Save it
                ret["LepGood_mvaTTH%s"%self.suffix].append(mva)
                setattr(lep, "mvaTTH%s"%self.suffix, mva)
            else:
                ret["LepGood_mvaTTH%s"%self.suffix].append(-1)
                    
        writeOutput(self, ret)
        return True

if __name__ == '__main__':
    """ Debug the module """
    from sys import argv
    from copy import deepcopy
    from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
    from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput
    from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
    
    mainpath = "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022PostEE/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_PostEE_oct2023_WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/231023_150004/0000/"
    process = "tree_12"
    
    nentries = int(argv[1])
    ### Open the main file
    file_ = ROOT.TFile( os.path.join(mainpath, process+".root") )
    tree = file_.Get("Events")

    
    ### Replicate the eventLoop
    tree = InputTree(tree)
    outFile = ROOT.TFile.Open("test_%s.root"%process, "RECREATE")
    #outTree = FriendOutput(file_, tree, outFile)
    outTree = FullOutput(file_, tree, outFile, maxEntries = nentries)
    
    weightspath_2022EE   = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/lepMVA/2022EE")
    
    from CMGTools.TTHAnalysis.tools.nanoAOD.wzsm_modules import lepMerge_EE
    import CMGTools.TTHAnalysis.tools.nanoAOD.mvaTTH_vars_run3 as mvatth_cfg

    weightspath_2022EE = os.path.join(os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3/")

    module_test = lepMVAWZ_run3(
        weightspath_2022EE, 
        elxmlpath = "EGM/Electron-mvaTTH.2022EE.weights_mvaISO.xml", 
        muxmlpath = "MUO/Muon-mvaTTH.2022EE.weights.xml", 
        suffix = "_run3",
        inputVars = {"muons":  mvatth_cfg.muon_df("2022"), "electrons" : mvatth_cfg.electron_df_wIso("2022")}
    )
    
    module_test.beginJob()
    (nall, npass, timeLoop) = eventLoop([lepMerge_EE, module_test], file_, outFile, tree, outTree, maxEvents = nentries)
    print(('Processed %d preselected entries from %s (%s entries). Finally selected %d entries' % (nall, __file__.split("/")[-1].replace(".py", ""), nentries, npass)))
    outTree.write()
    file_.Close()
    outFile.Close()
    print("Test done")
    module_test.endJob()




