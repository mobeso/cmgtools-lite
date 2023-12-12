# Just commands to plot stuff
# color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


mode=$1
step=$2

function measure_fr () {
    # ----------------- Inputs ----------------- #
    year=$1
    lepton=$2
    trigger=$3
    what=$4
    step=$5

    # ----------------- Define here some metadata ----------------- #
    # I/O
    trees="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc_fr/$year"
    trees_data="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/data_fr/$year"
    friends=" --Fs {P}/frUtils --Fs {P}/lepmva"
    PBASE="plots/WZRUN3/lepMVA/v1.0/fr-meas/qcd1l/$lepton/$year/HLT_$trigger/$what"
    
    # Command
    BCORE="wz-run3/fr-measurement/mca-qcd1l-${year}.txt" # MCA
    BCORE="${BCORE} wz-run3/fr-measurement/qcd1l.txt" # CUT
    BCORE="${BCORE} wz-run3/fr-measurement/qcd1l_plots.txt" # PLOTS
    BCORE="${BCORE} --tree NanoAOD" 
    BCORE="${BCORE} -P $trees -P $trees_data"
    BCORE="${BCORE} $friends"
    BCORE="${BCORE} ttH-multilepton/functionsTTH.cc"
    
    BG="-j 8"
    
    plotfile_xvars=wz-run3/fr-measurement/plots-fr-xvars.txt
    functions=""
    
    # Cosmetics
    LEGEND=" --legend=TL --fontsize 0.05 --legendWidth 0.4"
    RANGES=" --showRatio  --ratioRange 0.00 2.99 "
    STACK="python wz-run3/fr-measurement/stack_fake_rates_data.py "
    

    # ----------------- Figure out the details ----------------- #
    case $lepton in
        mu) 
            cuts="-E ^mu"
            procs="--xf 'EGamma.*' "
            NUM="mu_num_mva_064"
            QCD="QCDMu"
            conept="LepGood_pt*if3(LepGood_mvaTTH_run3_withDF_withISO>0.64 && LepGood_mediumId>0, 1.0, 0.9*(1+LepGood_jetRelIso))"
            
            case $trigger in
                Mu3_PFJet40)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_${trigger}' -A 'entry point' recoptfortrigger 'LepGood_pt>4.0 && LepGood_awayJet_pt>45'  "
                    RANGES="${RANGES} --xcut 10 30 --xline 10 --xline 15";;
                Mu8)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_${trigger}' -A 'entry point' recoptfortrigger 'LepGood_pt>8 && $conept > 13'  " 
                    XVAR="${XVAR/_coarselongbin/_coarsemu8bin}"
                    RANGES="${RANGES} --xcut 13 45 --xline 15 --xline 32";;
                Mu17)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_${trigger}' -A 'entry point' recoptfortrigger 'LepGood_pt>17 && $conept > 25' "
                    XVAR="${XVAR/_coarselongbin/_coarsemu17bin}"
                    RANGES="${RANGES} --xcut 25 100 --xline 32 ";;
                Mu20)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_${trigger}' -A 'entry point' recoptfortrigger 'LepGood_pt>20 && $conept > 30' "
                    XVAR="${XVAR/_coarselongbin/_coarsemu20bin}"
                    RANGES="${RANGES} --xcut 30 100 --xline 32 ";;
                Mu27)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_${trigger}' -A 'entry point' recoptfortrigger 'LepGood_pt>27 && $conept > 40' "
                    XVAR="${XVAR/_coarselongbin/_coarsemu27bin}"
                    RANGES="${RANGES} --xcut 40 100 --xline 45 ";;
            esac
            
            
            BARREL="00_12"; ENDCAP="12_24"; ETA="1.2"
            CONSTRFSIG=0.075; CONSTRFBKG=0.03 # For constraining fit
            XVAR="mu_mva064";;
        el) 
            cuts="-E ^el"
            procs="--xf 'Muon.*' "
            NUM="ele_num_mva_097"
            QCD="QCDEl"
            conept="LepGood_pt*if3(LepGood_mvaTTH_run3_withDF_withISO>0.97 && LepGood_mediumId>0, 1.0, 0.9*(1+LepGood_jetRelIso))"
            
            case $trigger in
                Ele8|Ele8_CaloIdM_TrackIdM_PFJet30)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_Ele8_CaloIdM_TrackIdM_PFJet30' -A 'entry point' recoptfortrigger 'LepGood_pt>8 && $conept > 13'  "; 
                    PUW=" -L ttH-multilepton/lepton-fr/frPuReweight.cc -W 'puwEle8_${YEAR}(PV_npvsGood)' ";;
                Ele17|Ele17_CaloIdM_TrackIdM_PFJet30)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_Ele17_CaloIdM_TrackIdM_PFJet30' -A 'entry point' recoptfortrigger 'LepGood_pt>17 && $conept > 25'  "; 
                    PUW=" -L ttH-multilepton/lepton-fr/frPuReweight.cc -W 'puwEle17_${YEAR}(PV_npvsGood)' ";;
                Ele23|Ele23_CaloIdM_TrackIdM_PFJet30)
                    BCORE="${BCORE} -A 'entry point' trigger 'HLT_Ele23_CaloIdM_TrackIdM_PFJet30' -A 'entry point' recoptfortrigger 'LepGood_pt>23 && $conept > 32'  "; 
                    PUW=" -L ttH-multilepton/lepton-fr/frPuReweight.cc -W 'puwEle23_${YEAR}(PV_npvsGood)' ";;
            esac
            
            BARREL="00_15"; ENDCAP="15_25"; ETA="1.479"
            CONSTRFSIG=0.05; CONSTRFBKG=0.10 # For constraining fit
            XVAR="ele_mva097";;
    esac
    
    
    
    # Selections
    EWKONE="-p ${QCD}_red,EWK,data"
    EWKSPLIT="-p ${QCD}_red,WJets,DYJets,Top,data"
    QCDEWKSPLIT="-p ${QCD}_[bclg]jets,WJets,DYJets,Top,data"
    FITEWK=" $EWKSPLIT --flp WJets,DYJets,Top,${QCD}_red --peg-process DYJets WJets --peg-process Top WJets "
    QCDNORM=" $QCDEWKSPLIT --sp WJets,DYJets,Top,${QCD}_.jets --scaleSigToData  "
    QCDFITEWK=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[clg]jets ${QCD}_bjets "
    QCDFITQCD=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_[gl]jets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "
    QCDFITALL=" $QCDEWKSPLIT --flp WJets,DYJets,${QCD}_.jets --peg-process DYJets WJets --peg-process ${QCD}_gjets WJets --peg-process ${QCD}_cjets ${QCD}_bjets "

    
    case $what in
    nvtx)
        echo -e "$RED ----- Compute prescale weights for FR. Trigger: $trigger ----- $NC" 
        echo "python mcPlots.py -f $BG $BCORE --pdir $PBASE --sP nvtx $EWKONE " 
        echo ""
        echo "python ../tools/vertexWeightFriend.py _puw${trigger}_${YEAR} $PBASE/qcd1l_plots.root ";
        echo -e " $GREEN ---- Now you should put the normalization and weight into frPuReweight.cc defining a puw${trigger}_${YEAR} ----- $NC' ";
        ;;
    nvtx-closure)
        echo -e "$RED ----- Compute closure test for $trigger PU reweighting ----- $NC" 
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE --sP nvtx $EWKONE " 
        ;;
    coneptw)
        echo -e "$RED ----- Compute conept weights to account for prescale ----- $NC" 
        echo "python mcPlots.py -f $BG $BCORE --pdir $PBASE --sP ${CONEPTVAR}_nvtx $EWKONE " 
        echo ""
        echo "python ttH-multilepton/lepton-fr/frConePtWeights.py coneptw${trigger}_${YEAR} $PBASE/make_fake_rates_xvars.root ${CONEPTVAR}_nvtx  ";
        echo -e " $GREEN ---- Now you should put the normalization and weight into frPuReweight.cc defining a coneptw${trigger}_${YEAR} ----- $NC ";
        ;;
    coneptw-closure)
        echo -e "$RED ----- Compute closure test for $trigger conept reweighting ----- $NC" 
        echo "python mcPlots.py -f $BG $BCORE $PUW ttH-multilepton/lepton-fr/make_fake_rates_xvars.txt --pdir $PBASE --sP ${CONEPTVAR}_nvtx,$CONEPTVAR,nvtx $EWKONE " 
        ;;
    fit-*)
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE -E $what $FITEWK --preFitData ${what/fit-/}  $PLOTOPTS " 
        ;;
    num-fit-*)
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE -E $what $FITEWK --preFitData ${what/num-fit-/}  $PLOTOPTS -E num" 
        ;;
    num-mcshapes)
        echo -e "$RED ----- Compute numerator shape ----- $NC" 
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE ${EWKSPLIT/,data/} --sP met --plotmode=nostack"
        echo -e "$RED ----------------------------------- $NC" 
 
        ;;
    qcdflav-norm)
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE -E $what $QCDNORM --showRatio $PLOTOPTS" 
        ;;
    qcdflav-fit)
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE -E $what $QCDFITEWK --preFitData ${what/flav-fit/}  $PLOTOPTS " 
        ;;
    flav-fit*)
        echo "python mcPlots.py -f $BG $BCORE $PUW --pdir $PBASE -E $what $QCDFITQCD --preFitData ${what/flav-fit/}  $PLOTOPTS " 
        ;;
    fakerates-*)
        fitVar=${what/fakerates-/}
        
        # Build the skeleton command
        MCEFF="python ttH-multilepton/dataFakeRate.py" 
        MCEFF="${MCEFF} -f  $BCORE" # Add basic core of the command
        MCEFF="${MCEFF} $EWKONE --groupBy cut wz-run3/fr-measurement/plots-fr-ids.txt wz-run3/fr-measurement/plots-fr-xvars.txt  "
        MCEFF="${MCEFF} --sp ${QCD}_red  "
        MCEFF="${MCEFF} --sP ${NUM} --sP ${XVAR} --sP $fitVar $fitVar  --ytitle 'Fake rate' "
        MCEFF="${MCEFF} --fixRatioRange --maxRatioRange 0.7 1.29 " # ratio for other plots
        MCEFF="${MCEFF} $LEGEND $RANGES"


        if [[ $step == 1 ]]; then
            # -------------------------------------- Histogram generation --------------------------------------- #
            # Here one generates the histograms that will be used for the fit later. This is done for a given     #
            # trigger HLT path (thus, for a given bin of pT and eta).                                             #
            # --------------------------------------------------------------------------------------------------- #
            MCGOBARREL="$MCEFF -o $PBASE/fr_sub_eta_${BARREL}.root --bare -A 'entry point' eta 'abs(LepGood_eta)<$ETA' $BG"
            MCGOENDCAP="$MCEFF -o $PBASE/fr_sub_eta_${ENDCAP}.root --bare -A 'entry point' eta 'abs(LepGood_eta)>$ETA' $BG"

            echo $MCGOBARREL
            echo $MCGOENDCAP
        fi
    ;;
    esac
}




measure_fr 2022EE mu Mu8 num-mcshapes
#measure_fr 2022EE mu Mu8 fakerates-mtW1R $step; 
