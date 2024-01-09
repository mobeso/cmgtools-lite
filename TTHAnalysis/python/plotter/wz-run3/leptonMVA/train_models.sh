# macro to train models
# v1--> first version
# v2--> 
#      * fix the electron veto to EE region (one branch nos being read correctly)
#      * After results from v1, increased the number of trees for performance of BDTG2
#                               also changed number of cuts.
# nanoAODv12 -->
#      * Retrain with latest nanoAOD. 2022 and 2022EE trainings included

year=$1
if [[ -z $year ]]; then
  echo Please select a year for the training
  exit 0
fi


logoutput="lepmva_results/logs_training/"
if [[ ! -d $logoutput ]]; then
  mkdir -p $logoutput
fi

# Electrons 
for presel in tth ttw; do
  for btag in df pnet; do
    for iso in _useIso _useNoIso ""; do
      name="el_${presel}Presel_nanoAODv12_${year}_${btag}${iso}"
      mode="el_${presel}_${btag}${iso}_${year}"
      sbatch -J el_mva -e $logoutput/$name.err -o $logoutput/$name.out --wrap "./train_model.sh $name $mode $year"
      done
  done
done

# Muons
for presel in tth ttw; do
  for btag in df pnet; do
    name="mu_${presel}Presel_nanoAODv12_${year}_${btag}${iso}"
    mode="mu_${presel}_${btag}${iso}_${year}"
    sbatch -J mu_mva -e $logoutput/$name.err -o $logoutput/$name.out --wrap "./train_model.sh $name $mode $year"
    done
done
