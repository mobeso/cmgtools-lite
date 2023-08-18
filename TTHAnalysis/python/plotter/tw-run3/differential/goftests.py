from copy import deepcopy
import ROOT as r
import warnings as wr
import os, sys, math, array, argparse
import numpy as np
from scipy.stats import chisquare, chi2

sys.path.append('{cmsswpath}/src/CMGTools/TTHAnalysis/python/plotter/tw-run3/differential/'.format(cmsswpath = os.environ['CMSSW_BASE']))
import beautifulUnfoldingPlots as bp
import errorPropagator as ep
#import getLaTeXtable as tex
import varList as vl

r.gROOT.SetBatch(True)
vl.SetUpWarnings()


#def GiveMeMyGOFTests(var): # Old code!
    #f1 = r.TFile.Open(pathtothings + "particleOutput.root", "read")
    #f2 = r.TFile.Open(pathtothings + "particle.root", "read")
    ##f3 = r.TFile.Open(pathtothings + "{vr}/ClosureTest_DS_{vr}.root".format(vr = var), "read")
    ##f4 = r.TFile.Open(pathtothings + "{vr}/ClosureTest_aMCatNLO_{vr}.root".format(vr = var), "read")
    
    #hData     = deepcopy(f1.Get(var).Clone("hData"))
    #hDataUp   = deepcopy(f1.Get("nom0").Clone("hDataUp"))
    #hDataDown = deepcopy(f1.Get("nom1").Clone("hDataDown"))
    #hDR       = deepcopy(f2.Get("tW").Clone("hDR"))
    ##hDS       = deepcopy(f3.Get("tW").Clone("hDS"))
    ##haMCatNLO = deepcopy(f4.Get("tW").Clone("haMCatNLO"))
    
    #f1.Close(); f2.Close(); #f3.Close(); f4.Close()
    
    #hData.SetFillColor(r.kWhite)
    #hData.SetLineWidth(2)
    #hData.SetLineColor(r.kBlack)
    #hData.SetLineStyle(2)
    #for bin in range(1, hData.GetNbinsX() + 1):
        #hData.SetBinError(bin, max( [hDataUp.GetBinError(bin), hDataDown.GetBinError(bin)] ))
    
    #hDR.SetFillColor(r.kWhite)
    #hDR.SetLineWidth(2)
    #hDR.SetLineColor(r.kRed)
    
    ##hDS.SetFillColor(r.kWhite)
    ##hDS.SetLineWidth(2)
    ##hDS.SetLineColor(r.kGreen)
    ##hDS.GetXaxis().SetTitle(vl.varList[var]['xaxis'])
    
    ##haMCatNLO.SetFillColor(r.kWhite)
    ##haMCatNLO.SetLineWidth(2)
    ##haMCatNLO.SetLineColor(r.kBlue)
    
    
    #plot           = bp.beautifulUnfPlot("GOF_{vr}".format(vr = var))
    #plot.doRatio   = False
    #plot.doFit     = False
    #plot.plotspath = outputpath + "/"
    
    ##plot.addHisto(hDS,       'hist',      'tW DS',      'L', 'mc')
    #plot.addHisto(hDR,       'hist,same', 'tW Powheg',  'L', 'mc')
    #plot.addHisto(haMCatNLO, 'hist,same', 'tW aMC@NLO', 'L', 'mc')
    #plot.addHisto(hData,     'hist,same', 'Data',       'L', 'mc')
    
    #l1 = r.TLatex(0.65, 0.700, '#scale[0.4]{DR - KS: %4.10f}'%hData.KolmogorovTest(hDR))
    #l2 = r.TLatex(0.65, 0.675, '#scale[0.4]{DR - KS (toys): %4.10f}'%hData.KolmogorovTest(hDR,'X'))
    #l3 = r.TLatex(0.65, 0.650, '#scale[0.4]{DR - #chi^{2}: %4.10f}'%hData.Chi2Test(hDR,'WW'))
    ##l4 = r.TLatex(0.65, 0.625, '#scale[0.4]{DS - KS: %4.10f}'%hData.KolmogorovTest(hDS))
    ##l5 = r.TLatex(0.65, 0.600, '#scale[0.4]{DS - KS (toys): %4.10f}'%hData.KolmogorovTest(hDS,'X'))
    ##l6 = r.TLatex(0.65, 0.575, '#scale[0.4]{DS - #chi^{2}: %4.10f}'%hData.Chi2Test(hDS,'WW'))
    ##l7 = r.TLatex(0.65, 0.550, '#scale[0.4]{aMC@NLO - KS: %4.10f}'%hData.KolmogorovTest(haMCatNLO))
    ##l8 = r.TLatex(0.65, 0.525, '#scale[0.4]{aMC@NLO - KS (toys): %4.10f}'%hData.KolmogorovTest(haMCatNLO,'X'))
    ##l9 = r.TLatex(0.65, 0.500, '#scale[0.4]{aMC@NLO - #chi^{2}: %4.10f}'%hData.Chi2Test(haMCatNLO,'WW'))
    
    #l1.SetNDC(True); l2.SetNDC(True); l3.SetNDC(True); #l4.SetNDC(True); l5.SetNDC(True); l6.SetNDC(True)
    ##l7.SetNDC(True); l8.SetNDC(True); l9.SetNDC(True);

    #l1.Draw('same'); l2.Draw('same'); l3.Draw('same'); #l4.Draw("same"); l5.Draw("same"); l6.Draw("same")
    ##l7.Draw("same"); l8.Draw("same"); l9.Draw("same")
    
    #plot.saveCanvas("TR")
    #del plot
    
    #print 'DR - KS:', hData.KolmogorovTest(hDR)
    #print 'DR - KS (toys):', hData.KolmogorovTest(hDR,'X')
    #print 'DR - chi2:', hData.Chi2Test(hDR,'WW')
    ##print 'DS - KS:', hData.KolmogorovTest(hDS)
    ##print 'DS - KS (toys):', hData.KolmogorovTest(hDS,'X')
    ##print 'DS - chi2:', hData.Chi2Test(hDS,'WW')
    ##print 'aMC@NLO - KS:', hData.KolmogorovTest(haMCatNLO)
    ##print 'aMC@NLO - KS (toys):', hData.KolmogorovTest(haMCatNLO,'X')
    ##print 'aMC@NLO - chi2:', hData.Chi2Test(haMCatNLO,'WW')
    #return


