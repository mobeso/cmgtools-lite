folder=$1
name=$2
year=$3

if [[ $name == *"mu"* ]]; then
    echo Submitting muon training...
    root -l -b -q 'trainMuonID_NanoAODv11.cxx("'"$folder"'", "'"$name"'", "'"$year"'")'
else
    echo Submitting electron training...
    root -l -b -q 'trainElectronID_NanoAODv11.cxx("'"$folder"'", "'"$name"'", "'"$year"'")'
fi



