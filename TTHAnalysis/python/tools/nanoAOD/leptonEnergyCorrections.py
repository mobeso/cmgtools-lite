import ROOT
import correctionlib._core as core
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput
import ROOT, copy, os
import array, math
import numpy as np

""" Module to apply lepton corrections for Run3. 
[13/01/2024]: there are no rochester, so the module just adds a branch "correctedpt" which
is equal to the nanoAOD properties for the muon.
"""
class leptonEnergyCorrections( Module ):
    def __init__(self, basepath, file_electrons, eras_electrons, isData = False):
        self.basepath = basepath
        self.variations = ["ptSmearUp","ptSmearDown", "ptScaleUp", "ptScaleDown"]
        self.isData = isData
        # Stuff for muons: nothing
        
        # Stuff for electrons:
        print(f" >> Loading electron scale and smearing from file: {self.basepath}/{file_electrons}" )
        self.electron_evaluatorScaleName = f"{eras_electrons}_ScaleJSON"
        self.electron_evaluatorSmearingName = f"{eras_electrons}_SmearingJSON"
        self.electron_evaluatorScale = core.CorrectionSet.from_file(self.basepath + file_electrons)[self.electron_evaluatorScaleName]
        self.electron_evaluatorSmearing = core.CorrectionSet.from_file(self.basepath + file_electrons)[self.electron_evaluatorSmearingName]

        self.listBranches()
        
    def analyze(self, event):
        self.resetMemory(event)
        self.correctTheLeptons(event)
        return True

    def listBranches(self):
        self.branches = []
        # very annoying but if we don't use another variable for nLepGood then it overwrites some stuff
        # e.g. If I use nLepGood --> then nLepGood becomes always 20 in some cases, so I prefer
        # to always do it like this and just not use the nLepGood_corrected
        self.branches.append(("LepGood_correctedpt", "F", 20, "nLepGood_corrected"))
        if not self.isData:      
            for var in self.variations:
                self.branches.append(("LepGood_corrected" + var, "F", 20, "nLepGood_corrected")) 
    
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        declareOutput(self, wrappedOutputTree, self.branches)
        return
    
    def correctTheLeptons(self, event):
        self.lepCorr = [l for l  in Collection(event, "LepGood", "nLepGood")  ]
        for l in self.lepCorr:
            if abs(l.pdgId) == 13: 
                ptCorr = 1
                setattr(l, "pt", l.pt*ptCorr)
                if not self.isData:
                    setattr(l, "ptSmearUp", l.pt*ptCorr)
                    setattr(l, "ptSmearDown", l.pt*ptCorr) 
                    setattr(l, "ptScaleUp", l.pt*ptCorr)
                    setattr(l, "ptScaleDown", l.pt*ptCorr)

            if abs(l.pdgId) == 11:
                # --- Inputs for the electron corrections
                seedGain = l.seedGain
                etaSC = l.eta + l.deltaEtaSC
                run = float(event.run)
                r9 = l.r9
                pt = l.pt
                if self.isData:
                    scale = self.electron_evaluatorScale.evaluate("total_correction", seedGain, run, etaSC, r9, pt)
                    corrected_pt = scale * pt
                    setattr(l, "pt", corrected_pt)
                else:
                    rho = self.electron_evaluatorSmearing.evaluate("rho", etaSC, r9)  # rho is internal scale and smearing lingo
                    # It does not correspond to the pileup rho energy density, instead it is the standard deviation of the Gaussian used to draw the smearing
                    rng = np.random.default_rng()  # The smearing is done statistically, so we need some random numbers
                    smearing = rng.normal(loc=1., scale=rho) # We could try to improve this setting the seed deterministically to have reproducible results
                    corrected_pt = smearing * pt
                    setattr(l, "pt", corrected_pt)

                    # Systematic uncertainty on smearing
                    unc_rho = self.electron_evaluatorSmearing.evaluate("err_rho",  etaSC, r9)
                    rho_up = rho + unc_rho
                    rho_down = rho - unc_rho
                    smearing_up = rng.normal(loc=1., scale=rho_up)
                    smearing_down = rng.normal(loc=1., scale=rho_down)
                    corrected_pt_smearing_up = smearing_up * pt
                    corrected_pt_smearing_down = smearing_down * pt
                    setattr(l, "ptSmearUp", corrected_pt_smearing_up)
                    setattr(l, "ptSmearDown", corrected_pt_smearing_down)    

                    
                    # Systematic uncertainty on scale
                    scale_MC_unc = self.electron_evaluatorScale.evaluate("total_uncertainty", seedGain, run, etaSC, r9, pt)
                    corrected_pt_scale_up = (1+scale_MC_unc) * pt
                    corrected_pt_scale_down = (1-scale_MC_unc) * pt
                    setattr(l, "ptScaleUp", corrected_pt_scale_up)
                    setattr(l, "ptScaleDown", corrected_pt_scale_down)
                    
        # Now write everything in the tree   
        self.ret["nLepGood_corrected"] = len(self.lepCorr)
        for i, l in enumerate(self.lepCorr):
            self.ret["LepGood_correctedpt"][i] = getattr(l, "pt", -999)
            #print( "nominal", l.pdgId, getattr(l, "pt", -999) )
            if not self.isData:
                for var in self.variations:
                    self.ret["LepGood_corrected" + var][i] = getattr(l, var, -999.)
                    #print( l.pdgId, getattr(l, var, -999.), getattr(l, var, -999.)/getattr(l, "pt", -999.) )
                #print(" ---- ")
        writeOutput(self, self.ret)
        return 


    def resetMemory(self, ev):
        self.ret = {}
        #for i in range(8):
        self.ret["nLepGood_corrected"] = 0
        self.ret["LepGood_correctedpt"] = [-999]*ev.nLepGood
        if not self.isData:      
            for var in self.variations:
                    self.ret["LepGood_corrected" + var] = [-999.]*ev.nLepGood

if __name__ == '__main__':
    """ Debug the module """
    from sys import argv
    from copy import deepcopy
    import os
    from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
    from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput
    from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
    from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import conept
    
    mainpath = "/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees_v2/mc/2022EE/"
    process = "WZto3LNu"
    
    friends = []
    nentries = int(argv[1])
    ### Open the main file
    file_ = ROOT.TFile( os.path.join(mainpath, process+".root") )
    tree = file_.Get("Events")
    for friend in friends:
      print(os.path.join(mainpath, friend, process+"_Friend.root"))
      friendfile = ROOT.TFile( os.path.join(mainpath, friend, process+"_Friend.root") ) 
      tree.AddFriend("Friends", friendfile)
    
    ### Replicate the eventLoop
    tree = InputTree(tree)
    outFile = ROOT.TFile.Open("test_%s.root"%process, "RECREATE")
    outTree = FriendOutput(file_, tree, outFile)
    
    module_test =  leptonEnergyCorrections(
        basepath       = os.environ["CMSSW_BASE"] + "/src/CMGTools/TTHAnalysis/data/WZRun3/EGM/2022EE/",
        file_electrons = "electronSS_EFG.json", 
        eras_electrons = "2022Re-recoE+PromptFG",
        isData = False
    )
    
    module_test.beginJob()
    (nall, npass, timeLoop) = eventLoop([module_test], file_, outFile, tree, outTree, maxEvents = nentries)
    print(('Processed %d preselected entries from %s (%s entries). Finally selected %d entries' % (nall, __file__.split("/")[-1].replace(".py", ""), nentries, npass)))
    outTree.write()
    file_.Close()
    outFile.Close()
    print("Test done")
    module_test.endJob()
