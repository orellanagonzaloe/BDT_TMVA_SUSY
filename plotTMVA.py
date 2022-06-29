#! /usr/bin/env python

import os
import sys
import math
import argparse
import glob
import shutil

import ROOT
ROOT.gROOT.SetBatch(True)

inputFile = '/eos/user/g/goorella/PhX_TMVA/EWK_v3/trainOutput_EWK_v3_GGM_N1N2C1_phb_450/EWK_v3_GGM_N1N2C1_phb_450.root'
dirName = 'DL_EWK_v3_GGM_N1N2C1_phb_450'
outputDir = '/eos/user/g/goorella/plots/PhX_TMVA/DL_EWK_v3_GGM_N1N2C1_phb_450/plots/'


if not os.path.exists(dirName):
	os.makedirs(dirName)

if not os.path.exists(outputDir):
	os.makedirs(outputDir)



rootFile = ROOT.TFile.Open(inputFile)

keylist = ROOT.TMVA.GetKeyList('InputVariables')

keylist = rootFile.GetDirectory(dirName).GetListOfKeys()

for varKey in keylist:

	str_varKey = varKey.GetName()

	if not 'InputVariables' in str_varKey: continue

	title = 'Input variables %s-transformed (training sample)' % str_varKey.replace('InputVariables_','')

	if 'Id' in str_varKey: title = 'Input variables (training sample)'

	ROOT.TMVA.variables(dirName, inputFile, str_varKey, title)

ROOT.TMVA.correlations(dirName, inputFile)

ROOT.TMVA.efficiencies(dirName, inputFile, 1)
ROOT.TMVA.efficiencies(dirName, inputFile, 2)
ROOT.TMVA.efficiencies(dirName, inputFile, 3)


ROOT.TMVA.mvas(dirName, inputFile)
ROOT.TMVA.mvas(dirName, inputFile, ROOT.TMVA.kCompareType)
ROOT.TMVA.mvas(dirName, inputFile, ROOT.TMVA.kProbaType)
ROOT.TMVA.mvas(dirName, inputFile, ROOT.TMVA.kRarityType)

ROOT.TMVA.BDT(dirName, inputFile)
ROOT.TMVA.BDTControlPlots(dirName, inputFile)

os.system('mv %s/plots/* %s' % (dirName, outputDir))
os.system('rm -r %s' % dirName)


