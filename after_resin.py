import ROOT
import numpy as np
import os
import pandas as pd
from Functions import *       # CreatePlot, FitCurve, MPV, PhotonNumber, MPPN

NR2_files = np.array([])
AC3_files = np.array([])
EJ2_files = np.array([])
OF2_files = np.array([])


# ------ Write File Names into Arrays ------
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)

for i in range(5): 
    NR2_files = np.append(NR2_files, parent_dir + f"/Data with resin/NR2_a_resin_{i+1}.csv")
    AC3_files = np.append(AC3_files, parent_dir + f"/Data with resin/AC3_a_resin_{i+1}.csv")
    EJ2_files = np.append(EJ2_files, parent_dir + f"/Data with resin/EJ2_a_resin_{i+1}.csv")
    OF2_files = np.append(OF2_files, parent_dir + f"/Data with resin/OF2_a_resin_{i+1}.csv")



# ------ Estimation of mu for each dataset ------
NR2_mu = np.array([365, 350, 345, 340, 348])
AC3_mu = np.array([351, 348, 350, 350, 350])
EJ2_mu = np.array([360, 358, 350, 347, 350])
OF2_mu = np.array([350, 350, 350, 350, 350])
# -----------------------------------------------

NR2_gains = np.array([])
AC3_gains = np.array([])
EJ2_gains = np.array([])
OF2_gains = np.array([])
NR2_MPVs = np.array([])
AC3_MPVs = np.array([])
EJ2_MPVs = np.array([])
OF2_MPVs = np.array([])



for i in range(5): 

    NR2_gains = np.append(NR2_gains, FitCurve(NR2_files[i],73,28,4,NR2_mu[i] , plot=False))
    AC3_gains = np.append(AC3_gains, FitCurve(AC3_files[i],73,28,4,AC3_mu[i] , plot=False))
    EJ2_gains = np.append(EJ2_gains, FitCurve(EJ2_files[i],73,28,4,EJ2_mu[i] , plot=False))
    OF2_gains = np.append(OF2_gains, FitCurve(OF2_files[i],73,28,4,OF2_mu[i] , plot=False))

    NR2_MPVs = np.append(NR2_MPVs, MPV(NR2_files[i], range_plus=100, viewCanvas=False))
    AC3_MPVs = np.append(AC3_MPVs, MPV(AC3_files[i], range_plus=250, viewCanvas=False))
    EJ2_MPVs = np.append(EJ2_MPVs, MPV(EJ2_files[i], range_plus=250, viewCanvas=False))
    OF2_MPVs = np.append(OF2_MPVs, MPV(OF2_files[i], range_plus=250, viewCanvas=False))    

# print(np.mean(NR2_gains), np.mean(AC3_gains), np.mean(EJ2_gains), np.mean(OF2_gains))

NR2_PCs = (NR2_MPVs - 50)/ np.mean(NR2_gains)
AC3_PCs = (AC3_MPVs - 50)/np.mean(AC3_gains)
EJ2_PCs = (EJ2_MPVs - 50)/np.mean(EJ2_gains)
OF2_PCs = (OF2_MPVs - 50)/np.mean(OF2_gains)

NR2_PC = np.mean(NR2_PCs)
AC3_PC = np.mean(AC3_PCs)
EJ2_PC = np.mean(EJ2_PCs)
OF2_PC = np.mean(OF2_PCs)

PCs = np.array([NR2_PCs, AC3_PCs, EJ2_PCs, OF2_PCs])
np.save('PCs_samples_after_resin.npy', PCs)
np.savetxt('PCs_sample_after_resin.txt', PCs)
print("NR2 PhotonCount: ", NR2_PC) # , np.mean(NR2_PCs2 ))
print("AC3 PhotonCount: ",AC3_PC) # , np.mean(AC3_PCs2))
print("EJ2 PhotonCount: ",EJ2_PC)
print("OF2 PhotonCount: ", OF2_PC)

