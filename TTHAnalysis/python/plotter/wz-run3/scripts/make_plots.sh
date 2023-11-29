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

