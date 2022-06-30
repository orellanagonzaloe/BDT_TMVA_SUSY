#! /usr/bin/env python

import argparse
import yaml
import glob

import ROOT

import samples as sam
from utils import printMsg


parser = argparse.ArgumentParser()

parser.add_argument('--config', dest='config', type=str, default='config.yaml')
args = parser.parse_args()

with open(args.config, 'r') as f:
	cfg = yaml.safe_load(f)



samplesPath = cfg['samplesPath']


for sample in cfg['samplesBkg']+cfg['samplesSig']:

	printMsg('Sample: %s' % (sample), 0)

	if sample in cfg['trainTestSplit']: 

		trainTestSplit = cfg['trainTestSplit'][sample]

	elif sample in cfg['samplesSig']: 

		trainTestSplit = cfg['trainTestSplit']['signal']

	elif sample in cfg['samplesBkg']:

		trainTestSplit = cfg['trainTestSplit']['bkg']

	printMsg('trainTestSplit: %d%%' % (trainTestSplit), 0)

	for sampleSlice in sam.samples_dict[sample]:

		globDir = '%s/%s*' % (samplesPath, sampleSlice)
		inputDirs = glob.glob(globDir)

		for inDir in inputDirs:

			outputDir = '%s/' % (cfg['TMVAsamplesPath'])

			processLine = '.x lib/createTrainTestSamples.cxx(\"%s\", \"%s\", %f)' % (inDir, outputDir, trainTestSplit)

			ROOT.gROOT.ProcessLine(processLine)

