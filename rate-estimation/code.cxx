#include "TGraphErrors.h"
#include "TCanvas.h"
#include "TH1D.h"
#include "TFile.h"
#include "TLine.h"
#include "TGraph.h"
#include <algorithm>
#include <array>
#include <string>
#include <vector>
#include <iostream>
//TH1D* SumTwoHists(const TH1D* const first, const TH1D* const second);

int code(){

  auto c1 = new TCanvas("c1","A Simple Graph with error bars",200,10,700,500);
  c1->SetGrid();

  // create the coordinate arrays
  int n = 10;

  float x[10]  = {-.22,.05,.25,.35,.5,.61,.7,.85,.89,.95};
  float y[10]  = {1,2.9,5.6,7.4,9,9.6,8.7,6.3,4.5,1};

  // create the error arrays
  float ex[10] = {.05,.1,.07,.07,.04,.05,.06,.07,.08,.05};
  float ey[10] = {.8,.7,.6,.5,.4,.4,.5,.6,.7,.8};

  // create the TGraphErrors and draw it
  auto gr = new TGraphErrors(n,x,y,ex,ey);
  gr->SetTitle("TGraphErrors Example");
  gr->SetMarkerColor(4);
  gr->SetMarkerStyle(21);
  gr->Draw("ALP");
  c1->Update();

  return 0;

}
