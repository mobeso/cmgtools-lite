# Just commands to plot stuff
# color
RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color


mode=$1
step=$2

function optimise_wp () {
    # ----------------- Inputs ----------------- #
    year=$1
    
    # ----------------- Define here some metadata ----------------- #
    trees="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/mc_fr/$year"
    friends=" --Fs {P}/frUtils --Fs {P}/lepmva"
    
    cmd="python3 mcEfficiencies.py"
    mcafile=wz-run3/mca/includes/mca_qcd.txt
    cutfile=wz-run3/fr-measurement/lepton-perlep.txt
    plotfile_ids=wz-run3//fr-measurement/plots-fr-ids.txt
    plotfile_xvars=wz-run3//fr-measurement/plots-fr-xvars.txt
    functions="wz-run3/functionsWZ.cc"
    mvaName=LepGood_mvaTTH_run3_withDF_withISO
    
    
    signal="TT_SS_red"
    
    # ----------------- Used to define num/den ----------------- #
    
    # + Jets
    AwayJetPt=30
    JetPt="1/(1+LepGood_jetRelIso) > 0.7"
    
    # + B tagging WPs (DeepJET) 
    VDFL="LepGood_jetBTagDeepFlav < 0.0614"
    VDFM="LepGood_jetBTagDeepFlav < 0.3196"
    VDFT="LepGood_jetBTagDeepFlav < 0.73"
    VDXT="LepGood_jetBTagDeepFlav < 0.8184"
    VDXXT="LepGood_jetBTagDeepFlav < 0.9542"
    
    # + Muons
    MuIdDen=0
    MuRecoPt=10
    MuMVAWP=0.64
    
    # + Electrons
    EleTC=0
    IDEmu=1
    EleRecoPt=10
    EleMVAWP=0.97
    
    # + Leptons in general
    SIP8="LepGood_sip3d < 8" 
    VETOCONVERSIONS="LepGood_mcPromptGamma==0"
    
    # ----------------- Build Numerators/Denominators ----------------- #
    SelDen="-A pt20 den '$SIP8'"
    
    
    # + Denominator for muons
    MuDen="$SelDen -A pt20 ptfden '($mvaName > $MuMVAWP || $JetPt)' -A pt20 mmuid 'LepGood_mediumId>=${MuIdDen}' -A pt20 mpt 'LepGood_pt > ${MuRecoPt}' "
    MuNum="mu_num_mva_${MuMVAWP//./}"
    MuXVar="mu_mva${MuMVAWP//./}"
    
    # + Denominator for electrons
    EleDen="$SelDen -A pt20 ptfden '($mvaName > $ElMVAWP || $JetPt)'"
    EleDen="$EleDen -I mu"
    EleDen="$EleDen -A pt20 convveto 'LepGood_convVeto && LepGood_lostHits == 0 && LepGood_tightCharge >= ${EleTC} && ${IDEmu}'"
    EleDen="$EleDen -A pt20 elpt 'LepGood_pt > ${EleRecoPt}'  "
    EleNum="ele_num_mva_${EleMVAWP//./}"
    EleXVar="ele_mva${EleMVAWP//./}"
    
    # + Cut on away jets
    JetBDen="-A pt20 jet 'LepGood_awayJet_pt >= $AwayJetPt' -A pt20 mll 'nLepGood == 1'"

    # ----------------- Build final command ----------------- #
    cmd="${cmd} $mcafile"
    cmd="${cmd} $cutfile"
    cmd="${cmd} $plotfile_ids"
    cmd="${cmd} $plotfile_xvars"
    cmd="${cmd} --tree NanoAOD"
    cmd="${cmd} -L $functions"
    cmd="${cmd} -P $trees $friends"
    cmd="${cmd} --groupBy cut"
    
    # cosmectic stuff
    cmd="${cmd} --legend=TR --showRatio --ratioRange 0.00 1.99   --yrange 0 0.35"
    
    # + Add denominator (muons)
    cmd_muon="${cmd} --sP ${MuNum} ${MuDen} ${JetBDen} "     
    cmd_muon="${cmd_muon} --sP '${MuXVar}_coarsecomb'"
    cmd_muon="${cmd_muon} --sp ${signal}"
    cmd_muon="${cmd_muon} --xcut 10 999 --xline 15"
    
    echo -e " $GREEN >> Fake rate command for muons $NC"
    echo $cmd_muon
    
}

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
    trees_data="/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/trees/data/$year"
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
    BCORE="${BCORE} --mcc ttH-multilepton/mcc-eleIdEmu2.txt"
    
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
}


if [[ $mode == *"optimise_wp"* ]]; then 
    optimise_wp; 
fi

if [[ $mode == *"measure_fr"* ]]; then 
    measure_fr 2022EE mu Mu8 fakerates-mtW1R $step; 
fi
