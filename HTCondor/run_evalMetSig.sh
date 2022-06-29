#! /usr/bin/bash

methodsPath=$1
outputDir=$2

pwd
ls

echo "Setting up ATLAS..."
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -- # the 2 dashes are to avoid problems with negative mu

echo "Configuring ROOT"

. /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh


echo "Starting evaluateMethodSig.py"

python evaluateMethodSig.py --methodsPath "$methodsPath" --outputDir "$outputDir"

ls

echo "Finished evaluateMethodSig.py"


