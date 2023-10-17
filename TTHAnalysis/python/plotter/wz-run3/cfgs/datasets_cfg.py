import os, re, sys
from cfgs.samplepaths import samplepaths as paths
from cfgs.xsecs_cfg import xsecs

# Add some other functions useful for debugging
sys.path.append( os.path.join( os.environ["CMSSW_BASE"], "src/CMGTools/TTHAnalysis/python/plotter/wz-run3/"))
from functions import color_msg


class dataset:
    """ Objects from this class inherit different useful metadata for a given dataset """
    def __init__(self, 
            name, 
            dbspath = None, 
            isData = False, 
            regex = "", 
            xsec = -1, 
            year = "2022EE", 
            label = "", 
            fC = ""):
                
        # dataset metadata
        self.name = name
        self.dbspath = dbspath
        self.isData = isData
        self.regex = regex
        self.xsec = xsec
        self.year = year
        self.label = label
        self.fC = fC
        
        # Logistics
        self.type_ = "data" if isData else "mc" 
        yearstr = "2022PostEE" if year == "2022EE" else "2022" 
        
        # This is where the nanoAOD is stored
        
        # How data is placed in the filesystem is very annoying, because
        # it follows a different scheme as in MC. Hence we have to do it
        # in different ways...
        if not self.isData:
            self.raw_nano = os.path.join(paths["nanoaod"][self.type_], yearstr)
        else:
            datasetname = re.match("(.*)_Run.*", name).groups()[0]
            self.raw_nano = os.path.join(paths["nanoaod"][self.type_], yearstr, datasetname)

        return
    
    def get_pure_nanoaod(self):
        """ 
        This function finds a match to a local directory and provides the raw nanoAOD files
        in a list. 
        """
        
        # Get a list of all the folders inside the raw nanoAOD folder
        dataset_paths = os.listdir(self.raw_nano)
        match = re.compile(self.regex)
        process_path = list(filter(match.match, dataset_paths))     
        
        if len(process_path) > 1:
            color_msg(">> Whops. Two folders matched the same regexp, please use another one which is not ambiguous", "red")
            print("  - Folders: ", process_path)
            sys.exit(0)
            
        # Ideally there will be just one matched folder
        process_path = os.path.join(self.raw_nano, process_path[0])
        
        # Now get the full path where the raw nanoAOD files are stored
        nanofiles = []

        for root, dirs, files in os.walk( process_path ):      
            # -- First find the folders with rootfiles only
            are_there_rfiles = any([".root" in f for f in files])

            if not are_there_rfiles: continue
            nanofiles.append(root)

        return nanofiles, process_path
    
    def get_processed_files(self):
        """
        This function returns the name that the sample has after postprocessing it
        """
        inpath = os.path.join(paths["processed"], "data" if self.isData else "mc", self.year)
        files = list(filter(lambda element: self.name in element, os.listdir(inpath)))
        files = [file_.replace(".root", "") for file_ in files]
        return files

