using std::cout;
using std::endl;

double method_cut(int step, double start, double end, double npoints) {
	return start + (end-start)*step/npoints;
}

// double reweight_event(bool isSignal, bool isPhZ, int n1decays) {

// 	if (!isSignal) return 1.;

// 	else if (isPhZ) {
// 		if (n1decays == 1) return 9./4.; // phph event
// 		if (n1decays == 2) return 9./4.; // phZ event
// 		if (n1decays == 3) return 0.; // phh event
// 		if (n1decays == 4) return 9./4.; // ZZ event
// 		if (n1decays == 5) return 0.; // Zh event
// 		if (n1decays == 6) return 0.; // hh event
// 		cout<<"N1 decay not recognised: "<<n1decays<<endl;
// 		return 0.;
// 	}
// 	else {
// 		if (n1decays == 1) return 9./4.; // phph event
// 		if (n1decays == 2) return 0.; // phZ event
// 		if (n1decays == 3) return 9./4.; // phh event
// 		if (n1decays == 4) return 0.; // ZZ event
// 		if (n1decays == 5) return 0.; // Zh event
// 		if (n1decays == 6) return 9./4.; // hh event
// 		cout<<"N1 decay not recognised: "<<n1decays<<endl;
// 		return 0.;
// 	}

// }

