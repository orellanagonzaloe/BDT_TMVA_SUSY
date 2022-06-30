
using std::cout;
using std::endl;

float get_m_yy(float ph_pt1, float ph_eta1, float ph_phi1, float ph_pt2, float ph_eta2, float ph_phi2) {

	TLorentzVector ph1, ph2;

	ph1.SetPtEtaPhiM(ph_pt1, ph_eta1, ph_phi1, 0.);
	ph2.SetPtEtaPhiM(ph_pt2, ph_eta2, ph_phi2, 0.);

	return (ph1 + ph2).M();
	
}

float get_st_gam(float met_et, vector<float> *ph_pt) {

	float st_gam = met_et;

	for (const auto& pt : *ph_pt) {

		st_gam += pt;

	}

	return st_gam;
	
}


void createTrainTestSamples(TString inputdir, TString outputdir, float trainTestSplit, int nEntries = -1) {	

	// init config

	if (!inputdir.EndsWith("/"))  inputdir  = inputdir+"/";
	if (!outputdir.EndsWith("/")) outputdir = outputdir+"/";

	int division = rint(100./trainTestSplit);

	TObjArray* tokens = inputdir.Tokenize("/");
	TString filename = ((TObjString*) (*tokens).Last())->GetString();

	bool isdata = false;

	if (filename.Contains("data") || filename.Contains("efake") || filename.Contains("jfake"))
		isdata = true;

	TChain chain("mini");
	chain.Add(inputdir+"*.root*");
	chain.SetMakeClass(1);

	if (nEntries<0)
		nEntries = chain.GetEntries();

	cout<<"nEntries: "<<nEntries<<endl;

	if (nEntries<2) {
		cout<<"Chain with not enough events"<<endl;
		return;
	} 

	TH1F * h_events = new TH1F("events", "Events", 6, 0.5, 6.5);
	h_events->GetXaxis()->SetBinLabel(1, "# events initial");
	h_events->GetXaxis()->SetBinLabel(2, "# events selected");
	h_events->GetXaxis()->SetBinLabel(3, "sumw initial");
	h_events->GetXaxis()->SetBinLabel(4, "sumw selected");
	h_events->GetXaxis()->SetBinLabel(5, "sumw2 initial");
	h_events->GetXaxis()->SetBinLabel(6, "sumw2 selected");

	auto dir = gSystem->OpenDirectory(inputdir);
	while (auto f = gSystem->GetDirEntry(dir)) {

		if (!strcmp(f,".") || !strcmp(f,"..")) continue;

		TFile *file_tmp = new TFile(inputdir+f);

		TH1F * h_events_tmp = (TH1F*)file_tmp->Get("events");
		h_events->Add(h_events_tmp, 1./division);

		delete h_events_tmp;
		delete file_tmp;
		
	}
	gSystem->FreeDirectory(dir);


	// TString filename_tmp = filename(0, filename.Length()-5); // remove '.root' from end: Not needed anymore

	TString outputdir_test = outputdir + filename + "_test/";
	TString outputdir_train = outputdir + filename + "_train/";

	system(TString("mkdir -p " + outputdir_test).Data());
	system(TString("mkdir -p " + outputdir_train).Data());

	TString output_test = outputdir_test + filename + "_test.root";
	TString output_train = outputdir_train + filename + "_train.root";

	TFile *f_bkg_test = new TFile(output_test, "recreate");
	TTree *t_bkg_test = new TTree("mini", "mini");

	h_events->Write("events");

	TFile *f_bkg_train = new TFile(output_train, "recreate");
	TTree *t_bkg_train = new TTree("mini", "mini");

	h_events->Write("events");


	// old variables

	int pass_g140=0, mcveto=0, n1decays=0;
	int ph_n=0, el_n=0, mu_n=0, jet_n=0, bjet_n=0;
	float met_et=-99., dphi_jetmet=-99., dphi_gammet=-99., dphi_gamjet=-99., ht=-99., ht0=-99., rt4=-99., met_sig_obj=-99., met_sig_evt=-99., mt_gam=-99., meff=-99.;
	float weight_mc=1., weight_pu=1., weight_sf=1., weight_ff=1.;
	std::vector<float> *ph_pt = 0, *ph_eta = 0, *ph_phi = 0, *jet_pt = 0;

	chain.SetBranchAddress("pass_g140", &pass_g140);
	if (!isdata)
	{
		chain.SetBranchAddress("mcveto", &mcveto);
		chain.SetBranchAddress("n1decays", &n1decays);
	}
	else
	{
		chain.SetBranchAddress("weight_ff", &weight_ff);
	}

	chain.SetBranchAddress("weight_mc", &weight_mc);
	chain.SetBranchAddress("weight_pu", &weight_pu);
	chain.SetBranchAddress("weight_sf", &weight_sf);

	chain.SetBranchAddress("ph_n", &ph_n);
	chain.SetBranchAddress("el_n", &el_n);
	chain.SetBranchAddress("mu_n", &mu_n);
	chain.SetBranchAddress("jet_n", &jet_n);
	chain.SetBranchAddress("bjet_n", &bjet_n);
	chain.SetBranchAddress("ph_pt", &ph_pt);
	chain.SetBranchAddress("jet_pt", &jet_pt);
	chain.SetBranchAddress("met_et", &met_et);
	chain.SetBranchAddress("met_sig_obj", &met_sig_obj);
	chain.SetBranchAddress("met_sig_evt", &met_sig_evt);
	chain.SetBranchAddress("dphi_jetmet", &dphi_jetmet);
	chain.SetBranchAddress("dphi_gammet", &dphi_gammet);
	chain.SetBranchAddress("dphi_gamjet", &dphi_gamjet);
	chain.SetBranchAddress("mt_gam", &mt_gam);
	chain.SetBranchAddress("meff", &meff);
	chain.SetBranchAddress("ht", &ht);
	chain.SetBranchAddress("ht0", &ht0);
	chain.SetBranchAddress("rt4", &rt4);

	chain.SetBranchAddress("ph_etas2", &ph_eta);
	chain.SetBranchAddress("ph_phi", &ph_phi);

	// new variables

	TBranch *b_pass_g140_test = t_bkg_test->Branch("pass_g140", &pass_g140, "pass_g140/I");
	TBranch *b_mcveto_test = t_bkg_test->Branch("mcveto", &mcveto, "mcveto/I");
	TBranch *b_n1decays_test = t_bkg_test->Branch("n1decays", &n1decays, "n1decays/I");

	TBranch *b_weight_ff_test = t_bkg_test->Branch("weight_ff", &weight_ff, "weight_ff/F");
	TBranch *b_weight_mc_test = t_bkg_test->Branch("weight_mc", &weight_mc, "weight_mc/F");
	TBranch *b_weight_pu_test = t_bkg_test->Branch("weight_pu", &weight_pu, "weight_pu/F");
	TBranch *b_weight_sf_test = t_bkg_test->Branch("weight_sf", &weight_sf, "weight_sf/F");

	TBranch *b_ph_n_test = t_bkg_test->Branch("ph_n", &ph_n, "ph_n/I");
	TBranch *b_el_n_test = t_bkg_test->Branch("el_n", &el_n, "el_n/I");
	TBranch *b_mu_n_test = t_bkg_test->Branch("mu_n", &mu_n, "mu_n/I");
	TBranch *b_jet_n_test = t_bkg_test->Branch("jet_n", &jet_n, "jet_n/I");
	TBranch *b_bjet_n_test = t_bkg_test->Branch("bjet_n", &bjet_n, "bjet_n/F");
	TBranch *b_ph_pt_test = t_bkg_test->Branch("ph_pt", &ph_pt);
	TBranch *b_jet_pt_test = t_bkg_test->Branch("jet_pt", &jet_pt);
	TBranch *b_met_et_test = t_bkg_test->Branch("met_et", &met_et, "met_et/F");
	TBranch *b_met_sig_obj_test = t_bkg_test->Branch("met_sig_obj", &met_sig_obj, "met_sig_obj/F");
	TBranch *b_met_sig_evt_test = t_bkg_test->Branch("met_sig_evt", &met_sig_evt, "met_sig_evt/F");
	TBranch *b_dphi_jetmet_test = t_bkg_test->Branch("dphi_jetmet", &dphi_jetmet, "dphi_jetmet/F");
	TBranch *b_dphi_gammet_test = t_bkg_test->Branch("dphi_gammet", &dphi_gammet, "dphi_gammet/F");
	TBranch *b_dphi_gamjet_test = t_bkg_test->Branch("dphi_gamjet", &dphi_gamjet, "dphi_gamjet/F");
	TBranch *b_mt_gam_test = t_bkg_test->Branch("mt_gam", &mt_gam, "mt_gam/F");
	TBranch *b_meff_test = t_bkg_test->Branch("meff", &meff, "meff/F");
	TBranch *b_ht_test = t_bkg_test->Branch("ht", &ht, "ht/F");
	TBranch *b_ht0_test = t_bkg_test->Branch("ht0", &ht0, "ht/F");
	TBranch *b_rt4_test = t_bkg_test->Branch("rt4", &rt4, "rt4/F");


	TBranch *b_pass_g140_train = t_bkg_train->Branch("pass_g140", &pass_g140, "pass_g140/I");
	TBranch *b_mcveto_train = t_bkg_train->Branch("mcveto", &mcveto, "mcveto/I");
	TBranch *b_n1decays_train = t_bkg_train->Branch("n1decays", &n1decays, "n1decays/I");

	TBranch *b_weight_ff_train = t_bkg_train->Branch("weight_ff", &weight_ff, "weight_ff/F");
	TBranch *b_weight_mc_train = t_bkg_train->Branch("weight_mc", &weight_mc, "weight_mc/F");
	TBranch *b_weight_pu_train = t_bkg_train->Branch("weight_pu", &weight_pu, "weight_pu/F");
	TBranch *b_weight_sf_train = t_bkg_train->Branch("weight_sf", &weight_sf, "weight_sf/F");

	TBranch *b_ph_n_train = t_bkg_train->Branch("ph_n", &ph_n, "ph_n/I");
	TBranch *b_el_n_train = t_bkg_train->Branch("el_n", &el_n, "el_n/I");
	TBranch *b_mu_n_train = t_bkg_train->Branch("mu_n", &mu_n, "mu_n/I");
	TBranch *b_jet_n_train = t_bkg_train->Branch("jet_n", &jet_n, "jet_n/I");
	TBranch *b_bjet_n_train = t_bkg_train->Branch("bjet_n", &bjet_n, "bjet_n/F");
	TBranch *b_ph_pt_train = t_bkg_train->Branch("ph_pt", &ph_pt);
	TBranch *b_jet_pt_train = t_bkg_train->Branch("jet_pt", &jet_pt);
	TBranch *b_met_et_train = t_bkg_train->Branch("met_et", &met_et, "met_et/F");
	TBranch *b_met_sig_obj_train = t_bkg_train->Branch("met_sig_obj", &met_sig_obj, "met_sig_obj/F");
	TBranch *b_met_sig_evt_train = t_bkg_train->Branch("met_sig_evt", &met_sig_evt, "met_sig_evt/F");
	TBranch *b_dphi_jetmet_train = t_bkg_train->Branch("dphi_jetmet", &dphi_jetmet, "dphi_jetmet/F");
	TBranch *b_dphi_gammet_train = t_bkg_train->Branch("dphi_gammet", &dphi_gammet, "dphi_gammet/F");
	TBranch *b_dphi_gamjet_train = t_bkg_train->Branch("dphi_gamjet", &dphi_gamjet, "dphi_gamjet/F");
	TBranch *b_mt_gam_train = t_bkg_train->Branch("mt_gam", &mt_gam, "mt_gam/F");
	TBranch *b_meff_train = t_bkg_train->Branch("meff", &meff, "meff/F");
	TBranch *b_ht_train = t_bkg_train->Branch("ht", &ht, "ht/F");
	TBranch *b_ht0_train = t_bkg_train->Branch("ht0", &ht0, "ht/F");
	TBranch *b_rt4_train = t_bkg_train->Branch("rt4", &rt4, "rt4/F");

	for (int iEntry = 0; iEntry < nEntries; iEntry++)
	{	

		// if (nEntries>10 && iEntry % (int)(nEntries/10) == 0) 
		// 	cout<<"Running... "<<iEntry * 100. / nEntries<<"%"<<endl; /* progress */

		if (iEntry % division == 0) {	

			// get entry
			chain.GetEntry(iEntry);

			// event filters here
			if (pass_g140==1 && ph_n>0 && jet_n>0 && met_et>50);
			else continue;

			// new variables here
			// ...

			// fill
			t_bkg_test->Fill();

		}
		
		if ((iEntry-1) % division == 0) {	

			// get entry
			chain.GetEntry(iEntry);

			// event filters here
			if (pass_g140==1 && ph_n>0 && jet_n>0 && met_et>50);
			else continue;

			// new variables here
			// ...

			// fill
			t_bkg_train->Fill();

		}

	}

	f_bkg_test->cd();
	t_bkg_test->Write("",TObject::kOverwrite);

	f_bkg_train->cd();
	t_bkg_train->Write("",TObject::kOverwrite);

	delete f_bkg_test;
	delete f_bkg_train;

	cout<<"Created train file: "<<output_train<<endl;
	cout<<"Created test file: "<<output_test<<endl;
	cout<<endl;

	delete h_events;


}