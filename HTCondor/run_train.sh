#! /usr/bin/bash

mN1train=$1
N1BRs=$2
year=$3
tag=$4
outputDir=$5
config=$6

mN1train=${mN1train//_/ }
N1BRs=${N1BRs//_/ }
year=${year//_/ }

echo "Signal samples to train: $mN1train"
echo "N1 with BR: $N1BRs"
echo "Years: $year"
echo "Tag: $tag"
echo "Output dir: $outputDir"
echo "Config: $config"

pwd
ls

N1BRsclean=${N1BRs//./p}

echo "Setting up ATLAS..."
export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase
source $ATLAS_LOCAL_ROOT_BASE/user/atlasLocalSetup.sh -- # the 2 dashes are to avoid problems with negative mu

echo "Configuring ROOT"

. /cvmfs/sft.cern.ch/lcg/app/releases/ROOT/6.22.02/x86_64-centos7-gcc48-opt/bin/thisroot.sh

echo "setting up libraries"

export SUSY_ANALYSIS=$PWD
export PLOTTOOLS="PlotTools/"
export PATH=$SUSY_ANALYSIS/scripts:$PLOTTOOLS:$PATH
export PYTHONPATH=$SUSY_ANALYSIS/lib:$SUSY_ANALYSIS/methods:$PLOTTOOLS:$PYTHONPATH

echo "Starting trainMethods.py"

python trainMethods.py --mN1train $mN1train --N1BRs $N1BRs --year $year --tag "$tag" --outputDir "$outputDir" --config "$config" 2>&1 > log_"${mN1train// /_}"_"${N1BRsclean// /_}".txt

echo "ls:"

ls

echo "Finished trainMethods.py"

ls

mv log_"${mN1train// /_}"_"${N1BRsclean// /_}".txt "$outputDir"/trainOutput_"$tag"_"${mN1train// /_}"_"${N1BRsclean// /_}"/

ls "$outputDir"/trainOutput_"$tag"_"${mN1train// /_}"_"${N1BRsclean// /_}"
