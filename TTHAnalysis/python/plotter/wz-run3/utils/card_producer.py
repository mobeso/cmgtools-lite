from .producer import producer
from utils.ftree_producer import ftree_producer
from utils.plot_producer import plot_producer
from cfgs.lumi import lumis
from cfgs.friends_cfg import friends as modules
import os

class card_producer(plot_producer):
  name = "card_producer"
  basecommand = "python3 makeShapeCards_wzRun3.py"
  jobname = "CMGCard"

  def add_more_options(self, parser):
    super().add_more_options(parser)

    #self.parser = parser
    # -- CMGTools configuration files -- #
    
    self.parser.add_option("--var", dest = "var", type="string", default = "(abs(LepZ1_pdgId)+abs(LepZ2_pdgId)+abs(LepW_pdgId)-33)/2", 
                  help = '''Variable to make card''')
    self.parser.add_option("--binning", dest = "binning", type="string", default = "4,-0.5,3.5", 
                  help = '''Binning for variable''')
    self.parser.add_option("--binname", dest = "binname", default = "wz_card",
                      help = ''' Name of the bin within the fit.''')
 
    return
    
  def run(self):
    # Yearly stuff 
    year     = self.year
    binname  = self.binname
    outname  = self.outname.replace("plots", "cards")
    if self.region == None:
        self.raiseError("Please you have to specify a region to do cards")
    outname  = os.path.join(outname, self.region)
    self.outname = outname
    extra    = self.extra
    mincuts  = self.get_cut(self.region)
    uncfile  = self.uncfile
    lumi     = lumis[year]
    mcpath   = os.path.join(self.inpath, "mc", self.year)
    datapath = os.path.join(self.inpath, "data", self.year)

    doAsimov = "--xp data --asimov signal" if self.region == "srwz" else "" # Always blind the fit for SR!!!
    # List with all the options given to CMGTools
    self.commandConfs = ["%s"%self.mca, 
                   "%s"%self.cutfile,
                   '"%s"'%self.var,
                   '"%s"'%self.binning,
                   "--binname %s"%binname,
                   "--tree %s "%self.treename,
                   "-P {mcpath} -P {datapath}".format(mcpath = mcpath, datapath = datapath),
                   self.add_friends(),
                   "-L " + " -L ".join(self.functions),
                   "-W '%s'"%("*".join(self.weights)) if len(self.weights) else "",
                   "-j %s"%(self.ncores),
                   "-l %s"%lumi,
                   doAsimov,
                   "%s"%mincuts,
                   "--unc %s"%uncfile,
                   "--od %s/"%outname,
                   "--autoMCStats",
                   "%s"%extra]
    return


