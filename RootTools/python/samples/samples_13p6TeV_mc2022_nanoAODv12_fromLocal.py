#!/bin/env python3
# Config file for Run3 sample postprocessing
# File automatically generated by create_cfg.py script on 2024-01-09 [yyyy-mm-dd] -- EDIT AT YOUR OWN RISK
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
kreator = ComponentCreator()
# ------ Group: WZ
#  + Process: WZto3LNu 
WZto3LNu_0 = kreator.makeMCComponentFromLocal("WZto3LNu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_WZto3LNu_TuneCP5_13p6TeV_powheg-pythia8/231102_115409/0000", ".*root", 5.31)
WZ = [WZto3LNu_0]

# ------ Group: ZZ
#  + Process: ZZto4L 
ZZto4L_0 = kreator.makeMCComponentFromLocal("ZZto4L", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_ZZto4L_TuneCP5_13p6TeV_powheg-pythia8/231102_115030/0000", ".*root", 1.65)
ZZ = [ZZto4L_0]

# ------ Group: ttX
#  + Process: TTG_1Jets_PTG_10to100 
TTG_1Jets_PTG_10to100_0 = kreator.makeMCComponentFromLocal("TTG_1Jets_PTG_10to100", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/mcRun3_2022_oct2023_TTG-1Jets_PTG-10to100_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/231229_175000/0000", ".*root", 4.216)
#  + Process: TTG_1Jets_PTG_100to200 
TTG_1Jets_PTG_100to200_0 = kreator.makeMCComponentFromLocal("TTG_1Jets_PTG_100to200", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/mcRun3_2022_oct2023_TTG-1Jets_PTG-100to200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/231229_175157/0000", ".*root", 0.411)
#  + Process: TTG_1Jets_PTG_200 
TTG_1Jets_PTG_200_0 = kreator.makeMCComponentFromLocal("TTG_1Jets_PTG_200", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/mcRun3_2022_oct2023_TTG-1Jets_PTG-200_TuneCP5_13p6TeV_amcatnloFXFXold-pythia8/231229_175352/0000", ".*root", 0.128)
#  + Process: TTHtoNon2B_M_125 
#  + Process: TTLNu_1Jets 
TTLNu_1Jets_0 = kreator.makeMCComponentFromLocal("TTLNu_1Jets", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTLNu-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/mcRun3_2022_oct2023_TTLNu-1Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/231230_151244/0000", ".*root", 0.25)
#  + Process: TTLL_MLL_50 
TTLL_MLL_50_0 = kreator.makeMCComponentFromLocal("TTLL_MLL_50", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_TTLL_MLL-50_TuneCP5_13p6TeV_amcatnlo-pythia8/231102_120217/0000", ".*root", 0.08646)
#  + Process: TTLL_MLL_4to50 
TTLL_MLL_4to50_0 = kreator.makeMCComponentFromLocal("TTLL_MLL_4to50", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_TTLL_MLL-4to50_TuneCP5_13p6TeV_amcatnlo-pythia8/231109_113223/0000", ".*root", 0.03949)
ttX = [TTG_1Jets_PTG_10to100_0, TTG_1Jets_PTG_100to200_0, TTG_1Jets_PTG_200_0, TTLNu_1Jets_0, TTLL_MLL_50_0, TTLL_MLL_4to50_0]

# ------ Group: TZQ
TZQ = []

# ------ Group: Others
Others = []

# ------ Group: VVV
#  + Process: WWW_4F 
#  + Process: WWZ_4F 
WWZ_4F_0 = kreator.makeMCComponentFromLocal("WWZ_4F", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_WWZ_4F_TuneCP5_13p6TeV_amcatnlo-pythia8/231117_104238/0000", ".*root", 0.1851)
#  + Process: WZZ 
WZZ_0 = kreator.makeMCComponentFromLocal("WZZ", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/231117_104100/0000", ".*root", 0.06206)
#  + Process: ZZZ 
ZZZ_0 = kreator.makeMCComponentFromLocal("ZZZ", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/231117_104419/0000", ".*root", 0.01591)
VVV = [WWZ_4F_0, WZZ_0, ZZZ_0]

# ------ Group: Fakes_TT
#  + Process: TTto2L2Nu 
TTto2L2Nu_0 = kreator.makeMCComponentFromLocal("TTto2L2Nu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/231102_112426/0000", ".*root", 97.4488)
Fakes_TT = [TTto2L2Nu_0]

# ------ Group: Fakes_ST
#  + Process: TWminusto2L2Nu 
TWminusto2L2Nu_0 = kreator.makeMCComponentFromLocal("TWminusto2L2Nu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_TWminusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/231102_113242/0000", ".*root", 23.8979)
#  + Process: TbarWplusto2L2Nu 
TbarWplusto2L2Nu_1 = kreator.makeMCComponentFromLocal("TbarWplusto2L2Nu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_TbarWplusto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/231102_113434/0000", ".*root", 23.8979)
Fakes_ST = [TWminusto2L2Nu_0, TbarWplusto2L2Nu_1]

# ------ Group: Fakes_DY
#  + Process: DYto2L_2Jets_MLL_50 
DYto2L_2Jets_MLL_50_0 = kreator.makeMCComponentFromLocal("DYto2L_2Jets_MLL_50", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/mcRun3_2022_oct2023_DYto2L-2Jets_MLL-50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/231109_113024/0000", ".*root", 6345.99)
#  + Process: DYto2L_2Jets_MLL_10to50 
DYto2L_2Jets_MLL_10to50_0 = kreator.makeMCComponentFromLocal("DYto2L_2Jets_MLL_10to50", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/mcRun3_2022_oct2023_DYto2L-2Jets_MLL-10to50_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/231102_114339/0000", ".*root", 19982.5)
Fakes_DY = [DYto2L_2Jets_MLL_50_0, DYto2L_2Jets_MLL_10to50_0]

# ------ Group: Fakes_VV
#  + Process: ZZto2L2Q 
ZZto2L2Q_0 = kreator.makeMCComponentFromLocal("ZZto2L2Q", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_ZZto2L2Q_TuneCP5_13p6TeV_powheg-pythia8/231102_114849/0000", ".*root", 8.08)
#  + Process: ZZto2L2Nu 
ZZto2L2Nu_0 = kreator.makeMCComponentFromLocal("ZZto2L2Nu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_ZZto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/231102_114704/0000", ".*root", 1.19)
#  + Process: WWto2L2Nu 
WWto2L2Nu_0 = kreator.makeMCComponentFromLocal("WWto2L2Nu", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/mcRun3_2022_oct2023_WWto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/231102_115810/0000", ".*root", 12.98)
Fakes_VV = [ZZto2L2Q_0, ZZto2L2Nu_0, WWto2L2Nu_0]

# ------ Group: Wjets
#  + Process: WtoLNu_2Jets 
WtoLNu_2Jets_0 = kreator.makeMCComponentFromLocal("WtoLNu_2Jets", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/mcRun3_2022_oct2023_WtoLNu-2Jets_TuneCP5_13p6TeV_amcatnloFXFX-pythia8/231102_114521/0000", ".*root", 64481.58)
Wjets = [WtoLNu_2Jets_0]

# ------ Group: convs
#  + Process: WGtoLNuG_1Jets_PTG_10to100 
#  + Process: WGtoLNuG_1Jets_PTG_100to200 
#  + Process: WGtoLNuG_1Jets_PTG_200 
#  + Process: WZGtoLNuZG 
WZGtoLNuZG_0 = kreator.makeMCComponentFromLocal("WZGtoLNuZG", "", "/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022/WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8/mcRun3_2022_oct2023_WZGtoLNuZG_TuneCP5_13p6TeV_amcatnlo-pythia8/231117_104913/0000", ".*root", 0.08425)
#  + Process: ZGto2LG 
convs = [WZGtoLNuZG_0]




mcSamples_list = WZ + ZZ + ttX + TZQ + Others + VVV + Fakes_TT + Fakes_ST + Fakes_DY + Fakes_VV + Wjets + convs
mcSamples_toImport = mcSamples_list
