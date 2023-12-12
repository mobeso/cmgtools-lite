datasets="DoubleMuon EGamma JetHT JetMET MET Muon MuonEG SingleMuon"
inpath="/pool/phedex/nanoAODv10/27sep2022/Data"
#golden="Cert_Collisions2022_355100_357900_Golden.json" # Eras CD
#golden="Cert_Collisions2022_355100_360491_Golden.json" # ERAS CDE
#golden="Cert_Collisions2022_355100_362104_Golden.json" # ERAS CDEF
#golden="Cert_Collisions2022_355100_362439_Golden.json"  # ERAS CDEF_v2
golden="Cert_Collisions2022_355100_362760_Golden.json" # ERAS CDEFG

## DoubleMuon ##
python3 buildJSONfromNano.py --datasets DoubleMuon --inpath $inpath --filterjson $golden --filter-by-era Run2022C 

## SingleMuon ##
python3 buildJSONfromNano.py --datasets SingleMuon --inpath $inpath --filterjson $golden --filter-by-era Run2022C 

## Muon ##
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v1



## EGamma ##
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v2 
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v2
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v1


## JetHT ##
python3 buildJSONfromNano.py --datasets JetHT --inpath $inpath --filterjson $golden --filter-by-era Run2022C

## MET ##
python3 buildJSONfromNano.py --datasets MET --inpath $inpath --filterjson $golden --filter-by-era Run2022C

## JetMET ##
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v2
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v1



## MuonEG ##
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022F --filter-by-version v1-v2
python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022G --filter-by-version v1-v1