def getNumpyArray(histo):
    ret = None
    if   isinstance(histo, r.TH2):
        ret = np.zeros( (histo.GetNbinsX(), histo.GetNbinsX()), dtype = np.double )
        for i in range(1, histo.GetNbinsX() + 1):
            for j in range(1, histo.GetNbinsX() + 1):
                ret[i-1, j-1] = histo.GetBinContent(i, j)

    elif isinstance(histo, r.TH1):
        ret = np.array([histo.GetBinContent(bin) for bin in range(1, histo.GetNbinsX() + 1)], dtype = np.double)
    else:
        raise RuntimeError("FATAL: unsupported type " + str(type(histo)) + ".")

    return ret


def Chi2TestForMultivarNormal(w1, V1, w2, V2):
    #print "VAINAS RARAS"
    #escalaobtusa = 10000
    #escalaobtusa = 1
    #w1 = ww1*escalaobtusa ; w2 = ww2*escalaobtusa ; V1 = VV1*escalaobtusa**2; V2 = VV2*escalaobtusa **2


    if not isinstance(w1, np.ndarray):
        w1 = getNumpyArray(w1)
    if not isinstance(w2, np.ndarray):
        w2 = getNumpyArray(w2)

    if isinstance(V1, r.TH1) and not isinstance(V1, r.TH2):
        V1 = np.diag(np.array([V1.GetBinError(bin)**2 for bin in range(1, V1.GetNbinsX() + 1)], dtype = np.double))
    elif not isinstance(V1, np.ndarray):
        V1 = getNumpyArray(V1)

    if isinstance(V2, r.TH1) and not isinstance(V2, r.TH2):
        V2 = np.diag(np.array([V2.GetBinError(bin)**2 for bin in range(1, V2.GetNbinsX() + 1)], dtype = np.double))
    elif not isinstance(V2, np.ndarray):
        V2 = getNumpyArray(V2)


    if len(w1) != len(w2):
        raise RuntimeError("The length of both arrays is not the same.")
    if V1.shape != V2.shape:
        raise RuntimeError("The shape of the covariance matrices is not the same.")
    if V1.shape[0] != V1.shape[0] or V2.shape[1] != V2.shape[1]:
        raise RuntimeError("One (or both) covariance matrix is (are) not squared.")
    if len(w1) != V1.shape[0] or len(w2) != V2.shape[0]:
        raise RuntimeError("The length of one (or both) array is not the same as the number of lines or columns of its respective covariance matrix.")
    
    dof = len(w1) - 1
    #V1 = np.diag([ V1[el, el] for el in range(len(w1)) ]) ### FORCED DIAGONALISATION
    invV1 = np.linalg.inv(V1); invV2 = np.linalg.inv(V2)
    W1 = sum(w1); W2 = sum(w2)
    #print "W1:",  W1
    #print "W2:",  W2
    #print "dof:", dof
    #print "pruebina:", invV1.dot(V1)[2, 2]
    # 1) Calculation of MLE of the vector of probabilities of each bin
    p    = np.linalg.inv(W1**2 * invV1 + W2**2 * invV2).dot( W1 * invV1.dot(w1) + W2 * invV2.dot(w2) )
    #print "el p esti", p
    # 2) Calculation of the Pearson's chi-squared test statistic
    est  = ((w1 - W1 * p).dot(invV1)).dot((w1 - W1 * p).transpose()) + ((w2 - W2 * p).dot(invV2)).dot((w2 - W2 * p).transpose())
    
    # 3) Calculation of the corresponding p-value
    pval = 1 - chi2.cdf(est, dof)
    return pval, est


