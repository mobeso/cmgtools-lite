#!/bin/env python3
# Config file for Run3 sample postprocessing
# File automatically generated by create_cfg.py script on 2024-01-09 [yyyy-mm-dd] -- EDIT AT YOUR OWN RISK
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
kreator = ComponentCreator()
json = os.environ["CMSSW_BASE"]+"/src/CMGTools/TTHAnalysis/cfg/Cert_Collisions2022_355100_362760_Golden.json"
# ------ Group: data
#  + Process: Muon_Run2022C 
Muon_Run2022C_0 = kreator.makeDataComponentFromLocal("Muon_Run2022C", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/Muon/dataRun3_2022_oct2023_Muon_Run2022C-22Sep2023-v1/231102_102752/0000", "", ".*root", "2022", [], json = json)
#  + Process: EGamma_Run2022C 
EGamma_Run2022C_0 = kreator.makeDataComponentFromLocal("EGamma_Run2022C", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/EGamma/dataRun3_2022_oct2023_EGamma_Run2022C-22Sep2023-v1/231102_104146/0000", "", ".*root", "2022", [], json = json)
#  + Process: MuonEG_Run2022C 
MuonEG_Run2022C_0 = kreator.makeDataComponentFromLocal("MuonEG_Run2022C", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022C-22Sep2023-v1/231102_103458/0000", "", ".*root", "2022", [], json = json)
#  + Process: JetMET_Run2022C 
JetMET_Run2022C_0 = kreator.makeDataComponentFromLocal("JetMET_Run2022C", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/JetMET/dataRun3_2022_oct2023_JetMET_Run2022C-22Sep2023-v1/231102_104919/0000", "", ".*root", "2022", [], json = json)
#  + Process: Muon_Run2022D 
Muon_Run2022D_0 = kreator.makeDataComponentFromLocal("Muon_Run2022D", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/Muon/dataRun3_2022_oct2023_Muon_Run2022D-22Sep2023-v1/231102_103015/0000", "", ".*root", "2022", [], json = json)
#  + Process: EGamma_Run2022D 
EGamma_Run2022D_0 = kreator.makeDataComponentFromLocal("EGamma_Run2022D", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/EGamma/dataRun3_2022_oct2023_EGamma_Run2022D-22Sep2023-v1/231102_104428/0000", "", ".*root", "2022", [], json = json)
#  + Process: MuonEG_Run2022D 
MuonEG_Run2022D_0 = kreator.makeDataComponentFromLocal("MuonEG_Run2022D", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/MuonEG/dataRun3_2022_oct2023_MuonEG_Run2022D-22Sep2023-v1/231102_103711/0000", "", ".*root", "2022", [], json = json)
#  + Process: JetMET_Run2022D 
JetMET_Run2022D_0 = kreator.makeDataComponentFromLocal("JetMET_Run2022D", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/2022/JetMET/dataRun3_2022_oct2023_JetMET_Run2022D-22Sep2023-v1/231102_105627/0000", "", ".*root", "2022", [], json = json)
data = [Muon_Run2022C_0, EGamma_Run2022C_0, MuonEG_Run2022C_0, JetMET_Run2022C_0, Muon_Run2022D_0, EGamma_Run2022D_0, MuonEG_Run2022D_0, JetMET_Run2022D_0]




dataSamples_list = data
dataSamples_toImport = dataSamples_list