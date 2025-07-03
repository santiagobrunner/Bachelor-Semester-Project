import ROOT
import numpy
import os
import pandas as pd
from Functions import *       # CreatePlot, FitCurve, MPV, PhotonNumber, MPPN
import matplotlib.pyplot as plt


# ----- import Data -----
AC_Data = np.loadtxt('AC4_Data.txt', delimiter=',')
AC_Data_after=np.loadtxt('AC4_Data_with_resin.txt', delimiter=',')
EJ_Data = np.loadtxt('EJ3_Data.txt', delimiter=',')
EJ_Data_after = np.loadtxt('EJ3_Data_with_resin.txt', delimiter=',')
OF_Data = np.loadtxt('OF3_Data.txt', delimiter=',')
OF_Data_after = np.loadtxt('OF3_Data_with_resin.txt', delimiter=',')


distance = np.arange(0,200,10) +2+1.465
# -----------------------------------------


def before_after(x, y_Data1, y_Data2=-99, Title="Title", fitting=False):
    print(Title)
    MPVs1 = y_Data1[:,0]
    Gains1 = y_Data1[:,2]
    Errors1 = y_Data1[:,1] # Errors propagieren
    PCs1 = (MPVs1 - 50)/np.mean(Gains1) 
    # Create a TGraph object
    n_points = len(distance)
    graph1 = ROOT.TGraph(n_points)

    if type(y_Data2)!=int:
        MPVs2 = y_Data2[:,0]
        Gains2 = y_Data2[:,2]
        Errors2 = y_Data2[:,1] # Errors propagieren
        PCs2 = (MPVs2 - 50)/np.mean(Gains2) 
        graph2 = ROOT.TGraph(n_points)


    # Fill the TGraph with data points from the NumPy arrays
    for i in range(n_points):
        graph1.SetPoint(i, x[i], PCs1[i])
        if type(y_Data2)!=int:
            graph2.SetPoint(i, x[i], PCs2[i])

    # Set titles and labels
    graph1.SetTitle(rf"{Title};Distance [cm];Photon Count")

    # Customize the graph (optional)
    graph1.SetMarkerStyle(20)  # Set marker style
    graph1.SetMarkerSize(1)    # Set marker size
    graph1.SetMarkerColor(ROOT.kBlack)  # Set marker color
    if type(y_Data2)!=int:
        graph2.SetMarkerStyle(20)  # Set marker style
        graph2.SetMarkerSize(1)    # Set marker size
        graph2.SetMarkerColor(ROOT.kBlue)  # Set marker color
        # Calculate the combined y-axis range
        combined_y_min = min(min(PCs1), min(PCs2))
        combined_y_max = max(max(PCs1), max(PCs2))
        graph2.GetYaxis().SetRangeUser(0, 17)
        # Set y-axis range for both graphs
        graph1.GetYaxis().SetRangeUser(0, 17)
        graph2.GetXaxis().SetRangeUser(0,200)
        graph1.GetXaxis().SetRangeUser(0, 200)

    # Create a canvas to draw the graph
    canvas = ROOT.TCanvas("canvas", "Scatter Plot", 800, 600)
    # Add a legend to distinguish the datasets
    legend = ROOT.TLegend(0.6, 0.7, 0.9, 0.9)

    graph1.Draw("ALP")
    legend.AddEntry(graph1, "Without resin", "p")
    if type(y_Data2)!=int:
        graph2.Draw("LP SAME")  # "A" draws the axis, "P" draws the points, "L" to connect points
        legend.AddEntry(graph2, "With resin", "p")

# ----- Fit -----
    if fitting:
        double_exp = ROOT.TF1("double_exp", "[0]*exp(-x/[1]) + [2]*exp(-x/[3])", 2,192)         
        double_exp.SetParameters(12, 400, 1, 30)
        double_exp.SetParName(0, "I_core")
        double_exp.SetParName(1, "Lambda_core")
        double_exp.SetParName(2, "I_clad")
        double_exp.SetParName(3, "Lambda_clad")
        double_exp.SetParLimits(0, 7,18)
        double_exp.SetParLimits(1, 100,400)
        double_exp.SetParLimits(2, 0,6)
        double_exp.SetParLimits(3, 0,30)

        double_exp.SetLineColor(ROOT.kRed)
        double_exp.SetLineStyle(9)
        double_exp.SetLineWidth(4)

        graph1.Fit(double_exp, "R+")
        legend.AddEntry(double_exp, "Double Exponential Fit", "l")
        legend.SetTextSize(0.03)
        # if type(y_Data2)!=int:
        #     simple_exp =ROOT.TF1("simple_exp", "[0]*exp(-x/[1])", 2,192) 
        #     simple_exp.SetParameters(12, 400)
        #     simple_exp.SetLineColor(6)
        #     simple_exp.SetLineStyle(9)
        #     simple_exp.SetLineWidth(5)
        #     graph2.Fit(simple_exp,"R+")
        #     legend.AddEntry(simple_exp, "Simple exp. fit", "l")


    legend.Draw()
    # Update the canvas to display the plot
    canvas.Update()
    # canvas.SaveAs(f"{Title}_plot2.png")
    canvas.WaitPrimitive()
    # return double_exp.GetParameter(0),double_exp.GetParameter(1),double_exp.GetParameter(2),double_exp.GetParameter(3)

before_after(distance, OF_Data, OF_Data_after, "OF (n=1.33)", True)
# before_after(distance, EJ_Data, EJ_Data_after, 'EJ (n=1.57)', True)
# before_after(distance, AC_Data,AC_Data_after,Title= "AC (n=1.52)", fitting=True)

