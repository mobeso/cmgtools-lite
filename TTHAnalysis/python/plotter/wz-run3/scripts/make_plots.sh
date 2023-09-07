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
    new_extra=$(echo "$extra" | sed -E "s/(--outname [^[:space:]]+)/\1\/$1/")
}

# Since these scripts are for specific studies, let's just add a basic outname that
# we can later modify insitu
isThereOutname=$( echo $extra | grep outname)
if [[ -z $isThereOutname ]]; then
    extra="$extra --outname plots"
fi


# Produce plots per flavor
if [[ $mode == *perflav* ]]; then
    for flav in eee eem mme mmm; do
        # Create an specific folder for each flavor channel
        append_to_path $flav

        echo -e $GREEN SUBMITTING for flavor: $flav $NC
        python wz-run3/wz-run.py plot --extra "-E ^flav_${flav}" $new_extra --plot-group main
        echo "-----------------------------"
    done
fi

# Produce plots for trigger efficiency measuremtn
if [[ $mode == *trigger_eff* ]]; then
    cuts="wz-run3/common/cuts_trigger.txt"
    mca="wz-run3/mca/mca_wz_triggerEff.txt"

    

    # Numerator
    echo -e $GREEN ">> Command for running the plot for the numerator $NC"
    append_to_path numerator
    python wz-run3/wz-run.py plot --mca $mca --cutfile $cuts --extra "-E ^trigger" $new_extra --plot-group trigger
    echo "-----------------------------"

    
    # Denominator
    echo -e $GREEN ">> Command for running the plot for the denominator $NC" 
    append_to_path denominator
    python wz-run3/wz-run.py plot --mca $mca --cutfile $cuts  $new_extra --plot-group trigger
    echo "-----------------------------"

fi


