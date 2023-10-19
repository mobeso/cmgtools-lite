# Just commands to plot stuff
# color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

mode=$1
extra="${@:2}"

function append_to_path (){
    # This function appends an additional name to the output
    # name given to the script
    outname=$(echo "$extra" | sed -E "s/(--outname [^[:space:]]+)/\1\/$1/")
}

# Since these scripts are for specific studies, let's just add a basic outname that
# we can later modify insitu
isThereOutname=$( echo $extra | grep outname)
if [[ -z $isThereOutname ]]; then
    extra="$extra --outname plots"
fi


# --------------------------------------------- #
#   1. PRODUCE ALL PLOTS USED IN THE ANALYSIS   #
# --------------------------------------------- #
if [[ $mode == *analysis* ]]; then

    echo -e $GREEN SUBMITTING for flavor: inclusive $NC
    append_to_path inclusive
    python3 wz-run3/wz-run.py plot $outname --plot-group main
    echo "-----------------------------"

    # Produce plots per flavor
    if [[ $mode == *perflav* ]]; then
    for flav in eee eem mme mmm; do
        # Create an specific folder for each flavor channel
        append_to_path $flav
        echo -e $GREEN SUBMITTING for flavor: $flav $NC
        python3 wz-run3/wz-run.py plot --extra "-E ^flav_${flav}" $outname --plot-group main
        echo "-----------------------------"
    done
    fi
fi

# ------------------------------------------------------ #
#   2. PRODUCE PLOTS FOR TRIGGER EFFICIENCY MEASUREMENT  #
# ------------------------------------------------------ #
if [[ $mode == *trigger_eff* ]]; then
    cuts="wz-run3/common/cuts_trigger.txt"
    mca="wz-run3/mca/mca_wz_triggerEff.txt"
    
    for barrelN in Inclusive barrel0 barrel1 barrel2 barrel3; do 
        
        if [[ ! $barrelN == Inclusive ]]; then extracut=" -E ^$barrelN"; fi
        # Numerator
        echo -e $GREEN ">> Command for running the plot for the numerator: $barrelN $NC"
        append_to_path "numerator\/$barrelN"
        python3 wz-run3/wz-run.py plot --mca $mca --cutfile $cuts --extra "--uf -E ^trigger $extracut" $outname --plot-group trigger
        echo "-----------------------------"

        
        # Denominator
        echo -e $GREEN ">> Command for running the plot for the denominator: $barrelN $NC"
        append_to_path "denominator\/$barrelN"
        python3 wz-run3/wz-run.py plot --mca $mca --cutfile $cuts  $outname --plot-group trigger --extra " --uf $extracut "
        echo "-----------------------------"
    done
fi

# -------------------------- #
#   3. MET CUT OPTIMISATION  #
# -------------------------- #
if [[ $mode == *metopt* ]]; then
    echo -e $GREEN ">> Command for running the plot with met cut 10 $NC"
    python3 wz-run3/wz-run.py plot --outname plots/met_10 --extra '-E ^met_10' --region srwz --plot-groups main $extra
fi