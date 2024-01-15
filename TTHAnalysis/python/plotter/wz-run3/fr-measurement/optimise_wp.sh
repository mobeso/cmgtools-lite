# Just commands to prompt stuff with color
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'

NC='\033[0m' # No Color

# --------------------------------------------------------------------------------------------------- #
# This script is used to optimise the conePt WP. The main idea is to achieve a value of conePt that:  #
#  - Reduces the bias towards different possible flavours of the fake jet                             #
#  - Minimises the FR in the window that is used to define the b tagging WP of the FO.                #
# --------------------------------------------------------------------------------------------------- #

lepton=$1
submit=$2

function optimise_wp () {
    # ----------------- Inputs ----------------- #
    year=$1
    lepton=$2
    jetptiso=$3
    SELECTPROCESS=$4
    outfolder=$5
    submit=$6

    jetptisoname="${jetptiso/./}"
    # ----------------- Define here some metadata ----------------- #
    # I/O
    trees="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc_fr/$year"
    trees_data="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/data_fr/$year"
    friends=" --Fs {P}/frUtils --Fs {P}/lepmva"
    PBASE="plots/WZRUN3/lepMVA/v1.0/conept-optimise/$jetptisoname/$lepton/$year/$outfolder"
    
    # Command
    cmd="python3 mcEfficiencies.py"
    BCORE="${cmd} wz-run3/fr-measurement/mca-qcdfr-coneptTuning.txt" # MCA
    BCORE="${BCORE} wz-run3/fr-measurement/qcd1l.txt" # CUT
    BCORE="${BCORE} wz-run3/fr-measurement/plots-fr-ids.txt" # PLOTS IDs
    BCORE="${BCORE} wz-run3/fr-measurement/plots-fr-xvars.txt" # PLOTS xvars
    BCORE="${BCORE} --tree NanoAOD" 
    BCORE="${BCORE} -P $trees -P $trees_data"
    BCORE="${BCORE} $friends"
    BCORE="${BCORE} -L wz-run3/functionsWZ.cc -L functions.cc"
    
    BG="24"
        
    # Cosmetics
    LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
    RANGES=" --yrange 0.0 0.5 "
    
    # ----------------- Figure out the details ----------------- #

    # + Common den
    SIP8="LepGood_sip3d < 8"
    SelDen="" #"-A AtLeastOnePair den '$SIP8'" # I don't think this cut is needed.
    # + Jet contribution to DEN
    AwayJetPt=30
    JetDen="-A AtLeastOnePair nlep 'nLepGood == 1' "
    

    SelDen="-E ^${lepton} ${SelDen} ${JetDen}"
    QCD="QCD"
    case $lepton in
        mu) 
            WPNUM="0.64"
            Num="mu_num_mva_${WPNUM/./}"
            XVar="mu_mva${WPNUM/./}_Pt${jetptisoname}"
            
            # Below define your FO object (note that the base is the Loose selection)
            MuRecoPt=12 # A bit higher than the loose pT
            MuIdDen=0

            # Now for the b tagging part
            SelDen="${SelDen} -A AtLeastOnePair mmuid 'LepGood_mediumId>${MuIdDen}'" # ID
            SelDen="${SelDen} -A AtLeastOnePair mpt 'LepGood_pt > ${MuRecoPt}' "      # pT
            ETA="1.2"
            ;;
        el) 
            WPNUM="0.97"
            Num="ele_num_mva_${WPNUM/./}"
            XVar="ele_mva${WPNUM/./}"

            # Below define your FO object (note that the base is the Loose selection)
            EleRecoPt=12 # A bit higher than the loose pT
            EleTC=0

            SelDen="${SelDen} -A AtLeastOnePair elpt 'LepGood_pt > ${EleRecoPt}'"
            SelDen="${SelDen} -A AtLeastOnePair convveto 'LepGood_convVeto && LepGood_lostHits == 0"
            SelDen="${SelDen} -A AtLeastOnePair charge 'LepGood_tightCharge >= ${EleTC}'"
            SelDen="${SelDen} -A AtLeastOnePair sieie  'LepGood_sieie < (0.011+0.019*(abs(LepGood_eta+LepGood_deltaEtaSC)>1.479))' "
            SelDen="${SelDen} -A AtLeastOnePair hoe  'LepGood_hoe < 0.10' "
            SelDen="${SelDen} -A AtLeastOnePair btag '${BTagDen}'"
            
            ETA="1.479"
            ;;
    esac

    # Now for the b tagging part
    conept="LepGood_pt*if3(LepGood_mvaTTH_run3_withDF_withISO>$WPNUM, 1.0, $jetptiso*(1+LepGood_jetRelIso))"
    BTagDen="LepGood_jetBTagDeepFlav < smoothBFlav($conept, 20, 45)"
    
    SelDen="${SelDen} -A AtLeastOnePair btag '${BTagDen}'"

    FakeVsPt="$SelDen --sP '${XVar}' --sP '${Num}' -p $SELECTPROCESS --xcut 10 999 --xline 15 "

    
    cmdbarrel="$BCORE $FakeVsPt -o $PBASE/${lepton}_eta_00_12.root   -A AtLeastOnePair eta 'abs(LepGood_eta)<$ETA'   -j ${BG} --groupBy cut"
    cmdendcap="$BCORE $FakeVsPt -o $PBASE/${lepton}_eta_12_24.root    -A AtLeastOnePair eta 'abs(LepGood_eta)>$ETA'   -j ${BG} --groupBy cut"
    
    barrelwrap='"'${cmdbarrel}'"'
    endcapwrap='"'${cmdendcap}'"'

    cmdbarrel_submit="sbatch -c ${BG} -J fr_${outfolder}_${outfolder}_barrel -e ${PBASE}/logs/logBarrel.%j.%x.err -o ${PBASE}/logs/logBarrel.%j.%x.out --wrap $barrelwrap "
    cmdendcap_submit="sbatch -c ${BG} -J fr_${outfolder}_${outfolder}_barrel -e ${PBASE}/logs/logEndcap.%j.%x.err -o ${PBASE}/logs/logEndcap.%j.%x.out --wrap $endcapwrap "

    echo -e "  $RED  + Command for barrel $NC"
    echo $cmdbarrel_submit
    echo ""
    echo -e "  $RED  + Command for endcap $NC"
    echo $cmdendcap_submit

    # Submit if requested
    if [[ ! -z $submit ]]; then
        if [[ ! -d $PBASE/logs ]]; then mkdir -p $PBASE/logs; fi
        echo $cmdbarrel_submit | bash
        echo $cmdendcap_submit | bash
    fi
}