def GiveMeMyGoodGOFTests(tsk):
    inpath, iY, var, ty = tsk
    pathtothings = inpath + "/" + iY + "/" + var
    print("\n====== Performing tests for variable", var, "and with type", ty, "\n")
    if   ty == "particle":
        f1 = r.TFile.Open(pathtothings + "/particleOutput.root",        "read")
        f2 = r.TFile.Open(pathtothings + "/particle.root",              "read")
        f5 = r.TFile.Open(pathtothings + "/CovMat_particle.root",       "read")
    elif ty == "particlefidbin":
        f1 = r.TFile.Open(pathtothings + "/particlefidbinOutput.root",  "read")
        f5 = r.TFile.Open(pathtothings + "/CovMat_particlefidbin.root", "read")
    else:
        raise RuntimeError("FATAL: type {t} is not implemented.".format(t = ty))
    

    hData     = deepcopy(f1.Get(var).Clone("hData"))
    hDataCov  = deepcopy(f5.Get("finalmat").Clone("hDataCov"))
    if ty == "particle":
        hDR       = deepcopy(f2.Get("x_tw").Clone("hDR"))
        hDS       = deepcopy(f2.Get("x_twds").Clone("hDS"))
        hHerwig   = deepcopy(f2.Get("x_twherwig").Clone("hHerwig"))
        f1.Close(); f2.Close();  f5.Close() #f3.Close(); f4.Close();
    elif ty == "particlefidbin":
        hDR       = deepcopy(f1.Get("tru").Clone("hDR"))
        hDS       = deepcopy(f1.Get("tru_DS").Clone("hDS"))
        hHerwig   = deepcopy(f1.Get("tru_herwig").Clone("hHerwig"))
        f1.Close(); f5.Close()
    
    hData.SetFillColor(r.kWhite)
    hData.SetLineWidth(2)
    hData.SetLineColor(r.kBlack)
    hData.SetLineStyle(2)

    thelumi = vl.TotalLumi if iY == "run3" else vl.LumiDict[iY]
    scaleval = 1/thelumi/1000

    hDR.SetFillColor(r.kWhite)
    hDR.SetLineWidth(2)
    hDR.SetLineColor(r.kRed)
    if ty == "particle":
        hDR.Scale(scaleval)
    
    #hDS.SetFillColor(r.kWhite)
    #hDS.SetLineWidth(2)
    #hDS.SetLineColor(r.kGreen)
    #hDS.GetXaxis().SetTitle(vl.varList[var]['xaxis'])
    
    #haMCatNLO.SetFillColor(r.kWhite)
    #haMCatNLO.SetLineWidth(2)
    #haMCatNLO.SetLineColor(r.kBlue)
    
    covmat = np.zeros( (hData.GetNbinsX(), hData.GetNbinsX()), dtype = np.double )
    
    for i in range(1, hData.GetNbinsX() + 1):
        for j in range(1, hData.GetNbinsX() + 1):
            #if i != j: continue
            covmat[i-1, j-1] = hDataCov.GetBinContent(i, j)
    
    DRcovmat       = np.diag(np.array([hDR.GetBinError(bin)**2       for bin in range(1, hDR.GetNbinsX() + 1)],     dtype = np.double))
    DScovmat       = np.diag(np.array([hDS.GetBinError(bin)**2       for bin in range(1, hDS.GetNbinsX() + 1)],     dtype = np.double))
    Herwigcovmat   = np.diag(np.array([hHerwig.GetBinError(bin)**2   for bin in range(1, hHerwig.GetNbinsX() + 1)], dtype = np.double))
    #aMCatNLOcovmat = np.diag(np.array([haMCatNLO.GetBinError(bin)**2 for bin in range(1, haMCatNLO.GetNbinsX() + 1)], dtype = np.double))
    
    #covmat         *= 10000**2
    #DRcovmat       *= 10000**2
    #DScovmat       *= 10000**2
    #aMCatNLOcovmat *= 10000**2
    #hDR.Scale(10000)
    #hDS.Scale(10000)
    #haMCatNLO.Scale(10000)
    #hData.Scale(10000)
    #print "\ncovmat de DR\n", DRcovmat
    
    coses = {}
    coses["DR"] = {
        "hist"   : deepcopy(hDR),
        "covmat" : deepcopy(DRcovmat)
    }
    coses["DS"] = {
        "hist"   : deepcopy(hDS),
        "covmat" : deepcopy(DScovmat)
    }
    coses["Herwig"] = {
        "hist"   : deepcopy(hHerwig),
        "covmat" : deepcopy(Herwigcovmat)
    }
    #coses["aMCatNLO"] = {
        #"hist"   : deepcopy(haMCatNLO),
        #"covmat" : deepcopy(aMCatNLOcovmat)
    #}
    
    #for i in range(1, coses["DR"]["hist"].GetNbinsX() + 1):
        #print coses["DR"]["hist"].GetBinContent(
    
    vdata = np.array([hData.GetBinContent(bin) for bin in range(1, hData.GetNbinsX() + 1)], dtype = np.double)
    
    #print "\nWOLOLO\n", coses["aMCatNLO"]["covmat"]
    
    #covmatdiagonal = np.diag(np.array(np.linalg.eig(covmat)[0], dtype = np.double))
    #matriztransf   = np.linalg.eig(covmat)[1]
    #res2           = matriztransf.dot(vdata)
    #res2DR         = matriztransf.dot(np.array([coses["DR"]["hist"].GetBinContent(bin) for bin in range(1, coses["DR"]["hist"].GetNbinsX() + 1)], dtype = np.double))
    #covmatres2DR   = (np.linalg.inv(matriztransf).dot(coses["DR"]["covmat"])).dot(matriztransf)
    #res2DS         = matriztransf.dot(np.array([coses["DS"]["hist"].GetBinContent(bin) for bin in range(1, coses["DS"]["hist"].GetNbinsX() + 1)], dtype = np.double))
    #covmatres2DS   = (np.linalg.inv(matriztransf).dot(coses["DS"]["covmat"])).dot(matriztransf)
    #res2aMC        = matriztransf.dot(np.array([coses["aMCatNLO"]["hist"].GetBinContent(bin) for bin in range(1, coses["aMCatNLO"]["hist"].GetNbinsX() + 1)], dtype = np.double))
    #covmatres2aMC  = (np.linalg.inv(matriztransf).dot(coses["aMCatNLO"]["covmat"])).dot(matriztransf)
    
    #hData2 = deepcopy(hData.Clone("hData2"))
    #hDR2   = deepcopy(coses["DR"]["hist"].Clone("hDR2"))
    #hDS2   = deepcopy(coses["DS"]["hist"].Clone("hDS2"))
    #haMC2  = deepcopy(coses["aMCatNLO"]["hist"].Clone("haMC2"))
    
    #print res2
    #print res2DR
    #print res2DS
    #print "WOLOLO", covmatdiagonal
    #print covmatres2DR
    #print covmatres2DS
    #print covmatres2aMC
    
    #for bin in range(1, hData2.GetNbinsX() + 1):
        #hData2.SetBinContent(bin, res2[bin - 1])
        #hData2.SetBinError(bin, r.TMath.Sqrt(covmatdiagonal[bin-1, bin-1]))
        #hDR2.SetBinContent(bin, res2DR[bin - 1])
        #hDR2.SetBinError(bin, r.TMath.Sqrt(covmatres2DR[bin-1, bin-1]))
        ##print "dif. DR y datos al cuadrao", (hDR2.GetBinContent(bin) - hData2.GetBinContent(bin))**2
        ##print "cov. de datos en este bin", covmatdiagonal[bin-1, bin-1]
        ##print "Cov. de DR en este bin", covmatres2DR[bin-1, bin-1]
        #hDS2.SetBinContent(bin, res2DS[bin - 1])
        #hDS2.SetBinError(bin, r.TMath.Sqrt(covmatres2DS[bin-1, bin-1]))
        #haMC2.SetBinContent(bin, res2aMC[bin - 1])
        #haMC2.SetBinError(bin, r.TMath.Sqrt(covmatres2aMC[bin-1, bin-1]))
    
    #print "\nPRUEBINA", ty
    #print 'DR - p-val.:',        hData2.KolmogorovTest(hDR2)
    ##print 'DR - p-val. (toys):', hData2.KolmogorovTest(hDR2,'X')
    #print 'DR - p-val. (chi2):', hData2.Chi2Test(hDR2,'WW')
    #print 'DS - p-val.:',        hData2.KolmogorovTest(hDS2)
    ##print 'DS - p-val. (toys):', hData2.KolmogorovTest(hDS2,'X')
    #print 'DS - p-val. (chi2):', hData2.Chi2Test(hDS2,'WW')
    #print 'aMCatNLO - p-val.:',        hData2.KolmogorovTest(haMC2)
    ##print 'aMCatNLO - p-val. (toys):', hData2.KolmogorovTest(haMC2,'X')
    #print 'aMCatNLO - p-val. (chi2):', hData2.Chi2Test(haMC2,'WW')
    #print "\n"
    #print "\nPRUEBINA PERO CON LO DE ANTES"
    #print 'DR - p-val.:',        hData.KolmogorovTest(hDR)
    ##print 'DR - p-val. (toys):', hData.KolmogorovTest(hDR,'X')
    #print 'DR - p-val. (chi2):', hData.Chi2Test(hDR,'WW')
    #print 'DS - p-val.:',        hData.KolmogorovTest(hDS)
    ##print 'DS - p-val. (toys):', hData.KolmogorovTest(hDS,'X')
    #print 'DS - p-val. (chi2):', hData.Chi2Test(hDS,'WW')
    #print 'aMCatNLO - p-val.:',        hData.KolmogorovTest(haMCatNLO)
    ##print 'aMCatNLO - p-val. (toys):', hData.KolmogorovTest(haMCatNLO,'X')
    #print 'aMCatNLO - p-val. (chi2):', hData.Chi2Test(haMCatNLO,'WW')
    #print "\n"
    
    #print "Cosa de Serchio pa DR\n"
    #estad = ((res2 - res2DR).dot(np.linalg.inv(covmatdiagonal))).dot((res2 - res2DR).transpose())
    #print "estad.:", estad
    #print "p-valor:", 1 - chi2.cdf(estad, hData.GetNbinsX() - 1)
    
    #print "\nLo mismo pero no en lo de aquello"
    #estad = ((vdata - np.array([coses["DR"]["hist"].GetBinContent(bin) for bin in range(1, coses["DR"]["hist"].GetNbinsX() + 1)], dtype = np.double)).dot(np.linalg.inv(covmat))).dot((vdata - np.array([coses["DR"]["hist"].GetBinContent(bin) for bin in range(1, coses["DR"]["hist"].GetNbinsX() + 1)], dtype = np.double)).transpose())
    #print "estad.:", estad
    #print "p-valor:", 1 - chi2.cdf(estad, hData.GetNbinsX() - 1)
    
    #sys.exit()
    
    ## Valores de atlas manualmente: (E(b))
    #ATLASdata = np.array([ 0.00438, 0.00613, 0.00474, 0.00252, 0.00103 ], dtype = np.double)
    #ATLASmc   = np.array([ 0.0054, 0.0075, 0.005, 0.003, 0.0006 ], dtype = np.double)
    #ATLAScov  = np.diag(([ 0.41, 0.34, 0.44, 0.53, 0.18 ] * ATLASdata)**2)
    
    #pv, es = Chi2TestForMultivarNormal(ATLASdata, ATLAScov, ATLASmc, ATLAScov)
    #print "pv:", pv, "est", es
    #sys.exit()
    
    
    for key in coses:
        vtemp = np.array([coses[key]["hist"].GetBinContent(bin) for bin in range(1, coses[key]["hist"].GetNbinsX() + 1)], dtype = np.double)
        #print "\ncomprobacion de lo que-y metemos al alg."
        #print "covmat datos bin 1", covmat[0,0]
        #print "covmat datos bin 2", covmat[1,1]
        #print "covmat datos bin 3", covmat[2,2]
        #print "covmat datos bin 4", covmat[3,3]
        #print "datos", vdata
        #print "covmat MC bin 1", coses[key]["covmat"][0,0]
        #print "covmat MC bin 2", coses[key]["covmat"][1,1]
        #print "covmat MC bin 3", coses[key]["covmat"][2,2]
        #print "covmat MC bin 4", coses[key]["covmat"][3,3]
        #print "mc", vtemp
        pv, es = Chi2TestForMultivarNormal(vdata, covmat, vtemp, coses[key]["covmat"])
        coses[key]["p-value"]   = pv
        coses[key]["statistic"] = es
    
    if not os.path.isdir(pathtothings + "/goftestplots"):
        os.system("mkdir -p " + pathtothings + "/goftestplots")
    
    plot           = bp.beautifulUnfPlot(var + "_GOF_" + ty, var)
    plot.doRatio   = False
    plot.doFit     = False
    plot.plotspath = pathtothings + "/goftestplots"
    
    #hDS.GetYaxis().SetRangeUser(0, 1.1 * max( [hDS.GetMaximum(), hDR.GetMaximum(), haMCatNLO.GetMaximum(), hData.GetMaximum()] ))
    hDR.GetYaxis().SetRangeUser(0, 1.1 * max( [hDR.GetMaximum(), hData.GetMaximum()] ))
    
    plot.addHisto(hDR,       'hist',      'tW Powheg+Pythia8 DR',  'L', 'mc')
    plot.addHisto(hDS,       'hist,same', 'tW Powheg+Pythia8 DS',  'L', 'mc')
    plot.addHisto(hHerwig,   'hist,same', 'tW Powheg+Herwig7 DR',  'L', 'mc')
    #plot.addHisto(haMCatNLO, 'hist,same', 'tW aMC@NLO', 'L', 'mc')
    plot.addHisto(hData,     'hist,same', 'Data',       'L', 'mc')
    
    l1 = r.TLatex(0.65, 0.650, '#scale[0.4]{DR - p-val.:                %4.10f}'%coses["DR"]["p-value"])
    l2 = r.TLatex(0.65, 0.625, '#scale[0.4]{DR - stat.:                 %4.10f}'%coses["DR"]["statistic"])
    l3 = r.TLatex(0.65, 0.600, '#scale[0.4]{DS - p-val.:                %4.10f}'%coses["DS"]["p-value"])
    l4 = r.TLatex(0.65, 0.575, '#scale[0.4]{DS - stat.:                 %4.10f}'%coses["DS"]["statistic"])
    l5 = r.TLatex(0.65, 0.550, '#scale[0.4]{Herwig - p-val.:            %4.10f}'%coses["Herwig"]["p-value"])
    l6 = r.TLatex(0.65, 0.525, '#scale[0.4]{Herwig - stat.:             %4.10f}'%coses["Herwig"]["statistic"])
    #l7 = r.TLatex(0.65, 0.550, '#scale[0.4]{aMC@NLO - p-val.: %4.10f}'%coses["aMCatNLO"]["p-value"])
    #l8 = r.TLatex(0.65, 0.525, '#scale[0.4]{aMC@NLO - stat.:  %4.10f}'%coses["aMCatNLO"]["statistic"])
    
    l1.SetNDC(True); l2.SetNDC(True); l3.SetNDC(True); l4.SetNDC(True); l5.SetNDC(True); l6.SetNDC(True)

    l1.Draw('same'); l2.Draw('same'); l3.Draw('same'); l4.Draw('same'); l5.Draw('same'); l6.Draw('same')
    
    plot.saveCanvas("TR")
    del plot
    
    outfile = open(pathtothings + "/goftestplots/" + var + "_goftests_" + ty + ".txt", "w")
    outtxt = ""
    outtxt += "Results of GOF tests\n"
    outtxt += "Variable: {vr} \n".format(vr = var)
    outtxt += "=========================================\n"

    for key in ["DR", "DS", "Herwig"]:
        outtxt += key + " / p-value: "        + str(coses[key]["p-value"])   + "\n"
        outtxt += key + " / test statistic: " + str(coses[key]["statistic"]) + "\n"

    outfile.write(outtxt)
    outfile.close(); del outfile;


    print('\nDR - p-val.:',    coses["DR"]["p-value"])
    print('DR - stat.:',       coses["DR"]["statistic"])
    print('DS - p-val.:',      coses["DS"]["p-value"])
    print('DS - stat.:',       coses["DS"]["statistic"])
    print('Herwig - p-val.:',  coses["Herwig"]["p-value"])
    print('Herwig - stat.:',   coses["Herwig"]["statistic"])
    #print 'aMC@NLO - p-val.:', coses["aMCatNLO"]["p-value"]
    #print 'aMC@NLO - stat.:',  coses["aMCatNLO"]["statistic"], "\n"
    del coses
    return



