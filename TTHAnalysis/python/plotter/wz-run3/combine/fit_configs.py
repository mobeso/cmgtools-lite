"""
Macro with combine configurations to run fits. This is designed to be 
loaded from a combine executor.
"""
import os
mainpath = os.path.join( os.environ["HOME"], "WorkSpace/wz-run3/CMSSW_12_4_12/src/CMGTools/TTHAnalysis/python/plotter/") 


def inclusiveFlavorFit(getDescription = False):
    """ 
        Here we:
         * Fit all the lepton bins
         * Let WZ float only. ZZ is supposed to have a normalisation uncertainty.
    """
    config = {
        # ------- For card combination
        "cards" : {
            "srwz" : os.path.join( mainpath, "cards/wz/srwz_withNorm/" ),
            #"crzz" : os.path.join( mainpath, "cards/wz/crzz/" ),
            #"crtt" : os.path.join( mainpath, "cards/wz/crtt/" )
        },
        "filtercards" : "*txt",
        # ------- For workspace creation
        "ws" : "workspace_wz_inclusiveFlavorFit.root",
        "pois" : [(".*prompt_WZ", "r_wz")],
        "combineModel" : "HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel",
        "out" : "inclusiveFlavorFit",

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

    if getDescription:
        return " Fit to all lepton bins considering SRWZ, CRZZ, CRTT. Only SRWZ floats."
    return config

def mmmFit(getDescription = False):
    """ 
        Here we:
         * Fit only to 3 muon bins
         * Let WZ float only. ZZ is supposed to have a normalisation uncertainty.
    """
    config = inclusiveFlavorFit()
    config["filtercards"] = "*mmm*txt"
    config["out"] = "mmmFit"
    config["ws"] = "workspace_wz_mmmFit.root"
    if getDescription:
        return " Fit only to 3mu bins considering SRWZ, CRZZ, CRTT. Only SRWZ floats."
    return config

def mmeFit(getDescription = False):
    """ 
        Here we:
         * Fit only to mme bins
         * Let WZ float only. ZZ is supposed to have a normalisation uncertainty.
    """
    config = inclusiveFlavorFit()
    config["filtercards"] = "*mme*txt"
    config["out"] = "mmeFit"
    config["ws"] = "workspace_wz_mmeFit.root"
    if getDescription:
        return " Fit only to mme bins considering SRWZ, CRZZ, CRTT. Only SRWZ floats."
    return config

def eemFit(getDescription = False):
    """ 
        Here we:
         * Fit only to eem bins
         * Let WZ float only. ZZ is supposed to have a normalisation uncertainty.
    """
    config = inclusiveFlavorFit()
    config["filtercards"] = "*eem*txt"
    config["out"] = "eemFit"
    config["ws"] = "workspace_wz_eemFit.root"
    if getDescription:
        return " Fit only to eem bins considering SRWZ, CRZZ, CRTT. Only SRWZ floats."
    return config

def eeeFit(getDescription = False):
    """ 
        Here we:
         * Fit only to 3 electron bins
         * Let WZ float only. ZZ is supposed to have a normalisation uncertainty.
    """
    config = inclusiveFlavorFit()
    config["filtercards"] = "*eee*txt"
    config["out"] = "eeeFit"
    config["ws"] = "workspace_wz_eeeFit.root"
    if getDescription:
        return " Fit only to 3e bins considering SRWZ, CRZZ, CRTT. Only SRWZ floats."
    return config


configs = {
    "inclusiveFlavorFit" : inclusiveFlavorFit,
    "mmmFit" : mmmFit,
    "mmeFit" : mmeFit,
    "eemFit" : eemFit,
    "eeeFit" : eeeFit,
}
