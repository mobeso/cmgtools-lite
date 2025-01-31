#!/bin/bash
# Mostly based on @vischia's implementation at https://github.com/vischia/stopLimits/blob/master/estimateImpact.sh

# Usage: sh estimateImpact.sh [DATACARD NAME] [What to use as data: d (data), t0 (background only Asimov), t1 (s+b Asimov)] [Number of parallel jobs]  [OUTPUT shortname] [Extra commands to be feeded to combineToools]

# Prerequisite: installing the combineTool.py tool.
#       Method 1 (install only the script):
#                  bash <(curl -s https://raw.githubusercontent.com/cms-analysis/CombineHarvester/master/CombineTools/scripts/sparse-checkout-ssh.sh)
#       Method 2 (install the whole CombineHarvester):
#                  cd $CMSSW_BASE/src
#                  git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester
#                  scram b -j 4


DATACARD=$1
ASIMOV=$2
JOBS=$3
OUTPUT=$4
EXTRA=$5
HERE="$PWD/"

 
if [ "$DATACARD" = "" ]; then
   echo "You need to provide a datacard!!"
   exit
fi

if [ "$ASIMOV" = "" ]; then
   echo "Defaulting to data"
fi

if [ "$ASIMOV" = "d" ]; then
   echo "Using data"
   ASIMOV=""
   PREFIX="d"
fi

if [ "$ASIMOV" = "t0" ]; then
   echo "Using background-only Asimov dataset"
   ASIMOV=" -t -1 --expectSignal 0 --rMin -10"
   PREFIX="t0"
fi

if [ "$ASIMOV" = "t1" ]; then
   echo "Using signal + background Asimov dataset"
   ASIMOV=" -t -1 --setParameters r=1 "
   PREFIX="t1"
fi

if [  "$JOBS" = ""  ]; then
    JOBS=1
    echo "Defaulting to 1 parallel job"
fi

if [ "$OUTPUT" = "" ]; then
   OUTPUT="impacts"   
fi

cd $OUTPUT


echo "---------------------------------"
echo "---------------------------------"

echo "You are about to run impacts for datacard $DATACARD with $JOBS parallel jobs. Additional toy options are set to $ASIMOV. Extra parameters to be passed to combine are: $EXTRA" 

echo "---------------------------------"
echo "---------------------------------"


if [[ "$DATACARD" != *"root"* ]]; then
   echo "Preliminary: convert to rootspace"
   echo "---------------------------------"
   text2workspace.py $HERE/${DATACARD}
   DATACARD="${DATACARD//.txt/.root}"
   echo "Card is $DATACARD"
fi



echo "First Stage: fit for each POI"
echo "-----------------------------"

combineTool.py -M Impacts -d $HERE/${DATACARD} --doInitialFit --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 $ASIMOV $EXTRA -m 1 -n $PREFIX --floatOtherPOIs 1 --parallel $JOBS --cminDefaultMinimizerType Minuit


echo "Second Stage: fit scan for each nuisance parameter"
echo "--------------------------------------------------"

combineTool.py -M Impacts -d $HERE/${DATACARD} --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --doFits $ASIMOV $EXTRA -m 1 -n $PREFIX --parallel $JOBS --cminDefaultMinimizerType Minuit

echo "Third Stage: collect outputs"
echo "----------------------------"

combineTool.py -M Impacts -d $HERE/${DATACARD} --robustFit 1 --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 -o impacts$PREFIX.json $ASIMOV $EXTRA -m 1 -n $PREFIX --parallel $JOBS --cminDefaultMinimizerType Minuit

echo "Fourth Stage: plot pulls and impacts"
echo "------------------------------------"

plotImpacts.py -i impacts$PREFIX.json -o impacts$PREFIX

cp $HERE/$DATACARD ./
cd $HERE
