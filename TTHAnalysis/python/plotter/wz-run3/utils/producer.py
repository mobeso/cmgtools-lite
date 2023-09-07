''' Main class for producing CMGtools commands '''
# -- Import libraries -- #
import argparse
import os,sys
from cfgs.samplepaths import samplepaths as paths
from functions import color_msg

class producer(object):
    weights = ['puWeight*muonSF*electronSF*bTagWeight']
    functions = ["wz-run3/functionsWZ.cc"]

    name = "producer"
    cluster_comm = "sbatch -c {nc} -J {jn} -p {q} -e {logpath}/logs/log.%j.%x.err -o {logpath}/logs/log.%j.%x.out --wrap '{comm}' "
    jobname = "CMGjob"
    
    def __init__(self, parser):
        self.add_more_options(parser)
        self.unpack_opts()
        self.doData = "data" if self.isData else "mc"

        return

    def add_more_options(self, parser):
        self.parser = parser 
        return

    def summarize(self):
        ''' Method to show a summary of the given options '''
        color_msg(" >> %s will run with the following options"%self.name, "green") 
        opts = vars(self.opts)
        
        for opt in opts:
            if opt == "extra" : continue # Plot this at the end 
            print("    * %s : %s"%(opt, getattr(self, opt)))
        print("    * extra : %s"%(getattr(self, "extra")))
        color_msg(" >> Command below:", "green")
        return
 
    def submit_InCluster(self):
        nc = self.ncores
        jn = self.jobname
        q    = self.queue
        logpath = self.outname
        ### Make sure log folder exists
        if not os.path.exists("%s/logs"%logpath):
            os.system("mkdir -p %s/logs"%logpath)
        newcommand = self.cluster_comm.format(nc = nc, jn = jn, q = q, logpath = logpath, comm = self.command)
        return newcommand

    def build_command(self):
        if self.summary: self.summarize() 
        confs = self.commandConfs 
        command = "%s %s"%(self.basecommand," ".join(confs))
        self.command = command
        return

    def submit_command(self):
        comm = self.command
        if not self.run_local: 
            comm = self.submit_InCluster()
        print(comm) 
        if self.doSubmit:
            os.system(comm)
        return
         
    def unpack_opts(self):
        ''' Method to unpack the given options into a dictionary '''
        self.opts, self.args = self.parser.parse_args()
        for opt in vars(self.opts):
            setattr(self, opt, vars(self.opts)[opt])
        return

    def run(self):
        ''' To be implemented in different classes ''' 
        pass

    def get_cut(self, region):
        ''' Minimal cuts to define different regions of the analysis '''
        cuts = {
            "srwz" : "-E ^SRWZ",
            "crzz" : "-E ^CRZZnomet -X ^AllTight -E ^ZZTight",
            "crdy" : "-E ^CRDY",
            "crtt" : "-E ^CRTT",
            "crxg" : "-E ^CRconv"
        }
        return cuts[region]
        
    def raiseError(self, msg):
        logmsg = "[%s::ERROR]: %s"%(self.name, msg)
        color_msg(logmsg, "red")
        sys.exit(1)
        

    def raiseWarning(self, msg):
        logmsg = "[%s::WARNING]: %s"%(self.name, msg)
        color_msg(logmsg, "yellow")
        return

