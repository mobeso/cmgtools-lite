import ROOT
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from CMGTools.TTHAnalysis.tools.nanoAOD.friendVariableProducerTools import declareOutput, writeOutput

from copy import copy, deepcopy
import math
""" Define some useful functions """
def deltaPhi( p1, p2):
    '''Computes delta phi, handling periodic limit conditions.'''
    res = p1 - p2
    while res > math.pi:
        res -= 2*math.pi
    while res < -math.pi:
        res += 2*math.pi
    return res


def deltaR2( e1, p1, e2=None, p2=None):
    """Take either 4 arguments (eta,phi, eta,phi) or two objects that have 'eta', 'phi' attributes)"""
    if (e2 == None and p2 == None):
        return deltaR2(e1.eta,e1.phi, p1.eta, p1.phi)
    de = e1 - e2
    dp = deltaPhi(p1, p2)
    return de*de + dp*dp


def deltaR( *args ):
    return math.sqrt( deltaR2(*args) )



def minMllTL(lepsl, lepst, bothcut=lambda lep:True, onecut=lambda lep:True, paircut=lambda lep1,lep2:True):
      pairs = []
      for l1 in lepst:
          if not bothcut(l1): continue
          for l2 in lepsl:
              if l2 == l1 or not bothcut(l2): continue
              if not onecut(l1) and not onecut(l2): continue
              if not paircut(l1,l2): continue
              mll = (l1.p4() + l2.p4()).M()
              pairs.append(mll)
      if len(pairs):
          return min(pairs)
      return -1

def passMllVeto(l1, l2, mZmin, mZmax, isOSSF ):
  if  l1.pdgId == -l2.pdgId or not isOSSF:
      mz = (l1.p4() + l2.p4()).M()
      if mz > mZmin and  mz < mZmax:
          return False
  return True

def passMllTLVeto(lep, lepsl, mZmin, mZmax, isOSSF):
  for ll in lepsl:
      if ll == lep: continue
      if not passMllVeto(lep, ll, mZmin, mZmax, isOSSF):
          return False
  return True

def passTripleMllVeto(l1, l2, l3, mZmin, mZmax, isOSSF ):
  ls = [passMllVeto(l1, l2, mZmin, mZmax, isOSSF), \
        passMllVeto(l1, l3, mZmin, mZmax, isOSSF), \
        passMllVeto(l2, l3, mZmin, mZmax, isOSSF)]
  if all(ls): return True
  return False

""" These are just some stupid functions to print messages with coloring and all that. Useful for debugging. """
def color_msg(msg, color = "none"):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "none" : "0m",
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
        "yellow" : "1;35m"
    }

    print("\033[%s%s \033[0m"%(codes[color], msg))
    return


