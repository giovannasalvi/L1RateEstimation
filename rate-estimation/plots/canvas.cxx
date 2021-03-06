#include "TGraph.h"
#include "TH1.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TGaxis.h"
#include "TLegend.h"
#include <iostream>
#include <string>            
#include <TH2D.h>            
#include <TFile.h>           
#include <TCanvas.h>         
#include <TPad.h>            
#include <TLegend.h>         
#include <TLatex.h>                                                                                                                 

int canvas()
{
  // note: this macro assumes that both graphs have the same x-axis range
  //TH2F* h1 = new TH2F("h1", "h1 title", 100, 0.0, 200, 100, 0.0, 200);
  // TH2F* h2 = new TH2F("h2", "h2 title", 100, 0.0, 200, 100, 0.0, 200);
  
  //  TFile* histFile1 = TFile::Open(myfile1.c_str(),"READ");
  //TH1D* dataHisto1 = (TH1D*)histFile1->Get("Histo_CHF_400");
  
    
  TFile *f1 = TFile::Open("54_6923.root");
  //f1->ls();
  TH2D* histo1 = (TH2D*)f1->Get("fd;1");  
  histo1->SetLineColor(2);

  TFile *f2 = TFile::Open("246_6923.root");
  //f2->ls();
  TH2D* histo2 = (TH2D*)f2->Get("fd;1");



  TCanvas canvas("canvas","canvas",800,600);//800,600                                                                                         
  canvas.cd();
  histo1->SetLineColor(4);
  histo1->Draw("");
  histo2->Draw("same");
    
  //  canvas.SaveAs("Comparison.pdf");

  return 0;    
}
