import ROOT as r

'''
This script plots electrons and jets to see the veto maps of each one.
'''

path = "/beegfs/data/nanoAODv11/tw-run3/productions/2023-06-02/2022PostEE/"
file = "TTto2L2Nu_TuneCP5_13p6TeV_powheg_pythia8_analysis_0.root"
friendFile = "TTto2L2Nu_TuneCP5_13p6TeV_powheg_pythia8_analysis_0_Friend.root"
output = "/mnt_pool/c3_users/user/asoto/Proyectos/tW-Run3/CMSSW_12_4_12/src/CMGTools/TTHAnalysis/python/plotter/tw-run3/utils/vetoMaps/"

friends = ["0_jecs/", "2_cleaning/"]

rootFile = r.TFile(path+file)
tree = rootFile.Get("Events")

# Add friends
for friend in friends:
    tree.AddFriend("Friends", path+friend+friendFile)

# Electron 2D histograms (eta, phi)
h_electron_eta_phi = r.TH2F("h_electron_eta_phi", "Electron #eta vs #phi", 100, -5, 5, 100, -3.2, 3.2)
h_electron_eta_phi.SetStats(False)
h_electron_eta_phi.GetXaxis().SetTitle("#eta")
h_electron_eta_phi.GetYaxis().SetTitle("#phi")
h_electron_eta_phi.GetXaxis().SetTitleOffset(1.2)
h_electron_eta_phi.GetYaxis().SetTitleOffset(1.2)

# Electron 2D histograms (seediEtaOriX, seediPhiOriY)
h_electron_ieta_iphi = r.TH2F("h_electron_ieta_iphi", "Electron seed i#eta vs seed i#phi", 100, 0, 110, 100, 0, 110)
h_electron_ieta_iphi.SetStats(False)
h_electron_ieta_iphi.GetXaxis().SetTitle("seed i#eta")
h_electron_ieta_iphi.GetYaxis().SetTitle("seed i#phi")
h_electron_ieta_iphi.GetXaxis().SetTitleOffset(1.2)
h_electron_ieta_iphi.GetYaxis().SetTitleOffset(1.2)

#Electron 2D histograms (eta, phi) before veto
h_electron_eta_phi_before = r.TH2F("h_electron_eta_phi_before", "Electron #eta vs #phi", 100, -5, 5, 100, -3.2, 3.2)
h_electron_eta_phi_before.SetStats(False)
h_electron_eta_phi_before.GetXaxis().SetTitle("#eta")
h_electron_eta_phi_before.GetYaxis().SetTitle("#phi")
h_electron_eta_phi_before.GetXaxis().SetTitleOffset(1.2)
h_electron_eta_phi_before.GetYaxis().SetTitleOffset(1.2)

# Jet 2D histograms (eta, phi)
h_jet_eta_phi = r.TH2F("h_jet_eta_phi", "Jet #eta vs #phi", 100, -5, 5, 100, -3.2, 3.2)
h_jet_eta_phi.SetStats(False)
h_jet_eta_phi.GetXaxis().SetTitle("#eta")
h_jet_eta_phi.GetYaxis().SetTitle("#phi")
h_jet_eta_phi.GetXaxis().SetTitleOffset(1.2)
h_jet_eta_phi.GetYaxis().SetTitleOffset(1.2)

# Jet 2D histograms before veto (eta, phi)
h_jet_eta_phi_before = r.TH2F("h_jet_eta_phi_before", "Jet #eta vs #phi", 100, -5, 5, 100, -3.2, 3.2)
h_jet_eta_phi_before.SetStats(False)
h_jet_eta_phi_before.GetXaxis().SetTitle("#eta")
h_jet_eta_phi_before.GetYaxis().SetTitle("#phi")
h_jet_eta_phi_before.GetXaxis().SetTitleOffset(1.2)
h_jet_eta_phi_before.GetYaxis().SetTitleOffset(1.2)

# Fill the histograms
counter = 0
for event in tree:
    # Electrons
    for i in range(len(event.LepGood_eta)):
        if abs(event.LepGood_pdgId[i]) == 11:
            h_electron_eta_phi.Fill(event.LepGood_eta[i], event.LepGood_phi[i])
        # for endcap electrons
            if event.LepGood_eta[i] + event.LepGood_deltaEtaSC[i] > 1.479:
                h_electron_ieta_iphi.Fill(event.LepGood_seediEtaOriX[i], event.LepGood_seediPhiOriY[i])
    # Electron before
    for i in range(len(event.Electron_eta)):
        h_electron_eta_phi_before.Fill(event.Electron_eta[i], event.Electron_phi[i])
    
    # Jets
    for i in range(len(event.Jet_pt)):
        if i in event.iJetSel30_Recl:
            h_jet_eta_phi.Fill(event.Jet_eta[i], event.Jet_phi[i])
        h_jet_eta_phi_before.Fill(event.Jet_eta[i], event.Jet_phi[i])

    counter += 1
    if counter % 10000 == 0:
        print("Processed {ev} events".format(ev=counter))
    if counter == 300000:
        break
    
# Plot the histograms
c1 = r.TCanvas("c1", "c1", 800, 600)
c1.cd()
h_electron_eta_phi.Draw("COLZ")
c1.SaveAs(output+"electron_eta_phi.png")
c1.SaveAs(output+"electron_eta_phi.pdf")
c1.SaveAs(output+"electron_eta_phi.root")

c2 = r.TCanvas("c2", "c2", 800, 600)
c2.cd()
h_jet_eta_phi.Draw("COLZ")
c2.SaveAs(output+"jet_eta_phi.png")
c2.SaveAs(output+"jet_eta_phi.pdf")
c2.SaveAs(output+"jet_eta_phi.root")

c3 = r.TCanvas("c3", "c3", 800, 600)
c3.cd()
h_electron_ieta_iphi.Draw("COLZ")
c3.SaveAs(output+"electron_ieta_iphi.png")
c3.SaveAs(output+"electron_ieta_iphi.pdf")
c3.SaveAs(output+"electron_ieta_iphi.root")

c4 = r.TCanvas("c4", "c4", 800, 600)
c4.cd()
h_jet_eta_phi_before.Draw("COLZ")
c4.SaveAs(output+"jet_eta_phi_before.png")
c4.SaveAs(output+"jet_eta_phi_before.pdf")
c4.SaveAs(output+"jet_eta_phi_before.root")

c5 = r.TCanvas("c5", "c5", 800, 600)
c5.cd()
h_electron_eta_phi_before.Draw("COLZ")
c5.SaveAs(output+"electron_eta_phi_before.png")
c5.SaveAs(output+"electron_eta_phi_before.pdf")
c5.SaveAs(output+"electron_eta_phi_before.root")
