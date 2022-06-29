#! /usr/bin/env python

import os
import sys
import math
import argparse
import glob
import array
import yaml

import ROOT
ROOT.gROOT.SetBatch(True)

import utils as utils
import style as sty

import plotFunc as PTf
import classes as PTc


def retrieveHistos(methodsPath, histPath, cfg, trainCfg):

	d_passEvents = {}
	TG_sig = {}
	h_method = {}

	for method in trainCfg['trainMethods']:

		d_passEvents[method[0]] = {}
		TG_sig[method[0]] = {}
		h_method[method[0]] = {}

		for sam in cfg['samplesBkg'] + cfg['samplesSig']:

			d_passEvents[method[0]][sam] = [0.] * trainCfg['plotPointsMethod']



	for i_method, method in enumerate(trainCfg['trainMethods']):

		d_passEvents[method[0]]['total_bkg'] = [0.] * trainCfg['plotPointsMethod']

		start = utils.methodsRange[method[1]][0]
		end = utils.methodsRange[method[1]][1]

		h_method[method[0]]['total_bkg'] = ROOT.TH1D('%s_total_bkg' % (method[0]), '%s_total_bkg' % (method[0]), trainCfg['plotPointsMethod'], start, end)

		for sam in cfg['samplesBkg']:

			h_method[method[0]][sam] = ROOT.TH1D('%s_%s' % (method[0], sam), '%s_%s' % (method[0], sam), trainCfg['plotPointsMethod'], start, end)

			d_passEvents[method[0]][sam] = [0.] * trainCfg['plotPointsMethod']

			for year in cfg['years']:

				output_sam_file = ROOT.TFile('%s/h_pass_%s_%s.root' % (histPath, sam, year), 'READ')
				h_pass_tmp = output_sam_file.Get('h_passEvents')
				h_pass_tmp.SetDirectory(0)

				for x in xrange(trainCfg['plotPointsMethod']):

					d_passEvents[method[0]][sam][x] += h_pass_tmp.GetBinContent(i_method+1, x+1)
					d_passEvents[method[0]]['total_bkg'][x] += h_pass_tmp.GetBinContent(i_method+1, x+1)

					method_output = start + (end-start)*(x+0.5)/trainCfg['plotPointsMethod']

					h_method[method[0]][sam].Fill(method_output, h_pass_tmp.GetBinContent(i_method+1, x+1))

				output_sam_file.Close()



		for sam in cfg['samplesSig']:

			h_method[method[0]][sam] = ROOT.TH1D('%s_%s' % (method[0], sam), '%s_%s' % (method[0], sam), trainCfg['plotPointsMethod'], start, end)

			h_method[method[0]]['%s_sig' % sam] = ROOT.TH1D('%s_%s_sig' % (method[0], sam), '%s_%s_sig' % (method[0], sam), trainCfg['plotPointsMethod'], start, end)

			d_passEvents[method[0]][sam] = [0.] * trainCfg['plotPointsMethod']

			for year in cfg['years']:

				output_sam_file = ROOT.TFile('%s/h_pass_%s_%s.root' % (histPath, sam, year), 'READ')
				h_pass_tmp = output_sam_file.Get('h_passEvents')
				h_pass_tmp.SetDirectory(0)

				for x in xrange(trainCfg['plotPointsMethod']):

					d_passEvents[method[0]][sam][x] += h_pass_tmp.GetBinContent(i_method+1, x+1)

					method_output = start + (end-start)*(x+0.5)/trainCfg['plotPointsMethod']

					h_method[method[0]][sam].Fill(method_output, h_pass_tmp.GetBinContent(i_method+1, x+1))

				output_sam_file.Close()

			x_tmp, y_tmp = array.array('f'), array.array('f')

			for x in xrange(trainCfg['plotPointsMethod']):

				method_output = start + (end-start)*x/trainCfg['plotPointsMethod']
				bkg_tmp = d_passEvents[method[0]]['total_bkg'][x]
				sig_tmp = d_passEvents[method[0]][sam][x]

				z_tmp = ROOT.RooStats.NumberCountingUtils.BinomialExpZ(sig_tmp, bkg_tmp, 0.3)

				if sig_tmp<3. or bkg_tmp<1. or z_tmp<0. or z_tmp==float('Inf'): z_tmp=0.

				x_tmp.append(method_output)
				y_tmp.append(z_tmp) 

				h_method[method[0]]['%s_sig' % sam].SetBinContent(x+1, z_tmp)

			TG_sig[method[0]]['%s_sig' % sam] = ROOT.TGraph(trainCfg['plotPointsMethod'], x_tmp, y_tmp)

			# TG_sig[method[0]]['%s_sig' % sam].Print('all')

	return d_passEvents, TG_sig, h_method


