inpath="/beegfs/data/nanoAODv11/30march2023/data/2022PostEE/"
golden="Cert_Collisions2022_355100_362760_Golden.json" # ERAS CDEFG

## Muon ##
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v2
#
#
### EGamma ##
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v2


## MuonEG ##
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v2

