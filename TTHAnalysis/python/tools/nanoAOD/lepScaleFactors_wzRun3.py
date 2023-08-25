from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from copy import deepcopy
import math
import ROOT as r
import os

# -- Define where to extrac the SFs from
files = {
  # ----- MVATTH 2022
  "muon"     : {
    "IDTight"  : {"file" : "Muon_SFS_balvarez_{year}",
                  "hist" : "EGamma_SF2D",
                  "unc"  : ["unc"]}},
  "electron" : {
    "IDTight"  : {"file" : "Electron_SFS_balvarez_{year}", 
                  "hist" : "EGamma_SF2D",
                  "unc"  : ["unc"]}},
  }
  # ----- Cutbased 2018
  #"muon"     : {
  #  "IDTight"  : {"file" : "Efficiencies_muon_generalTracks_Z_Run{year}_UL_ID",
  #                "hist" : "NUM_TightID_DEN_TrackerMuons_abseta_pt",
  #                "unc"  : ["stat", "syst"]},
  #  "ISOTight" : {"file" : "Efficiencies_muon_generalTracks_Z_Run{year}_UL_ISO",
  #                "hist" : "NUM_TightRelIso_DEN_TightIDandIPCut_abseta_pt",
  #                "unc"  : ["stat", "syst"]}
  #  },
  #"electron" : {
  #  "IDTight"  : {"file" : "Electron_{year}UL_IDTight", 
  #                "hist" : "EGamma_SF2D",
  #                "unc"  : ["unc"]},
  #  "RECOTight": {"file" : "Electron_{year}UL_RECO", 
  #                "hist" : "EGamma_SF2D",
  #                "unc"  : ["unc"]}
  #}
  
    