def plotSignificance(TG_sig, method, methodsPath, cfg, trainCfg, outputDirPlots):

	canvas = ROOT.TCanvas('canvas','canvas', 0, 0, 800, 600)

	color_list = ['#1cd759', '#84c915', '#b9b600', '#e49e00', '#ff811b', '#ff614e', '#ff467c', '#ff41ac', '#e755d9']	

	ROOT.gPad.SetRightMargin(0.05)
	ROOT.gPad.SetTopMargin(0.06)

	mg = ROOT.TMultiGraph()

	legend = ROOT.TLegend(0.15,0.5,0.5,0.91)
	legend.SetNColumns(3)

	# [150, 250, 350, 450, 550, 650, 750, 850, 950, 1050, 1250, 1450]



	for i_color, mN1 in enumerate([150, 250, 350, 450, 550, 650, 750, 850, 950]):

		TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1].SetMarkerStyle(20)
		TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1].SetMarkerSize(1.2)
		TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1].SetLineWidth(2)

		TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1].SetMarkerColor(ROOT.TColor.GetColor(color_list[i_color]))
		TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1].SetLineColor(ROOT.TColor.GetColor(color_list[i_color]))

		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetMarkerStyle(52)
		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetMarkerSize(1.2)
		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetLineWidth(2)
		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetLineStyle(7)

		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetMarkerColor(ROOT.TColor.GetColor(color_list[i_color]))
		TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1].SetLineColor(ROOT.TColor.GetColor(color_list[i_color]))

		legend.AddEntry(TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1], 'phZ', 'pl')
		legend.AddEntry(TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1], 'phb', 'pl')
		legend.AddEntry(TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1], 'mN1 = %i' % mN1, '')

		mg.Add(TG_sig[method[0]]['GGM_N1N2C1_phZ_%i_sig' % mN1])
		mg.Add(TG_sig[method[0]]['GGM_N1N2C1_phb_%i_sig' % mN1])


	mg.Draw('cp same')

	mg.GetXaxis().SetRangeUser(utils.methodsRange[method[1]][0], utils.methodsRange[method[1]][1])
	mg.GetXaxis().SetLabelFont(42)
	# mg.GetXaxis().SetLabelSize(0.05)
	# mg.GetXaxis().SetTitleSize(0.05)
	mg.GetXaxis().SetTitleOffset(1.1)
	mg.GetXaxis().SetTitleFont(42)
	mg.GetXaxis().SetTitle('%s output' % method[0])

	mg.GetYaxis().SetRangeUser(0., 20.)
	mg.GetYaxis().SetLabelFont(42)
	# mg.GetYaxis().SetLabelSize(0.05)
	# mg.GetYaxis().SetTitleSize(0.05)
	mg.GetYaxis().SetTitleOffset(1.1)
	mg.GetYaxis().SetTitleFont(42)
	mg.GetYaxis().SetTitle('Significance')


	data_label = ROOT.TLatex(0.12, 0.96, '%s trained with %s (30%% Bkg. Unc.)' % (method[0], trainCfg['tag']))
	data_label.SetNDC()
	data_label.SetTextFont(42)
	data_label.SetTextSize(0.035)
	data_label.SetLineWidth(2)
	data_label.Draw()

	legend.SetTextSize(0.04)
	legend.SetBorderSize(0)
	legend.Draw()

	line3 = ROOT.TLine()
	line3.SetY1(3.)
	line3.SetY2(3.)
	line3.SetX1(utils.methodsRange[method[1]][0])
	line3.SetX2(utils.methodsRange[method[1]][1])
	line3.SetLineColor(ROOT.kGray)
	line3.SetLineWidth(1)
	line3.SetLineStyle(2)
	line3.Draw()

	line5 = ROOT.TLine()
	line5.SetY1(5.)
	line5.SetY2(5.)
	line5.SetX1(utils.methodsRange[method[1]][0])
	line5.SetX2(utils.methodsRange[method[1]][1])
	line5.SetLineColor(ROOT.kGray)
	line5.SetLineWidth(1)
	line5.SetLineStyle(2)
	line5.Draw()

	plot_name = 'plotSignificance_%s_%s.pdf' % (method[0], trainCfg['tag'])

	canvas.Print('%s/%s' % (outputDirPlots, plot_name))


