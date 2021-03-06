#!/usr/bin/env python
# encoding: utf-8

# File        : CompHLT.py
# Author      : Zhenbin Wu
# Contact     : zhenbin.wu@gmail.com
# Date        : 2016 Aug 25
#
# Description :

import pandas as pd
import numpy as np
import glob
import math
import ROOT
import collections
import os
import re
import tdrstyle
import rootpy
from rootpy.interactive import wait
from rootpy.io import root_open
from matplotlib import pyplot as plt
from Config import DualMap, S1S2Map, S2S1Map

foldername = "Random"

fit_min = 31
fit_max = 55
plot_min = 0
plot_max = 70
maxx = 70
maxy = 200

####	for 1866 bunches	####
#PU = 61		#61.00 for col 1.6
#PU = 57		#57.19 for col 1.5
#PU = 50		#49.56 for col 1.3
#PU = 38		#38.12 for col 1.0

####	for 2544 bunches	####
#PU = 62		#61.52 for col 2.2
PU = 45
#PU = 56		#55.93 for col 2.0
#PU = 50		#50.33 for col 1.8


freq = 11245.6
config = 2017
#config = 2018

#fitname = "pol0"
#fitname = "expo"
#fitname = ROOT.TF1("fitname","[0]*x + [1]*x*x",0,80);
#fitname.SetParameters(0.1,0.001);

#filedir = "/eos/uscms/store/user/huiwang/L1Menu2017/" + foldername + "/*Default_PU.csv"
#filedir = "/uscms_data/d3/huiwang/CMSSW_9_2_2/src/L1TriggerDPG/L1Menu/macros/results/Prescale_2018_v1_0_0_Col_2.0_Pure_Rate_run_Hcal_319449_and_319450_new_v2_emulate_PU.csv"
#filedir = "/afs/cern.ch/work/u/usarkar/L1TriggerMenu/CMSSW_11_0_2/src/L1MenuTools/rate-estimation/results/fill_6923_54_PU.csv"
filedir = "/afs/cern.ch/user/g/gsalvi/CMSSW_11_0_2/src/L1MenuTools/rate-estimation/results/fill_6923_54_PU.csv"

if config == 2017:
    #nBunches = 1866
    nBunches = 2544
    #nBunches = 424
    unit = "kHz"

if config == 2018:
    nBunches = 2544
    unit = "kHz"

if config == 1:
    nBunches = 1
    unit = "Hz"

pubins = np.arange(plot_min,plot_max, 1)
pumap = collections.defaultdict(list)

PatMap = {  
#    "L1_SingleLooseIsoEG28er2p5" : "L1_SingleLooseIsoEG28er2p5",
    "L1_SingleMu22" : "L1_SingleMu22",
#    "L1_SingleLooseIsoEG28_FWD2p5" : "L1_SingleLooseIsoEG28_FWD2p5",
    
}

def DrawPU(canvas, f, l1seed, count, key=None):
    df = f[(f.L1Seed == l1seed )]
    RetVar = None

    for i in range(0, len(pubins) -1):
        pumap[pubins[i]] = []
        pumap[pubins[i]].append(df[np.logical_and(df.PileUp > pubins[i], df.PileUp <= pubins[i+1])].Fired0.sum())
        pumap[pubins[i]].append(df[np.logical_and(df.PileUp > pubins[i], df.PileUp <= pubins[i+1])].Total.sum())

    x = []
    y = []
    yerr = []
    for k, v in pumap.iteritems():
        if v[1] != 0:
            x.append(k)
            if unit == "Hz":
                y.append(float(v[0])/v[1] * freq * nBunches )
                yerr.append( math.sqrt(float(v[0]))/v[1] * freq * nBunches )
            if unit == "kHz":
                y.append(float(v[0])/v[1] * freq * nBunches / 1000)
                yerr.append( math.sqrt(float(v[0]))/v[1] * freq * nBunches / 1000)

    ## Draw the plot
    graph = ROOT.TGraphErrors(len(x))

    for i, (xx, yy, yee) in enumerate(zip(x, y, yerr)):
        # if yy != 0 and yee/yy >0.3:
            # continue
	#if i == 22 or i == 23 or i == 24:
	    # continue
        graph.SetPoint(i, xx, yy)
	#print (i,xx,yy,yee)
        #print "h1->SetBinContent( %d, %f);" %(xx,yy)
        #print "h1->SetBinError( %d, %f);" %(xx,yee)
        graph.SetPointError(i, 0, yee)

    graph.SetMarkerStyle(20+count)
    graph.SetMarkerSize(1.5)
    graph.SetMarkerColor(1+count)
    graph.SetLineColor(1+count)
    graph.SetLineWidth(2)
    tdrstyle.setTDRStyle()
    canvas.cd()
    canvas.Update()
    if count == 0:
        graph.Draw("AP")
        graph.GetXaxis().SetTitle("PileUp")
        graph.GetXaxis().SetLimits(plot_min, maxx)
        graph.GetYaxis().SetRangeUser(0, maxy)
        graph.GetYaxis().SetTitle("Rate (nBunches = %d) [%s]" % (nBunches, unit))
    else:
        graph.Draw("P")
    canvas.Update()
    leg.AddEntry(graph, l1seed, "p")

