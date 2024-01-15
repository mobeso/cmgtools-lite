from .producer import producer
from utils.ftree_producer import ftree_producer
from cfgs.lumi import lumis
import os
import numpy as np
from cfgs.friends_cfg import friends as modules
from cfgs.datasets_cfg import mcas

from functions import color_msg


class plot_producer(producer):
  name = "plot_producer"
  basecommand = "python3 mcPlots.py"
  jobname = "CMGPlot"

  # This is a dictionary that are interesting to make grouped together
  # for different purposes

  plots = {
     "main" : [
        "charge.*", "flavor.*", 
        "m3l", "m3lmet_Meas", "mll3l.*",
        "nJet30.*", "jet.*", "met",
        "lep.*" 
      ],
      "mva" : [
         "mva_lep1.*", "mva_lep2.*", "mva_lep3.*", "mvatth.*"
      ],
      "trigger" : [
         "tot_weight", "lepZ2_pt_trig"
      ]
  }
  
  def add_more_options(self, parser):
    self.parser = parser
    # -- mca includes to consider -- #
    parser.add_option("--mca", dest = "mca", type="string", default = "wz-run3/mca/mca_wz_3l.txt", 
                  help = '''Input mcafile''')
    # -- CMGTools configuration files -- #
    parser.add_option("--mccfile", dest = "mccfile", type="string", default = None, 
                  help = '''Event selection requirements file''')
    parser.add_option("--plotfile", dest = "plotfile", type="string", default = "wz-run3/common/plots_wz.txt", 
                  help = '''File with plots''')
    parser.add_option("--uncfile", dest = "uncfile", type="string", default = "wz-run3/common/systs-wz.txt",
            help = "File with systematic variations")
    parser.add_option("--treename", dest = "treename", default = "NanoAOD", 
                  help = ''' Name of the tree file ''')
    
    # --- More options for customization --- #
    parser.add_option("--blind", dest = "blind", default = False, action = "store_true",
                  help = ''' Blind data flag.''')
    parser.add_option("--unc", dest = "unc", default = False, action = "store_true",
                  help = ''' Apply uncertainties (default is false).''')
    parser.add_option("--cutfile", dest = "cutfile", default = "wz-run3/common/cuts-srwz.txt",
                  help = ''' Region for cut application.''')
    parser.add_option("--normtodata", dest = "normtodata", default = False, action = "store_true",
                  help = ''' Normalize MC to data.''')
    parser.add_option("--plot-groups", dest = "plot_group", default = None,
                  help = ''' Make groups of plots.''')
    
    # --- Override main producer option for output path
    parser.add_option("--outname", dest = "outname", type="string", default = "plots/",
          help = "Output (folder) name")
    parser.add_option("--unweight", dest = "unweight", action="store_true", default = False,
      help = "Don't use corrections")
    return

  def add_friends(self, maxstep = -1):
      """ Method to add friends to command """
      friends = []
      # Iterate over modules available in this year
      for step, module in enumerate(modules[self.year]):
          modulename = module["outname"]
          addmethod = "simple"
          if "addmethod" in module:
            addmethod = module["addmethod"]
          if addmethod == "mc": 
              friends.append( " --FMCs {P}/%s "%(modulename))
          if addmethod == "data": 
              friends.append( " --FDs {P}/%s "%(modulename))
          if addmethod == "simple": 
              friends.append( " --Fs {P}/%s "%(modulename))
      
      return " ".join(friends)
 
  def get_additional_plots(self):
    plots = ""
    if self.plot_group in self.plots.keys():
        plots = " --sP " + " --sP ".join(self.plots[self.plot_group])
    else:
       self.raiseWarning(" >> Warning, there is no group of plots named %s. This will print everything under %s"%(self.plot_group, self.plotfile))
    return plots
  
  def norm_data(self):
    texttonorm = ""

    # Get the correct list of MCA processes
    mc = { group : mcas[group] for group in mcas if group != "data"}
    for group, procs in mc.items():
      for procname in procs.get_datasets():
        texttonorm += "--scaleBkgSigToData %s "%procname if "--scaleBkgSigToData %s "%procname not in texttonorm else ""
    return texttonorm 
 
  def run(self):
    # Yearly stuff 
    year      = self.year
    outname   = self.outname
    extra     = self.extra
    blind     = self.blind
    uncfile   = self.uncfile
    mccfile   = self.mccfile
    apply_unc = self.unc
    lumi      = lumis[year]
    unweight  = self.unweight

    # Other plotting stuff 
    plottingStuff =  "--obj Events "
    plottingStuff += "--maxRatioRange 0.7 1.3 "
    plottingStuff += "--fixRatioRange "
    plottingStuff += "--print C,pdf,png,txt "
    plottingStuff += "--legendWidth 0.23 "
    plottingStuff += "--legendFontSize 0.036 "
    plottingStuff += "--showMCError "
    plottingStuff += "--showRatio "
#    plottingStuff += "--perBin "
    plottingStuff += "--showRatio "
    plottingStuff += "--neg "
    plottingStuff += "--TotalUncRatioColor 922 922 "
    plottingStuff += "--TotalUncRatioStyle 3444 0 "
    plottingStuff += "--plotgroup prompt_WZ+=prompt_WZ_nonfiducial"

    if self.normtodata: plottingStuff += self.norm_data()
    
    plots = ""
    if self.plot_group:
        plots = self.get_additional_plots()
    elif "sP" not in extra:
       self.raiseWarning(" This command will submit everything under %s"%self.plotfile)

    self.mcpath = os.path.join(self.inpath, "mc", self.year)
    self.datapath = os.path.join(self.inpath, "data", self.year)
    
    # List with all the options given to CMGTools
    self.commandConfs = ["%s"%self.mca, 
                   "%s"%self.cutfile,
                   "%s"%self.plotfile,
                   "-l %s"%lumi,
                   "-f --pdir %s"%outname,
                   "--tree %s "%self.treename,
                   "-P {mcpath} -P {datapath}".format(mcpath = self.mcpath, datapath = self.datapath),
                   self.add_friends(),
                   "-L " + " -L ".join(self.functions),
                   "-W '%s'"%("*".join(self.weights)) if not unweight else "-W 'puWeight'", # Always keep PU weights
                   "%s"%plottingStuff,
                   "-j %s"%(self.ncores),
                   "--mcc %s"%mccfile if mccfile != None else "", 
                   "--unc %s"%uncfile if apply_unc else "",
                   "--xp data" if blind else "",
                   plots,
                   "%s"%extra]
    return


