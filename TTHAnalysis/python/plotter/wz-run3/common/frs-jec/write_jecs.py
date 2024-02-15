text = '''
change: m3Lmet\\b: m3Lmet_{nuis}{var}
change: MET_pt_central\\b: PuppiMET_T1_pt_{nuis}{var}
### --- Please review if that is the branch we have to change.... Rember issue with MET_pt_central and PuppiMet and all that
change: nBJetTight25_Mini\\b: nBJetTight25_Mini_{nuis}{var}
change: nBJetTight25\\b: nBJetTight25_Mini_{nuis}{var}
change: nBJetMedium25_Mini\\b: nBJetMedium25_Mini_{nuis}{var}
change: nBJetMedium25\\b: nBJetMedium25_Mini_{nuis}{var}
change: nBJetLoose25_Mini\\b: nBJetLoose25_Mini_{nuis}{var}
change: nBJetLoose25\\b: nBJetLoose25_Mini_{nuis}{var}

change: bTagWeight\\b: bTagWeight_{nuis}{var}
change: bTagWeight\\b: bTagWeight_{nuis}{var}
change: bTagWeight\\b: bTagWeight_{nuis}{var}

change: JetClean25_pt\\b: JetClean25_pt_{nuis}{var}
weight:1
'''

nuisances = "jesTotal jesHF jesBBEC1_year jesFlavorQCD jesRelativeSample_year jesEC2 jesHF_year jesRelativeBal jesAbsolute_year jesBBEC1 jesEC2_year jesAbsolute jer"
nuisances = nuisances.split(" ")

for var in ["Up", "Down"]:
  for nuis in nuisances:
    f = open("fr-standard-%s%s.txt"%(nuis, var), "w")
    f.write(text.format(nuis = nuis, var = var))
    f.close()
