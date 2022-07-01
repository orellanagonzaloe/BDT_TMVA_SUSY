#! /usr/bin/env python

import os
import sys
import argparse
import glob
import yaml
import copy

import ROOT

import xsutils as xsu
import samples as sam
import utils as utils
from utils import printMsg


parser = argparse.ArgumentParser()

parser.add_argument('--methodsPath', dest='methodsPath', type=str, default=None)
parser.add_argument('--nPoints', dest='nPoints', type=int, default=20)
parser.add_argument('--samplesBkg', dest='samplesBkg', nargs='+')
parser.add_argument('--samplesSig', dest='samplesSig', nargs='+')
parser.add_argument('--mN1test', dest='mN1test', nargs='+')
parser.add_argument('--N1BRs', dest='N1BRs', nargs='+') # BR_y, BR_Z, BR_h
parser.add_argument('--year', dest='year', nargs='+', default=['2015', '2016', '2017', '2018'])


args = parser.parse_args()

methodsPath = args.methodsPath

if methodsPath.endswith('/'): methodsPath = methodsPath[:-1]

with open('%s/config.yaml' % (methodsPath), 'r') as f:
	trainCfg = yaml.safe_load(f)

trainCfg['plotPointsMethod'] = args.nPoints

with open('%s/config.yaml' % (methodsPath), 'w+') as f:
	data = yaml.dump(trainCfg, f)

if args.samplesSig: samplesSig = args.samplesSig
else: samplesSig = trainCfg['samplesSig']

if args.samplesBkg: samplesBkg = args.samplesBkg
else: samplesBkg = trainCfg['samplesBkg']

if args.mN1test: mN1test = args.mN1test
else: mN1test = trainCfg['mN1train']

if args.N1BRs: N1BRs = args.N1BRs
else: N1BRs = trainCfg['N1BRs']

if args.year: _years = args.year
else: _years = trainCfg['year']

tag = trainCfg['tag']

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

utils.define_weights(trainCfg['eventByEventWeight'])

BRs = N1BRs.split(',')
BR_y, BR_Z, BR_h = float(BRs[0]), float(BRs[1]), float(BRs[2])
utils.reweight_event(BR_y, BR_Z, BR_h)

ROOT.gInterpreter.Declare(open('lib/evaluateMethodSig.cxx').read())



for sample in samplesBkg + samplesSig:

	isSignal = sample in samplesSig

	years = copy.deepcopy(_years)

	if not utils.isdata(sample) and '2015' in years and '2016' in years:
		years.remove('2015')
		years.remove('2016')
		years.insert(0, '20152016')

	for year in years:

		h_passEvents = ROOT.TH2D('h_passEvents', 'h_passEvents', nMethods, 0, nMethods, trainCfg['plotPointsMethod'], 0, trainCfg['plotPointsMethod'])
		h_passEvents.SetDirectory(0)

		_sample = sample

		if utils.isdata(sample):

			_sample = '%s%s' % (sample, year[-2:])

		for sampleSlice in sam.samples_dict[_sample]:

			printMsg('Evaluating %s %s %s' % (sample, year, sampleSlice), 0)

			globDir = '%s/%s.*.%s.*' % (trainCfg['samplesPath'], sampleSlice, utils.campaign_tag[year])

			if sample in trainCfg['samplesWithTestSample']:

				globDir = '%s/%s.*_test' % (trainCfg['TMVAsamplesPath'], sampleSlice)

			print globDir
			sampleDir = glob.glob(globDir)

			if len(sampleDir) != 1:
				printMsg('Empty sample %s' % sampleDir, 1)
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

