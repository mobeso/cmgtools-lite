RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


cuts="wz-run3/common/cuts-mvaValidation-2l.txt"
mca="wz-run3/mca/mca_wz_2l.txt"
outname="wz-run3/scripts/leptonMVA/plots_validation/"

extra=$1

# Plot mva variables per flavor on OS events
for flav in flav_ee flav_mm flav_em; do
    echo -e $GREEN ">> Command for running the plot for $flav: OS events $NC"
    sbatch -c 32 -J CMGPlot -p batch -e wz-run3/scripts/leptonMVA/plots_validation/OS/$flav/logs/log.%j.%x.err -o wz-run3/scripts/leptonMVA/plots_validation/OS/$flav/logs/log.%j.%x.out --wrap "python3 mcPlots.py wz-run3/mca/mca_wz_2l.txt wz-run3/common/cuts-mvaValidation-2l.txt wz-run3/common/plots_wz.txt -l 20.67 -f --pdir wz-run3/scripts/leptonMVA/plots_validation/OS/$flav --tree NanoAOD -P /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc/2022EE -P /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/data/2022EE --Fs {P}/jmeCorrections --Fs {P}/lepmva --Fs {P}/leptonJetRecleaning --Fs {P}/leptonBuilder -L wz-run3/functionsWZ.cc -W 'puWeight' --obj Events --maxRatioRange 0.5 2.0 --fixRatioRange --print C,pdf,png,txt --legendWidth 0.23 --legendFontSize 0.036 --showMCError --showRatio --showRatio --neg --TotalUncRatioColor 922 922 --TotalUncRatioStyle 3444 0 -j 32 --sP mva_lep1.* --sP mva_lep2.* --sP mva_lep3.* --sP mvatth.* -E ^$flav -E ^os_only "
#    sbatch -c 32 -J CMGPlot -p batch -e wz-run3/scripts/leptonMVA/plots_validation/OS/$flav/logs/log.%j.%x.err -o wz-run3/scripts/leptonMVA/plots_validation/OS/$flav/logs/log.%j.%x.out --wrap "python3 mcPlots.py wz-run3/mca/mca_wz_2l.txt wz-run3/common/cuts-mvaValidation-2l.txt wz-run3/common/plots_wz.txt -l 20.67 -f --pdir wz-run3/scripts/leptonMVA/plots_validation/OS/$flav --tree NanoAOD -P /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc/2022EE -P /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/data/2022EE --Fs {P}/jmeCorrections --Fs {P}/lepmva --Fs {P}/leptonJetRecleaning --Fs {P}/leptonBuilder -L wz-run3/functionsWZ.cc -W 'puWeight' --obj Events --maxRatioRange 0.5 2.0 --fixRatioRange --print C,pdf,png,txt --legendWidth 0.23 --legendFontSize 0.036 --showMCError --showRatio --showRatio --neg --TotalUncRatioColor 922 922 --TotalUncRatioStyle 3444 0 -j 32 --sP mva_lep1.* --sP mva_lep2.* --sP mva_lep3.* --sP mvatth.* -E ^$flav -E ^os_only --scaleBkgSigToData TOP --scaleBkgSigToData Fakes_TOP--scaleBkgSigToData Wjets --scaleBkgSigToData EWK" 
    echo "-----------------------------"
done

