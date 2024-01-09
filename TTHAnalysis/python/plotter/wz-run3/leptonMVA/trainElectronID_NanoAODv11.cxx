/* 
Script to launch TMVA training for lepton MVA used in Run2. Adapted to
be used in Run3 as well.

author: carlos.vico.villalba@cern.ch
*/

// Import libraries
#include <assert.h>
using namespace std;


// Main macro implementation
void trainElectronID_NanoAODv11(TString folder, TString name, TString year) {

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
  
  // Training variables for Electrons
  // Use NanoAOD-like variables
  dataloader->AddVariable("Electron_pt",'D');
  dataloader->AddVariable("Electron_eta",'D');
  dataloader->AddVariable("Electron_pfRelIso03_all",'D'); 
  dataloader->AddVariable("Electron_miniPFRelIso_chg",'D'); 
  dataloader->AddVariable("Electron_miniRelIsoNeutral := Electron_miniPFRelIso_all - Electron_miniPFRelIso_chg", 'D');
  dataloader->AddVariable("Electron_jetNDauCharged",'D'); 
  dataloader->AddVariable("Electron_jetPtRelv2", 'D');

  // Test out the performance for different taggers
  if (name.Contains("df")){
    std::cout << "    - Using DF b tagger" << std::endl;
    dataloader->AddVariable("Electron_jetBTagDeepFlavB := Electron_jetIdx > -1 ? Jet_btagDeepFlavB[Electron_jetIdx] : 0", 'D');
  } else if (name.Contains("pnet")) {
    std::cout << "    - Using ParticleNet b tagger" << std::endl;
    dataloader->AddVariable("Electron_jetBTagPNET := Electron_jetIdx > -1 ? Jet_btagPNetB[Electron_jetIdx] : 0", 'D');
  } 
  dataloader->AddVariable("Electron_jetPtRatio := min(1 / (1 + Electron_jetRelIso), 1.5)", 'D'); 
  dataloader->AddVariable("Electron_sip3d", 'D'); 
  dataloader->AddVariable("Electron_log_dxy := log(abs(Electron_dxy))",'D'); 
  dataloader->AddVariable("Electron_log_dz  := log(abs(Electron_dz))",'D'); 
  
  // Test out the performance using noISO mva
  if (name.Contains("useNoIso")){
    std::cout << "    - Using noISO mva" << std::endl;
    dataloader->AddVariable("Electron_mvaNoIso", 'D');  
  } else if (name.Contains("useIso")) {
    std::cout << "    - Using ISO mva" << std::endl;
    dataloader->AddVariable("Electron_mvaIso", 'D');
  }

  /*
  // Use MiniAOD-like variables
  dataloader->AddVariable("Electron_LepGood_pt",'D');
  dataloader->AddVariable("Electron_LepGood_eta",'D');
  dataloader->AddVariable("Electron_LepGood_pfRelIso03_all",'D'); 
  dataloader->AddVariable("Electron_LepGood_miniRelIsoCharged",'D'); 
  dataloader->AddVariable("Electron_LepGood_miniRelIsoNeutral", 'D');
  dataloader->AddVariable("Electron_LepGood_jetNDauChargedMVASel",'D'); 
  dataloader->AddVariable("Electron_LepGood_jetPtRelv2", 'D');

  // Test out the performance for different taggers
  if (name.Contains("df")){
    std::cout << "    - Using DF b tagger" << std::endl;
    dataloader->AddVariable("Electron_LepGood_jetDF", 'D');
  } else if (name.Contains("pnet")) {
    std::cout << "    - Using ParticleNet b tagger" << std::endl;
    dataloader->AddVariable("Electron_LepGood_jetPNET", 'D');
  } 
  dataloader->AddVariable("Electron_LepGood_jetPtRatio", 'D'); 
  dataloader->AddVariable("Electron_LepGood_sip3d", 'D'); 
  dataloader->AddVariable("Electron_LepGood_dxy",'D'); 
  dataloader->AddVariable("Electron_LepGood_dz",'D'); 
  
  // Test out the performance using noISO mva
  if (name.Contains("useNoIso")){
    std::cout << "    - Using noISO mva" << std::endl;
    dataloader->AddVariable("Electron_LepGood_mvaWinter22V1noIso", 'D');  
  }
  */

  lepton += "Electron_miniPFRelIso_all < 0.4 && Electron_sip3d < 8";
  lepton += "Electron_lostHits <= 1"; 
  lepton += "abs(Electron_dxy) < 0.05 && abs(Electron_dz) < 0.1"; 

  if (name.Contains("tth")){
    lepton += "abs(Electron_eta) < 2.5 && Electron_pt > 5 ";
    //lepton += "Electron_mvaNoIso_Fall17V2_WPL == 1";
    if (year == "2022EE") {
      lepton += "(Electron_eta > 1.56 && int(Electron_seediEtaOriX) < 45 && Electron_seediPhiOriY > 72)? 0 : 1";
    }  
  }
  else if (name.Contains("ttw")){
    lepton += "Electron_pt > 10 && abs(Electron_eta) < 2.5";
    if (year == "2022EE") {
      lepton += "(Electron_eta > 1.56 && int(Electron_seediEtaOriX) < 45 && Electron_seediPhiOriY > 72)? 0 : 1";
    }
  }


  double wSig = 1.0, wBkg = 1.0;
  dataloader->AddSignalTree(dSig1, wSig);
  dataloader->AddBackgroundTree(dBg1, wBkg);
  // Apply preselection and divide the sample in signal and background
  dataloader->PrepareTrainingAndTestTree(lepton+" Electron_genPartFlav == 1 || Electron_genPartFlav == 15", lepton+" Electron_genPartFlav != 1 && Electron_genPartFlav != 15", "");
  
  TString BDTGopt  = "!H:!V:NTrees=500:BoostType=Grad:Shrinkage=0.10:!UseBaggedGrad:nCuts=2000:UseNvars=9:MaxDepth=8";
  BDTGopt += ":CreateMVAPdfs"; // Create Rarity distribution
  factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDTG", BDTGopt);
  
  factory->TrainAllMethods();
  factory->TestAllMethods();
  factory->EvaluateAllMethods();
  
  fOut->Close();

}
