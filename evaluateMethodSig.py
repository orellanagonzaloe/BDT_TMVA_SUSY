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


parser = argparse.ArgumentParser()

parser.add_argument('--methodsPath', dest='methodsPath', type=str, default=None)
parser.add_argument('--outputDir', dest='outputDir', type=str, default='./')
parser.add_argument('--config', dest='config', type=str, default='config.yaml')

args = parser.parse_args()

outputDir = args.outputDir
methodsPath = args.methodsPath
config = args.config


if not os.path.exists(outputDir):
	os.makedirs(outputDir)

if methodsPath.endswith('/'): methodsPath = methodsPath[:-1]

with open('%s/config.yaml' % (methodsPath), 'r') as f:
	trainCfg = yaml.safe_load(f)

with open('%s' % (config), 'r') as f:
	cfg = yaml.safe_load(f)

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
from ROOT import evaluateMethodSig

if cfg['samplesBkg'] == None: cfg['samplesBkg'] = []
if cfg['samplesSig'] == None: cfg['samplesSig'] = []

for sample in cfg['samplesBkg'] + cfg['samplesSig']:

	print 'Sample: %s' % sample

	isSignal = sample in cfg['samplesSig']
	isPhZ = '_phZ' in sample

	for year in cfg['years']:

		print 'Year: %s' % year

		h_passEvents = ROOT.TH2D('h_passEvents', 'h_passEvents', nMethods, 0, nMethods, cfg['plotPointsMethod'], 0, cfg['plotPointsMethod'])
		h_passEvents.SetDirectory(0)

		for sampleSlice in sam.samples_dict[sample]:

			print sampleSlice

			DID = sampleSlice.split('/')[-1].split('.')[1]
			xs = xsu.get_xs_from_did(int(DID))
			samplePath = '%s/%s*%s*' % (cfg['samplesPath'], sampleSlice, utils.campaign_tag[year])

			if isSignal and cfg['useTestForPlotSig']: 

				samplePath = '%s/%s*%s*test*' % (cfg['TMVAsamplesPath'], sampleSlice, utils.campaign_tag[year])

			if not isSignal and cfg['useTestForPlotBkg']: 

				samplePath = '%s/%s*%s*test*' % (cfg['TMVAsamplesPath'], sampleSlice, utils.campaign_tag[year])

			sampleDir = glob.glob(samplePath)

			if len(sampleDir) != 1:
				utils.print_msj('Empty sample %s' % samplePath, 0)
				continue

			sampleDir = sampleDir[0]

			w_lumi_pseudo = (utils.lumi_dict[year] * xs)

			if sample in cfg['alpha']:
				w_lumi_pseudo *= cfg['alpha'][sample]

			ROOT.evaluateMethodSig(h_passEvents, sampleDir, weightsDir, w_lumi_pseudo, trainVars, specVars, trainMethods, methodsRangeDn, methodsRangeUp, cfg['plotPointsMethod'], isSignal, isPhZ)


		# h_passEvents.Print('all')

		outputFile = '%s/h_pass_%s_%s.root' % (outputDir, sample, year)
		output_sample_file = ROOT.TFile(outputFile, 'RECREATE')
		h_passEvents.Write('h_passEvents')
		output_sample_file.Close()

		print '%s created' % outputFile
