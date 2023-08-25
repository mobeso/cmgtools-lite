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
               bAlgo="DeepCSV"):

    # --- Constructor --- #
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

    # * Control verbosity 
    self.debugprinted = False

    # * Other stuff
    self.storeJetVariables = storeJetVariables
    self.year = year
    self.bAlgo = bAlgo
    
    # List the branches that will be written to declare the output
    self.listBranches()

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
        comesfromZ  = (not doVetoZ  or passMllTLVeto(lep, lepsforveto, 76, 106, True))
        comesfromLM = (not doVetoLM or passMllTLVeto(lep, lepsforveto,  0,  12, True))
        if comesfromLM and comesfromZ:
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

  def recleanJets(self, jetcollcleaned, jetcolldiscarded, lepcoll, postfix, ret, jetret, discjetret):
    ## Define jets
    ret["iJSel"+postfix]     = [] 
    ret["iDiscJSel"+postfix] = []

    # 0. mark each jet as clean
    for j in jetcollcleaned+jetcolldiscarded: 
      j._clean = True
      if getattr(j,  "idx_veto") != -1:
        j._clean = False # Already discard the jet if it's in the veto region of the HCAL

    # 1. associate to each lepton passing the cleaning selection its nearest jet 
    for lep in lepcoll:
        best = None; bestdr = 0.4
        for j in jetcollcleaned+jetcolldiscarded:
            dr = deltaR(lep, j)
            if dr < bestdr:
                best = j; bestdr = dr
        if best is not None and self.cleanJet(lep, best, bestdr):
            best._clean = False

    # 2. compute the jet list
    for ijc, j in enumerate(jetcollcleaned):
        if not self.selectJet(j): 
          continue
        elif not j._clean: 
          ret["iDiscJSel"+postfix].append(ijc)
        else: 
          ret["iJSel"+postfix].append(ijc)

    for ijd,j in enumerate(jetcolldiscarded):
        if not self.selectJet(j): 
          continue
        elif not j._clean: 
          ret["iDiscJSel"+postfix].append(-1-ijd)
        else: 
          ret["iJSel"+postfix].append(-1-ijd)

    # 3. sort the jets by pt
    ret["iJSel"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else jetcolldiscarded[-1-idx].pt, reverse = True)
    ret["iDiscJSel"+postfix].sort(key = lambda idx : jetcollcleaned[idx].pt if idx >= 0 else jetcolldiscarded[-1-idx].pt, reverse = True)
    ret["nJetSel"+postfix] = len(ret["iJSel"+postfix])
    ret["nDiscJetSel"+postfix] = len(ret["iDiscJSel"+postfix])

    # 4. if needed, store the jet 4-vectors
    if self.storeJetVariables:
        if postfix==self.label:
            for jfloat in "pt eta phi mass btagDeepB".split():
                jetret[jfloat] = []
                discjetret[jfloat] = []
            for idx in ret["iJSel"+postfix]:
                jet = jetcollcleaned[idx] if idx >= 0 else jetcolldiscarded[-1-idx]
                for jfloat in "pt eta phi mass btagDeepB".split():
                    jetret[jfloat].append( getattr(jet,jfloat) )
            for idx in ret["iDiscJSel"+postfix]:
                jet = jetcollcleaned[idx] if idx >= 0 else jetcolldiscarded[-1-idx]
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
    alljets = jetcollcleaned + jetcolldiscarded
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
        if j.pt > float(self.bJetPt):
            if self.year == 2022 and self.bAlgo == "DeepCSV":
                ret["nJet"+self.strBJetPt+postfix] += 1
                ret["htJet"+self.strBJetPt+"j"+postfix] += j.pt 
                if j.btagDeepB>0.0490: ret["nBJetLoose"+self.strBJetPt+postfix]  += 1
                if j.btagDeepB>0.6321: ret["nBJetMedium"+self.strBJetPt+postfix] += 1
                if j.btagDeepB>0.8953: ret["nBJetTight"+self.strBJetPt+postfix]  += 1
                mhtBJetPtvec = mhtBJetPtvec - j.p4()
            if self.year == 2022 and self.bAlgo == "DeepJet":
                ret["nJet"+self.strBJetPt+postfix] += 1
                ret["htJet"+self.strBJetPt+"j"+postfix] += j.pt 
                if j.btagDeepFlavB>0.0614: ret["nBJetLoose"+self.strBJetPt+postfix]  += 1
                if j.btagDeepFlavB>0.2783: ret["nBJetMedium"+self.strBJetPt+postfix] += 1
                if j.btagDeepFlavB>0.7100: ret["nBJetTight"+self.strBJetPt+postfix]  += 1
                mhtBJetPtvec = mhtBJetPtvec - j.p4()

        if j.pt > float(self.jetPt):
            if self.year == 2022 and self.bAlgo == "DeepCSV":
                ret["nJet"+self.strJetPt+postfix] += 1
                ret["htJet"+self.strJetPt+"j"+postfix] += j.pt
                if j.btagDeepB>0.2217: ret["nBJetLoose"+self.strJetPt+postfix]  += 1
                if j.btagDeepB>0.6321: ret["nBJetMedium"+self.strJetPt+postfix] += 1
                if j.btagDeepB>0.8953: ret["nBJetTight"+self.strJetPt+postfix]  += 1
                mhtBJetPtvec = mhtBJetPtvec - j.p4()
            if self.year == 2022 and self.bAlgo == "DeepJet":
                ret["nJet"+self.strJetPt+postfix] += 1; ret["htJet"+self.strJetPt+"j"+postfix] += j.pt; 
                if j.btagDeepFlavB>0.0490: ret["nBJetLoose"+self.strJetPt+postfix]  += 1
                if j.btagDeepFlavB>0.2783: ret["nBJetMedium"+self.strJetPt+postfix] += 1
                if j.btagDeepFlavB>0.7100: ret["nBJetTight"+self.strJetPt+postfix]  += 1
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
      for j in self.nominal_jetsc:
        jcopy = copy(j)
        #print(" -- nominal pt: %3f"%j.pt)
        setattr(jcopy, "pt", getattr(jcopy, "pt%s"%jecvar))
        #print(" -- variated pt: %3f "%jcopy.pt)
        #print(" ------- ")
        jetsc.append(jcopy)
      #print("===========")
      jetsd = []
      
      # Now do the cleaning with the variated jet
      cleanjets[jecvar] = self.recleanJets(
        jetcollcleaned   = jetsc,
        jetcolldiscarded = jetsd,
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
    # Use a copy of the nominal leptons
    leplabel = "_%s"%lepvar if lepvar else ""
    ret  = {}
    leps = [copy(l) for l in self.nominal_leps]
    
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
    
    # -- Compute lepton pair masses
    ret['mZ1%s'%leplabel]        = bestZ1TL(lepsl, lepsl)
    ret['minMllAFAS%s'%leplabel] = minMllTL(lepsl, lepsl)
    ret['minMllAFOS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge !=  l2.charge)
    ret['minMllAFSS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.charge ==  l2.charge)
    ret['minMllSFOS%s'%leplabel] = minMllTL(lepsl, lepsl, paircut = lambda l1,l2 : l1.pdgId  == -l2.pdgId)
    
    # Do the cleaning if needed 
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
      ht            =1, 
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
      doVetoLM      = self.doVetoLMf, 
      extraTag      = leplabel
    )
    return ret, leps
  
  def analyze(self, event):
    ''' Method called at runtime by the PostProcesssor '''
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
    for k, v in self.jetret.items():
      self.fullret["JetSel%s_%s"%(self.label, k)] = v
          
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


if  __name__ == '__main__':
  pass        
