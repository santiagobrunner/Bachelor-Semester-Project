import ROOT
import numpy as np
import pandas as pd
from Functions import *       # CreatePlot, FitCurve, MPV, PhotonNumber, MPPN

NR2_files = np.array([])
AC3_files = np.array([])
EJ2_files = np.array([])
OF2_files = np.array([])


# ------ Write File Names into Arrays ------
for i in range(5): 
    NR2_files = np.append(NR2_files, f"Data/NR2_b_resin_{i+1}.csv")
    AC3_files = np.append(AC3_files, f"Data/AC3_b_resin_{i+1}.csv")
    EJ2_files = np.append(EJ2_files, f"Data/EJ2_b_resin_{i+1}.csv")
    OF2_files = np.append(OF2_files, f"Data/OF2_b_resin_{i+1}.csv")

# ------ Estimation of mu for each dataset ------
NR2_mu = np.array([352, 352, 345, 355, 360])
AC3_mu = np.array([350, 353, 353, 360, 360])
EJ2_mu = np.array([360, 360, 362, 363, 365])
OF2_mu = np.array([360, 360, 364, 364, 365])

NR2_gains = np.array([])
AC3_gains = np.array([])
EJ2_gains = np.array([])
OF2_gains = np.array([])
NR2_MPVs = np.array([])
AC3_MPVs = np.array([])
EJ2_MPVs = np.array([])
OF2_MPVs = np.array([])


# -----
# CreatePlot(AC3_files[1])
# CreatePlot(EJ2_files[1])
# CreatePlot(OF2_files[1])
# -----


for i in range(5):

    NR2_gains = np.append(NR2_gains, FitCurve(NR2_files[i],85,28,4,NR2_mu[i] , plot=False))
    # AC3_gains = np.append(AC3_gains, FitCurve(AC3_files[i],85,28,4,AC3_mu[i] , plot=False))
    EJ2_gains = np.append(EJ2_gains, FitCurve(EJ2_files[i],85,28,4,EJ2_mu[i] , plot=False))
    OF2_gains = np.append(OF2_gains, FitCurve(OF2_files[i],85,28,4,OF2_mu[i] , plot=False))

    NR2_MPVs = np.append(NR2_MPVs, MPV(NR2_files[i], 250, viewCanvas=False))
    # AC3_MPVs = np.append(AC3_MPVs, MPV(AC3_files[i], viewCanvas=False))
    EJ2_MPVs = np.append(EJ2_MPVs, MPV(EJ2_files[i], viewCanvas=False))
    OF2_MPVs = np.append(OF2_MPVs, MPV(OF2_files[i], viewCanvas=False))    


NR2_PCs = (NR2_MPVs - 50)/ NR2_gains
# AC3_PCs = (AC3_MPVs - 50)/AC3_gains
EJ2_PCs = (EJ2_MPVs - 50)/EJ2_gains
OF2_PCs = (OF2_MPVs - 50)/OF2_gains

print("NR2 PhotonCount: ",np.mean(NR2_PCs))
# print("AC3 PhotonCount: ",np.mean(AC3_PCs))
print("EJ2 PhotonCount: ",np.mean(EJ2_PCs))
print("OF2 PhotonCount: ",np.mean(OF2_PCs))

''''
Zuerst für alle datensets den Startpeak finden
Gain für alle berechnen mit Mu=Startpeak
Plot photon numbers

MPV anschauen
'''



