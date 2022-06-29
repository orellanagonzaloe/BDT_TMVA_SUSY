#! /usr/bin/bash

signal=$1
tag=$2
outputDir=$3
config=$4

echo "Signal sample: $signal"

pwd
ls

echo "Setting up ATLAS..."
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -- # the 2 dashes are to avoid problems with negative mu

echo "Configuring ROOT"

. /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh

echo "Starting trainMethods.py"

python trainMethods.py --signal "$signal" --tag "$tag" --outputDir "$outputDir" --config "$config" 2>&1 > log_"$signal".txt

echo "ls:"

ls

echo "Finished trainMethods.py"

ls

mv log_"$signal".txt "$outputDir"/trainOutput_"$tag"_"$signal"/

ls "$outputDir"/trainOutput_"$tag"_"$signal"
