#include <iostream>
#include <string>            // For strings
#include <TH2D.h>            // ROOT histograms                                                                                                                                                                                                                                          
#include <TFile.h>           // ROOT files                                                                                                   
                                                                                                                                         
#include <TCanvas.h>         // ROOT canvas for plotting                                                                                     
                                                                                                                                            
#include <TPad.h>            // ROOT pads for advanced plotting                                                                                     
#include <TLegend.h>         // ROOT legends for p
#include <TLatex.h>          // ROOT latex for flexible text drawing
#include <TLine.h>           // ROOT support for drawing lines
                                                                                                                                             


int confronto(std::string myfile1, std::string myfile2){


  TFile* histFile1 = TFile::Open(myfile1.c_str(),"READ");
  TH2D* dataHisto1 = (TH2D*)histFile1->Get("fd;1");

  TFile* histFile2 = TFile::Open(myfile2.c_str(),"READ");
  TH2D* dataHisto2 = (TH2D*)histFile2->Get("fd;1");
 

  dataHisto1->SetDirectory(0);
  dataHisto2->SetDirectory(0);
  
 
  histFile1->Close();
  histFile2->Close();

  dataHisto1->SetStats(0);
  dataHisto2->SetStats(0);                                                                                                                  

  dataHisto1->SetLineColor(kRed);
  dataHisto2->SetLineColor(kBlue);
  
    
  TCanvas canvas("canvas","canvas",800,600);//800,600                                                                                         
 
  canvas.cd();
    
  //  dataHisto1->SetMarkerSize(3);
  //dataHisto1->SetMarkerStyle(7);
  //dataHisto2->SetMarkerSize(3);
  //dataHisto2->SetMarkerStyle(7);
  //dataHisto1->SetMarkerColor(2);
  //dataHisto2->SetMarkerColor(4);
  dataHisto1->Draw("");
  dataHisto2->Draw("SAME");
                                                                                                            
  
  //canvas.Print(signal.c_str());
  canvas.SaveAs("confronto.pdf");
  return 0;
}
