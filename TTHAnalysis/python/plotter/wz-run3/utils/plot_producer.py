from .producer import producer
from utils.ftree_producer import ftree_producer
from cfgs.lumi import lumis
import os
from cfgs.friends_cfg import friends as modules
from cfgs.datasets_cfg import datasets
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
         "lepsel1_pt", "lepsel1_eta", "lepsel1_minireliso",
         "lepsel2_pt", "lepsel2_eta", "lepsel2_minireliso",
         "lepsel3_pt", "lepsel3_eta", "lepsel3_minireliso",
          "jetptratio", "relv2", "jetdf"
      ],
      "trigger" : [
         "lepZ1_pt", "lepZ2_pt", "lepZ3_pt", 
         "lepZ1_eta", "lepZ2_eta", "lepZ3_eta",
         "tot_weight"
      ]
  }
  

  def add_more_options(self, parser):
    self.parser = parser
    # -- mca includes to consider -- #
    parser.add_option("--mca", dest = "mca", type="string", default = "wz-run3/mca/mca_wz_3l.txt", 
                  help = '''Input mcafile''')
    # -- CMGTools configuration files -- #
    parser.add_option("--cutfile", dest = "cutfile", type="string", default = "wz-run3/common/cuts_wzsm.txt", 
                  help = '''Event selection requirements file''')
    parser.add_option("--mcc", dest = "mcc", type="string", default = "wz-run3/common/mcc_triggerdefs.txt", 
                  help = '''Event selection requirements file''')
    parser.add_option("--plotfile", dest = "plotfile", type="string", default = "wz-run3/common/plots_wz.txt", 
                  help = '''File with plots''')
    parser.add_option("--unc", dest = "uncfile", type="string", default = "wz-run3/common/systs_wz.txt",
            help = "File with systematic variations")
    parser.add_option("--treename", dest = "treename", default = "NanoAOD", 
                  help = ''' Name of the tree file ''')
    
    # --- More options for customization --- #
    parser.add_option("--blind", dest = "blind", default = False, action = "store_true",
                  help = ''' Blind data flag.''')
    parser.add_option("--region", dest = "region", default = "srwz",
                  help = ''' Region for cut application.''')
    parser.add_option("--normtodata", dest = "normtodata", default = False, action = "store_true",
                  help = ''' Normalize MC to data.''')
    parser.add_option("--plot-groups", dest = "plot_group", default = None,
                  help = ''' Make groups of plots.''')
    
    # --- Override main producer option for output path
    parser.add_option("--outname", dest = "outname", type="string", default = "plots/",
          help = "Output (folder) name")
    return

  def add_friends(self, maxstep = -1):
      """ Method to add friends to command """
      friends = []
      # Iterate over modules available in this year
      for step, module in modules[self.year].items():
          # Only add friends to a certain point if step is given
          if maxstep != -1 and step >= maxstep:
              continue
          modulename = module["outname"]
          addmethod = module["addmethod"]
          if addmethod == "mc": 
              friends.append( " --FMCs {P}/%s "%(modulename))
          if addmethod == "data": 
              friends.append( " --FDs {P}/%s "%(modulename))
          if addmethod == "simple": 
              friends.append( " --Fs {P}/%s "%(modulename))
      
      return " ".join(friends)
  
  def norm_data(self):
    texttonorm = ""

    # Get the correct list of MCA processes
    for mca, mca_procs in datasets["mc"].items():
      for proc in mca_procs:
        procname = proc.replace("+","")
        texttonorm += "--scaleBkgSigToData %s "%procname if "--scaleBkgSigToData %s "%procname not in texttonorm else ""
    return texttonorm 
 
  def get_additional_plots(self):
    plots = ""
    if self.plot_group in self.plots.keys():
        plots = " --sP " + " --sP ".join(self.plots[self.plot_group])
    else:
       self.raiseWarning(" >> Warning, there is no group of plots named %s. This will print everything under %s"%(self.plot_group, self.plotfile))
    return plots
     
  def run(self):
    # Yearly stuff 
    year     = self.year
    outname  = os.path.join(self.outname, self.region)
    self.outname = outname
    extra    = self.extra
    blind    = self.blind if self.region == "srwz" else False # Only blind SR
    mincuts  = self.get_cut(self.region)
    uncfile  = self.uncfile
    lumi     = lumis[year]


    # Other plotting stuff 
    plottingStuff =  "--obj Events "
    plottingStuff += "--maxRatioRange 0.5 2.0 "
    plottingStuff += "--fixRatioRange "
    plottingStuff += "--print C,pdf,png,txt "
    plottingStuff += "--legendWidth 0.23 "
    plottingStuff += "--legendFontSize 0.036 "
    plottingStuff += "--showMCError "
    plottingStuff += "--showRatio "
    plottingStuff += "--perBin "
    plottingStuff += "--showRatio "
    plottingStuff += "--neg "
    plottingStuff += "--TotalUncRatioColor 922 922 "
    plottingStuff += "--TotalUncRatioStyle 3444 0 "

    if self.normtodata: plottingStuff += self.norm_data()
    
    plots = ""
    if self.plot_group:
        plots = self.get_additional_plots()
    else:
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
                   "-W '%s'"%("*".join(self.weights)) if len(self.weights) else "",
                   "%s"%plottingStuff,
                   "-j %s"%(self.ncores),
                   "%s"%mincuts,
                   #"--unc %s"%uncfile,
                   "--xp data" if blind else "",
                   plots,
                   "%s"%extra]
    return


