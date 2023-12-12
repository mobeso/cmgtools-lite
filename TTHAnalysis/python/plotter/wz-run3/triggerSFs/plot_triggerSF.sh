# Just commands to plot stuff
# color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

step=$1

function trigger_efficiency_plots (){
    # ------------------------------------------------------ #
    #   PRODUCE PLOTS FOR TRIGGER EFFICIENCY MEASUREMENT  #
    # ------------------------------------------------------ #
    cuts="wz-run3/triggerSFs/cuts_trigger.txt"
    mca="wz-run3/mca/mca_wz_triggerEff.txt"
    outname=wz-run3/scripts/triggerSFs
    for barrelN in Inclusive barrel0 barrel1 barrel2 barrel3; do 
        
        if [[ ! $barrelN == Inclusive ]]; then extracut=" -E ^$barrelN"; fi
        # Numerator
        echo -e $GREEN ">> Command for running the plot for the numerator: $barrelN $NC"
        python3 wz-run3/wz-run.py plot --mca $mca --cutfile $cuts --extra "-E ^trigger $extracut" $outname/numerator --plot-group trigger
        echo "-----------------------------"

        
        # Denominator
        echo -e $GREEN ">> Command for running the plot for the denominator: $barrelN $NC"
        python3 wz-run3/wz-run.py plot --mca $mca --cutfile $cuts  $outname/denominator --plot-group trigger --extra " -E $extracut "
        echo "-----------------------------"
    done
}

if [[ $step == 1 ]]; then
    trigger_efficiency_plots
fi

