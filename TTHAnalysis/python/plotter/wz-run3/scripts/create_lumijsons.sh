datasets="DoubleMuon EGamma JetHT JetMET MET Muon MuonEG SingleMuon"
inpath="/pool/phedex/nanoAODv10/27sep2022/Data"
#golden="Cert_Collisions2022_355100_357900_Golden.json" # Eras CD
golden="Cert_Collisions2022_355100_360491_Golden.json" # ERAS CDE

## DoubleMuon ##
python buildJSONfromNano.py --datasets DoubleMuon --inpath $inpath --filterjson $golden --filter-by-era Run2022C 

## SingleMuon ##
python buildJSONfromNano.py --datasets SingleMuon --inpath $inpath --filterjson $golden --filter-by-era Run2022C 

## Muon ##
python buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
python buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python buildJSONfromNano.py --datasets Muon --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3



## EGamma ##
python buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v2 
python buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v2
python buildJSONfromNano.py --datasets EGamma --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v2


## JetHT ##
python buildJSONfromNano.py --datasets JetHT --inpath $inpath --filterjson $golden --filter-by-era Run2022C

## MET ##
python buildJSONfromNano.py --datasets MET --inpath $inpath --filterjson $golden --filter-by-era Run2022C

## JetMET ##
python buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v2
python buildJSONfromNano.py --datasets JetMET --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3


## MuonEG ##
python buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
python buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
python buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022D --filter-by-version v1-v1
python buildJSONfromNano.py --datasets MuonEG --inpath $inpath --filterjson $golden --filter-by-era Run2022E --filter-by-version v1-v3


