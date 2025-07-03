import ROOT
import numpy as np
import pandas as pd

def CreatePlot(file):
    '''
    Creates a Histogram with a Logarithmic y-axis, when a csv file from the data is given.
    x-axis: ADC Value
    y-axis: Counts
    '''
    df = pd.read_csv(file, header=4)
    df_np = pd.Series.to_numpy(df["PHA_LG"])  #np.array of the ADC Values  
    n = len(df_np)
    hist = ROOT.TH1F("channel1", "test" ,2**13, 0, 2**13)
    # hist = ROOT.TH1F("channel1", "test" ,2**8, 0, 2**13)   # create "empty" Histogram
# parameters of TH1F here: name of hist, hist title, no. of bins, 
#                           low edge of first bin, upper edge last bin

    for i in range(n):
        hist.Fill(df_np[i]) # Fill Histogram

    canvas = ROOT.TCanvas("canvas1", "canvas1")
    canvas.SetLogy()
    canvas.SetTicks()
    hist.Draw()
    #hist.SetAxisRange(200,1500, "X")      # < ---------------------
    hist.SetStats(0)
    hist.SetLineColor(1)
    hist.SetTitle("")
    hist.GetXaxis().SetTitle("ADC Value")
    hist.GetYaxis().SetTitle("Counts")

    canvas.Update()
    canvas.WaitPrimitive()
    # gSystem.ProcessEvents()
    return canvas, hist

def FitCurve(file, init_gain, init_range, n_gauss,mu,sigma=20, plot=True):
    '''
    If plot=True, it plots a histogram, just like in CreatePlot but also fits n_gauss Gaussian
    Curves to the "oscillations". The average gain (distance between those peaks) is returned.
    If plot=False, then only the avg. gain is returned, but nothing is plotted/fitted. 
    '''
    df = pd.read_csv(file, header=4)
    df_np = pd.Series.to_numpy(df["PHA_LG"])  #np.array of the ADC Values  
    n = len(df_np)
    hist = ROOT.TH1F("channel1", "" ,2**13, 0, 2**13)   # create "empty" Histogram
    for i in range(n):
        hist.Fill(df_np[i]) # Fill Histogram
    if plot:
        canvas = ROOT.TCanvas("canvas1", "canvas1")
        canvas.SetLogy()
        canvas.SetTicks()
        hist.Draw()
        hist.SetStats(0)
        hist.SetLineColor(1)
        hist.SetTitle("")
        hist.SetAxisRange(200,1000, "X")      # < ---------------------
        hist.GetXaxis().SetTitle("ADC Value")
        hist.GetYaxis().SetTitle("Counts")
        # hist.GetXaxis().SetRangeUser(200,1000)  # < -----------

    # mu= hist.GetMaximumBin()
        

    # Compute the first two mu values to obtain a good estimate for the gain
    # Like that we have init_gain
    if n_gauss>=2:
        mu_1 = mu
        a_1 = hist.GetBinContent(int(mu_1))
        fit_test1 = ROOT.TF1(f"fit_test1", "gaus", mu_1-init_range, mu_1 +init_range)
        fit_test1.SetParameters(a_1, mu_1, sigma)
        hist.Fit(fit_test1, "R0")   # R: use range specified, 0: do not plot
        
        mu_2 = mu_1 + init_gain
        a_2 = hist.GetBinContent(int(mu_2))
        fit_test2 = ROOT.TF1(f"fit_test2", "gaus", mu_2-init_range, mu_2 +init_range)
        fit_test2.SetParameters(a_2, mu_2, sigma)
        hist.Fit(fit_test2, "R0")

        print("provisorisches gain = ", fit_test2.GetParameter(1)-fit_test1.GetParameter(1))
        init_gain = fit_test2.GetParameter(1)-fit_test1.GetParameter(1)
    
    mu_arr = np.array([])
    for i in range(n_gauss):
        mu_i = mu
        a_i = hist.GetBinContent(int(mu_i))
        fit = ROOT.TF1(f"fit{i}", "gaus", mu_i-init_range, mu_i +init_range)
        fit.SetParameters(a_i, mu_i, sigma)
        hist.Fit(fit, "R+")
        mu_arr = np.append(mu_arr, fit.GetParameter(1))
        if len(mu_arr)==1:      # Since we only have one value of mu,
            mu += init_gain     # we cannot yet compute the gain
        else:
            mu += np.mean(np.diff(mu_arr))

    avg_gain =np.mean(np.diff(mu_arr))
    # print("avg. gain = ", avg_gain)
    
    if plot:
        canvas.Update()
        canvas.WaitPrimitive()
        # gSystem.ProcessEvents()

    return avg_gain

