import os, sys, argparse

systsGroup = {
    #### Statistical
    'mc_stat' : [
        "prop_binch1_bin0",
        "prop_binch1_bin1",
        "prop_binch1_bin2",
        "prop_binch1_bin3",
        "prop_binch1_bin4",
        "prop_binch1_bin5",
        "prop_binch1_bin6",
        "prop_binch1_bin7",
        "prop_binch1_bin8",
        "prop_binch1_bin9",
        "prop_binch1_bin10",
        "prop_binch1_bin11",
        "prop_binch1_bin12",
        "prop_binch1_bin13",
        "prop_binch1_bin14",
        "prop_binch1_bin15",
        "prop_binch1_bin16",
        "prop_binch1_bin17",
        "prop_binch1_bin18",
        "prop_binch1_bin19",
        "prop_binch2_bin0",
        "prop_binch2_bin1",
        "prop_binch2_bin2",
        "prop_binch2_bin3",
        "prop_binch2_bin4",
        "prop_binch2_bin5",
        "prop_binch2_bin6",
        "prop_binch2_bin7",
        "prop_binch2_bin8",
        "prop_binch2_bin9",
        "prop_binch2_bin10",
        "prop_binch2_bin11",
        "prop_binch3_bin0",
        "prop_binch3_bin1",
        "prop_binch3_bin2",
        "prop_binch3_bin3",
        "prop_binch3_bin4",
        "prop_binch3_bin5",
        "prop_binch3_bin6",
        "prop_binch3_bin7",
        "prop_binch3_bin8",
        "prop_binch3_bin9",
        "prop_binch3_bin10",
        "prop_binch3_bin11",
        "prop_binch3_bin12",
        "prop_binch3_bin13",
        "prop_binch3_bin14",
        "prop_binch3_bin15",
    ],

    #### Systematic
    # Experimental
    'jes': [
#        "jes",
        "jes_HF",
        "jes_HF_2016",
        "jes_HF_2017",
        "jes_HF_2018",
        "jes_BBEC1",
        "jes_BBEC1_2016",
        "jes_BBEC1_2017",
        "jes_BBEC1_2018",
        "jes_FlavorQCD",
        "jes_RelativeSample_2016",
        "jes_RelativeSample_2017",
        "jes_RelativeSample_2018",
        "jes_EC2",
        "jes_EC2_2016",
        "jes_EC2_2017",
        "jes_EC2_2018",
        "jes_RelativeBal",
        "jes_Absolute",
        "jes_Absolute_2016",
        "jes_Absolute_2017",
        "jes_Absolute_2018",
    ],
    'jer': [
        "jer_2016",
        "jer_2017",
        "jer_2018",
    ],
    'unclenergy' : [
        "unclenergy",
    ],
    'trigger': [
        "triggereff_2016",
        "triggereff_2017",
        "triggereff_2018",
    ],
    'pileup': [
        "pileup",
    ],
    'elec': [
        "elecidsf",
        "elecrecosf",
    ],
    'muon': [
        "muonen_2016",
        "muonen_2017",
        "muonen_2018",
        "muonidsf_stat_2016",
        "muonidsf_stat_2017",
        "muonidsf_stat_2018",
        "muonidsf_syst",
        "muonisosf_stat_2016",
        "muonisosf_stat_2017",
        "muonisosf_stat_2018",
        "muonisosf_syst",
    ],
    'btag': [
        "btagging_2016",
        "btagging_2017",
        "btagging_2018",
        "btagging_corr",
    ],
    'mistag': [
        "mistagging_2016",
        "mistagging_2017",
        "mistagging_2018",
        "mistagging_corr",
    ],
    'lumi': [
        "lumi_2016",
        "lumi_2017",
        "lumi_2018",
        "lumi_corr",
        "lumi_corr1718",
    ],
    'prefiring' : [
        "prefiring_2016",
        "prefiring_2017",
    ],

    # Normalisation
    'ttbar_norm' : [
        "ttbar_norm",
    ],
    'nonworz_norm' : [
        "nonworz_norm",
    ],
    'dy_norm' : [
        "dy_norm",
    ],
    'vvttv_norm' : [
        "vvttv_norm",
    ],

    # Modelling
    'pdf' : [
        "pdfhessian",
    ],
    'matching' : [
        "ttbar_matching",
    ],
    'ttbar_scales' : [
        "ttbar_scales",
    ],
    'tw_scales' : [
        "tw_scales",
    ],
    'isr' : [
        "isr_ttbar",
        "isr_tw",
    ],
    'fsr' : [
        "fsr",
    ],
    'colour' : [
        "colour_rec_erdon",
        "colour_rec_cr1",
        "colour_rec_cr2",
    ],
    'ue' : [
        "ue",
    ],
    'toppt' : [
        "topptrew",
    ],
    'mtop' : [
        "mtop",
    ],
    'ds' : [
        "ds",
    ],
}

