# -- Friend tree modules 
friends = { 
    "2022": {
        1 : {
            "data" : "jmeCorrections_data", 
            "mc"   : "jmeCorrections_mc", 
            "addmethod" : "simple", 
            "outname" : "jmeCorrections"
            },
        2 : {
            "data" : "leptonJetRecleaning",
            "mc"   : "leptonJetRecleaning",
            "addmethod" : "simple",
            "outname" : "leptonJetRecleaning"
            },
        3 : {
            "data" : "leptonBuilder",
            "mc"   : "leptonBuilder",
            "addmethod" : "simple",
            "outname" : "leptonBuilder"
            },
        4 : {
            "data" : None,
            "mc"   : "scalefactors",
            "addmethod" : "simple",
            "outname" : "scalefactors"
            }
        
    },
    "2022EE": {
        1 : {
            "data" : "jmeCorrections_data_EE", 
            "mc"   : "jmeCorrections_mc_EE", 
            "addmethod" : "simple", 
            "outname" : "jmeCorrections"},
        2 : {
            "data" : "leptonJetRecleaning",
            "mc"   : "leptonJetRecleaning",
            "addmethod" : "simple",
            "outname" : "leptonJetRecleaning" 
            },
        3 : {
            "data" : "leptonBuilder",
            "mc"   : "leptonBuilder",
            "addmethod" : "simple",
            "outname" : "leptonBuilder"
            },
        4 : {
            "data" : None,
            "mc"   : "scalefactors",
            "addmethod" : "mc",
            "outname" : "scalefactors"
            }
    }
}