def plotStack(method, h_samples, cfg, trainCfg, outputDirPlots):

	pconfig = PTc.PlotConfig()

	pconfig.CanvasW = 800
	pconfig.CanvasH = 800
	
	pconfig.Logy = 1
	pconfig.Ratio = True
	pconfig.Tickx = 1
	pconfig.Ticky = 1

	pconfig.TPadY = 0.3 

	pconfig.Output = '%s/plotStack_%s_%s.pdf' % (outputDirPlots, method[0], trainCfg['tag'])

	pconfig.XTitle = method[0]
	pconfig.XRange = (utils.methodsRange[method[1]][0], utils.methodsRange[method[1]][1])

	pconfig.YTitle = 'Events'
	pconfig.YRange[0] = 0.015

	# pconfig.LegendX1 = 0.62
	# pconfig.LegendX2 = 0.93
	# pconfig.LegendY1 = 0.68
	# pconfig.LegendY2 = 0.93
	# pconfig.LegendTextSize = 0.025

	# lumi = 0.
	# for l in year:
	# 	lumi += sty.lumi_label[l]

	# pconfig.LabelData = '#sqrt{s} = 13 TeV, %s fb^{-1}' % lumi
	# pconfig.LabelData2 = reg
	# pconfig.LabelX = 0.25
	# pconfig.LabelY = 0.85

	# pconfig.LegendNColumns = 2

	l_po = []
	
	# bkg histograms
	for s in cfg['samplesBkg']:

		color_tmp = '#000000'
		if s in sty.colors_dict:
			color_tmp = sty.colors_dict[s]

		label_tmp = '???'
		if s in sty.labels_dict:
			label_tmp = sty.labels_dict[s]

		po = PTc.PlotObject()
		po.Object = h_samples[s]
		po.LineColor = ROOT.kBlack
		po.MarkerColor = ROOT.TColor.GetColor(color_tmp)
		po.FillColor = ROOT.TColor.GetColor(color_tmp)
		po.Legend = label_tmp
		po.LegendFill = 'f'
		po.LineWidth = 1
		po.THStack = True
		po.Draw = 'e0 same'

		l_po.append(po)


	# total SM

	_h_total = ROOT.TH1D()
	_h_total.Sumw2()
	_h_total.SetDirectory(0)
	_h_total = h_samples['total_bkg'].Clone()

	po = PTc.PlotObject()
	po.Object = h_samples['total_bkg']
	po.LineColor = ROOT.kGray+3
	po.FillColor = ROOT.kGray+3
	po.FillStyle = 3354
	po.MarkerSize = 0
	po.LineWidth = 2
	po.Legend = 'SM Total'
	po.LegendFill = 'lf'
	po.Draw = 'hist e2 ][ same'

	l_po.append(po)

	po = PTc.PlotObject()
	po.Object = _h_total
	po.LineColor = ROOT.kGray+3
	po.FillColor = 0
	po.MarkerSize = 0
	po.LineWidth = 2
	po.Draw = 'hist ][ same'

	l_po.append(po)

	color_list = ['#1cd759', '#84c915', '#b9b600', '#e49e00', '#ff811b', '#ff614e', '#ff467c', '#ff41ac', '#e755d9']

	for i_index, s in enumerate(cfg['samplesSig']):

		if any(['_1050' in s, '_1250' in s, '_1450' in s]): continue

		if 'phb' in s:
			color_tmp = color_list[i_index-len(cfg['samplesSig'])/2]
		else:
			color_tmp = color_list[i_index]

		label_tmp = '???'
		if s in sty.labels_dict:
			label_tmp = sty.labels_dict[s]

		po = PTc.PlotObject()
		po.Object = h_samples[s]
		po.MarkerColor = ROOT.TColor.GetColor(color_tmp)
		po.FillColor = ROOT.TColor.GetColor(color_tmp)
		po.LineColor = ROOT.TColor.GetColor(color_tmp)
		po.Legend = label_tmp
		po.LegendFill = 'l'
		po.Draw = 'hist same'
		po.LineStyle = 2
		po.LineWidth = 3 
		po.FillColor = 0

		if 'phb' in s:
			po.LineStyle = 3
			po.LineWidth = 2

		l_po.append(po)

		# signal significance

		pconfig.YTitle_dn = 'Significance'
		pconfig.YRange_dn = (0., 10.)

		po = PTc.PlotObject()
		po.Object = h_samples['%s_sig' % s]
		po.MarkerColor = ROOT.TColor.GetColor(color_tmp)
		po.FillColor = ROOT.TColor.GetColor(color_tmp)
		po.LineColor = ROOT.TColor.GetColor(color_tmp)
		po.Legend = None
		po.Draw = 'hist same'
		po.LineStyle = 2
		po.LineWidth = 3 
		po.FillColor = 0
		po.TPad = 'dn'

		if 'phb' in s:
			po.LineStyle = 3
			po.LineWidth = 2

		l_po.append(po)

	PTf.plotMain(l_po, pconfig)


