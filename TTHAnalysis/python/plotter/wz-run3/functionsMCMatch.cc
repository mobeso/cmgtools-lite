#include "TH2F.h"
#include "TMath.h"
#include "TGraphAsymmErrors.h"
#include "TFile.h"
#include "TSystem.h"
#include <iostream>

using namespace std;

bool isFakeL(int id){
  return (id == 2) || (id == 3) || (id == 12) || (id == 13) || (id == -1) || (id == 9) || (id == 5) || (id == 15);
}

bool isFakeT(int id){
  return (id != 5);
}

int countTaus(int nLep, int l1pdgId, int l2pdgId, int l3pdgId, int l4pdgId = 0){
    if(nLep == 3) return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15);
    return (abs(l1pdgId)==15)+(abs(l2pdgId)==15)+(abs(l3pdgId)==15)+(abs(l4pdgId)==15);
}


bool atLeastOneFake(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (nTaus == 0){
    return isFakeL(idl1) || isFakeL(idl2) || isFakeL(idl3);
  }
  if (nTaus == 1){
    return isFakeL(idl1) || isFakeL(idl2) || isFakeT(idt1);
  }
  if (nTaus == 2){
    return isFakeL(idl1) || isFakeT(idt1) || isFakeT(idt2);
  }
}

bool atLeastOneFake4(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (nTaus == 0){
    return isFakeL(idl1) || isFakeL(idl2) || isFakeL(idl3) || isFakeL(idl4);
  }
  if (nTaus == 1){
    return isFakeL(idl1) || isFakeL(idl2) || isFakeL(idl3) || isFakeT(idt1);
  }
  if (nTaus == 2){
    return isFakeL(idl1) || isFakeL(idl2) || isFakeT(idt1) || isFakeT(idt2);
  }
}

bool isConv(int id){
  return (id == 4) || (id == 14);
}

bool atLeastOneConv(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (atLeastOneFake(idl1, idl2, idl3, idl4, idt1, idt2, nTaus)) return false;
  if (nTaus == 0){
    return isConv(idl1) || isConv(idl2) || isConv(idl3);
  }
  if (nTaus == 1){
    return isConv(idl1) || isConv(idl2);
  }
  if (nTaus == 2){
    return isConv(idl1);
  }
}

bool atLeastOneConv2(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (atLeastOneFake(idl1, idl2, idl3, idl4, idt1, idt2, nTaus)) return false;
  if (true){
    return isConv(idl1) || isConv(idl2);
  }
}


bool atLeastOneConv4(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (atLeastOneFake(idl1, idl2, idl3, idl4, idt1, idt2, nTaus)) return false;
  if (nTaus == 0){
    return isConv(idl1) || isConv(idl2) || isConv(idl3) || isConv(idl4);
  }
  if (nTaus == 1){
    return isConv(idl1) || isConv(idl2) || isConv(idl3);
  }
  if (nTaus == 2){
    return isConv(idl1) || isConv(idl2);
  }
}

bool isPromptL(int id){
  return (id == 0) || (id == 1) || (id == 5) || (id == 10) || (id == 11) || (id == 15);
}

bool isPromptT(int id){
  return (id == 5);
}

bool allPrompt2(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (true){
    return isPromptL(idl1) || isPromptL(idl2);
  }
}


bool allPrompt4(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (nTaus == 0){
    return isPromptL(idl1) || isPromptL(idl2) || isPromptL(idl3) || isPromptL(idl4);
  }
  if (nTaus == 1){
    return isPromptL(idl1) || isPromptL(idl2) || isPromptL(idl3) || isPromptT(idt1);
  }
  if (nTaus == 2){
    return isPromptL(idl1) || isPromptL(idl2) || isPromptT(idt1) || isPromptT(idt2);
  }
}

bool allPrompt(int idl1, int idl2, int idl3, int idl4, int idt1, int idt2, int nTaus) {
  if (nTaus == 0){
    return isPromptL(idl1) || isPromptL(idl2) || isPromptL(idl3);
  }
  if (nTaus == 1){
    return isPromptL(idl1) || isPromptL(idl2) || isPromptT(idt1);
  }
  if (nTaus == 2){
    return isPromptL(idl1) || isPromptT(idt1) || isPromptT(idt2);
  }
}

int unused4(int id1, int id2, int ord){
    int idx = 0;
    for (int i = 0; i< 4; i ++){
        if (i == id1 || i == id2){continue;}
        else idx++;
        if (idx == ord) return i;
    }
    return -1;
}


void functionsMCMatch() {}
