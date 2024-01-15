# -- Friend tree modules 
friends = { 
    "2022": [
        { "data" : "lepEnergyCorrection_2022_data", "mc" : "lepEnergyCorrection_2022",   "outname" : "leptonEnergyCorrections"},
        { "data" : "jmeCorrections_data",           "mc" : "jmeCorrections_mc",          "outname" : "jmeCorrections"},
        { "data" : "lepmvas_2022",                  "mc" : "lepmvas_2022",               "outname" : "lepmva" },
        { "data" : "leptonJetRecleaning",           "mc" : "leptonJetRecleaning",        "outname" : "leptonJetRecleaning"},
        { "data" : "leptonBuilder",                 "mc" : "leptonBuilder",              "outname" : "leptonBuilder" },
        { "data" : None,                            "mc" : "scalefactors_2022",          "outname" : "scalefactors", "addmethod" : "mc" },       
        { "data" : None,                            "mc" : "leptonGENBuilder",           "outname" : "lepGEN", "addmethod" : "mc" },       
    ],
    "2022EE": [
        { "data" : "lepEnergyCorrection_2022EE_data", "mc" : "lepEnergyCorrection_2022EE", "outname" : "leptonEnergyCorrections"},
        { "data" : "jmeCorrections_data_EE",          "mc" : "jmeCorrections_mc_EE",       "outname" : "jmeCorrections"},
        { "data" : "lepmvas_2022EE",                  "mc" : "lepmvas_2022EE",             "outname" : "lepmva" },
        { "data" : "leptonJetRecleaning_2022EE",      "mc" : "leptonJetRecleaning_2022EE", "outname" : "leptonJetRecleaning"},
        { "data" : "leptonBuilder",                   "mc" : "leptonBuilder",              "outname" : "leptonBuilder" },
        { "data" : None,                              "mc" : "scalefactors_2022EE",        "outname" : "scalefactors", "addmethod" : "mc" },       
        { "data" : None,                              "mc" : "leptonGENBuilder",           "outname" : "lepGEN", "addmethod" : "mc" },       
    ],
}