def plotTMVAgraphs(methodsPath, cfg, trainCfg, outputDirPlots):


	inputFile = '%s/%s.root' % (methodsPath, trainCfg['tag'])
	dirName = 'DL_%s' % (trainCfg['tag'])

	if not os.path.exists(dirName):
		os.makedirs(dirName)

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

	os.system('mv %s/plots/* %s' % (dirName, outputDirPlots))
	os.system('rm -r %s' % dirName)


def bkgComp(d_samples, method, methodOut, cfg, trainCfg):

	start = utils.methodsRange[method[1]][0]

	end = utils.methodsRange[method[1]][1]

	for sam in cfg['samplesBkg']+cfg['samplesSig']:

		index = int((methodOut - start) * trainCfg['plotPointsMethod'] / (end - start))

		print sam, d_samples[sam][index]




###################################################################################################
###################################################################################################
###################################################################################################



parser = argparse.ArgumentParser()

parser.add_argument('--plotSignificance', action='store_true')
parser.add_argument('--plotTMVA', action='store_true')
parser.add_argument('--plotMethods', action='store_true')
parser.add_argument('--methodsPath', dest='methodsPath', type=str, default=None)
parser.add_argument('--tag', dest='tag', type=str, default=None)
parser.add_argument('--outputDirPlots', dest='outputDirPlots', type=str, default='/eos/user/g/goorella/plots/PhX_TMVA/')
parser.add_argument('--histPath', dest='histPath', type=str, default=None)
parser.add_argument('--config', dest='config', type=str, default='config.yaml')

args = parser.parse_args()

if args.histPath == None: args.histPath = args.methodsPath

with open('%s' % (args.config), 'r') as f:
	cfg = yaml.safe_load(f)

with open('%s/config.yaml' % (args.methodsPath), 'r') as f:
	trainCfg = yaml.safe_load(f)

if not os.path.exists(args.outputDirPlots):
	os.makedirs(args.outputDirPlots)


if args.plotSignificance:

	d_passEvents, TG_sig, h_method = retrieveHistos(args.methodsPath, args.histPath, cfg, trainCfg)

	for method in trainCfg['trainMethods']:

		plotSignificance(TG_sig, method, args.methodsPath, cfg, trainCfg, args.outputDirPlots)

		plotStack(method, h_method[method[0]], cfg, trainCfg, args.outputDirPlots)

		# bkgComp(d_passEvents[method[0]], method, 0.315, cfg, trainCfg)


if args.plotTMVA:

	plotTMVAgraphs(args.methodsPath, cfg, trainCfg, args.outputDirPlots)