if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inpath',    '-i', metavar = 'inpath',     dest = "inpath",   required = False, default = "./temp/differential")
    parser.add_argument('--year',      '-y', metavar = 'year',       dest = "year",     required = False, default = "all")
    parser.add_argument('--variable',  '-v', metavar = 'variable',   dest = "variable", required = False, default = "all")
    parser.add_argument('--extraArgs', '-e', metavar = 'extra',      dest = "extra",    required = False, default = "")
    parser.add_argument('--nthreads',  '-j', metavar = 'nthreads',   dest = "nthreads", required = False, default = 0, type = int)
    parser.add_argument('--pretend',   '-p', action  = "store_true", dest = "pretend",  required = False, default = False)


    args     = parser.parse_args()
    year     = args.year
    extra    = args.extra
    nthreads = args.nthreads
    pretend  = args.pretend
    inpath   = args.inpath
    variable = args.variable

    #### First, find the tasks
    vetolist = ["plots", "Fiducial", "control", "tables"]
    tasks = []
    if year == "all":
        if variable == "all":
            theyears = []
            presentyears = next(os.walk(inpath))[1]
            if "2022" in presentyears:
                theyears.append("2022")
            if "2022PostEE" in presentyears:
                theyears.append("2022PostEE")
            if "run3" in presentyears:
                theyears.append("run3")

            for iY in theyears:
                if iY != "run3": continue
                thevars = next(os.walk(inpath + "/" + iY))[1]
                for iV in thevars:
                    if any(el in iV for el in vetolist): continue

                    #for t in ["particle", "particlefidbin"]:
                    for t in ["particlefidbin"]:
                        tasks.append( (inpath, iY, iV, t) )

    #tasks = [ (inpath, "2016", "Lep1_Pt") ]

    if nthreads > 1:
        pool = Pool(nthreads)
        pool.map(GiveMeMyGoodGOFTests, tasks)
        pool.close()
        pool.join()
    else:
        for tsk in tasks:
            GiveMeMyGoodGOFTests(tsk)
