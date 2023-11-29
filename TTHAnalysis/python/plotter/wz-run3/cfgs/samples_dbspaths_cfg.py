

dbs_data = {
    # Era C
    "JetMET_Run2022C" : { "dbs": "/JetMET/Run2022C-22Sep2023-v1/NANOAOD"},
    "EGamma_Run2022C" : { "dbs": "/EGamma/Run2022C-22Sep2023-v1/NANOAOD"},
    "MuonEG_Run2022C" : { "dbs": "/MuonEG/Run2022C-22Sep2023-v1/NANOAOD"},
    "Muon_Run2022C"   : { "dbs": "/Muon/Run2022C-22Sep2023-v1/NANOAOD"},
    # Era D
    "JetMET_Run2022D" : { "dbs": "/JetMET/Run2022D-22Sep2023-v1/NANOAOD"},
    "EGamma_Run2022D" : { "dbs": "/EGamma/Run2022D-22Sep2023-v1/NANOAOD"},
    "MuonEG_Run2022D" : { "dbs": "/MuonEG/Run2022D-22Sep2023-v1/NANOAOD"},
    "Muon_Run2022D"   : { "dbs": "/Muon/Run2022D-22Sep2023-v1/NANOAOD"},
    # Era E
    "JetMET_Run2022E" : { "dbs": "/JetMET/Run2022E-22Sep2023-v1/NANOAOD"},
    "EGamma_Run2022E" : { "dbs": "/EGamma/Run2022E-22Sep2023-v1/NANOAOD"},
    "MuonEG_Run2022E" : { "dbs": "/MuonEG/Run2022E-22Sep2023-v1/NANOAOD"},
    "Muon_Run2022E"   : { "dbs": "/Muon/Run2022E-22Sep2023-v1/NANOAOD"},
    # Era F
    "JetMET_Run2022F" : { "dbs": "/JetMET/Run2022F-22Sep2023-v1/NANOAOD"},
    "EGamma_Run2022F" : { "dbs": "/EGamma/Run2022F-22Sep2023-v1/NANOAOD"},
    "MuonEG_Run2022F" : { "dbs": "/MuonEG/Run2022F-22Sep2023-v1/NANOAOD"},
    "Muon_Run2022F"   : { "dbs": "/Muon/Run2022F-22Sep2023-v1/NANOAOD"},
    # Era G
    "JetMET_Run2022G" : { "dbs": "/JetMET/Run2022G-22Sep2023-v1/NANOAOD"},
    "EGamma_Run2022G" : { "dbs": "/EGamma/Run2022G-22Sep2023-v1/NANOAOD"},
    "MuonEG_Run2022G" : { "dbs": "/MuonEG/Run2022G-22Sep2023-v1/NANOAOD"},
    "Muon_Run2022G"   : { "dbs": "/Muon/Run2022G-22Sep2023-v1/NANOAOD"},
}

