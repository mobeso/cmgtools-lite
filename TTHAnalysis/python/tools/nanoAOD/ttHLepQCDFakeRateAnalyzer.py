from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
import ROOT 

class ttHLepQCDFakeRateAnalyzer( Module ):
    def __init__(self, jetSel = lambda jet : True, 
                       pairSel = lambda p : True, 
                       requirePair = True, 
                       maxLeptons = -1, 
                       isMC = None, 
                       saveJetIndex = True,
                       jetFloats = ["pt", "eta", "phi", "btagCSVV2", "btagDeepB", "btagDeepC", "btagDeepFlavB", "btagDeepFlavC"],
                       jetInts = ["jetId", "hadronFlavour"]):
        self.jetSel = jetSel
        self.pairSel = pairSel
        self.maxLeptons = maxLeptons
        self.requirePair = requirePair
        self.jetFloats = jetFloats
        self.jetInts = jetInts
        self.isMC = isMC
        self.saveIndex = saveJetIndex

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        vnames = []

        self.out.branch("FR_nPairs", "I")
        for v in self.jetFloats[:]:
            if not inputTree.GetBranch("Jet_"+v): 
                print("Skip missing Jet_"+v)
                continue
            self.out.branch("LepGood_awayJet_"+v, "F", lenVar="nLepGood")
            vnames.append(v)
        for v in self.jetInts[:]:
            if not inputTree.GetBranch("Jet_"+v): 
                print("Skip missing Jet_"+v)
                continue
            self.out.branch("LepGood_awayJet_"+v, "I", lenVar="nLepGood")
            vnames.append(v)
        if self.saveIndex:
            self.out.branch("LepGood_awayJet_index", "I", lenVar="nLepGood")
        self.vnames = vnames


    def analyze(self, event):
        leps = Collection(event, 'LepGood')
        
        #if self.maxLeptons > 0 and len(leps) > self.maxLeptons:
        #    return False
        
        jets = []
        for ij,j in enumerate(Collection(event, 'Jet')):
            if self.jetSel(j): jets.append((ij,j))
        jets.sort(key = lambda ijj : ijj[1].pt, reverse=True)

        ret = dict((v, [0 for l in leps]) for v in self.vnames)
        indices = [ -1 for l in leps ]

        npairs = 0
        for i,lep in enumerate(leps):
            for ij, jet in jets:
                if self.pairSel((lep,jet)):
                    for v in self.vnames:
                        ret[v][i] = getattr(jet, v)
                    indices[i] = ij
                    npairs += 1
                    break

#        if self.requirePair:
#            if npairs == 0: 
#                return False
        self.out.fillBranch("FR_nPairs", npairs)

        for v in self.vnames:
            self.out.fillBranch("LepGood_awayJet_"+v, ret[v])
        
        if self.saveIndex:
            self.out.fillBranch("LepGood_awayJet_index", indices)
        return True

if __name__ == '__main__':
    """ Debug the module """
    from sys import argv
    from copy import deepcopy
    import os
    from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import eventLoop
    from PhysicsTools.NanoAODTools.postprocessing.framework.output import FriendOutput, FullOutput
    from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import InputTree
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
    
    from CMGTools.TTHAnalysis.tools.nanoAOD.lepJetBTagAdder import lepJetBTagAdder
    from CMGTools.TTHAnalysis.tools.nanoAOD.functions_wz import deltaR
    from CMGTools.TTHAnalysis.tools.nanoAOD.nBJetCounter import nBJetCounter
    centralJetSel = lambda j : j.pt > 25 and abs(j.eta) < 4.7 and (j.jetId & 2)
    nBJetDeepFlav25NoRecl = lambda : nBJetCounter("DeepFlav25", "btagDeepFlavB", centralJetSel)

    # --- b tagging working points from 2018
    looseDeepFlavB = 0.0494
    mediumDeepFlavB = 0.2770
    looselep = lambda lep          : _loose_lepton(lep, looseDeepFlavB, mediumDeepFlavB)
    cleanlep = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
    folep    = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
    tightlep = lambda lep, jetlist : _tight_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)


    mainpath = "/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc_fr/2022EE/"
    process = "TTtoLNu2Q_part1"
    
    friends = [

    ]
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
    
    module_test =  ttHLepQCDFakeRateAnalyzer(
        jetSel = centralJetSel,
        pairSel = lambda pair : deltaR(pair[0].eta, pair[0].phi, pair[1].eta, pair[1].phi) > 0.7,
        maxLeptons = 1, 
        requirePair = True
    )
    module_test.beginJob()

    (nall, npass, timeLoop) = eventLoop([lepJetBTagAdder("btagDeepFlavB", "jetBTagDeepFlav"), module_test, nBJetCounter("DeepFlavB25", "btagDeepFlavB", centralJetSel, "2022")], file_, outFile, tree, outTree, maxEvents = nentries)
    print(('Processed %d preselected entries from %s (%s entries). Finally selected %d entries' % (nall, __file__.split("/")[-1].replace(".py", ""), nentries, npass)))
    outTree.write()
    file_.Close()
    outFile.Close()
    print("Test done")
    module_test.endJob()
      
