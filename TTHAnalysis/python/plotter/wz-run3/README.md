# WZ Run3 analysis folder
## Disclaimer
Every script must be run from the root folder, i.e., `wz-run3`. Otherwise there will be import problems.

## Logistics
### Important paths
 * nanoAODv11 of Run3 MC and data is stored in: `/beegfs/data/nanoAODv11/30march2023/`
   * Postprocess trees are stored in `/beegfs/data/nanoAODv11/wz/trees/`

## Generate config files to run postprocessing over MC or data
Use the `create_sample_cfg.py` script to automatically write the CFG as follows:
```
# For nanoAODv11
# MC 2022
python3 create_sample_cfg.py -w
python3 create_sample_cfg.py --year 2022EE -w
# Data 2022
python3 create_sample_cfg.py --isData -w
python3 create_sample_cfg.py --isData --year 2022EE -w
```
This reads `cfgs/datasets_cfg.py` and uses the metadata in there to generate postprocessing config files.
If the option `-w` is not given, then a printout summarizing all the samples that are used will appear in
the prompt.

## How to run the postprocessing 
This step basically runs over raw nanoAOD and performs:
 1. An skimming that keeps only 2 same-sign lepton events.
 2. When running over data, it removes trigger overlap between datasets.
 3. Adds a few branches for dataset metadata (cross sections, a tag that identifies data or mc, etc...)
 4. Run3 Lepton MVA evaluation.

**For MC**
```
cd $CMSSW_BASE/src/CMGTools/cfg
python3 ../python/plotter/wz-run3/wz-run.py postproc
```

**For Data**
```
cd $CMSSW_BASE/src/CMGTools/cfg
python3 ../python/plotter/wz-run3/wz-run.py postproc --isData
```

**Merge chunks (not recommended)**
**Note**: the scripts work, but for some cases there are inconsistencies in the merging of some samples, so the use of this is not recommended.
```
cd $CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/wz-run3/scripts/
python3 doChunkStuff.py --mode postproc --inpath $PATH_TO_POSTPROC_OUTPUT 
```
This will submit a job to merge the output of the postprocessing in single root files. Samples will be splitted if need so that the maximum size of the merged file is not larger than 15 Gb.
## Friend trees
**In general**:
```
cd $CMSSW_BASE/src/CMGTools/macros
python3 ../python/plotter/wz-run3/wz-run.py friend --step $STEP
```

Now just change step for:

  * **1**: for JME corrections.
  * **2**: for lepton-jet recleaning.
  * **3**: for lepton variable builder.
  * **4**: for definition of the trigger strategy.
  * **5**: for scalefactors

By default this will run for MC of 2022, in order to run over data just add `--isData` to the command above, and in order to run over 2022EE data or MC use `--year 2022EE`. To merge output friends do:

```
cd $CMSSW_BASE/src/CMGTools/TTHAnalysis/python/plotter/wz-run3/scripts/
python3 doChunkStuff.py --mode friend --inpath $PATH_TO_FRIEND_CHUNKS
```

## Generate analysis files
This is basically writing mca files automatically based on the information stored under `cfgs/datasets_cfg.py`.

```
python3 write_mca.py
```

This will:
 * Generate mca individual files for each group of processes as defined in the dictionary of datasets.
 * Generate a global mca file which includes all the generated individual mcas.

 **<span style="color:RED">NOTE</span>**: There are some issues with the dataset name matching. WW gets matched in the WWZ line as well, so it's included twice.

 ## Run trigger efficiencies
 All the results for the trigger efficiency measurements can be repeated by executing the following commands:

 **Generate yields/plots for both numerator (PR+HLT) and denominator (PR) region.**
 ```
 ./wz-run3/scripts/make_plots.sh trigger_eff --ncores 16 --outname wz-run3/scripts/trigger_efficiencies --do-submit
 ```
 **Produce table with trigger efficiencies, yields and SFs.**
 ```
 cd wz-run3/scripts/
 python3 get_triggerSF.py
 ```