""" Proper class implementation """
class LeptonJetRecleanerWZSM(Module):
  def __init__(self, label,
               # Lepton selectors
               looseLeptonSel,
               cleaningLeptonSel, 
               FOLeptonSel,
               tightLeptonSel,
               # Jet selectors
               cleanJet, 
               selectJet,
               # Tau selectors
               cleanTau,
               looseTau,
               tightTau,
               cleanJetsWithTaus,
               # extra stuff
               doVetoZ,
               doVetoLMf,
               doVetoLMt,
               jetPt,
               bJetPt,
               coneptdef,
               storeJetVariables=False,
               cleanTausWithLoose=False, 
               systsJEC      = [],
               systsLepScale = [],
               year=2022, 
               bAlgo="btagDeepFlavB",
               btag_wps = None,
               verbosity = 0):
    # --- Constructor --- #
    self.verbosity = verbosity
    # * Label for output variables
    self.label = "" if (label in ["",None]) else ("_"+label)
    
    # * Lepton selection at different levels
    self.looseLeptonSel = looseLeptonSel
     
    # * The following are applied on top of looseLepton selections
    self.cleaningLeptonSel = cleaningLeptonSel 
    self.FOLeptonSel = FOLeptonSel             
    self.tightLeptonSel = tightLeptonSel 
    
    # * Jet selections
    self.selectJet = selectJet
    self.cleanJet = cleanJet

    # * Tau selections
    self.cleanTau = cleanTau
    self.looseTau = looseTau
    self.tightTau = tightTau
    
    # * Booleans to control which leptons are to be cleaned from the jets. 
    self.cleanJetsWithTaus = cleanJetsWithTaus
    self.cleanTausWithLoose = cleanTausWithLoose

    # * Other vetos
    self.doVetoZ = doVetoZ
    self.doVetoLMf = doVetoLMf
    self.doVetoLMt = doVetoLMt
    
    # * Definitions
    self.coneptdef = coneptdef
    ### Compute the cone-corrected pT for each lepton
    if not self.coneptdef:
      raise RuntimeError("[leptonJetReCleaner::Error]: Choose a definition for cone pt")
    
    self.jetPt = jetPt # Minimum jet pT
    self.bJetPt = bJetPt # Minimum b tag pT
    self.strJetPt = str(int(jetPt))
    self.strBJetPt = str(int(bJetPt))

    # * Systematic variations
    self.systsJEC      = systsJEC
    self.systsLepScale = systsLepScale

    # * Other stuff
    self.storeJetVariables = storeJetVariables
    self.year = year
    self.bAlgo = bAlgo
    self.btag_wps = btag_wps
    
    # List the branches that will be written to declare the output
    self.listBranches()
    if self.verbosity > 0:
      color_msg(" >> Module %s initiated in debug mode"%(self.__class__.__name__), "green")

  def listBranches(self):
    ''' Method to prompt with a list of the branches produced in this module'''
    label = self.label
    branches = []
    
    lep_iters = [""] + self.systsLepScale
    for lepvar in lep_iters:
      lepvar = "_%s"%lepvar if lepvar != "" else lepvar
      branches.extend([
        ("nLepGood"+lepvar,"I"), 
        ("LepGood_conePt"+lepvar,"F",20,"nLepGood"+lepvar),
        ("nLepLoose%s%s"%(lepvar, label), "I"), 
        ("iL%s%s"%(lepvar, label),"I",20, "nLepLoose%s%s"%(lepvar, label)), # passing loose
        ("nLepLooseVeto%s%s"%(lepvar, label), "I"), 
        ("iLV%s%s"%(lepvar, label),"I",20, "nLepLooseVeto%s%s"%(lepvar, label)), # passing loose + veto
        ("nLepCleaning%s%s"%(lepvar, label), "I"), 
        ("iC%s%s"%(lepvar, label),"I",20, "nLepCleaning%s%s"%(lepvar, label)), # passing cleaning
        ("nLepCleaningVeto%s%s"%(lepvar, label), "I"), 
        ("iCV%s%s"%(lepvar, label),"I",20, "nLepCleaningVeto%s%s"%(lepvar, label)), # passing cleaning + veto
        ("nLepFO%s%s"%(lepvar, label), "I"), 
        ("iF%s%s"%(lepvar, label),"I",20, "nLepFO%s%s"%(lepvar, label)), # passing FO, sorted by conept
        ("nLepFOVeto%s%s"%(lepvar, label), "I"), 
        ("iFV%s%s"%(lepvar, label),"I",20, "nLepFOVeto%s%s"%(lepvar, label)), # passing FO + veto, sorted by conept
        ("nLepTight%s%s"%(lepvar, label), "I"), 
        ("iT%s%s"%(lepvar, label),"I", 20, "nLepTight%s%s"%(lepvar, label)), # passing tight, sorted by conept
        ("nLepTightVeto%s%s"%(lepvar, label), "I"), 
        ("iTV%s%s"%(lepvar, label),"I",20, "nLepTightVeto%s%s"%(lepvar, label)), # passing tight + veto, sorted by conept
        ("LepGood_isLoose%s%s"%(lepvar, label),"I", 20,"nLepGood"+lepvar),
        ("LepGood_isLooseVeto%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isCleaning%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isCleaningVeto%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isFO%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isFOVeto%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isTight%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("LepGood_isTightVeto%s%s"%(lepvar, label),"I",20,"nLepGood"+lepvar),
        ("mZ1%s%s"%(lepvar, label),"F"), 
        ("minMllAFAS%s%s"%(lepvar, label),"F"), 
        ("minMllAFOS%s%s"%(lepvar, label),"F"), 
        ("minMllAFSS%s%s"%(lepvar, label),"F"), 
        ("minMllSFOS%s%s"%(lepvar, label),"F")
        ])

    jet_iters = [""] + self.systsJEC
    for jecvar in jet_iters:
      jecvar = "_%s"%jecvar if jecvar != "" else jecvar
      branches.extend([
      ("nJetSel%s%s"%(label, jecvar), "I"), 
      ("iJSel%s%s"%(label, jecvar),"I",20,"nJetSel%s%s"%(label, jecvar)), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
      ("nDiscJetSel%s%s"%(label, jecvar), "I"), 
      ("iDiscJSel%s%s"%(label, jecvar),"I",20,"nDiscJetSel%s%s"%(label, jecvar)), # index >= 0 if in Jet; -1-index (<0) if in DiscJet
      ("nJet"+self.strJetPt+label+jecvar, "I"), 
      "htJet"+self.strJetPt + "j%s%s"%(label, jecvar),
      "mhtJet"+self.strJetPt + label+jecvar, 
      ("nBJetLoose"+self.strJetPt+label+jecvar, "I"), 
      ("nBJetMedium"+self.strJetPt+label+jecvar, "I"), 
      ("nBJetTight"+self.strJetPt+label+jecvar, "I"),
      ("nJet"+self.strBJetPt+label+jecvar, "I"), 
      "htJet"+self.strBJetPt+"j%s%s"%(label, jecvar),
      "mhtJet"+self.strBJetPt + label+jecvar, 
      ("nBJetLoose"+self.strBJetPt+label+jecvar, "I"), 
      ("nBJetMedium"+self.strBJetPt+label+jecvar, "I"), 
      ("nBJetTight"+self.strBJetPt+label+jecvar, "I"),
      ])


    if self.storeJetVariables:
        for jfloat in "pt eta phi mass btagDeepB".split():
            for jecvar in jet_iters:
                jecvar = "_%s"%jecvar if jecvar != "" else jecvar
                branches.append( ("JetSel%s%s_%s"%(label, jecvar, jfloat),"F",20,"nJetSel"+label) )
    self.branches = branches
    return 
  
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    declareOutput(self, wrappedOutputTree, self.branches)
    return
  
  def fillCollWithVeto(
    self,
    ret,
    refcollection,
    leps,
    lab,
    labext,
    selection,
    lepsforveto,
    doVetoZ,
    doVetoLM,
    sortby,
    ht=-1,
    pad_zeros_up_to=0,
    extraTag ="" 
    ):
    ''' 
        Method to categorise leptons using selections 
        
      Three lepton lists are crated: 
          * lepspass : leptons that pass selection criteria
          * lepsforveto : leptons to veto with
          * lepspassveto : vetoed leptons

    '''
    
    ret['i'+lab+extraTag]     = []; # List of leptons that pass selection
    ret['i'+lab+'V'+extraTag] = []; # List of vetoed leptons
    
    for lep in leps:
        ## doVeto: True if the lepton passes a given selection 
        ## ht = -1: selection = loose selection 
        ## ht = 1 : selection = other selection (cleaning, FO, tight) 
        doVeto = selection(lep) if ht <0 else selection(lep, self.nominal_jetsc)
        if (doVeto):
            ret['i'+lab+extraTag].append(refcollection.index(lep)) # Keep the index of the leptons that pass the selection

    ## Sort the list of selected leptons 
    ret['i'+lab+extraTag] = self.sortIndexListByFunction(
      indexlist = ret['i'+lab+extraTag], 
      parentcollection = refcollection, 
      func = sortby
    )
    
    ret['nLep'+labext+extraTag]       = len(ret['i'+lab+extraTag])
    ret['LepGood_is'+labext+extraTag] = [(1 if i in ret['i'+lab+extraTag] else 0) for i in range(len(refcollection))]
    
    ## Fetch leptons that pass the selection
    lepspass = [ refcollection[il] for il in ret['i'+lab+extraTag]  ]
    if lepsforveto == None: 
      lepsforveto = lepspass # Veto selected leptons among themselves
    
    for lep in lepspass:
        ## Veto leptons that belong to any OSSF pair that does not originate from a 
        ## Z or low mass resonance. 
        NOcomesfromZ  = (not doVetoZ  or passMllTLVeto(lep, lepsforveto, 76, 106, True))
        NOcomesfromLM = (not doVetoLM or passMllTLVeto(lep, lepsforveto,  0,  12, True))
        if NOcomesfromLM and NOcomesfromZ:
            ret['i'+lab+'V'+extraTag].append(refcollection.index(lep))

    ## Sort the vetoed leptons
    ret['i'+lab+'V'+extraTag] = self.sortIndexListByFunction(
      indexlist        = ret['i'+lab+'V'+extraTag],
      parentcollection = refcollection,
      func             = sortby
    )   
    ret['nLep'+labext+'Veto'+extraTag]       = len(ret['i'+lab+'V'+extraTag])
    ret['LepGood_is'+labext+'Veto'+extraTag] = [(1 if i in ret['i'+lab+'V'+extraTag] else 0) for i in range(len(refcollection))]

    ## List of leptons that pass selection criteria but are vetoed
    lepspassveto              = [ refcollection[il] for il in ret['i'+lab+'V'+extraTag]  ]
    ret['i'+lab+extraTag]     = ret['i'+lab+extraTag] + [0]*(pad_zeros_up_to-len(ret['i'+lab+extraTag]))
    ret['i'+lab+'V'+extraTag] = ret['i'+lab+'V'+extraTag] + [0]*(pad_zeros_up_to-len(ret['i'+lab+'V'+extraTag]))

    return (ret, lepspass, lepspassveto)

  def sortIndexListByFunction(self, indexlist, parentcollection, func):
    if not func: return indexlist[:]
    newsort = sorted([(ij,parentcollection[ij]) for ij in indexlist], key = lambda x: func(x[1]), reverse=True)
    return [x[0] for x in newsort]

  def recleanJets(self, jetcollcleaned, lepcoll, postfix, ret, jetret, discjetret):
    ## Define jets
    ret["iJSel"+postfix]     = [] 
    ret["iDiscJSel"+postfix] = []

    # 0. mark each jet as clean
    for j in jetcollcleaned: 
      j._clean = True
      if getattr(j,  "idx_veto") != -1:
        j._clean = False # Already discard the jet if it's in the veto region of the HCAL

    if self.verbosity > 0:
      color_msg("      o I'm going to assume all jets are good.", "red")
      
    # 1. associate to each lepton passing the cleaning selection its nearest jet 
    for ilep, lep in enumerate(lepcoll):
      if self.verbosity > 0:
        color_msg("      o Cleaning lepton %d"%ilep, "green")
      
      
      best = None; bestdr = 0.4
      for j in jetcollcleaned:
          dr = deltaR(lep, j)
          if dr < bestdr:
              best = j; bestdr = dr
      
      if self.verbosity > 0:
        print("         > Best jet candidate:", best)
      if best is not None and self.cleanJet(lep, best, bestdr):
          best._clean = False
      
      if self.verbosity > 0 and best is not None:
          print("         > This jet will be removed.")



    # 2. compute the jet list
    for ijc, j in enumerate(jetcollcleaned):
        if not self.selectJet(j): 
          continue
        elif not j._clean: 
          ret["iDiscJSel"+postfix].append(ijc)
        else: 
          ret["iJSel"+postfix].append(ijc)
    
    # 3. sort the jets by pt
    ret["iJSel"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt, reverse = True)
    ret["iDiscJSel"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt, reverse = True)
    if self.verbosity > 0:
      print("      o (Ordered by pT) Finally selected these jets. (these are indices in the main jet list)", ret["iJSel"+postfix])
      print("      o (Ordered by pT) Finally discarded these jets. (these are indices in the main jet list)", ret["iDiscJSel"+postfix])
    ret["nJetSel"+postfix] = len(ret["iJSel"+postfix])
    ret["nDiscJetSel"+postfix] = len(ret["iDiscJSel"+postfix])

    # 4. if needed, store the jet 4-vectors
    if self.storeJetVariables:
        if postfix==self.label:
            for jfloat in "pt eta phi mass btagDeepB".split():
                jetret[jfloat] = []
                discjetret[jfloat] = []
            for idx in ret["iJSel"+postfix]:
                jet = jetcollcleaned[idx]
                for jfloat in "pt eta phi mass btagDeepB".split():
                    jetret[jfloat].append( getattr(jet,jfloat) )
            for idx in ret["iDiscJSel"+postfix]:
                jet = jetcollcleaned[idx]
                for jfloat in "pt eta phi mass btagDeepB".split():
                    discjetret[jfloat].append( getattr(jet,jfloat) )

    # 5. compute some variables and their sum
    ret["nJet"+self.strBJetPt+postfix] = 0
    ret["htJet"+self.strBJetPt+"j"+postfix] = 0
    ret["mhtJet"+self.strBJetPt+postfix] = 0
    ret["nBJetLoose"+self.strBJetPt+postfix] = 0
    ret["nBJetMedium"+self.strBJetPt+postfix] = 0 
    ret["nBJetTight"+self.strBJetPt+postfix] = 0
            
    ret["nJet"+self.strJetPt+postfix] = 0
    ret["htJet"+self.strJetPt+"j"+postfix] = 0
    ret["mhtJet"+self.strJetPt+postfix] = 0
    ret["nBJetLoose"+self.strJetPt+postfix] = 0
    ret["nBJetMedium"+self.strJetPt+postfix] = 0
    ret["nBJetTight"+self.strJetPt+postfix] = 0

    cleanjets = []
    alljets = jetcollcleaned
    mhtBJetPtvec = ROOT.TLorentzVector(0,0,0,0)
    mhtJetPtvec = ROOT.TLorentzVector(0,0,0,0)
    for x in lepcoll: 
      mhtBJetPtvec = mhtBJetPtvec - x.p4()
    for x in lepcoll: 
      mhtJetPtvec = mhtJetPtvec - x.p4()
    for j in alljets:
        if not (j._clean and self.selectJet(j)): 
          continue
        
        cleanjets.append(j)
        btagWPL = self.btag_wps[self.year][self.bAlgo]["L"]
        btagWPM = self.btag_wps[self.year][self.bAlgo]["M"]
        btagWPT = self.btag_wps[self.year][self.bAlgo]["T"]
        
        if self.verbosity > 0:
          print("         > Computing b tagging scores for algo: {algo} ({year})".format(algo = self.bAlgo, year = self.year))
          print("           o WPL", btagWPL)
          print("           o WPM", btagWPM)
          print("           o WPT", btagWPT)

        if j.pt > float(self.bJetPt):
          
          ret["nJet"+self.strBJetPt+postfix] += 1
          ret["htJet"+self.strBJetPt+"j"+postfix] += j.pt 
          if getattr(j, self.bAlgo) > btagWPL: ret["nBJetLoose"+self.strBJetPt+postfix]  += 1
          if getattr(j, self.bAlgo) > btagWPM: ret["nBJetMedium"+self.strBJetPt+postfix] += 1
          if getattr(j, self.bAlgo) > btagWPT: ret["nBJetTight"+self.strBJetPt+postfix]  += 1
          mhtBJetPtvec = mhtBJetPtvec - j.p4()

        if j.pt > float(self.jetPt):
          ret["nJet"+self.strJetPt+postfix] += 1; ret["htJet"+self.strJetPt+"j"+postfix] += j.pt; 
          if getattr(j, self.bAlgo) > btagWPL: ret["nBJetLoose"+self.strJetPt+postfix]  += 1
          if getattr(j, self.bAlgo) > btagWPM: ret["nBJetMedium"+self.strJetPt+postfix] += 1
          if getattr(j, self.bAlgo) > btagWPT: ret["nBJetTight"+self.strJetPt+postfix]  += 1
          mhtBJetPtvec = mhtBJetPtvec - j.p4()

    ret["mhtJet"+self.strBJetPt+postfix] = mhtBJetPtvec.Pt()
    ret["mhtJet"+self.strJetPt+postfix]  = mhtJetPtvec.Pt()
    return cleanjets
  
  
  def create_nominal_colls(self, event):
    ''' Method to create collections with nominal objects '''
    self.nominal_leps  = [copy(l) for l in Collection(event,"LepGood","nLepGood")]
    self.nominal_jetsc = [copy(j) for j in Collection(event,"Jet","nJet")]
    
    # -- Use the pt_nom for the nominal jets
    for j in self.nominal_jetsc:
      if hasattr(j, "pt_nom"):
        setattr(j, "pt", getattr(j, "pt_nom"))
    return
  
  def clean_jets(self, ret, leps, lepsl):
    # -- Compute leptons for cleaning: leptons that pass cleaning criteria
    lepsc = []; lepscv = []
    ret, lepsc, lepscv = self.fillCollWithVeto(
      ret           = ret,
      refcollection = leps,
      leps          = lepsl,
      lab           = 'C',
      labext        = 'Cleaning',
      selection     = self.cleaningLeptonSel, 
      lepsforveto   = lepsl, 
      doVetoZ       = self.doVetoZ, 
      doVetoLM      = self.doVetoLMf, 
      sortby        = None, 
      ht            = 1, 
      extraTag      = ""
    )

    cleanjets = {}; jetret = {}; discjetret = {}; retwlabel = {}
    for jecvar in [""] + self.systsJEC:
      # -- Create a copy of the nominal jets, but set the pt with the variation
      jetsc = []
      jecvar = "_%s"%jecvar if jecvar != "" else jecvar
      #print(">> var: %s"%jecvar)
      if self.verbosity > 0:
        print("    - Jets available for cleaning:", self.nominal_jetsc)
        print("    - Jet pTs:", [(ij, j.pt) for ij, j in enumerate(self.nominal_jetsc)])
        print("    - Jet Eta:", [(ij, abs(j.eta)) for ij, j in enumerate(self.nominal_jetsc)])
        print("    - Jet IDs:", [(ij, j.jetId) for ij, j in enumerate(self.nominal_jetsc)])


      for j in self.nominal_jetsc:
        jcopy = copy(j)
        #print(" -- nominal pt: %3f"%j.pt)
        setattr(jcopy, "pt", getattr(jcopy, "pt%s"%jecvar))
        #print(" -- variated pt: %3f "%jcopy.pt)
        #print(" ------- ")
        jetsc.append(jcopy)
      #print("===========")
      
      # Now do the cleaning with the variated jet
      cleanjets[jecvar] = self.recleanJets(
        jetcollcleaned   = jetsc,
        lepcoll          = lepsc, 
        postfix          = self.label + jecvar,
        ret              = retwlabel,
        jetret           = jetret,
        discjetret       = discjetret
      )
    self.jetret    = jetret
    self.retwlabel = retwlabel
    return 
  
  def create_leptons(self, doClean = False, lepvar = None):
    ''' Method to compute lepton collections really
       * If lepvar == None --> performs cleaning
       * If lepvar != None --> Create loose, FO and Tight collections (jets should be cleaned beforehand)
    '''
    if self.verbosity > 0:
      color_msg(">> Creating the lepton classes", "blue")
    # Use a copy of the nominal leptons
    leplabel = "_%s"%lepvar if lepvar else ""
    ret  = {}
    
    leps = [copy(l) for l in self.nominal_leps]
    if self.verbosity > 0:
      color_msg("  * All leptons", "yellow")
      print("   - ", leps)
      print("   - ", [lep.pdgId for lep in leps], "PDGID")

    # -- Set the lepton scale variations, if needed
    for lep in leps:
      #if lepvar == "elScaleUp"   and l.pdgId == 11: 
      #  l.pt = l.correctedptUp
      #if lepvar == "elScaleDown" and l.pdgId == 11: 
      #  l.pt = l.correctedptDown
      #if lepvar == "muScaleUp"   and l.pdgId == 13: 
      #  l.pt = l.correctedptUp
      #if lepvar == "muScaleDown" and l.pdgId == 13: 
      #  l.pt = l.correctedptDown 
        
      ## Now set the cone-corrected pT for the leptons    
      lep.conept = self.coneptdef(lep)
        
    # -- Compute loose leptons
    lepsl = []; lepslv = []
    ret, lepsl, lepslv = self.fillCollWithVeto(
      ret           = ret,
      refcollection = leps,
      leps          = leps,
      lab           = 'L',
      labext        = 'Loose', 
      selection     = self.looseLeptonSel, 
      lepsforveto   = None, 
      doVetoZ       = self.doVetoZ, 
      doVetoLM      = self.doVetoLMf, 
      sortby        = None, 
      ht            = -1, 
      extraTag      = leplabel
    )
    if self.verbosity > 0:
      color_msg("  * Loose leptons", "yellow")
      print("   - ", lepsl)
      print("   - ", [lep.pdgId for lep in lepsl], "PDGID")

    
    # -- Compute lepton pair masses
    ret['mZ1%s'%leplabel]        = bestZ1TL(lepsl, lepsl)
    ret['minMllAFAS%s'%leplabel] = minMllTL(lepsl, lepsl)
    ret['minMllAFOS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge !=  l2.charge)
    ret['minMllAFSS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge ==  l2.charge)
    ret['minMllSFOS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.pdgId  == -l2.pdgId)
    
    # Do the cleaning if needed
    if self.verbosity > 0:
      color_msg("  * Going to clean jets now with FO leptons", "red")
    if doClean: self.clean_jets(ret, leps, lepsl)
        
    # -- Calculate FOs and tight leptons using the cleaned Jets, and sort by conePt
    lepsf = []; lepsfv = []
    ret, lepsf, lepsfv = self.fillCollWithVeto(
      ret           = ret, 
      refcollection = leps,
      leps          = lepsl,
      lab           = 'F',
      labext        = 'FO',
      selection     = self.FOLeptonSel,
      lepsforveto   = lepsl, 
      ht            = 1, 
      sortby        = lambda x: x.conept, 
      doVetoZ       = self.doVetoZ, 
      doVetoLM      = self.doVetoLMf, 
      extraTag      = leplabel
    )
    
    
    lepst = []; lepstv = []
    ret, lepst, lepstv = self.fillCollWithVeto(
      ret           = ret, 
      refcollection = leps,
      leps          = lepsl,
      lab           = 'T',
      labext        = 'Tight',
      selection     = self.tightLeptonSel,
      lepsforveto   = lepsl, 
      ht            = 1, 
      sortby        = lambda x: x.conept, 
      doVetoZ       = self.doVetoZ, 
      doVetoLM      = self.doVetoLMt, 
      extraTag      = leplabel
    )
    

    if self.verbosity > 0:
      color_msg("  * Tight leptons", "yellow")
      print("   - ", lepst)
      print("   - ", [lep.pdgId for lep in lepst], "PDGID")
      print("   - ", [lep.mvaTTH_run3 for lep in lepst], "PDGID")

    

    return ret, leps
  
  def analyze(self, event):
    ''' Method called at runtime by the PostProcesssor '''
    
    if self.verbosity > 0:
      color_msg("   ---- Analyzing event %d"%(event.event), "green")
      
    self.fullret = {}                # Container for variables
    self.create_nominal_colls(event) # Save nominal objects in lists

   
    isData = (event.datatag != 0) 
    if isData:
      self.systsJEC      = []
            
    # -- Create lepton collections for nominal + each systVariation of the leptons
    iterations = [""] + self.systsLepScale 
    for lepvar in iterations:
      leplabel = "_%s"%lepvar if lepvar != "" else lepvar
      doClean = (lepvar == "") # If true, clean jets with leptons
      ret, leps = self.create_leptons(doClean = doClean, lepvar = lepvar)
      
      # -- Attach labels and return
      self.fullret["nLepGood%s"%leplabel]       = len(leps)
      self.fullret["LepGood_conePt%s"%leplabel] = [lep.conept for lep in leps]
      for k, v in ret.items():
        self.fullret["%s%s"%(k, self.label)] = v

    # -- Save also some variables computed during the cleaning        
    self.fullret.update(self.retwlabel)
    if self.verbosity > 0:
      color_msg("      o Selected these jets:", "green")
    for k, v in self.jetret.items():
      if self.verbosity > 0:
        print("         > ", k, v) 
      self.fullret["JetSel%s_%s"%(self.label, k)] = v

    print("Loose: ", self.fullret["nBJetLoose"+self.strJetPt+"_Mini"])
    print("Medium: ", self.fullret["nBJetMedium"+self.strJetPt+"_Mini"])

    ### Write the output
    writeOutput(self, self.fullret)
    return True   

def bestZ1TL(lepsl,lepst,cut=lambda lep:True):
    pairs = []
    for l1 in lepst:
      if not cut(l1): continue
      for l2 in lepsl:
          if not cut(l2): continue
          if l1.pdgId == -l2.pdgId:
             mz = (l1.p4() + l2.p4()).M()
             diff = abs(mz-91)
             pairs.append( (diff,mz) )
    if len(pairs):
        pairs.sort()
        return pairs[0][1]
    return 0.


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
    
    # --- b tagging working points from 2018
    looseDeepFlavB = 0.0494
    mediumDeepFlavB = 0.2770
    looselep = lambda lep          : _loose_lepton(lep, looseDeepFlavB, mediumDeepFlavB)
    cleanlep = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
    folep    = lambda lep, jetlist :    _fO_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)
    tightlep = lambda lep, jetlist : _tight_lepton(lep, looseDeepFlavB, mediumDeepFlavB, jetlist)


    mainpath = "/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc/2022EE/"
    process = "TTto2L2Nu_part1"
#    process = "TTTo2L2Nu_part17"
    
    friends = [
      "jmeCorrections",
      "lepmva"
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
    module_test =  LeptonJetRecleanerWZSM(
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
    systsJEC = [],
    systsLepScale = [],
    # These are used for EWKino as well
    doVetoZ   = False,
    doVetoLMf = False,
    doVetoLMt = True,
    # ------------------------------------- #
    year  = "2022EE",
    btag_wps = btag_wps,
    bAlgo = "btagDeepFlavB",
    verbosity = 1
    )
    module_test.beginJob()
    (nall, npass, timeLoop) = eventLoop([module_test], file_, outFile, tree, outTree, maxEvents = nentries)
    print(('Processed %d preselected entries from %s (%s entries). Finally selected %d entries' % (nall, __file__.split("/")[-1].replace(".py", ""), nentries, npass)))
    outTree.write()
    file_.Close()
    outFile.Close()
    print("Test done")
    module_test.endJob()
      
