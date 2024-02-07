# Script to compute efficiencies
RED='\033[0;31m'
GREEN='\033[0;32m'
PURPLE='\033[0;35m'
CYAN='\033[1;36m'
NC='\033[0m' # No Color


measure=$1
extra=$2
## For the year: 2022, 2022EE or all
year=all

echo -e "$CYAN WARNING!! Remember that you are using the $year dataset!! :D"

function measure_efficiency() {
    # Computes the efficiency using mcPlots
    extra=$1 
    mca="wz-run3/inclusive_xsec/mca-eff.txt"
    cuts="wz-run3/inclusive_xsec/cuts-total.txt"
    outname="wz-run3/inclusive_xsec/efficiency/$year"

    basecmd="python3 wz-run3/wz-run.py plot"
    basecmd="$basecmd --ncores 32" # Add cores
    basecmd="$basecmd --mca $mca" # add mca
    basecmd="$basecmd --cutfile $cuts" # add cuts
    basecmd="$basecmd --mcpath /lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees_v2/mc_unskim_Jan2024" #Use unSkim samples trees
    ##For the year: 2022, 2022EE or all
    basecmd="$basecmd --year $year"

    echo -e "$PURPLE >> Computing efficiency $NC"

    # INCLUSIVE
    ## Denominator: Fiducial
    echo -e "$GREEN Inclusive Fiducial Denominator: $NC"
    cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial --sP tot_weight' --unweight --outname $outname/denominator/inclusive $extra"
    echo $cmd_den | bash
    ##Numerator: Reco
    echo -e "$GREEN Inclusive Fiducial Numerator: $NC"
    cmd_num="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^SRWZ --sP tot_weight' --outname $outname/numerator/inclusive $extra"
    echo $cmd_num | bash


    # EEE
    echo -e "$GREEN Fiducial Denominator eee: $NC"
    cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^eeegen --sP tot_weight' --unweight --outname $outname/denominator/eee $extra"
    echo $cmd_den | bash
    ##Numerator: Reco
    echo -e "$GREEN Fiducial Numerator eee: $NC"
    cmd_num="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^SRWZ -E ^eeegen -E ^eee --sP tot_weight' --outname $outname/numerator/eee $extra"
    echo $cmd_num | bash


    # EEM
    echo -e "$GREEN Fiducial Denominator eem: $NC"
    cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^eemgen --sP tot_weight' --unweight --outname $outname/denominator/eem $extra"
    echo $cmd_den | bash
    ##Numerator: Reco
    echo -e "$GREEN Fiducial Numerator eem: $NC"
    cmd_num="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^SRWZ -E ^eemgen -E ^eem --sP tot_weight' --outname $outname/numerator/eem $extra"
    echo $cmd_num | bash


    # MME
    echo -e "$GREEN Fiducial Denominator mme: $NC"
    cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^mmegen --sP tot_weight' --unweight --outname $outname/denominator/mme $extra"
    echo $cmd_den | bash
    ##Numerator: Reco
    echo -e "$GREEN Fiducial Numerator mme: $NC"
    cmd_num="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^SRWZ -E ^mmegen  -E ^mme --sP tot_weight' --outname $outname/numerator/mme $extra"
    echo $cmd_num | bash


    # MMM
    echo -e "$GREEN Fiducial Denominator mmm: $NC"
    cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^mmmgen --sP tot_weight' --unweight --outname $outname/denominator/mmm $extra"
    echo $cmd_den | bash
    ##Numerator: Reco
    echo -e "$GREEN Fiducial Numerator mmm: $NC"
    cmd_num="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial -E ^SRWZ -E ^mmmgen -E ^mmm --sP tot_weight' --outname $outname/numerator/mmm $extra"
    echo $cmd_num | bash

    # Make the command for the denominator (unweight events)
    #for flav in inclusive eee eem mme mmm; do
    #    echo -e "$PURPLE   Denominator. Fiducial $NC ($flav)"
    #    toAddDen="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^${flav}gen'" # plot number of events
    #    dencmd="$basecmd $toAddDen --unweight --outname $outname/denominator/$flav $extra"
    #    echo $dencmd | bash
    #    
    #    # Make the command for the numerator:
    #    echo -e "$PURPLE   Numerator. Fiducial + Signal Region $NC ($flav)"
    #    toAddNum="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^${flav}gen -E ^SRWZ -E ^${flav}'" # plot number of events
    #    numcmd="$basecmd $toAddNum --outname $outname/numerator/$flav $extra"
    #    echo $numcmd | bash
    #done
}

