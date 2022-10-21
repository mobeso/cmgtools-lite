datasets_wz = {
 "mc" : {
  # ----------------- Single boson
  "WJets"     : [("WJets_inc", ".*WJetsToLNu.*", 63199.9)
                ],
  # ----------------- Drell Yan
  "DY"        : [("DYJetsToLL_M-50", ".*DYJetsToLL_M-50", 6221.3),
                 ("DYJetsToLL_M-50_ext1", ".*DYJetsToLL_M-50_.*pythia8ext1", 6221.3),
                 ("DYJetsToLL_M-50_ext2", ".*DYJetsToLL_M-50_.*pythia8ext2", 6221.3),
                 ("DYJetsToLL_M10to50", ".*DYJetsToLL_M10to50.*", 19317.5)
                ],
  # ----------------- ttbar 
  "TT"        : [("TTTo2L2Nu", ".*TTo2L2Nu_CP5.*", 97.9140), 
                 ("TTTo2J1L1Nu", ".*TTo2J1L1Nu_CP5.*", 405.2403)
                ],
  # ----------------- Single top & tW
  "SingleTop" : [("tbarBQ_t", ".*TbarBQ_t.*", 87.2),
                 ("tBbarQ_t", ".*TBbarQ_t.*", 145.0),
                 ("TbarWplus", ".*TbarWplus.*", 24.2),
                 ("TWminus", ".*TWminus.*", 24.2)
                ],
  # ----------------- Dibosons
  "WZ"        : [("WZ", ".*WZ.*", 54.2776)
                ],
  "ZZ"        : [("ZZ", ".*ZZ.*", 16.7)
                ],
  "WW"        : [("WW", ".*WW.*", 116.8)
                ]
  },
 "data" : {
  # ---------------- Muon 
  "Muon"       : [("Muon_Run2022C", ".*Muon_Run2022C.*"),
                  ("Muon_Run2022D", ".*Muon_Run2022D.*")],
  # ---------------- EGamma 
  "EGamma"     : [("EGamma_Run2022C", ".*EGamma_Run2022C.*"), 
                  ("EGamma_Run2022D", ".*EGamma_Run2022D.*")],
  # ---------------- MuonEG 
  "MuonEG"     : [("MuonEG_Run2022C", ".*MuonEG_Run2022C.*"), 
                  ("MuonEG_Run2022D", ".*MuonEG_Run2022D.*")],
  
  # ---------------- SingleMuon
  "SingleMuon" : [("SingleMuon_Run2022C", ".*SingleMuon.*")],
  # ---------------- DoubleMuon
  "DoubleMuon" : [("DoubleMuon_Run2022C", ".*DoubleMuon.*")]
 # # ---------------- JetHT
 # "JetHT"      : [("JetHT_Run2022C", ".*JetHT.*")],
 # # ---------------- MET 
 # "MET"        : [("MET_Run2022C", ".*_MET.*")],
 # # ---------------- JetMET 
 # "JetMET"     : [("JetMET_Run2022C", ".*JetMET_Run2022C.*"), 
 #                 ("JetMET_Run2022D", ".*JetMET_Run2022D.*")],
 }
}