# --- Make efficiencies for all these cases
if [[ $lepton == mu ]]; then

    if [[ $submit == "submit" || -z $submit ]]; then
        for jetptiso in 0.70 0.80 0.90 ; do
            echo -e "$GREEN >> Testing jetptiso $jetptiso for $lepton $NC"
            echo -e " $YELLOW Origin: inclusive $NC"
            optimise_wp 2022EE $lepton $jetptiso "TT_red,QCDMu_red" inclusive $submit
            echo -e " $YELLOW ----------------------------------------- $NC"
            echo -e " $YELLOW Origin: B jet $NC"
            optimise_wp 2022EE $lepton $jetptiso "TT_bjets,QCDMu_bjets" fromB $submit
            echo -e " $YELLOW ----------------------------------------- $NC"
            echo -e " $YELLOW Origin: C jet $NC"
            optimise_wp 2022EE $lepton $jetptiso "TT_cjets,QCDMu_cjets" fromC $submit
            echo -e " $YELLOW ----------------------------------------- $NC"
            echo -e " $YELLOW Origin: Light jet $NC"
            optimise_wp 2022EE $lepton $jetptiso "TT_ljetsNC,QCDMu_ljets" fromL $submit
            echo -e " $YELLOW ----------------------------------------- $NC"
            
        done
    elif [[ $submit == "copy" ]]; then
        for jetptiso in 0.70 0.80 0.90; do
            for flav in inclusive fromB fromC fromL; do
                jetptisoname="${jetptiso/./}"
                PBASE="plots/WZRUN3/lepMVA/v1.0/conept-optimise/$jetptisoname/$lepton/2022EE/$flav"

                outfold="$HOME/www/private/wz-run3/dec-2023/fr/conept-optimise/$mu"

                if [[ ! -d $outfold ]]; then mkdir -p $outfold; fi

                echo -e "$GREEN >> Copying from $PBASE to $outfold $NC"

                # Copy results in barrel
                cp $PBASE/*00_12*.png $outfold/fr_jetpt${jetptisoname}_${flav}_barrel.png
                cp $PBASE/*00_12*.pdf $outfold/fr_jetpt${jetptisoname}_${flav}_barrel.pdf

                # Copy results in endcap
                cp $PBASE/*12_24*.png $outfold/fr_jetpt${jetptisoname}_${flav}_endcap.png
                cp $PBASE/*12_24*.pdf $outfold/fr_jetpt${jetptisoname}_${flav}_endcap.pdf

                # Copy the index.php
                cp wz-run3/scripts/index.php $outfold
            done
        done
    fi
fi


