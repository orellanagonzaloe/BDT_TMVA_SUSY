#! /usr/bin/env python

import os

import ROOT
ROOT.gROOT.SetBatch(True)


def plotStack():

	canvas = TCanvas('canvas', 'canvas', 0, 0, pconfig.CanvasW, pconfig.CanvasH)