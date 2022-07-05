#! /usr/bin/env python

import os
import sys
import argparse
import glob
import shutil
import yaml

import ROOT

import samples as sam
import xsutils as xsu
import utils as utils
from utils import printMsg

parser = argparse.ArgumentParser()

parser.add_argument('--mN1train', dest='mN1train', nargs='+', required=True)
parser.add_argument('--N1BRs', dest='N1BRs', nargs='+', required=True) # BR_y, BR_Z, BR_h
parser.add_argument('--year', dest='year', nargs='+', default=['2015', '2016', '2017', '2018'])
parser.add_argument('--outputDir', dest='outputDir', type=str, default='./')
parser.add_argument('--config', dest='config', type=str, default='config.yaml')
parser.add_argument('--tag', dest='tag', type=str, default='Default')

args = parser.parse_args()

printMsg('N1 masses used for training: %s' % ' '.join(args.mN1train), 0)
printMsg('N1 BRs: %s' % ' '.join(args.N1BRs), 0)
printMsg('Years: %s' % ' '.join(args.year), 0)
printMsg('Output Dir: %s' % args.outputDir, 0)
printMsg('Config file: %s' % args.config, 0)
printMsg('Tag: %s' % args.tag, 0)

#--- initialization

tag = '%s_%s_%s'% (args.tag, '_'.join(args.mN1train), '_'.join(args.N1BRs).replace('.', 'p'))

with open(args.config, 'r') as f:
	cfg = yaml.safe_load(f)

outputDir = '%s/trainOutput_%s' % (args.outputDir, tag)

if not os.path.exists(outputDir):
	os.makedirs(outputDir)

cfg['tag'] = tag
cfg['mN1train'] = ','.join(args.mN1train)
cfg['N1BRs'] = ','.join(args.N1BRs)
cfg['year'] = ','.join(args.year)

with open('%s/config.yaml' % (outputDir), 'w+') as f:
	data = yaml.dump(cfg, f)

outputFilename = '%s/%s.root' % (outputDir, tag)
outFile = ROOT.TFile(outputFilename, 'RECREATE')

print args.N1BRs
print args.N1BRs[0]
print args.N1BRs[1]
print args.N1BRs[2]
print float(args.N1BRs[0])


BR_y, BR_Z, BR_h = float(args.N1BRs[0]), float(args.N1BRs[1]), float(args.N1BRs[2])
utils.reweight_event(BR_y, BR_Z, BR_h)

#--- factory

factory = ROOT.TMVA.Factory(tag, outFile, cfg['factoryOptions'])
	
dataloader = ROOT.TMVA.DataLoader('DL_%s' % (tag))

#--- signal and background files

if not cfg['dataSelectionOptions']:

	types = ['test', 'train']
	samplePath = cfg['TMVAsamplesPath']
	dataPreparation = cfg['dataPreparation']

else:

	types = ['test and train']
	samplePath = cfg['samplesPath']
	dataPreparation = ':'.join([cfg['dataSelectionOptions'], cfg['dataPreparation']])

sigForTrain = [x for x in cfg['samplesSig'] for y in args.mN1train if y == x.split('_')[-1]]


for sampleType in types:

	for sample in cfg['samplesBkg'] + sigForTrain:

		years = args.year

		if not utils.isdata(sample) and '2015' in years and '2016' in years:
			years.remove('2015')
			years.remove('2016')
			years.insert(0, '20152016')

		for year in years:

			printMsg('Adding %s %s %s' % (sample, year, sampleType), 0)

			_sample = sample

			if utils.isdata(sample):

				_sample = '%s%s' % (sample, year[-2:])

			for sampleSlice in sam.samples_dict[_sample]:

				globFiles = '%s/%s.*.%s.*_%s/*.root*' % (samplePath, sampleSlice, utils.campaign_tag[year], sampleType)

				if utils.isdata(sample):
					globFiles = '%s/%s.*_%s/*.root*' % (samplePath, sampleSlice, sampleType)

				samplesFiles = glob.glob(globFiles)

				if len(samplesFiles)<1:
					printMsg('Empty sample %s' % globFiles, 1)
					continue

				sampleTree = ROOT.TChain('mini')

				sumw = 0.

				for file in samplesFiles:

					rootFile = ROOT.TFile.Open(file)

					if not rootFile or rootFile.IsZombie():
						printMsg('%s does not exist or is corrupted' % file, 2)
						continue
					if not rootFile.GetListOfKeys().Contains('events'):
						printMsg('\'events\' histogram not in %s' % file, 2)
						continue

					sampleTree.Add(file)

					sumw += rootFile.Get('events').GetBinContent(3) # bin 3 is the initial sumw

					rootFile.Close()

				if sampleTree.GetEntries()<1:
					printMsg('%s: has 0 events, skipping...' % globFiles, 1)
					continue

				weight = 1.

				if not utils.isdata(sample):

					DID = sampleSlice.split('.')[1]
					xs = xsu.get_xs_from_did(int(DID))

					weight = (utils.lumi_dict[year] * xs) / sumw

					if sample in cfg['sampleTF']:
						weight *= cfg['sampleTF'][sample]

				if sample in cfg['samplesBkg']:

					dataloader.AddBackgroundTree(sampleTree, weight, sampleType)

				else:

					dataloader.AddSignalTree(sampleTree, weight, sampleType)



#--- Event by event weights

printMsg('Set event by event weights', 0)

dataloader.SetBackgroundWeightExpression(cfg['eventByEventWeight'])

dataloader.SetSignalWeightExpression('%s*%s' % (cfg['eventByEventWeight'], 'reweight_event(n1decays)'))


#--- Variables

printMsg('Add variables for training and specting', 0)

for var in cfg['trainVars']:
	dataloader.AddVariable(var[0], var[1], var[2], var[3])

for var in cfg['specVars']:
	dataloader.AddSpectator(var[0], var[1], var[2])


#--- Preselection

printMsg('Add preselection cuts and prepare data', 0)

dataloader.PrepareTrainingAndTestTree(cfg['preselCuts'].strip(), dataPreparation)


#--- Method specification

printMsg('Book methods', 0)

for method in cfg['trainMethods']:

	printMsg('Adding %s...' % method[0], 0)

	factory.BookMethod(dataloader, utils.trainMethods[method[1]], method[0], method[2])


#--- ??? (STILL EXPERIMENTAL and only implemented for BDT's)

# factory.OptimizeAllMethods('SigEffAtBkg0.01','Scan')


#--- Training and Evaluation

printMsg('Train, test and evaluate methods', 0)

factory.TrainAllMethods()
factory.TestAllMethods()
factory.EvaluateAllMethods()


#--- Clean up

outFile.Close()


shutil.move('DL_%s' % (tag), outputDir)