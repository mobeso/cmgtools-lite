import correctionlib._core as core
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
import ROOT as r
import os
import numpy as np

class applyElectronSS( Module ):
    def __init__(self, basepath, isData, file = 'SS.json'):
        self.basepath     = basepath
        self.file = file
        self.isData = isData
        self.evaluatorScaleName = "Prompt2022FG_ScaleJSON"
        self.evaluatorSmearingName = "Prompt2022FG_SmearingJSON"
        if self.file == '':
            self.nominalValues = True
        else:
            self.nominalValues = False
            self.evaluatorScale = core.CorrectionSet.from_file(self.basepath + file)[self.evaluatorScaleName]
            self.evaluatorSmearing = core.CorrectionSet.from_file(self.basepath + file)[self.evaluatorSmearingName]

    def beginJob(self):
        pass

    def endJob(self):
        pass

    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.wrappedOutputTree = wrappedOutputTree
        self.wrappedOutputTree.branch("Electron_corrected_pt"  , 'F', lenVar = "nElectron")
        if not self.isData:
            self.wrappedOutputTree.branch("Electron_sigmaUp_pt"  , 'F', lenVar = "nElectron")
            self.wrappedOutputTree.branch("Electron_sigmaDown_pt", 'F', lenVar = "nElectron")
            self.wrappedOutputTree.branch("Electron_scaleUp_pt"  , 'F', lenVar = "nElectron")
            self.wrappedOutputTree.branch("Electron_scaleDown_pt", 'F', lenVar = "nElectron")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def analyze(self, ev):
        outpt = []; outsigmaup = []; outsigmadn = []; outscaleup = []; outscaledn = []
        if not self.nominalValues: # This will run corrections
            for iE in range(ev.nElectron):
                if self.isData:
                    #########
                    # Scale #
                    #########
                    scale = self.evaluatorScale.evaluate("total_correction", int(ord(ev.Electron_seedGain[iE])), float(ev.run), ev.Electron_eta[iE] + ev.Electron_deltaEtaSC[iE], ev.Electron_r9[iE], ev.Electron_pt[iE])
                    # Scale is multiplicative correction, unlike smearing, it is deterministic
                    corrected_pt = scale * ev.Electron_pt[iE]
                    outpt.append(corrected_pt)

                else:
                    ############
                    # Smearing #
                    ############
                    rho = self.evaluatorSmearing.evaluate("rho", ev.Electron_eta[iE] + ev.Electron_deltaEtaSC[iE], ev.Electron_r9[iE])  # rho is internal scale and smearing lingo
                    # It does not correspond to the pileup rho energy density, instead it is the standard deviation of the Gaussian used to draw the smearing
                    rng = np.random.default_rng()  # The smearing is done statistically, so we need some random numbers
                    smearing = rng.normal(loc=1., scale=rho) # We could try to improve this setting the seed deterministically to have reproducible results
                    corrected_pt = smearing * ev.Electron_pt[iE]
                    outpt.append(corrected_pt) 

                    # Systematic uncertainty on smearing (evaluated on MC)
                    unc_rho = self.evaluatorSmearing.evaluate("err_rho",  ev.Electron_eta[iE] + ev.Electron_deltaEtaSC[iE], ev.Electron_r9[iE])
                    rho_up = rho + unc_rho
                    rho_down = rho - unc_rho
                    smearing_up = rng.normal(loc=1., scale=rho_up)
                    smearing_down = rng.normal(loc=1., scale=rho_down)

                    # To use the systematic variations in your analysis, you should treat smearing_up and smearing_down as multiplicative factors for the uncorrected photon pt in MC
                    corrected_pt_smearing_up = smearing_up * ev.Electron_pt[iE]
                    corrected_pt_smearing_down = smearing_down * ev.Electron_pt[iE]    
                    outsigmaup.append(corrected_pt_smearing_up)
                    outsigmadn.append(corrected_pt_smearing_down)
                    
                    # Systematic uncertainty for scale: Careful, this is evaluated on MC because we always apply systematics on MC, not on data
                    scale_MC_unc = self.evaluatorScale.evaluate("total_uncertainty", int(ord(ev.Electron_seedGain[iE])), float(ev.run), ev.Electron_eta[iE] + ev.Electron_deltaEtaSC[iE], ev.Electron_r9[iE], ev.Electron_pt[iE])
                    
                    # To use the systematic variations in your analysis, you should treat scale_up and scale_down as multiplicative factors for the uncorrected (nominal) photon pt in MC
                    corrected_pt_scale_up = (1+scale_MC_unc) * ev.Electron_pt[iE]
                    corrected_pt_scale_down = (1-scale_MC_unc) * ev.Electron_pt[iE]
                    outscaleup.append(corrected_pt_scale_up)
                    outscaledn.append(corrected_pt_scale_down)
        else: # This will not run corrections
            for iE in range(ev.nElectron):
                outpt.append(ev.Electron_pt[iE])
                outsigmaup.append(ev.Electron_pt[iE])
                outsigmadn.append(ev.Electron_pt[iE])
                outscaleup.append(ev.Electron_pt[iE])
                outscaledn.append(ev.Electron_pt[iE])

        self.wrappedOutputTree.fillBranch("Electron_corrected_pt"  , outpt)
        if not self.isData:
            self.wrappedOutputTree.fillBranch("Electron_sigmaUp_pt"  , outsigmaup)
            self.wrappedOutputTree.fillBranch("Electron_sigmaDown_pt", outsigmadn)
            self.wrappedOutputTree.fillBranch("Electron_scaleUp_pt"  , outscaleup)
            self.wrappedOutputTree.fillBranch("Electron_scaleDown_pt", outscaledn)
                    
        return True
