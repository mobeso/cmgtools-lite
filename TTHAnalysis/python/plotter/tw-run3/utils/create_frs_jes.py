import os, sys
from CMGTools.TTHAnalysis.tools.nanoAOD.jetMetGrouper_TopRun3 import groups

'''
This script creates the files fr-jes{sys}Up.txt and fr-jes{sys}Dn.txt from the reference file fr-jesTotal.txt
Just need to keep updated the reference file and the groups in jetMetGrouper_TopRun3.py
'''

path = '{cmsswpath}/src/CMGTools/TTHAnalysis/python/plotter/tw-run3/frs-jecs/'.format(cmsswpath = os.environ['CMSSW_BASE'])

referenceFiles = ['fr-jesUp.txt', 'fr-jesDn.txt']

nameScaff = 'fr-jes{sys}{updn}.txt'

for group in groups:
    for i, updn in enumerate(["Up", "Down"]):
        print("Created: " + nameScaff.format(sys = group, updn = updn))
        # We create the file copying the reference file
        os.system("cp {path}{ref} {path}{name}".format(path = path, ref = referenceFiles[i], name = nameScaff.format(sys = group, updn = updn)))
        # We open the file and each line we replace jesTotal by jes{sys}
        with open(path + nameScaff.format(sys = group, updn = updn), 'r') as file:
            filedata = file.read()
        filedata = filedata.replace('jesTotal', 'jes{sys}'.format(sys = group))
        with open(path + nameScaff.format(sys = group, updn = updn), 'w') as file:
            file.write(filedata)

print("Done!")