dbs_mc = {
    # Signal
    'WZto3LNu': {'dbs': '/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 5.31}, 
    
    # Prompts
    'ZZto4L': {'dbs': '/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 1.65}, 
    'TTG_1Jets_PTG_100to200': {'dbs': '/TTG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTG_1Jets_PTG_200': {'dbs': '/TTG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/', 'xsec': 1}, # Revisit XSEC 
    'TTG_1Jets_PTG_10to100': {'dbs': '/TTG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTHtoNon2B_M_125': {'dbs': '/TTHtoNon2B_M-125_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTLL_MLL_50': {'dbs': '/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 0.08646}, 
    'TTLL_MLL_4to50': {'dbs': '/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 0.03949}, 
    'TTLNu_1Jets': {'dbs': '/TTLNu-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TZQB_4FS_OnshellZ': {'dbs': '/TZQB-4FS_OnshellZ_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 1}, # Revisit XSEC 
    'WZZ': {'dbs': '/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 0.06206}, 
    'WWW_4F': {'dbs': '/WWW_4F_TuneCP5_13p6TeV_amcatnlo-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    'WWZ_4F': {'dbs': '/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 0.18510}, 
    'ZZZ': {'dbs': '/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 0.01591}, 
    'TTWW': {'dbs': '/TTWW_TuneCP5_13p6TeV_madgraph-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTWH': {'dbs': '/TTWH_TuneCP5_13p6TeV_madgraph-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTTT': {'dbs': '/TTTT_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTHH': {'dbs': '/TTHH_TuneCP5_13p6TeV_madgraph-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTWZ': {'dbs': '/TTWZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    'TTZZ': {'dbs': '/TTZZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8/', 'xsec': 1}, # Revisit XSEC
    
    # TOP Fakes
    'TTto2L2Nu': {'dbs': '/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 97.4488},
    'TTtoLNu2Q' : {'dbs' : '/TTtoLNu2Q_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec':403.25},
 
    'TbarWplusto2L2Nu': {'dbs': '/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 23.8979}, 
    'TWminusto2L2Nu': {'dbs': '/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 23.8979}, 
    'TTZ_ZtoQQ_1Jets': {'dbs': '/TTZ-ZtoQQ-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 1}, # Revisit XSEC

    # Ewk fakes
    'WZto2L2Q': {'dbs': '/WZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 1}, # Revisit XSEC
    'WWto2L2Nu': {'dbs': '/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 12.98}, 
    'ZZto2L2Nu': {'dbs': '/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 1.19}, 
    'ZZto2L2Q': {'dbs': '/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/', 'xsec': 8.08},
    'DYto2L_2Jets_MLL_50': {'dbs': '/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 6345.99},
    'DYto2L_2Jets_MLL_10to50': {'dbs': '/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 19982.5}, 
    'WtoLNu_2Jets': {'dbs': '/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 64481.58}, 

    # Conversions
    'WGtoLNuG_PTG_10to100': {'dbs': '/WGtoLNuG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 1}, # Revisit XSEC
    'ZGto2LG': {'dbs': '/ZGto2LG_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 1}, # Revisit XSEC
    'WZGtoLNuZG': {'dbs': '/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8/', 'xsec': 1}, # Revisit XSEC
    'WGtoLNuG_PTG_100to200': {'dbs': '/WGtoLNuG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 1}, # Revisit XSEC
    'WGtoLNuG_PTG_200': {'dbs': '/WGtoLNuG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/', 'xsec': 1}, # Revisit XSEC
    
    # QCD no skim
    # EM enriched
    'QCD_PT_10to30_EMEnriched': {'dbs': '/QCD_PT-10to30_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT_30to50_EMEnriched': {'dbs': '/QCD_PT-30to50_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT_50to80_EMEnriched': {'dbs': '/QCD_PT-50to80_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT_80to120_EMEnriched': {'dbs': '/QCD_PT-80to120_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT_120to170_EMEnriched': {'dbs': '/QCD_PT-120to170_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT-170to300_EMEnriched': {'dbs': '/QCD_PT-170to300_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT_300_EMEnriched': {'dbs': '/QCD_PT-300_EMEnriched_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC


    # MU enriched
    "QCD_PT-15to20_MuEnrichedPt5" : {'dbs' : "/QCD_PT-15to20_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-20to30_MuEnrichedPt5" : {'dbs' : "/QCD_PT-20to30_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-30to50_MuEnrichedPt5" : {'dbs' : "/QCD_PT-30to50_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-50to80_MuEnrichedPt5" : {'dbs' : "/QCD_PT-50to80_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-80to120_MuEnrichedPt5" : {'dbs' : "/QCD_PT-80to120_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-120to170_MuEnrichedPt5" : {'dbs' : "/QCD_PT-120to170_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-170to300_MuEnrichedPt5" : {'dbs' : "/QCD_PT-170to300_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-300to470_MuEnrichedPt5" : {'dbs' : "/QCD_PT-300to470_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-470to600_MuEnrichedPt5" : {'dbs' : "/QCD_PT-470to600_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-600to800_MuEnrichedPt5" : {'dbs' : "/QCD_PT-600to800_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-800to1000_MuEnrichedPt5" : {'dbs' : "/QCD_PT-800to1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
    "QCD_PT-1000_MuEnrichedPt5" : {'dbs' : "/QCD_PT-1000_MuEnrichedPt5_TuneCP5_13p6TeV_pythia8/", 'xsec' : 1}, # Revisit XSEC
  
    
    # bcToE enriched
    'QCD_PT-20to30_bcToE': {'dbs': '/QCD_PT-20to30_bcToE_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT-30to80_bcToE': {'dbs': '/QCD_PT-30to80_bcToE_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT-80to170_bcToE': {'dbs': '/QCD_PT-80to170_bcToE_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT-170to250_bcToE': {'dbs': '/QCD_PT-170to250_bcToE_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
    'QCD_PT-250_bcToE': {'dbs': '/QCD_PT-250_bcToE_TuneCP5_13p6TeV_pythia8/', 'xsec': 1}, # Revisit XSEC
}