#    result_ptr = graph.Fit(fitname, "SQ", "", fit_min, fit_max)
#    error_vec = result_ptr.GetConfidenceIntervals()
#    print ("error vec size = %d, fitted PU = %d" % (error_vec.size(), fit_max - fit_min + 1))
#    f2 = graph.GetFunction("fitname").Clone()
    #f2 = graph.GetFunction(fitname).Clone()
#    f2.SetLineColor(1+count)
#    f2.SetLineWidth(2)
#    f2.SetRange(plot_min, fit_min)
#    f2.SetLineStyle(5)
#    minChi = f2.GetChisquare() / f2.GetNDF()
    #fun = "Fit = %.2f + %.2f*x + %.3f*x^2" % (f2.GetParameter(0), f2.GetParameter(1), f2.GetParameter(2) )
    #fun = "Fit = %f*x + %f*x^2" % (f2.GetParameter(0), f2.GetParameter(1) )
    #print fun
#    f2.Draw("same")
#    f2_2 = f2.Clone("dashline2")
#    f2_2.SetRange(fit_max, plot_max)
#    f2_2.Draw("same")
#    if config == 2017:
#        if PU <= fit_max: key = "Rate(PU=%d): %.2f +- %.2f, chi2/NDF=%.2f" %(PU, f2_2.Eval(PU), error_vec.at(PU-fit_min), minChi)
#        else: key = "Rate(PU=%d): %.2f +- %.2f, chi2/NDF=%.2f" %(PU, f2_2.Eval(PU), error_vec.back(), minChi)
#    if config == 2018:
#	#key = ""
#        key = "Rate: %.2f +- %.2f @PU50, %.2f +- %.2f @PU56, %.2f +- %.2f @PU62" %(f2_2.Eval(50), error_vec.at(50-fit_min), f2_2.Eval(56), error_vec.at(56-fit_min), f2_2.Eval(62), error_vec.at(62-fit_min))

    if key is not None:
        tex = ROOT.TLatex(0.2, 0.85, key)
        tex.SetNDC()
        tex.SetTextFont(61)
        tex.SetTextSize(0.055)
        tex.SetTextColor(ROOT.kGreen+2)
        tex.SetLineWidth(2)
        tex.Draw()

    canvas.Update()


def DrawL1(key, pattern):
    c1.Clear()
    leg.Clear()

    inputlist = []
    pat = re.compile('^%s$' % pattern)

    for x in [x for x in pd.unique(df.L1Seed)]:
        if pat.match(x):
            inputlist.append(x)
    #print key, " : ",  inputlist
    print key,

    for i, seed in enumerate(inputlist):
        DrawPU(c1, df, seed, i)
    leg.Draw()

    if config == 2017:
        l_PU = ROOT.TLine(PU, 0, PU, maxy)
        l_PU.SetLineColor(2)
        l_PU.SetLineWidth(2)
        l_PU.Draw()

    if config == 2018:
        l_1 = ROOT.TLine(50, 0, 50, maxy)
        l_1.SetLineColor(2)
        l_1.SetLineWidth(2)
        l_1.Draw()
        l_2 = ROOT.TLine(56, 0, 56, maxy)
        l_2.SetLineColor(2)
        l_2.SetLineWidth(2)
        l_2.Draw()
        l_3 = ROOT.TLine(62, 0, 62, maxy)
        l_3.SetLineColor(2)
        l_3.SetLineWidth(2)
        l_3.Draw()

    c1.SetGrid()

    box = ROOT.TBox(10, 8, 70, 12)
    box.SetFillColor(38)
    box.SetFillStyle(3002)

    c1.Update()
#    c1.SaveAs("plots/%s_%d_%s_PU%d.root" % (key, config, foldername, PU))
 #   c1.SaveAs("plots/%s_%d_%s_PU%d.png" % (key, config, foldername, PU))
    #c1.SaveAs("plots/%s_%d_%s_PU%d.pdf" % (key, config, foldername, PU))
    c1.SaveAs("54_6931.png")
#(("plots/%s_%d_%s_PU%d.root" % (key, config, foldername, PU))
    c1.SaveAs("54_6931.root")

if __name__ == "__main__":
    allfiles = glob.glob(filedir)
    if not os.path.exists("plots"):
        os.mkdir("plots")

    df = pd.DataFrame()
    flist = [ ]
    for file_ in allfiles:
        df_ = pd.read_csv(file_, index_col=None, header=0)
        flist.append(df_)
    df = pd.concat(flist)

    ## Redefine PatMap for each L1Seed in the dataframe
    #PatMap = {k:k for k in pd.unique(df.L1Seed)}

    ROOT.gStyle.SetOptStat(000000000)
    tdrstyle.setTDRStyle()
    c1 = ROOT.TCanvas("fd","Fdf", 1200, 1000)
    leg = ROOT.TLegend(0.15,0.7,0.45,0.75)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(62)
    leg.SetTextSize(0.05)
    for k, v in PatMap.items():
        DrawL1(k, v)
        # wait()

