# Script to test mvas


inpath=/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/ttSemilep_nanoAODv12_preEE/Run3Summer22NanoAODv12/231031_163325/0001/

year=$1
if [[ -z $year ]]; then
  echo Please select a year for the training
  exit 0
fi

# Electrons 

logoutput="lepmva_results/logs_evaluation/$year"
if [[ ! -d $logoutput ]]; then
  mkdir -p $logoutput
fi


sbatch --wrap "python3 evaluate_mva.py --inpath $inpath --year $year --nfiles 100 --mode electron_legacy"
for presel in tth ttw; do
  for btag in df pnet; do
    for iso in _wIso _wNoIso ""; do
      mode="electron_${btag}${iso}_${presel}"
      echo " >>> $mode"
      sbatch -e $logoutput/$mode.err -o $logoutput/$mode.out --wrap "python3 evaluate_mva.py --inpath $inpath --year $year --nfiles 100 --mode $mode"
      echo " ---- "
      done
  done
done

sbatch --wrap "python3 evaluate_mva.py --inpath $inpath --year $year --nfiles 100 --mode muon_legacy"
for presel in tth ttw; do
  for btag in df pnet; do
    mode="muon_${btag}_${presel}"
    echo " >>> $mode"
    sbatch -e $logoutput/$mode.err -o $logoutput/$mode.out --wrap "python3 evaluate_mva.py --inpath $inpath --year $year --nfiles 100 --mode $mode --year $year"
    echo " ---- "
  done
done
