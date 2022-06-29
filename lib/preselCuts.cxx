bool _preselCuts(Int_t pass_g140, Int_t pass_xe, Int_t mcveto, Int_t ph_n, Int_t el_n, Int_t mu_n, Int_t jet_n, std::vector<float> * ph_pt, Float_t met_et, Float_t dphi_jetmet, Float_t dphi_gammet, Float_t dphi_gamjet)
{
	if (met_et>200&&ph_n==1&&jet_n>0&&el_n+mu_n==0&&mcveto==0&&dphi_jetmet>0.4&&dphi_gammet>0.4&&pass_xe==1) return true;
	return false;
}