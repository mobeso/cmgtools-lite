inpath="/lustrefs/hdd_pool_dir/nanoAODv12/24october2023/data/"
golden="Cert_Collisions2022_355100_362760_Golden.json"


# DoubleMuon ##
#python3 buildJSONfromNano.py --datasets DoubleMuon --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C 
#
### SingleMuon ##
#python3 buildJSONfromNano.py --datasets SingleMuon --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C 
#
### Muon ##
#python3 buildJSONfromNano.py --datasets Muon --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
#python3 buildJSONfromNano.py --datasets Muon --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
#python3 buildJSONfromNano.py --datasets Muon --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022E --filter-by-version v1
#python3 buildJSONfromNano.py --datasets Muon --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022F --filter-by-version v2
#python3 buildJSONfromNano.py --datasets Muon --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022G --filter-by-version v1
#
#
#
### EGamma ##
#python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
#python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
#python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022E --filter-by-version v1
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022F --filter-by-version v1
python3 buildJSONfromNano.py --datasets EGamma --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022G --filter-by-version v2
#
#
### JetHT ##
#python3 buildJSONfromNano.py --datasets JetHT --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C
#
### MET ##
#python3 buildJSONfromNano.py --datasets MET --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C
#
### JetMET ##
#python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
#python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
#python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022E --filter-by-version v1
#python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022F --filter-by-version v2
#python3 buildJSONfromNano.py --datasets JetMET --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022G --filter-by-version v1



## MuonEG ##
#python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022C --filter-by-version v1 
#python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath/2022 --filterjson $golden --filter-by-era Run2022D --filter-by-version v1
#python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022E --filter-by-version v1
#python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022F --filter-by-version v1
#python3 buildJSONfromNano.py --datasets MuonEG --inpath $inpath/2022PostEE --filterjson $golden --filter-by-era Run2022G --filter-by-version v1
#