void evaluateMethodSig(TH2D *h_passEvents, TString sampleDir, TString weightsDir, double w_lumi, vector<TString> trainVars, vector<TString> specVars, vector<TString> trainMethods, vector<double> methodsRangeDn, vector<double> methodsRangeUp, int plotPointsMethod, bool isSignal) {		

	cout<<sampleDir<<endl;

	TChain chain("mini");

	chain.Add(sampleDir+"/*.root*");
	chain.SetMakeClass(1);

	// Define all possible variables

	Int_t ph_n, el_n, mu_n, jet_n, mcveto, pass_g140, n1decays;
	Float_t met_et, dphi_jetmet, dphi_gammet, dphi_gamjet, ht, rt4, met_sig_obj, met_sig_evt, mt_gam, st_gam, meff, m_yy;
	Float_t weight_mc, weight_pu, weight_sf, weight_ff;
	std::vector<float> *ph_pt=0, *jet_pt=0;

	Float_t ph_n_f, jet_n_f, bjet_n_f, ph_pt0, jet_pt0, lep_n, met_et_D_meff; // integers must be converted to Float_t

	TBranch	*b_ph_pt=0, *b_jet_pt=0;

	std::map<TString, Float_t*> varsMap { 
		{"ph_pt[0]", &ph_pt0},
		{"jet_pt[0]", &jet_pt0},
		{"ht", &ht},
		{"met_et", &met_et},
		{"met_et/meff", &met_et_D_meff},
		{"jet_n", &jet_n_f},
		{"bjet_n", &bjet_n_f},
		{"dphi_jetmet", &dphi_jetmet},
		{"dphi_gammet", &dphi_gammet},
		{"dphi_gamjet", &dphi_gamjet},
		{"met_sig_obj", &met_sig_obj},
		{"met_sig_evt", &met_sig_evt},
		{"mt_gam", &mt_gam},
		{"lep_n := el_n+mu_n", &lep_n},
		{"st_gam := met_et+ph_pt[0]", &st_gam},
		{"ph_n", &ph_n_f},
		{"rt4", &rt4},
		{"meff", &meff},
	};


	TMVA::Reader* reader = new TMVA::Reader("Silent");

	for(auto var : trainVars) {	
		if (varsMap.find(var) == varsMap.end()) {cout<<"\033[1;91mERROR: "<<var<<" not found in dict!!\033[0m"<<endl;return;}
		reader->AddVariable(var, varsMap[var]);
	}

	for(auto var : specVars) {	
		if (varsMap.find(var) == varsMap.end()) {cout<<"\033[1;91mERROR: "<<var<<" not found in dict!!\033[0m"<<endl;return;}
		reader->AddSpectator(var, varsMap[var]);
	}

	for(auto method : trainMethods) {	
		reader->BookMVA(method, Form("%s%s.weights.xml", weightsDir.Data(), method.Data()));
	}

	chain.SetBranchAddress("pass_g140", &pass_g140);
	chain.SetBranchAddress("weight_mc", &weight_mc);
	chain.SetBranchAddress("weight_pu", &weight_pu);
	chain.SetBranchAddress("weight_sf", &weight_sf);
	chain.SetBranchAddress("weight_ff", &weight_ff);
	chain.SetBranchAddress("mcveto", &mcveto);
	chain.SetBranchAddress("n1decays", &n1decays);

	chain.SetBranchAddress("ph_n", &ph_n);
	chain.SetBranchAddress("el_n", &el_n);
	chain.SetBranchAddress("mu_n", &mu_n);
	chain.SetBranchAddress("jet_n", &jet_n);
	chain.SetBranchAddress("bjet_n", &bjet_n);
	chain.SetBranchAddress("ph_pt", &ph_pt, &b_ph_pt);
	chain.SetBranchAddress("jet_pt", &jet_pt, &b_jet_pt);
	chain.SetBranchAddress("met_et", &met_et);
	chain.SetBranchAddress("met_sig_obj", &met_sig_obj);
	chain.SetBranchAddress("met_sig_evt", &met_sig_evt);
	chain.SetBranchAddress("dphi_jetmet", &dphi_jetmet);
	chain.SetBranchAddress("dphi_gammet", &dphi_gammet);
	chain.SetBranchAddress("dphi_gamjet", &dphi_gamjet);
	chain.SetBranchAddress("mt_gam", &mt_gam);
	chain.SetBranchAddress("meff", &meff);

	chain.SetBranchAddress("ht", &ht);
	chain.SetBranchAddress("rt4", &rt4);


	// long long nEntries = 5;
	long long nEntries = chain.GetEntries();
	cout<<"nEntries: "<<nEntries<<endl;


	for (long long iEntry = 0; iEntry < nEntries; iEntry++) {	

		if (nEntries>10 && iEntry % (long long)(nEntries/10) == 0) 
			cout<<"Running... "<<(int)round(iEntry * 100. / nEntries)<<"%"<<endl; /* progress */

		chain.GetEntry(iEntry);

		lep_n = el_n + mu_n;
		ph_n_f = Float_t(ph_n);
		jet_n_f = Float_t(jet_n);
		bjet_n_f = Float_t(bjet_n);

		if (ph_n>0) ph_pt0 = ph_pt->at(0);
		else ph_pt0 = -99.;

		if (jet_n>0) jet_pt0 = jet_pt->at(0);
		else jet_pt0 = -99.;

		if (meff>0) met_et_D_meff = met_et/meff;
		else met_et_D_meff = -99.;

		if (ph_n>0) st_gam = met_et + ph_pt0;
		else st_gam = -99.;

		if (!(preselCuts(pass_g140, mcveto, ph_n, el_n, mu_n, jet_n, ph_pt, met_et, dphi_jetmet, dphi_gammet, dphi_gamjet))) 
			continue;

		double weight = weight_sf * weight_pu * weight_mc * weight_ff * (mcveto==0) * w_lumi;

		weight *= reweight_event(n1decays);

		// cout<<"ph_pt0: "<<ph_pt0<<endl;
		// cout<<"ht: "<<ht<<endl;
		// cout<<"met_et: "<<met_et<<endl;
		// cout<<"met_et_D_meff: "<<met_et_D_meff<<endl;
		// cout<<"jet_n_f: "<<jet_n_f<<endl;
		// cout<<"dphi_jetmet: "<<dphi_jetmet<<endl;
		// cout<<"dphi_gammet: "<<dphi_gammet<<endl;
		// cout<<"dphi_gamjet: "<<dphi_gamjet<<endl;
		// cout<<"met_sig_obj: "<<met_sig_obj<<endl;
		// cout<<"ph_n_f: "<<ph_n_f<<endl;
		// cout<<"lep_n: "<<lep_n<<endl;
		// cout<<"mt_gam: "<<mt_gam<<endl;

		// cout<<"rt4: "<<rt4<<endl;
		// cout<<"meff: "<<meff<<endl;

		// cout<<"weight: "<<weight<<endl;

		// cout<<endl;

		for (int nPoint = 0; nPoint < plotPointsMethod; nPoint++) {

			for (int nMethod = 0; nMethod < trainMethods.size(); nMethod++) {

				double cut_tmp = method_cut(nPoint, methodsRangeDn.at(nMethod), methodsRangeUp.at(nMethod), plotPointsMethod);

				// The rectangular cut classifier is special since it returns a binary answer for a given set of input
				// variables and cuts. The user must specify the desired signal efficiency to define the working point
				// according to which the Reader will choose the cuts

				if (trainMethods.at(nMethod).Contains("Cuts") \
					&& reader->EvaluateMVA(cut_tmp, cut_tmp) ) 

					h_passEvents->Fill(trainMethods.at(nMethod), nPoint, weight);

				else if (reader->EvaluateMVA(trainMethods.at(nMethod)) > cut_tmp) 

					h_passEvents->Fill(trainMethods.at(nMethod), nPoint, weight);


			}

		} 

	}

	delete reader;
	
}