systsGroup = {
   'systematics': [        "prop_binch1_bin0",
       "prop_binch1_bin1",
       "prop_binch1_bin2",
       "prop_binch1_bin3",
       "prop_binch1_bin4",
       "prop_binch1_bin5",
       "prop_binch1_bin6",
       "prop_binch1_bin7",
       "prop_binch1_bin8",
       "prop_binch1_bin9",
       "prop_binch1_bin10",
       "prop_binch1_bin11",
       "prop_binch1_bin12",
       "prop_binch1_bin13",
       "prop_binch1_bin14",
       "prop_binch1_bin15",
       "prop_binch1_bin16",
       "prop_binch1_bin17",
       "prop_binch1_bin18",
       "prop_binch1_bin19",
       "prop_binch2_bin0",
       "prop_binch2_bin1",
       "prop_binch2_bin2",
       "prop_binch2_bin3",
       "prop_binch2_bin4",
       "prop_binch2_bin5",
       "prop_binch2_bin6",
       "prop_binch2_bin7",
       "prop_binch2_bin8",
       "prop_binch2_bin9",
       "prop_binch2_bin10",
       "prop_binch2_bin11",
       "prop_binch3_bin0",
       "prop_binch3_bin1",
       "prop_binch3_bin2",
       "prop_binch3_bin3",
       "prop_binch3_bin4",
       "prop_binch3_bin5",
       "prop_binch3_bin6",
       "prop_binch3_bin7",
       "prop_binch3_bin8",
       "prop_binch3_bin9",
       "prop_binch3_bin10",
       "prop_binch3_bin11",
       "prop_binch3_bin12",
       "prop_binch3_bin13",
       "prop_binch3_bin14",
       "prop_binch3_bin15",
       "jes_HF",
       "jes_HF_2016",
       "jes_HF_2017",
       "jes_HF_2018",
       "jes_BBEC1",
       "jes_BBEC1_2016",
       "jes_BBEC1_2017",
       "jes_BBEC1_2018",
       "jes_FlavorQCD",
       "jes_RelativeSample_2016",
       "jes_RelativeSample_2017",
       "jes_RelativeSample_2018",
       "jes_EC2",
       "jes_EC2_2016",
       "jes_EC2_2017",
       "jes_EC2_2018",
       "jes_RelativeBal",
       "jes_Absolute",
       "jes_Absolute_2016",
       "jes_Absolute_2017",
       "jes_Absolute_2018",
       "jer_2016",
       "jer_2017",
       "jer_2018",
       "unclenergy",
       "triggereff_2016",
       "triggereff_2017",
       "triggereff_2018",
       "pileup",
       "elecidsf",
       "elecrecosf",
       "muonen_2016",
       "muonen_2017",
       "muonen_2018",
       "muonidsf_stat_2016",
       "muonidsf_stat_2017",
       "muonidsf_stat_2018",
       "muonidsf_syst",
       "muonisosf_stat_2016",
       "muonisosf_stat_2017",
       "muonisosf_stat_2018",
       "muonisosf_syst",
       "btagging_2016",
       "btagging_2017",
       "btagging_2018",
       "btagging_corr",
       "mistagging_2016",
       "mistagging_2017",
       "mistagging_2018",
       "mistagging_corr",
       "prefiring_2016",
       "prefiring_2017",
       "ttbar_norm",
       "nonworz_norm",
       "dy_norm",
       "vvttv_norm",
       "pdfhessian",
       "ttbar_matching",
       "ttbar_scales",
       "tw_scales",
       "isr_ttbar",
       "isr_tw",
       "fsr",
       "colour_rec_erdon",
       "colour_rec_cr1",
       "colour_rec_cr2",
       "ue",
       "topptrew",
       "mtop",
       "ds",],
   'lumi': [
       "lumi_2016",
       "lumi_2017",
       "lumi_2018",
       "lumi_corr",
       "lumi_corr1718",
   ],     
}





POIs   = ["r"]



groupList   = ['fsr','pileup','dy_norm','colour','jes','matching','ttbar_norm','elec','nonworz_norm','btag','ue','toppt','tw_scales',
              'vvttv_norm','mc_stat','isr','ttbar_scales','lumi','pdf','mistag','ds','jer','trigger','prefiring','muon','mtop','unclenergy']

groupList = ['systematics','lumi']

#groupList   = ['lumi','ds','pileup','muon','dy_norm','colour','jes','matching','ttbar_norm','elec','nonworz_norm','btag','ue','ttbar_scales','tw_scales',
              #'vvttv_norm','mc_stat','isr','mtop','pdf','mistag','fsr','toppt','jer','trigger','prefiring']

