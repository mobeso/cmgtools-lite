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
    extra="$extra --outname cards"
fi


# -------------------------------------------- #
#   1. PRODUCE MAIN DISTRIBUTION FOR THE FIT   #
# -------------------------------------------- #
if [[ $mode == *analysis* ]]; then

    echo -e $GREEN SUBMITTING for flavor: inclusive $NC
    append_to_path inclusive
    python3 wz-run3/wz-run.py card $outname 
    echo "-----------------------------"

fi

# ------------------------------------------- #
#   2. PRODUCE CARDS FOR OPTIMISING MET CUT   #
# ------------------------------------------- #
if [[ $mode == *met_optimise* ]]; then
    for metcut in {10..30..5}; do        
        echo -e $GREEN SUBMITTING for met cut: ">$metcut" $NC
        append_to_path met_gt$metcut
        python3 wz-run3/wz-run.py card $outname --extra "-E ^met_${metcut}"
        echo "-----------------------------"
    done
fi