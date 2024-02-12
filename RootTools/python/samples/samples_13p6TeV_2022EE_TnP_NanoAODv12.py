#!/bin/env python3
# Config file for Run3 sample postprocessing
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator
import os
kreator = ComponentCreator()

# ------ DY_M50 dataset
DYJetsToLL_M50 = kreator.makeMCComponentFromLocal('DYJetsToLL_M_50', '', '/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/MC/2022PostEE/DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/dyCommonSkim_DYto2L-4Jets_MLL-50_TuneCP5_13p6TeV_madgraphMLM-pythia8/231220_095629/0000', '.*root', 6688.0)

DY_M50 = [DYJetsToLL_M50]

mcSamples_toImport = DY_M50 