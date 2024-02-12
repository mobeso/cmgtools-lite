#!/bin/env python3
# Config file for Run3 sample postprocessing
# File automatically generated by create_cfg.py script on 2023-05-06 [yyyy-mm-dd] -- EDIT AT YOUR OWN RISK
# Files read from: /lustrefs/hdd_pool_dir/nanoAODv11/30march2023/data
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
json = os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/cfg/Cert_Collisions2022_355100_362760_Golden.json"

kreator = ComponentCreator()

Muon_Run2022E_0 = kreator.makeDataComponentFromLocal("Muon_Run2022E", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/Muon/dataRun3_2022_oct2023_Muon_Run2022E-22Sep2023-v1/231102_103239/0000", "", ".*root", "2022EE", [], json = json)
Muon_Run2022F_0 = kreator.makeDataComponentFromLocal("Muon_Run2022F", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/Muon/dataRun3_PostEE_oct2023_Muon_Run2022F-22Sep2023-v1/231027_084304/0000", "", ".*root", "2022EE", [], json = json)
Muon_Run2022G_0 = kreator.makeDataComponentFromLocal("Muon_Run2022G", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/Muon/dataRun3_PostEE_oct2023_Muon_Run2022G-22Sep2023-v1/231027_084442/0000", "", ".*root", "2022EE", [], json = json)

EGamma_Run2022E_0 = kreator.makeDataComponentFromLocal("EGamma_Run2022E", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/EGamma/dataRun3_2022_oct2023_EGamma_Run2022E-22Sep2023-v1/231102_104657/0000", "", ".*root", "2022EE", [], json = json)
EGamma_Run2022F_0 = kreator.makeDataComponentFromLocal("EGamma_Run2022F", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/EGamma/dataRun3_PostEE_oct2023_EGamma_Run2022F-22Sep2023-v1/231027_084617/0000", "", ".*root", "2022EE", [], json = json)
EGamma_Run2022G_0 = kreator.makeDataComponentFromLocal("EGamma_Run2022G", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/EGamma/dataRun3_PostEE_oct2023_EGamma_Run2022G-22Sep2023-v2/231205_104236/0000", "", ".*root", "2022EE", [], json = json)

MuonEG_Run2022E_0 = kreator.makeDataComponentFromLocal("MuonEG_Run2022E", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022E-22Sep2023-v1/231102_103925/0000", "", ".*root", "2022EE", [], json = json)
MuonEG_Run2022F_0 = kreator.makeDataComponentFromLocal("MuonEG_Run2022F", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/MuonEG/dataRun3_PostEE_oct2023_MuonEG_Run2022F-22Sep2023-v1/231023_081125/0000", "", ".*root", "2022EE", [], json = json)
MuonEG_Run2022G_0 = kreator.makeDataComponentFromLocal("MuonEG_Run2022G", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022PostEE/MuonEG/dataRun3_PostEE_oct2023_MuonEG_Run2022G-22Sep2023-v1/231023_081300/0000", "", ".*root", "2022EE", [], json = json)

data = [
    Muon_Run2022E_0, 
    EGamma_Run2022E_0, 
    MuonEG_Run2022E_0,
#    Muon_Run2022F_0, 
#    EGamma_Run2022F_0, 
#    MuonEG_Run2022F_0, 
#    Muon_Run2022G_0, 
#    EGamma_Run2022G_0, 
#    MuonEG_Run2022G_0
]


dataSamples_toImport = data