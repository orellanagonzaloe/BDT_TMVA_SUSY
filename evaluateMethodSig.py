#! /usr/bin/env python

import os
import sys
import math
import argparse
import glob
import array
import yaml

import ROOT

import xsutils as xsu
import samples as sam
import utils as utils
from utils import printMsg


parser = argparse.ArgumentParser()

parser.add_argument('--methodsPath', dest='methodsPath', type=str, default=None)
parser.add_argument('--nPoints', dest='nPoints', type=int, default=20)
parser.add_argument('--samplesBkg', dest='sample', nargs='+')
parser.add_argument('--samplesSig', dest='sample', nargs='+')

args = parser.parse_args()

methodsPath = args.methodsPath

if methodsPath.endswith('/'): methodsPath = methodsPath[:-1]

if args.samplesSig: samplesSig = args.samplesSig
else samplesSig = trainCfg['samplesSig']

if args.samplesBkg: samplesBkg = args.samplesBkg
else samplesBkg = trainCfg['samplesBkg']

with open('%s/config.yaml' % (methodsPath), 'r') as f:
	trainCfg = yaml.safe_load(f)

trainCfg['plotPointsMethod'] = args.nPoints

with open('%s/config.yaml' % (methodsPath), 'w+') as f:
	data = yaml.dump(trainCfg, f)

tag = trainCfg['tag']
signal = trainCfg['signal']

weightsDir = '%s/DL_%s/weights/%s_' % (methodsPath, tag, tag)

nMethods = len(trainCfg['trainMethods'])

trainVars = ROOT.std.vector('TString')()
for var in trainCfg['trainVars']:
	trainVars.push_back(var[0])

specVars = ROOT.std.vector('TString')()
for var in trainCfg['specVars']:
	specVars.push_back(var[0])

trainMethods = ROOT.std.vector('TString')()
methodsRangeDn = ROOT.std.vector('double')()
methodsRangeUp = ROOT.std.vector('double')()

for method in trainCfg['trainMethods']:
	trainMethods.push_back(method[0])
	methodsRangeDn.push_back(utils.methodsRange[method[1]][0])
	methodsRangeUp.push_back(utils.methodsRange[method[1]][1])

utils.presel_cut(trainCfg['preselCuts'].replace('[0]', '->at(0)'))

ROOT.gInterpreter.Declare(open('lib/evaluateMethodSig.cxx').read())

BRs = trainCfg['BRs'].split(',')
BR_y, BR_Z, BR_h = args.BRs[0], args.BRs[1], args.BRs[2]
utils.reweight_event(BR_y, BR_Z, BR_h)


for sample in samplesBkg + samplesSig:

	isSignal = sample in samplesSig

	for year in trainCfg['years']:

		h_passEvents = ROOT.TH2D('h_passEvents', 'h_passEvents', nMethods, 0, nMethods, trainCfg['plotPointsMethod'], 0, trainCfg['plotPointsMethod'])
		h_passEvents.SetDirectory(0)

		for sampleSlice in sam.samples_dict[sample]:

			printMsg('Evaluating %s %s %s' % (sample, year, sampleSlice), 0)

			samplePath = '%s/%s*%s*' % (trainCfg['samplesPath'], sampleSlice, utils.campaign_tag[year])

			if isSignal and trainCfg['useTestForPlotSig']: 

				samplePath = '%s/%s*%s*_test' % (trainCfg['TMVAsamplesPath'], sampleSlice, utils.campaign_tag[year])

			if not isSignal and trainCfg['useTestForPlotBkg']: 

				samplePath = '%s/%s*%s*_test' % (trainCfg['TMVAsamplesPath'], sampleSlice, utils.campaign_tag[year])

			sampleDir = glob.glob(samplePath)

			if len(sampleDir) != 1:
				printMsj('Empty sample %s' % samplePath, 1)
				continue

			sampleDir = sampleDir[0]

			globFiles = '%s/*.root*' % (sampleDir)
			samplesFiles = glob.glob(globFiles)

			if len(samplesFiles)<1:
				printMsg('Empty sample %s' % globFiles, 1)
				continue

			sumw = 0.

			for file in samplesFiles:

				rootFile = ROOT.TFile.Open(file)

				if not rootFile or rootFile.IsZombie():
					printMsg('%s does not exist or is corrupted' % file, 2)
					continue
				if not rootFile.GetListOfKeys().Contains('events'):
					printMsg('\'events\' histogram not in %s' % file, 2)
					continue

				sumw += rootFile.Get('events').GetBinContent(3) # bin 3 is the initial sumw

				rootFile.Close()

			weight = 1.

			if not utils.isdata(sample):

				DID = sampleSlice.split('.')[1]
				xs = xsu.get_xs_from_did(int(DID))

				weight = (utils.lumi_dict[year] * xs) / sumw

				if sample in trainCfg['sampleTF']:
					weight *= trainCfg['sampleTF'][sample]

			ROOT.evaluateMethodSig(h_passEvents, sampleDir, weightsDir, weight, trainVars, specVars, trainMethods, methodsRangeDn, methodsRangeUp, trainCfg['plotPointsMethod'], isSignal)


		# h_passEvents.Print('all')

		outputFile = '%s/h_pass_%s_%s.root' % (methodsPath, sample, year)
		output_sample_file = ROOT.TFile(outputFile, 'RECREATE')
		h_passEvents.Write('h_passEvents')
		output_sample_file.Close()

		printMsg('%s created' % outputFile, 0)

