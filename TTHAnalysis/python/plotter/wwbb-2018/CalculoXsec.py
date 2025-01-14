import numpy as np



sigmawwbb     = 52.54160211872024
sigmattbar    = 88.28769753
sigmatw       = 19.4674104

#br            = 2*(4*0.11**2 + 4*0.11*0.11*0.17 + 4*(0.11*0.17)**2)
br            = 2*(2*0.11**2 + 4*0.11*0.11*0.17)
brttbar       = 1./3.
brtw          = 2*3*0.11**2

#k             = 1.1397
k             = 1.0695
lumi          = 59740

Nbg           = 10559.0913982 # senal no fiducial
Nwwbb         = sigmawwbb*lumi*k
Nttbar        = brttbar*sigmattbar*lumi
Ntw           = brtw*sigmatw*lumi
Ntot          = Nwwbb + Nttbar + Ntw

Nsigfid       = 56433.3896762 #N(signal + fiducial)
Nfiduc        = 125474.632481
#Nsignal      = 66610.4578863
Nsignal       = 66992.4810744      # From plots .txt

efic          = Nsigfid/Nfiduc
#acept         = Nfiduc/(Nwwbb + Nttbar + Ntw)
acept         = Nfiduc/(Nwwbb)


# CALCULO SUMA SECCIONES EFICACES

#sumaxsec      = sigmawwbb*k + sigmattbar*brttbar + sigmatw*brtw
sumaxsec      = sigmawwbb*k



######## ASIMOV

# CALCULO SECCION EFICAZ

sigmaasim         = (Nsignal - Nbg)/(lumi*efic*acept)
sigmabrasim       = (Nsignal  - 658.00 - 154.33 - 104.53 - Nbg)/(br*lumi*efic*acept)





######## DATOS

Ndatos        = 69120 - 658.00 - 154.33 - 104.53

sigma         = (Ndatos - Nbg)/(lumi*efic*acept)
sigmabr       = (Ndatos - Nbg)/(br*lumi*efic*acept)




print(('Eficiencia            = ' + str(efic)))
print(('Aceptancia            = ' + str(acept)))
print(('BR                    = ' + str(br)))
print(' ')
print(('xsec (DATOS)          = ' + str(sigma)))
print(('xsec(BR) (DATOS)      = ' + str(sigmabr)))
print(' ')
print(('xsec (ASIMOV)         = ' + str(sigmaasim)))
print(('xsec(BR) (ASIMOV)     = ' + str(sigmabrasim)))
print(' ')
print(('sumaxsec              = ' + str(sumaxsec)))