basecommand = 'combineTool.py -M MultiDimFit {algosettings} --rMin 0 --rMax 3 --floatOtherPOIs=1 -m 125 --split-points 1 --setParameters r=1 -t -1 --expectSignal=1 --saveInactivePOI 1 {parallel} {queue} {extra} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --robustFit 1 --cminDefaultMinimizerType Minuit'
basecommand = 'combineTool.py -M MultiDimFit {algosettings} --rMin 0 --rMax 3 --floatOtherPOIs=1 -m 125 --split-points 1 --saveInactivePOI 1 {parallel} {queue} {extra} --cminDefaultMinimizerStrategy 0 --X-rtd MINIMIZER_analytic --X-rtd MINIMIZER_MaxCalls=5000000 --robustFit 1 --expectSignal=1 --cminDefaultMinimizerType Minuit'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage = "python nanoAOD_checker.py [options]", description = "Checker tool for the outputs of nanoAOD production (NOT postprocessing)", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--inpath',    '-i',  metavar = 'inpath',     dest = "inpath",   required = False, default = "./temp/cards/combinada.root")
    parser.add_argument('--step',      '-s',  metavar = 'step',       dest = "step",     required = False, default = 0, type = int)
    parser.add_argument('--pretend',   '-p',  action  = "store_true", dest = "pretend",  required = False, default = False)
    parser.add_argument('--nPoints',   '-P',  metavar = 'npoints',    dest = "npoints",  required = False, default = 100, type = int)
    parser.add_argument('--queue',     '-q',  action  = "store_true", dest = "queue",    required = False, default = False)
    parser.add_argument('--ncores',    '-j',  metavar = 'ncores',     dest = "ncores",   required = False, default = None)
    parser.add_argument('--grUnc',     '-g',  metavar = 'grUnc',      dest = "grUnc",    required = False, default = None)

    args     = parser.parse_args()
    pretend  = args.pretend
    thecard  = args.inpath
    step     = args.step
    npoints  = args.npoints
    doBatch  = args.queue
    ncores   = args.ncores
    grUnc    = args.grUnc

    thepath  = "/".join(thecard.split("/")[:-1])
    
    if grUnc:
        groupList = []
        groupList.append(grUnc)

    if step == 0:
        for poi in POIs:
            cumulative      = [x for x in ["r"] if x != poi]

            nomcomm = basecommand.format(algosettings = "--algo grid --points " + str(npoints),
                                         queue        = "" if not doBatch else "--job-mode slurm --task-name nominal_" + poi,
                                         parallel     = "" if not ncores  else "--parallel " + str(ncores),
                                         extra        = '-n nominal_{p} {card} -P {p} {c}'.format(p = poi, card = thecard, c = ",".join(cumulative)))
            print("Command:", nomcomm)
            if not pretend: os.system(nomcomm)

            gridcomm = basecommand.format(algosettings = "--algo none",
                                          queue        = "",
                                          parallel     = "",
                                          extra        = '-n bestfit_{p} --saveWorkspace {card} -P {p}'.format(p = poi, card = thecard))
            print("Command:", gridcomm)
            if not pretend: os.system(gridcomm)

            for group in groupList:
                cumulative += systsGroup[group]
                thecomm = basecommand.format(algosettings = "--algo grid --points " + str(npoints),
                                             queue        = "" if not doBatch else "--job-mode slurm --task-name " + group + "_" + poi,
                                             parallel     = "" if not ncores  else "--parallel " + str(ncores),
                                             extra        = '-P {p} -n {g}_{p} higgsCombinebestfit_{p}.MultiDimFit.mH125.root --snapshotName MultiDimFit --freezeParameters {c}'.format(p = poi, g = group, c = ",".join(cumulative)))
                print("Command:", thecomm)
                if not pretend: os.system(thecomm)
    elif step == 1:
        for poi in POIs:
            fileList        = []
            nomcomm = 'hadd higgsCombinenominal_{p}.MultiDimFit.mH125.root higgsCombinenominal_{p}.POINTS.*.MultiDimFit.mH125.root'.format(p = poi)
            print("Command:", nomcomm)
            if not pretend: os.system(nomcomm)

            for gr in groupList:
                tmpcomm = 'hadd higgsCombine{gp}.MultiDimFit.mH125.root higgsCombine{gp}.POINTS.*.MultiDimFit.mH125.root'.format(gp = gr + '_' + poi)
                fileList.append( "'higgsCombine{gp}.MultiDimFit.mH125.root:Freeze += {g}:{i}'".format(gp = gr + '_' + poi,
                                                                                                      g  = gr,
                                                                                                      i  = groupList.index(gr)))

                print("Command:", tmpcomm)
                if not pretend: os.system(tmpcomm)

            thecomm = "plot1DScan.py higgsCombinenominal_{p}.MultiDimFit.mH125.root --others {l1} --breakdown {l2},stat --POI {p} ".format(
                p  = poi,
                l1 = ' '.join(fileList),
                l2 = ','.join(groupList))
            print("Command:", thecomm)
            if not pretend: os.system(thecomm)

            thecomm = 'mv scan.pdf scan_{p}.pdf; mv scan.png scan_{p}.png'.format(p = poi)
            print('Command:', thecomm)
            if not pretend: os.system(thecomm)

    else:
        raise RuntimeError("FATAL: unknown step asked to process.")
