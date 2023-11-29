from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module
from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 


""" These are just some stupid functions to print messages with coloring and all that. Useful for debugging. """
def color_msg(msg, color = "none"):
    """ Prints a message with ANSI coding so it can be printout with colors """
    codes = {
        "none" : "0m",
        "green" : "1;32m",
        "red" : "1;31m",
        "blue" : "1;34m",
        "yellow" : "1;35m"
    }

    print("\033[%s%s \033[0m"%(codes[color], msg))
    return
class nBJetCounter( Module ):
    
    def __init__(self, label, bTagLabel, jetSel, year = "2022EE"):
        self.btagWPs = {
            "btagDeepFlavB" : {
                "2022" : {"Loose" : 0.0583, "Medium" : 0.3086, "Tight" : 0.7183},
                "2022EE" : {"Loose" : 0.0614, "Medium" : 0.3196, "Tight" : 0.7300},
            }
        }

        self._label = label
        self._bTagLabel = bTagLabel
        self._jetCut = jetSel
        self._ops = {}
        
       
        self.WPs = [ (type_, wp) for type_, wp in self.btagWPs[bTagLabel][year].items() ]
        return
     
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        for type_wp, wp in self.WPs:
            self.out.branch("nBJet%s%s" % (self._label, type_wp), "I")
    
    def analyze(self, event):
        #self._n += 1
        jetvals = [ getattr(j, self._bTagLabel) for j in Collection(event, 'Jet') if self._jetCut(j) ]

        #color_msg(" >> Counting b-tagged jets", "green")
        #color_msg("    + Input:" + ", ".join(["%s"%jetval for jetval in jetvals]), "blue")
        for type_wp, wp in self.WPs:
            nBs = sum([v > wp for v in jetvals])
            #color_msg("     + nBs: %d for WP %s (%3.4f)"%(nBs, type_wp, wp))
            self.out.fillBranch("nBJet%s%s" % (self._label, type_wp), nBs)
        return True
