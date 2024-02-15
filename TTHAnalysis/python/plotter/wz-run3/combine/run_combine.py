from optparse import OptionParser
import os 
import re
import sys

mainpath = os.path.join( os.environ["HOME"], "WorkSpace/wz-run3/CMSSW_12_4_12/src/CMGTools/TTHAnalysis/python/plotter/") 
def color_msg(msg, color = "none", indentlevel=0):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "none" : "0m",
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
        "yellow" : "1;35m"
    }

    if indentlevel == 0: indentSymbol=">> "
    if indentlevel == 1: indentSymbol="+ "
    if indentlevel == 2: indentSymbol="* "

    indent = indentlevel*" " + indentSymbol
    print("\033[%s%s%s \033[0m"%(codes[color], indent, msg))
    return

def add_parsing_opts():
    ''' Function with base parsing arguments used by any script '''
    parser = OptionParser(usage = "python wz-run.py [options]", 
                                    description = "Main options for running WZ analysis") 

    # -- Input and outputs
    
    parser.add_option("--mode", dest = "mode", default = "combinecards",
                help = "Mode to run")
    parser.add_option("--add-filter", "-a", dest = "filters", action = "append", default = [],
                help = "All inputs will form a unique regular expression for filtering cards. ORDER MATTERS.")
    parser.add_option("--output", "-o", dest = "output_folder", default = "inclusiveFlavorFit",
                help = "Output folder")
    parser.add_option("--submit", dest = "submit", default = False, action="store_true",
                help = "Submit job.")
    return parser

def create_outpath(out):
    """ Function to make sure output path exists """
    if not os.path.exists( out ):
        os.system("mkdir -p %s"%out)
    return

def fit_configs(filters = [], out = "fitResult"):
    """ 
       Configure basic stuff for fits 
    """
    filtertext = "*".join( filters + [".txt"]) 
    config = {
        # ------- For card combination
        "cards" : {
            "srwz" : os.path.join( mainpath, "cards/wz/srwz/" ),
            "crzz" : os.path.join( mainpath, "cards/wz/crzz/" ),
            #"crtt" : os.path.join( mainpath, "cards/wz/crtt/" )
        },
        "filtercards" : "*{filters}".format( filters = filtertext ),
        # ------- For workspace creation
        "ws" : "workspace_wz.root",
        "pois" : [
            (".*prompt_WZ", "r_wz"), 
            (".*prompt_ZZ", "r_zz")
        ],
        "combineModel" : "HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel",
        "out" : "{out}".format( out = out ),

        # ------- For fits
        "signalPOI" : "r_wz",
        "blind" : True,
        "additional" : [
            # Add convergence options
            "--X-rtd MINIMIZER_MaxCalls=99999999999",
            " --maxFailedSteps 500", 
            "--X-rtd MINIMIZER_analytic",
            " --setRobustFitTolerance 0.05", 
            "--cminPreScan", 
            "--cminDefaultMinimizerStrategy 0"
        ]
    }

    return config

def combine_cards(config):
    """ Function to combine cards using fancy naming so they can be tracked in the impacts """
    combine_fields = []
    out = config["out"]

    maincmd="combineCards.py {cards} > combinedCard.dat"
    for binname, filespath in config["cards"].items():
        color_msg("Combing cards in %s"%filespath, "green", 1)
        combine_fields.append( "%s/%s"%(filespath, config["filtercards"] ) )
        #for file in os.listdir(filespath):
        #    if not re.match( config["filtercards"], file): continue
        #    color_msg("Found this card: %s"%file, "blue", 2)
        #    ch = file.replace(".txt", "")
        #    combine_fields.append( "{name}={path}/{card}".format( name = ch, path = filespath, card = file))
    
    cards = " ".join(combine_fields)

    cmd = maincmd.format(cards = cards)
    return [cmd]

def workspace(config):
    """ Function to create workspace """
    maincmd = "text2workspace.py combinedCard.dat -o {out} -P {combineModel} --PO verbose --PO {maps}"
    # Build the mappings
    maps = []

    for p in config["pois"]:
        maps.append( " 'map=.*/%s:%s[1, 0, 6]'"%(p[0], p[1])) # Float between 0 and 6 -- hardcoded

    cmd = maincmd.format( out = config["ws"], combineModel = config["combineModel"], maps = " --PO".join(maps))
    return [cmd]

