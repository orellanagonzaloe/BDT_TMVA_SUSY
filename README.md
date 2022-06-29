BDT with TMVA
=========================

Tool to train a BDT (or other methods) with TMVA from ROOT to discriminate signal from background in a SUSY EWK analysis


## Create train and test ntuples 

Despite TMVA has a method to create train and test samples, we use a custom script to do it. You can avoid this step if you want to use TMVA to create test and train samples.

Run `createTrainTestSamples.py` to create a new set of ntuples for train and test. This script uses a YAML config passed in the `--config` argument and runs `createTrainTestSamples.cxx`. In the latter are defined the variables stored in the new ntuples and the possible event filter as well. Ntuples are read from `samplesPath` and new ntuples are stored in `TMVAsamplesPath` from the config. Also in the config are declared the signal and background samples to run (`samplesSig` and `samplesBkg`), and the percentage of events kept for train and test in `trainTestSplit`, which can be customizable for each separate sample.


## Train methods

To train methods you have to use `trainMethods.py` with the following arguments
	
	--mN1: list of N1 masses to use for training
	--BRs: list BRs of the N1, BR_y, BR_Z, BR_h
	--year: years of datasets
	--outputDir: output directory
	--config: config file
	--tag: tag to identify run

The script will read the following arguments from the configfile
	
	dataSelectionOptions: option in TMVA for the splitting of samples located in samplesPath. Leave blank if you want to use your custom splitting located in TMVAsamplesPath
	dataPreparation: option of TMVA
	samplesSig and samplesBkg: signal and background samples used for training
	sampleTF: transfer factor from CRs obtained in the cut&count experiment
	eventByEventWeight: option of TMVA
	trainVars: option of TMVA
	specVars: option of TMVA
	preselCuts: option of TMVA

The trained methods are stored in:

## Plots 