def MPV(file,range_min=300, range_plus=1000,viewCanvas=True): #most probable value
    '''
    Returns the most probable value (MPV) of the data. The bin size of the histogram is 
    larger than before, s.t. the curve is smoother and we fit one bigger Gaussian. 
    From the x-position of the Peak (i.e. Mu) we obtain the MPV.
    '''
    df = pd.read_csv(file, header=4)
    df_np = pd.Series.to_numpy(df["PHA_LG"])  #np.array of the ADC Values  
    n = len(df_np)
    no_bins = 2**8
    ADC_max=2**13
    bin_size= ADC_max/no_bins
    hist = ROOT.TH1F("channel1", "" ,no_bins, 0, ADC_max)   # create "empty" Histogram
    for i in range(n):
        hist.Fill(df_np[i]) # Fill Histogram
    if viewCanvas:
        canvas = ROOT.TCanvas("canvas1", "canvas1")
        canvas.SetLogy()
        canvas.SetTicks()
        hist.Draw()
        hist.SetStats(0)
        hist.SetLineColor(1)
        hist.SetTitle("")
        hist.GetXaxis().SetTitle("ADC Value")
        hist.GetYaxis().SetTitle("Counts")

    

    a_w= hist.GetBinContent(int(mu_w))
    mu_w = mu_w*bin_size    #converted 
    print("mu =", mu_w)
    print("a_W = ", a_w)
    sigma_w = 200
    # fit_whole = ROOT.TF1("fit_whole", "gaus", mu_w-range_min, mu_w + range_plus)  # <------- was out of histogram range for after resin data
    fit_whole = ROOT.TF1("fit_whole", "gaus", range_min, mu_w + range_plus)
    fit_whole.SetParameters(a_w, mu_w, sigma_w)
    hist.Fit(fit_whole, "R+")
    if viewCanvas:
        canvas.Update()
        canvas.WaitPrimitive()
        #gSystem.ProcessEvents()
    return fit_whole.GetParameter(1), fit_whole.GetParameter(2) 

# not needed:
# def PhotonNumber(file, pedestal ,init_gain, init_range,mu, n_gauss=4, sigma=20, viewCanvas=True):
    '''
    Plots the data just as in CreatePlot but the x-axis is converted to Photons. To do so
    we first need to find the gain by using FitCurve. Then we can use the formula to 
    convert ADC value to No. of photons. The converted data is returned.
    '''
    gain = FitCurve(file, init_gain, init_range, n_gauss, mu,sigma=sigma, plot=False)
    # print("gain=", gain)
    df = pd.read_csv(file, header=4)
    df_np = pd.Series.to_numpy(df["PHA_LG"])  #np.array of the ADC Values  
    df_np = np.floor((df_np - pedestal)/gain) #Convert to No. of photons and convert into integer
    #print("df_np=",df_np)
    n = len(df_np)
    x_max = (2**13-pedestal)/gain #highest photon number
    # print("x_max=", x_max)
    hist = ROOT.TH1F("channel1", "test" ,int(x_max),0, int(x_max))
    for i in range(n):
        hist.Fill(df_np[i]) # Fill Histogram
    if viewCanvas:
        canvas2 = ROOT.TCanvas("canvas2", "canvas2")
        canvas2.SetLogy()
        canvas2.SetTicks()
        hist.Draw()
        hist.SetStats(0)
        hist.SetLineColor(1)
        hist.SetTitle("")
        hist.GetXaxis().SetTitle("Photon Number")
        hist.GetYaxis().SetTitle("Counts")
        canvas2.Update()
        canvas2.WaitPrimitive()
        # gSystem.ProcessEvents()
    return df_np # returns the converted Data

# def MPPN(file,init_gain, init_range,range_min=1000, range_plus=1000,viewCanvas=True, pedestal=50, n_gauss=4,sigma=20):
    df_np = PhotonNumber(file, pedestal, init_gain, init_range,viewCanvas=False)
    n = len(df_np)
    no_bins =100 #2**8
    Photon_max=100    #2**13
    bin_size= Photon_max/no_bins
    hist = ROOT.TH1F("channel1", "" ,no_bins, 0, Photon_max)   # create "empty" Histogram
    for i in range(n):
        hist.Fill(df_np[i]) # Fill Histogram
    if viewCanvas:
        canvas = ROOT.TCanvas("canvas1", "canvas1")
        canvas.SetLogy()
        canvas.SetTicks()
        hist.Draw()
        hist.SetStats(0)
        hist.SetLineColor(1)
        hist.SetTitle("")
        hist.GetXaxis().SetTitle("Photon Number")
        hist.GetYaxis().SetTitle("Counts")

    mu_w= hist.GetMaximumBin()
    a_w= hist.GetBinContent(int(mu_w))
    mu_w = mu_w*bin_size    #converted 
    print("mu =", mu_w)
    print("a_W = ", a_w)
    sigma_w = 200
    fit_whole = ROOT.TF1("fit_whole", "gaus", mu_w-range_min, mu_w + range_plus)
    fit_whole.SetParameters(a_w, mu_w, sigma_w)
    hist.Fit(fit_whole, "R+")
    if viewCanvas:
        canvas.Update()
        canvas.WaitPrimitive()
        #gSystem.ProcessEvents()
    return fit_whole.GetParameter(1)