class lepScaleFactors_wzrun3(Module):   
  # ============ MAIN METHODS =============== #
  def __init__(self, year_, lepenvars = [], keepOutput = 1, summary = False):
    self.basepath  = os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/data/WZRun3")
    self.lepsfpath = os.path.join( self.basepath, "lepton" )
    self.keepOutput = keepOutput
    self.files = files
    self.year = year_
    # Containers
    self.leptonSF     = {"muon" : {}, "electron" : {} }    
    # For systematics on the lepton energy corrections
    self.systsLepEn = {}
    if len(lepenvars):
      for i, var in enumerate(lepenvars):
        self.systsLepEn[i+1]    = "%sUp"%var
        self.systsLepEn[-(i+1)] = "%sDown"%var
        
    # Now load required histograms
    self.load_histograms()
    
    #print("[lepScaleFactors_wzRun3::constructor] - Finished loading histograms")
    if summary: self.printSummary() 
    return 
  
  def create_dict(self):
    # -- Create ones to accomodate SFs
    # This could be vastly improved with numpy arrays!
    self.sfs = {}
    for flav in ["muon", "electron"]:
      name = "%sSF"%flav
      self.sfs[name]           = 1
      self.sfs[name + "_Up"]   = 1 
      self.sfs[name + "_Down"] = 1 
      for delta,sys in self.systsLepEn.items():
          self.sfs[name  + "_%s"%sys] = 1
          self.sfs[name  + "_%s"%sys] = 1
      
      for typesf in self.files[flav]:
        self.sfs[name + "_%s"%typesf] = 1
        self.sfs[name + "_%sUp"%typesf] = 1
        self.sfs[name + "_%sDown"%typesf] = 1

        for unc in self.files[flav][typesf]["unc"]:
          self.sfs[name + "_%s_%s"%(typesf, unc)] = 1
          self.sfs[name + "_%s_%sUp"%(typesf, unc)] = 1
          self.sfs[name + "_%s_%sDown"%(typesf, unc)] = 1 
    return
  
  def analyze(self, event):
    year = self.year  
    self.create_dict()
    # -- Get the collection of leptons and analyze the topology (i.e. how many leptons are in the event)
    leps = [l for l in Collection(event, "LepGood")]    
    nleps = len(leps)
    
    self.event = event
 #   print((" ---- Event: %d"%event.event))
    self.nmuons = 0
    self.nelectrons = 0
    for ilep, lep in enumerate(leps):
      lep_pt  = lep.pt
      lep_eta = lep.eta
      lep_pdg = abs(lep.pdgId)
      
      if lep_pdg == 13: # Muon
        sf = self.getLepSF(lep_pt, lep_eta, "muon")
        self.nmuons += 1
      elif lep_pdg == 11: # Electron
        sf = self.getLepSF(lep_pt, lep_eta, "electron")
        self.nelectrons += 1
      else: # who knows
        raise RuntimeError("[lepScaleFactors_wzRun3::analyze]: Wrong pdgId %d"%pdgId)
      
      if ilep > 4:
        self.write_output() 
        return True # Stop beyond the fourth lepton
      
    self.write_output()  
    return True
  
  def write_output(self):
    #print("event: %s"%self.event.event)
    #print("nelectrons: %d"%self.nelectrons)
    #print("nmuons: %d"%self.nmuons)
    for sfname, sf in self.sfs.items():
 #     if sfname == "muonSF" or sfname == "electronSF":
 #       print(("\t>> Writing %s SF which has a value of %s (Up: %s, Dn: %s)"%(sfname, sf, self.sfs[sfname+"_Up"], self.sfs[sfname+"_Down"] )))
      self.out.fillBranch(sfname, sf)        
    return
  
  
  def getLepSF(self,  pt, eta, flav):
    ''' Function to get all the SFs for a given lepton '''
    name = "%sSF"%flav
    # -- Iterate over all the types of SF considered
    tot_sf  = 1
    variation_totsf = 0
    for typesf in self.leptonSF[flav]:
      h_nom = self.leptonSF[flav][typesf]["nominal"]
      typesf_val = self.getFromHisto(pt, abs(eta), h_nom)
      tot_var = 0
      self.sfs[name + "_%s"%typesf] *= typesf_val
      # -- Propagate to the global sf
      tot_sf *= typesf_val
      for unc in self.leptonSF[flav][typesf]:
        if unc == "nominal" : continue # Already used in the previous for
        uncname = "_%s"%unc
        # -- Get the histogram for the uncertainty and get the error
        if unc != "unc":
          h_unc     = self.leptonSF[flav][typesf][unc]
        else:
          h_unc = self.leptonSF[flav][typesf]["nominal"]
        variation = self.getFromHisto( pt, abs(eta), h_unc, err=True )  
        self.sfs[name + "_%s"%typesf + uncname + "Up"]   *= typesf_val*(1 + variation)
        self.sfs[name + "_%s"%typesf + uncname + "Down"] *= typesf_val*(1 - variation)
        #self.sfs[name + "_%s"%typesf + uncname + "Up"]   *= typesf_val+variation
        #self.sfs[name + "_%s"%typesf + uncname + "Down"] *= typesf_val-variation
        

        
        # -- Propagate to the entire systematic
        tot_var += variation*variation
      
      # -- Consider Extrapolation to top-like from DY-like phase space 
      #    (CMS-AN-"2018"-210) ---> Only for muons!
      if flav == "muon":
        tot_var += (tot_var*0.005)**2
        
      variation_totsf += tot_var 
      # Now compute the variations 
      #self.sfs[name + "_%sUp"%typesf]   *= typesf_val+ math.sqrt(tot_var)
      #self.sfs[name + "_%sDown"%typesf] *= typesf_val- math.sqrt(tot_var)
      self.sfs[name + "_%sUp"%typesf]   *= typesf_val*(1 + math.sqrt(tot_var))
      self.sfs[name + "_%sDown"%typesf] *= typesf_val*(1 - math.sqrt(tot_var))

    # Finally compute the overall sf + variations
    self.sfs[name]           *= tot_sf
    self.sfs[name + "_Up"]   *= tot_sf*(1 + math.sqrt(variation_totsf))
    self.sfs[name + "_Down"] *= tot_sf*(1 - math.sqrt(variation_totsf))
   # print(("%s total var: %s"%(flav, math.sqrt(variation_totsf))))
   # self.sfs[name + "_Up"]   *= tot_sf+math.sqrt(variation_totsf)
   # self.sfs[name + "_Down"] *= tot_sf-math.sqrt(variation_totsf)         
    return
  
  def getFromHisto(self, pt, eta, histo, err = False):
        #### NOTE: this method obtains the information for a given pt and eta. 
        normal = True # normal := {x: pt, y: eta}
        if (histo.GetXaxis().GetBinUpEdge(histo.GetNbinsX())) < 10: normal = False

        tmpeta = eta

        if    ((normal     and histo.GetYaxis().GetBinLowEdge(1) >= 0)
            or (not normal and histo.GetXaxis().GetBinLowEdge(1) >= 0)):
            tmpeta = abs(tmpeta)

        if normal:
            xbin = max(1, min(histo.GetNbinsX(), histo.GetXaxis().FindBin(pt)))
            ybin = max(1, min(histo.GetNbinsY(), histo.GetYaxis().FindBin(tmpeta)))
        else:
            xbin = max(1, min(histo.GetNbinsX(), histo.GetXaxis().FindBin(tmpeta)))
            ybin = max(1, min(histo.GetNbinsY(), histo.GetYaxis().FindBin(pt)))

        if err: return histo.GetBinError(xbin, ybin)
        else:   return histo.GetBinContent(xbin, ybin)
        return

  # ============ LOADING METHODS =============== #
  def load_histograms(self):
    ''' Method to load histograms for muon and electron SFs'''
    for flav in ["muon", "electron"]:
      for type_ in self.files[flav]:
        self.leptonSF[flav][type_] = self.load_histo(self.files[flav][type_])          
    return
  
  def load_histo(self, info):
    ''' Method to load histograms '''
    fil      = os.path.join( self.lepsfpath, info["file"].format(year = self.year) + ".root" )
    histname = info["hist"]
    uncs     = info["unc"]
    ret = {}
    
    # -- Open file
    tf = r.TFile.Open( fil )
    if not tf: 
      raise RuntimeError("[lepScaleFactors_wzRun3::loadHisto] FATAL: no such file %s"%fil)
    
    histnom = tf.Get(histname)
    # -- Get the histogram
    if not histnom: 
      raise RuntimeError("[lepScaleFactors_wzRun3::loadHistoWithVars] FATAL: no such object %s in %s"%(hist,fil))
    ret["nominal"] = deepcopy(histnom)
    
    # -- Get the uncertainty histos otherwise
    for var in uncs:
      tmphist = tf.Get(histname + "_%s"%var)
      ret[var] = deepcopy(tmphist)
      
    # -- Finally, close the file and return
    tf.Close()
    return ret 
  
  # ============ AUXILIAR METHODS =============== #
  def printSummary(self):
    print(" [lepScaleFactors_wzRun3::summary] --- SUMMARY ")
    for flav in ["muon", "electron"]:
      print((" -- %s scale factors:"%flav))
      for typesf in self.files[flav]:
        histo = self.files[flav][typesf]["hist"]
        print(("   >> Type: %s \n\t* file: %s"%(typesf, self.files[flav][typesf]["file"].format(year = self.year))))
        print(("\t* nominal histo:  %s"%histo))   
        for unc in self.files[flav][typesf]["unc"]:
          print(("\t* %s unc histo: %s"%(unc, histo+"_%s"%unc )))   
    return
  
  def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
    self.out = wrappedOutputTree    
    # -- This is the global SF
    self.out.branch("LEPSF", 'F')
    # -- Separated in flavor
    for lep in ["muon", "electron"]:
      self.out.branch("%sSF"%lep,      'F')
      self.out.branch("%sSF_Up"%lep,   'F')
      self.out.branch("%sSF_Down"%lep, 'F')
      
      # -- Separated on type of SF 
      for typesf in self.files[lep]:
        self.out.branch("%sSF_%s"%(lep, typesf), 'F')
        self.out.branch("%sSF_%sUp"%(lep, typesf), 'F')
        self.out.branch("%sSF_%sDown"%(lep, typesf), 'F')          
        # -- Splitted in UNC source
        for unctype in self.files[lep][typesf]["unc"]:
          self.out.branch("%sSF_%s_%s"%(lep, typesf, unctype), 'F')
          self.out.branch("%sSF_%s_%sUp"%(lep, typesf, unctype), 'F') 
          self.out.branch("%sSF_%s_%sDown"%(lep, typesf, unctype), 'F') 
                    
        # -- Now for the lepton energy variatons 
        for delta,sys in self.systsLepEn.items():
          self.out.branch('%sSF_%s_'  + sys, 'F')
          self.out.branch('%sSF_%s_'  + sys, 'F')
      
    return
  