def impacts(config):
    """ Function to run impacts """
    maincmd = "combineTool.py -M Impacts -m 125 -d {ws} --doInitialFit {blind} --redefineSignalPOI {signalPOI} {additional}"
    
    # Build the mappings
    blindtext = ""
    if config["blind"]:
        blindtext = "-t -1 --setParameters %s=1"%config["signalPOI"]
        #pois_fixed=[]
        #for poi in config["pois"]:
        #    pois_fixed.append("%s=1"%poi[1])
        
        #blindtext += ",".join(pois_fixed)

    initialFit = maincmd.format( ws = config["ws"], signalPOI = config["signalPOI"], blind = blindtext, additional = " ".join(config["additional"]))
#    doFits = initialFit.replace("doInitialFit", "doFits --parallel 12 --job-mode slurm --sub-opts='-p batch' ")
    doFits = initialFit.replace("doInitialFit", "doFits --parallel 12 ")

    collectImpacts = "combineTool.py -M Impacts -m 125 -o impacts.json --redefineSignalPOI {signalPOI} {blind} -d {ws}".format(ws = config["ws"], signalPOI = config["signalPOI"], blind = blindtext)
    plotImpacts = "plotImpacts.py -i impacts.json -o impacts"
    return [initialFit, doFits, collectImpacts, plotImpacts]

def scan(config):
    """ Function to run likelihood scan commands """
    points = 500
    maincmd = "combineTool.py -M MultiDimFit --algo grid --points {points} --rMin 0 --rMax 6 -m 125 -d {ws} {blind} --redefineSignalPOI {signalPOI} {additional} -n _nominal"
    
    # Build the mappings
    blindtext = ""
    if config["blind"]:
        blindtext = "-t -1 --setParameters %s=1"%config["signalPOI"]
        #pois_fixed=[]
        #for poi in config["pois"]:
        #    pois_fixed.append("%s=1"%poi[1])
        
        #blindtext += ",".join(pois_fixed)

    initialScan = maincmd.format( points = points, ws = config["ws"], signalPOI = config["signalPOI"], blind = blindtext, additional = " ".join(config["additional"]))
    snapshot = initialScan.replace("grid --points %d"%points, "none ").replace("nominal", "bestfit")
    snapshot += " --saveWorkspace"
    ScanFreeze = maincmd.format( points = points, ws = "higgsCombine_bestfit.MultiDimFit.mH125.root", signalPOI = config["signalPOI"], blind = blindtext, additional = " ".join(config["additional"]))
    ScanFreeze += " --snapshotName MultiDimFit --freezeParameters allConstrainedNuisances"
    ScanFreeze = ScanFreeze.replace("nominal", "stat")
    
    plotScan = "plot1DScan.py higgsCombine_nominal.MultiDimFit.mH125.root --POI {poi}  --others 'higgsCombine_stat.MultiDimFit.mH125.root:FreezeAll:2'  --breakdown Syst,Stat --logo-sub Internal".format(poi = config["signalPOI"])
    return [initialScan, snapshot, ScanFreeze, plotScan]

def fitDiagnostics(config):
    """ Function to run fitDiagnostics tool """
    maincmd = "sbatch --wrap 'combine -M FitDiagnostics {ws} -m 125 --plots --saveShapes -t -1 --setParameters %s=1 --saveWithUncertainties  --numToysForShapes 100 --skipBOnlyFit {additional} -v 3'"%config["signalPOI"]
    cmd = maincmd.format(ws = config["ws"], additional = " ".join(config["additional"]))
    return [cmd]

def multigof(config):
    points = 320000
    jobs = 32
    pointsperjob = points/jobs
    card = config["ws"]
    cmds = [ "sbatch --wrap 'combine -M GoodnessOfFit --algo saturated %s -t %i -s %i -m %i'"%(card, pointsperjob, i, i) for i in range(jobs)]
    return cmds

if __name__ == "__main__":
    opts, args = add_parsing_opts().parse_args()

    mode = opts.mode
    filters = opts.filters
    output_folder = opts.output_folder

    cmds = None
    
    # Get the proper configuration
    config_to_use = fit_configs(filters = filters, out = output_folder) 

    # make sure the output exists
    if opts.submit:
        create_outpath(config_to_use["out"])
    if mode == "combinecards": 
        cmds = combine_cards( config_to_use )
    elif mode == "workspace":
        cmds = workspace( config_to_use )
    elif mode == "impacts":
        cmds = impacts( config_to_use )
    elif mode == "scan":
        cmds = scan( config_to_use )
    elif mode == "fitDiagnostics":
        cmds = fitDiagnostics( config_to_use )
    elif mode == "multigof":
        cmds = multigof( config_to_use )
 
    for icmd, cmd in enumerate(cmds):
        color_msg("Command %d:"%icmd, "green")
        cmd = "cd %s; %s; cd -"%(config_to_use["out"], cmd)
        print(cmd) 
        if opts.submit:
            os.system(cmd)

