from .producer import producer
import os
from cfgs.samplepaths import samplepaths as paths
from cfgs.friends_cfg import friends_mc, friends_data

class ftree_producer(producer):
    name = "ftree_producer"
    basecommand = "python3 prepareEventVariablesFriendTree.py"
    wz_modules = "CMGTools.TTHAnalysis.tools.nanoAOD.wzsm_modules"

    jobname = "happyTreeFriend"

    def add_more_options(self, parser):
        self.parser = parser
        parser.add_option("--step", dest = "step", type = int, default = 1, 
                            help = '''Which friend-tree to run.''')
        parser.add_option("--outname", dest = "outname", type="string", default = paths["processed"],
                            help = "Output (folder) name")
        parser.add_option("--treename", dest = "treename", default = "NanoAOD", 
                            help = ''' Name of the tree file ''')
        parser.add_option("--chunksize", dest = "chunksize", default = 100000, 
                            help = ''' Number of chunks to split jobs''')
        parser.add_option("--analysis", dest = "analysis",  default = "main",
                            help = ''' Run for main analysis or FR analysis ''')
        return

    def submit_InCluster(self):
        queue  = self.queue
        logpath = self.outname
        newcommand = self.command + " --env oviedo -q %s --log-dir %s"%(queue, logpath)
        return newcommand

    def add_friends(self, modules, maxstep = -1):
        """ Method to add friends to command """
        friends = []
        jumpNext = False
        for step, module in enumerate(modules):
            modulename = module[0]
            
            # Only add friends to a certain point if step is given
            if step  >= maxstep: break 
            if not self.isData: 
                friends.append( " --FMC Friends %s/%s/{cname}_Friend.root "%(self.inpath, modulename))
            else: 
                friends.append( " -F Friends %s/%s/{cname}_Friend.root "%(self.inpath, modulename))
           

        return modules[maxstep][1][self.year], modules[maxstep][0], " ".join(friends)

    def run(self):
        ftree = None
        addFriends = None
        if self.isData:
            # Read from datapath
            self.inpath  = os.path.join(self.datapath, self.year)
            ftree, moduleName, addFriends = self.add_friends( friends_data, self.step - 1 ) 
        else:
            self.inpath  = os.path.join(self.mcpath, self.year)
            ftree, moduleName, addFriends = self.add_friends( friends_mc, self.step - 1 ) 
    
        self.outname = os.path.join(self.inpath, moduleName)

        if self.local_test:
            self.outname = "prueba"
            self.chunksize = 1000
            self.run_local = True
            if not self.isData:
                self.extra = "--dm WZ"
            else:
                self.extra = "--dm MuonEG"
            

        self.commandConfs = ["%s"%self.inpath,
            "%s"%self.outname,
            "--name %s"%self.jobname,
            "-t %s"%self.treename,
            "-n -I %s %s"%(self.wz_modules, ftree),
            " -N %s"%self.chunksize,
            "%s"%self.extra,
            addFriends
        ]

        return