# There will be one dataset file for each entry in this dictionary
datasets = {
    "data" : {
        "data" : {
            "Egamma" : [
                dataset("EGamma_Run2022F", 
                    dbspath = "/EGamma/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD", 
                    isData = True,
                    regex = ".*EGamma_Run2022F.*"),
                dataset("EGamma_Run2022G",
                    dbspath = "/EGamma/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD", 
                    isData = True,
                    regex = ".*EGamma_Run2022G.*")
                ],
            "Muon" : [
                dataset("Muon_Run2022F",
                    dbspath = "/Muon/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",  
                    isData = True,
                    regex = ".*Muon_Run2022F.*"),
                dataset("Muon_Run2022G", 
                    dbspath = "/Muon/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                    isData = True,
                    regex = ".*Muon_Run2022G.*")
                ],
            "MuonEG" : [
                dataset("MuonEG_Run2022F",
                    dbspath = "/MuonEG/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD", 
                    isData = True,
                    regex = ".*MuonEG_Run2022F.*"),
                dataset("MuonEG_Run2022G", 
                    dbspath = "/MuonEG/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                    isData = True,
                    regex = ".*MuonEG_Run2022G.*")
                ],
            "JetMET" : [
                dataset("JetMET_Run2022F",
                    dbspath = "/JetMET/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD", 
                    isData = True,
                    regex = ".*JetMET_Run2022F.*"),
                dataset("JetMET_Run2022G", 
                    dbspath = "/JetMET/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                    isData = True,
                    regex = ".*JetMET_Run2022G.*")
                ]}
    },
    "mc" : {
        # + Prompts
        "signal" : {
            "prompt_WZ" : [ 
                    dataset("WZto3LNu", 
                            dbspath = "/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM", 
                            isData = False,
                            regex = ".*WZto3LNu.*",
                            xsec = xsecs["WZto3LNu"],
                            label = "WZ",
                            fC = "kOrange")],
        },
        "prompts" : {
            "prompt_ZZ" : [ 
                dataset("ZZto4l",
                    dbspath = "/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM",  
                    isData = False,
                    regex = ".*ZZto4L_Tune.*",
                    xsec = xsecs["ZZto4L"],
                    label = "ZZ",
                    fC = "kGreen+1")],
            "prompt_VVV" : [
                dataset("WWZ", 
                    dbspath = "/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*WWZ.*",
                    xsec = xsecs["WWZ"],
                    label = "VVV",
                    fC = "kRed+1"),
                dataset("WZZ",
                    dbspath = "/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*WZZ.*",
                    xsec = xsecs["WZZ"],
                    label = "VVV",
                    fC = "kRed+1"),
                dataset("ZZZ", 
                    dbspath = "/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*ZZZ.*",
                    xsec = xsecs["ZZZ"],
                    label = "VVV",
                    fC = "kRed+1")],
            "prompt_hZZ" : [
                dataset("ggHtoZZto4L",
                    dbspath = "/GluGluHtoZZto4L_M-125_TuneCP5_13p6TeV_powheg2-JHUGenV752-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",   
                    isData = False,
                    regex = ".*GluGluHtoZZto4L.*",
                    xsec = xsecs["ggHtoZZto4L"],
                    label = "hZZ",
                    fC = "kGreen-1")],
            "prompt_TTX" : [
                dataset("TTLL_MLL_50", 
                    dbspath = "/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/NANOAODSIM",
                    isData = False,
                    regex = ".*TTLL_MLL-50.*",
                    xsec = xsecs["TTLL_MLL-50"],
                    label = "ttX",
                    fC = "kViolet-3"),
                dataset("TTLL_MLL_4to50", 
                   dbspath = "/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/NANOAODSIM",
                   isData = False,
                   regex = ".*TTLL_MLL-4to50.*",
                   xsec = xsecs["TTLL_MLL-4to50"],
                   label = "ttX",
                   fC = "kViolet-3")],
            "prompt_hZZ" : [
                dataset("ggHtoZZto4L",
                    dbspath = "/GluGluHtoZZto4L_M-125_TuneCP5_13p6TeV_powheg2-JHUGenV752-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",   
                    isData = False,
                    regex = ".*GluGluHtoZZto4L.*",
                    xsec = xsecs["ggHtoZZto4L"],
                    label = "hZZ",
                    fC = "kGreen-1")]},
        # + Prompt backgrounds
        "mcfakes" : {
            "fakes_VV" : [
                dataset("ZZto2L2Q",
                    dbspath = "/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM",  
                    isData = False,
                    regex = ".*ZZto2L2Q.*",
                    xsec = xsecs["ZZto2L2Q"],
                    label = "NP VV",
                    fC = "kGray+9"),
                dataset("ZZto2L2Nu",
                    dbspath = "/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v2/NANOAODSIM",  
                    isData = False,
                    regex = ".*ZZto2L2Nu.*",
                    xsec = xsecs["ZZto2L2Nu"],
                    label = "NP VV",
                    fC = "kGray+9"),                    
                dataset("WWto2L2Nu",
                    dbspath = "/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22NanoAODv11-126X_mcRun3_2022_realistic_v2-v2/NANOAODSIM",
                    isData = False,
                    regex = ".*WWto2L2Nu.*",
                    xsec = xsecs["WWto2L2Nu"],
                    label = "NP VV",
                    fC = "kGray+9")],
            "fakes_TT" :  [
                dataset("TTTo2L2Nu",
                    dbspath = "/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex  = ".*TTto2L2Nu_TuneCP5_13p6TeV.*",
                    xsec = xsecs["TTto2L2Nu"],
                    label = "NP TT",
                    fC = "kGray+2")],
            "fakes_DY" : [
                dataset("DYJetsToLL_M50",
                    dbspath = "/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",   
                    isData = False,
                    regex = ".*DYto2L-2Jets_MLL-50",
                    xsec = xsecs["DYJetstoLL_M-50"],
                    label = "NP DY",
                    fC = "kGray"),
                dataset("DYJetsToLL_M10to50",
                    dbspath = "/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*DYto2L-2Jets_MLL-10to50.*",
                    xsec = xsecs["DYJetstoLL_M10to50"],
                    label = "NP DY",
                    fC = "kGray")],
            "fakes_T" : [
                dataset("TWminus",
                    dbspath = "/TWminus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*TWminus_DR.*",
                    xsec = xsecs["TWminus"],
                    label = "NP ST",
                    fC = "kGray-2"),
                dataset("TbarWplus",
                    dbspath = "/TbarWplus_DR_AtLeastOneLepton_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*TbarWplus_DR.*",
                    xsec = xsecs["TbarWplus"],
                    label = "NP ST",
                    fC = "kGray-2")],
            "fakes_V" : [
                    dataset("WtoLnu_2jets",
                        dbspath = "/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",   
                        isData = False,
                        regex = ".*WtoLNu-2Jets.*",
                        xsec = xsecs["WtoLnu_2jets"],
                        label = "Wjets",
                        fC = "kGray-5")]},
        "convs" : {
            "convs" : [
                dataset("WZG",
                    dbspath = "/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                    isData = False,
                    regex = ".*WZG.*",
                    xsec = xsecs["WZG"],
                    label = "Convs.",
                    fC = "kOrange-3")]}
    }
}
