# Script to produce plots used in the analysis note
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


mode=$1
extra=$2

if [[ $mode == "srwz" || $mode == "all" ]]; then
    echo -e " $GREEN >> Plots from analysis signal region $NC"
    python3 wz-run3/wz-run.py plot --outname plots_AN23147/SRWZ --ncores 32 --unc --plot-group main $extra --extra '--addspam "WZ SR" --pseudoData all_asimov --perBin' --blind

    python3 wz-run3/wz-run.py plot --outname plots_AN23147/SRWZ_unblind --ncores 32 --unc --plot-group main $extra --extra '--addspam "WZ SR" --xP flavor3l --perBin' 
fi

if [[ $mode == "crzz" || $mode == "all" ]]; then    
    echo -e  " $GREEN >> Plots from analysis ZZ control region $NC"
    python3 wz-run3/wz-run.py plot --extra '--addspam "ZZ CR"' --outname plots_AN23147/CRZZ --ncores 32 --unc --plot-group main --cutfile wz-run3/common/cuts-crzz.txt $extra
fi

if [[ $mode == "crtt" || $mode == "all"  ]]; then    
    echo -e " $GREEN >> Plots from analysis ttZ control region $NC"
    python3 wz-run3/wz-run.py plot --extra '--addspam "ttZ CR"' --outname plots_AN23147/CRTT --ncores 32 --unc --plot-group main --cutfile wz-run3/common/cuts-crtt.txt $extra
fi