function measure_acceptance() {
    # Computes the acceptance using mcPlots
    sample=$1
    extra=$2
    mcpath="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees_v2/mc_unskim_Jan2024"
    
    case $sample in
        pow)
            mca="wz-run3/inclusive_xsec/mca-acc-powheg.txt"
            outname="wz-run3/inclusive_xsec/acceptance_powheg"
            ;;
        amc)
            mca="wz-run3/inclusive_xsec/mca-acc-amcnlo.txt"
            outname="wz-run3/inclusive_xsec/acceptance_amcnlo"
    esac
    
    cuts="wz-run3/inclusive_xsec/cuts-total.txt"

    basecmd="python3 wz-run3/wz-run.py plot"
    basecmd="$basecmd --ncores 12" # Add cores
    basecmd="$basecmd --mca $mca" # add mca
    basecmd="$basecmd --cutfile $cuts" # add cuts
    basecmd="$basecmd --unweight " # Unweight everything since this is fiducial level
    basecmd="$basecmd --unfriend " # There are no friend trees for the acceptance sample
    basecmd="$basecmd --mcpath $mcpath " # Unweight everything since this is fiducial level

    basecmd="$basecmd --year $year"

    #cmd_den="$basecmd --extra '-E ^total -E ^lightleps -E ^fiducial --sP tot_weight' --unweight --outname $outname/denominator/inclusive $extra"
 

    echo -e "$PURPLE >> Computing acceptance ($sample) $NC"

    #INCLUSIVE
    echo -e "$GREEN Inclusive denominator $NC"
    #dencmd="$basecmd --extra '--sP tot_weight -E ^total --FMCs {P}/[lepGEN]' --unweight --outname $outname/denominator/inclusive $extra"
    dencmd="$basecmd --extra '--sP tot_weight -E ^total --FMCs {P}/lepGEN_nondressed_withTaus' --unweight --outname $outname/denominator/inclusive/ $extra"
    #echo $dencmd
    echo $dencmd | bash
    echo -e "$GREEN Inclusive numerator $NC"
    numcmd="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial --FMCs {P}/lepGEN_nondressed_withTaus' --outname $outname/numerator/inclusive $extra"
    echo $numcmd | bash
    #echo $numcmd

    #EEE
    echo -e "$GREEN Denominator eee $NC"
    dencmd="$basecmd --extra '--sP tot_weight -E ^total -E ^eeegen --FMCs {P}/lepGEN_nondressed_withTaus' --unweight --outname $outname/denominator/eee $extra"
    #echo $dencmd
    echo $dencmd | bash
    echo -e "$GREEN Numerator eee $NC"
    numcmd="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^eeegen --FMCs {P}/lepGEN_nondressed_withTaus' --outname $outname/numerator/eee $extra"
    echo $numcmd | bash
    #echo $numcmd
    
    #EEM
    echo -e "$GREEN Denominator eem $NC"
    dencmd="$basecmd --extra '--sP tot_weight -E ^total -E ^eemgen --FMCs {P}/lepGEN_nondressed_withTaus' --unweight --outname $outname/denominator/eem $extra"
    #echo $dencmd
    echo $dencmd | bash
    echo -e "$GREEN Numerator eem $NC"
    numcmd="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^eemgen --FMCs {P}/lepGEN_nondressed_withTaus' --outname $outname/numerator/eem $extra"
    echo $numcmd | bash
    #echo $numcmd


    #MME
    echo -e "$GREEN Denominator mme $NC"
    dencmd="$basecmd --extra '--sP tot_weight -E ^total -E ^mmegen --FMCs {P}/lepGEN_nondressed_withTaus' --unweight --outname $outname/denominator/mme $extra"
    #echo $dencmd
    echo $dencmd | bash
    echo -e "$GREEN Numerator mme $NC"
    numcmd="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^mmegen --FMCs {P}/lepGEN_nondressed_withTaus' --outname $outname/numerator/mme $extra"
    echo $numcmd | bash
    #echo $numcmd


    #MMM
    echo -e "$GREEN Denominator mmm $NC"
    dencmd="$basecmd --extra '--sP tot_weight -E ^total -E ^mmmgen --FMCs {P}/lepGEN_nondressed_withTaus' --unweight --outname $outname/denominator/mmm $extra"
    #echo $dencmd
    echo $dencmd | bash
    echo -e "$GREEN Numerator mmm $NC"
    numcmd="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^mmmgen --FMCs {P}/lepGEN_nondressed_withTaus' --outname $outname/numerator/mmm $extra"
    echo $numcmd | bash
    #echo $numcmd



# Make the command for the denominator (unweight events)
    #for flav in inclusive eee eem mme mmm; do
    #    echo -e "$PURPLE   Denominator. Total region $NC ($flav)"
    #    toAddDen="$basecmd --extra '--sP tot_weight -E ^total'" # plot number of events
    #    dencmd="$basecmd $toAddDen --outname $outname/denominator/$flav $extra"
    #    echo $dencmd | bash
    #    
    #    # Make the command for the numerator: (bin in lepton flavor here)
    #    echo -e "$PURPLE   Numerator. Fiducial region $NC ($flav)"
    #    toAddNum="$basecmd --extra '--sP tot_weight -E ^total -E ^lightleps -E ^fiducial -E ^${flav}gen'" # plot number of events
    #    numcmd="$basecmd $toAddNum --outname $outname/numerator/$flav $extra"
    #    echo $numcmd
    #    echo $numcmd | bash
    #done
}

if [[ $measure == *"eff"* ]]; then measure_efficiency $extra; fi
if [[ $measure == *"acc_pow"* ]]; then measure_acceptance pow $extra; fi
if [[ $measure == *"acc_amc"* ]]; then measure_acceptance amc $extra; fi

