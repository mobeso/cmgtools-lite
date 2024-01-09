/* 
Script to launch TMVA training for lepton MVA used in Run2. Adapted to
be used in Run3 as well.

author: carlos.vico.villalba@cern.ch
*/

// Import libraries
#include <assert.h>
using namespace std;


// Main macro implementation
void trainMuonID_NanoAODv11(TString folder, TString name, TString year) {

  // To keep track of all samples used
  TString path;
  if (year == "2022"){
      path = "/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/ttSemilep_nanoAODv12_preEE/Run3Summer22NanoAODv12/231031_163325/0000/"; 
  }
  else if (year == "2022EE"){
    path = "/lustrefs/hdd_pool_dir/nanoAODv12/wz-run3/ttSemilep_nanoAODv12_postEE/Run3Summer22EENanoAODv12/231031_163052/0000/"; 
  }
  else {
    cout << "Please enter a valid era" << endl; 
    return;
  }

  // Chain signal and background samples (in this case we just have the one :D )
  TChain *dSig1 = new TChain("Events");
  TChain *dBg1  = new TChain("Events");

  int firstFile = 101;
  int lastFile = 201;
  for (int i = firstFile; i < lastFile; i++) {
    TString istr = TString::Format("%d", i);
    //std::cout << "Adding file step0_" << istr << std::endl;
    TString filename = path + "/step0_" + istr + ".root";
    dSig1 -> AddFile(filename);
    dBg1 -> AddFile(filename);
  } 
  std::cout << "Statistics: " << dSig1->GetEntries() << std::endl;
  // Prepare output 
  TString mkdir = "mkdir -p " + folder;
  gSystem -> Exec(mkdir);
  TFile *fOut = new TFile(folder + "/" + name + ".root", "RECREATE");
 
  // Now prepare training
  TString factory_conf = "!V:!Color:Transformations=I";

  TMVA::Factory    *factory    = new TMVA::Factory(name, fOut, factory_conf.Data());
  TMVA::DataLoader *dataloader = new TMVA::DataLoader("dataset");


  // This will be used to cut on the lepton properties for the training
  TCut lepton = "1";
  
  // Use NanoAOD-like variables
  dataloader->AddVariable("Muon_pt",'D');
  dataloader->AddVariable("Muon_eta",'D');
  dataloader->AddVariable("Muon_pfRelIso03_all",'D'); 
  dataloader->AddVariable("Muon_miniPFRelIso_chg",'D'); 
  dataloader->AddVariable("Muon_miniRelIsoNeutral := Muon_miniPFRelIso_all - Muon_miniPFRelIso_chg", 'D');
  dataloader->AddVariable("Muon_jetNDauCharged",'D'); 
  dataloader->AddVariable("Muon_jetPtRelv2", 'D');

  // Test out the performance for different taggers
  if (name.Contains("df")){
    std::cout << "    - Using DF b tagger" << std::endl;
    dataloader->AddVariable("Muon_jetBTagDeepFlavB := Muon_jetIdx > -1 ? Jet_btagDeepFlavB[Muon_jetIdx] : 0", 'D');
  } else if (name.Contains("pnet")) {
    std::cout << "    - Using ParticleNet b tagger" << std::endl;
    dataloader->AddVariable("Muon_jetBTagPNET := Muon_jetIdx > -1 ? Jet_btagPNetB[Muon_jetIdx] : 0", 'D');
  } 
  dataloader->AddVariable("Muon_jetPtRatio := min(1 / (1 + Muon_jetRelIso), 1.5)", 'D'); 
  dataloader->AddVariable("Muon_sip3d", 'D'); 
  dataloader->AddVariable("Muon_log_dxy := log(abs(Muon_dxy))",'D'); 
  dataloader->AddVariable("Muon_log_dz  := log(abs(Muon_dz))",'D'); 
  dataloader->AddVariable("Muon_segmentComp", 'D');  

  /*  
  // Use MiniAOD-like variables
  dataloader->AddVariable("Muon_LepGood_pt",'D');
  dataloader->AddVariable("Muon_LepGood_eta",'D');
  dataloader->AddVariable("Muon_LepGood_pfRelIso03_all",'D'); 
  dataloader->AddVariable("Muon_LepGood_miniRelIsoCharged",'D'); 
  dataloader->AddVariable("Muon_LepGood_miniRelIsoNeutral", 'D');
  dataloader->AddVariable("Muon_LepGood_jetNDauChargedMVASel",'D'); 
  dataloader->AddVariable("Muon_LepGood_jetPtRelv2", 'D'); 
  // Test out the performance for different taggers
  if (name.Contains("df")){
    std::cout << "    - Using DF b tagger" << std::endl;
    dataloader->AddVariable("Muon_LepGood_jetDF", 'D');
  } else if (name.Contains("pnet")) {
    std::cout << "    - Using ParticleNet b tagger" << std::endl;
    dataloader->AddVariable("Muon_LepGood_jetPNET", 'D');
  } 
  dataloader->AddVariable("Muon_LepGood_jetPtRatio", 'D'); 
  dataloader->AddVariable("Muon_LepGood_sip3d", 'D'); 
  dataloader->AddVariable("Muon_LepGood_dxy",'D'); 
  dataloader->AddVariable("Muon_LepGood_dz",'D'); 
  dataloader->AddVariable("Muon_LepGood_segmentComp", 'D');  
  */

  lepton += "Muon_miniPFRelIso_all < 0.4 && Muon_sip3d < 8 && abs(Muon_dxy) < 0.05 && abs(Muon_dz) < 0.1"; // line 18 
  if (name.Contains("tth")){
    lepton += "abs(Muon_eta) < 2.4 && Muon_pt > 5 ";
    lepton += "Muon_looseId == 1"; 
  }
  
  else if (name.Contains("ttw")){
    lepton += "Muon_pt > 10 && abs(Muon_eta) < 2.4";
    lepton += "(Muon_isGlobal == 1 || Muon_isTracker == 1)";
    lepton += "Muon_isPFcand == 1";
    lepton += "Muon_mediumId == 1";
  }

  double wSig = 1.0, wBkg = 1.0;
  dataloader->AddSignalTree(dSig1, wSig);
  dataloader->AddBackgroundTree(dBg1, wBkg);

  // Apply preselection and divide the sample in signal and background
  dataloader->PrepareTrainingAndTestTree(lepton+" Muon_genPartFlav == 1 || Muon_genPartFlav == 15", lepton+" Muon_genPartFlav != 1 && Muon_genPartFlav != 15", "");
  
  TString BDTGopt  = "!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:UseNvars=9:MaxDepth=8";

  BDTGopt += ":CreateMVAPdfs"; // Create Rarity distribution
  factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDTG", BDTGopt);

  factory->TrainAllMethods();
  factory->TestAllMethods();
  factory->EvaluateAllMethods();
  
  fOut->Close();  
}
