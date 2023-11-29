# Just commands to plot stuff
# color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

function plot_mtfix () {
    # This function just plots mTfix in QCD enriched region
    output=plots_mtfix
    
    cmd="python3 mcPlots.py"
    
    # CMGTools inputs
    mcafile=wz-run3/mca/includes/mca_qcd.txt
    cutfile=wz-run3/scripts/fr-measurement/cuts-fr.txt
    plotfile=wz-run3/scripts/fr-measurement/plots-fr.txt

    # Other configs
    lumi="-l 20.67"
    outputcmd="-f --pdir $output"
    trees="-P /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc_fr/2022EE --Fs {P}/frUtils --Fs {P}/lepmva"
    functions="-L wz-run3/functionsWZ.cc"
    otherStuff="-W 'puWeight' --obj Events --maxRatioRange 0.5 2.0 --fixRatioRange --print C,pdf,png,txt --legendWidth 0.23 --legendFontSize 0.036 --showMCError --showRatio --showRatio --neg --TotalUncRatioColor 922 922 --TotalUncRatioStyle 3444 0"
    
    
    # Parameters for batch job
    cores=8
    jobname=fakeRate
    outputlogs=$output/logs/log.%j.%x
    multithread="-j $cores"


    # Build the command
    cmd="$cmd $mcafile $cutfile $plotfile $lumi $outputcmd $trees $functions $otherStuff"
    echo $cmd
}

plot_mtfix