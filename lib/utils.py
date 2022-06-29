import ROOT

def printMsj(msj, level):

	color = ['[1;92mINFO', '[1;93mWARNING', '[1;91mERROR']

	print '\033%s: %s\033[0m' % (color[level], msj)


def reweight_event(br_y, br_Z, br_h):

	# n1decays variable in mini ntuples
	# if      (nGrav == 2 && nph == 2 && nZ == 0 && nh == 0) return 1; // phph event
	# else if (nGrav == 2 && nph == 1 && nZ == 1 && nh == 0) return 2; // phZ event
	# else if (nGrav == 2 && nph == 1 && nZ == 0 && nh == 1) return 3; // phh event
	# else if (nGrav == 2 && nph == 0 && nZ == 2 && nh == 0) return 4; // ZZ event
	# else if (nGrav == 2 && nph == 0 && nZ == 1 && nh == 1) return 5; // Zh event
	# else if (nGrav == 2 && nph == 0 && nZ == 0 && nh == 2) return 6; // hh event

	# original BRs
	br_y_orig = 1/3.
	br_Z_orig = 1/3.
	br_h_orig = 1/3.
	
	# original event type fraction
	f_yy_orig = br_y_orig * br_y_orig
	f_yZ_orig = 2 * br_y_orig * br_Z_orig
	f_yh_orig = 2 * br_y_orig * br_h_orig
	f_ZZ_orig = br_Z_orig * br_Z_orig
	f_Zh_orig = 2 * br_Z_orig * br_h_orig
	f_hh_orig = br_h_orig * br_h_orig

	# asked BRs/fractions
	f_yy = br_y * br_y
	f_yZ = 2 * br_y * br_Z
	f_yh = 2 * br_y * br_h
	f_ZZ = br_Z * br_Z
	f_Zh = 2 * br_Z * br_h
	f_hh = br_h * br_h

	# weights
	w_yy = f_yy / f_yy_orig
	w_yZ = f_yZ / f_yZ_orig
	w_yh = f_yh / f_yh_orig
	w_ZZ = f_ZZ / f_ZZ_orig
	w_Zh = f_Zh / f_Zh_orig
	w_hh = f_hh / f_hh_orig


	def_func = """
	float reweight_event(int n1decays) {
		if (n1decays == 1) return %.5f; // phph event
		if (n1decays == 2) return %.5f; // phZ event
		if (n1decays == 3) return %.5f; // phh event
		if (n1decays == 4) return %.5f; // ZZ event
		if (n1decays == 5) return %.5f; // Zh event
		if (n1decays == 6) return %.5f; // hh event
		std::cout<<"\033[1;91mERROR\033[0m: N1 decay not recognised "<<n1decays<<std::endl;
		return 0.;
	}
	""" % (w_yy, w_yZ, w_yh, w_ZZ, w_Zh, w_hh)

	ROOT.gInterpreter.Declare(def_func)


def presel_cut(cuts):

	def_func = """
	bool preselCuts(Int_t pass_g140, Int_t pass_xe, Int_t mcveto, Int_t ph_n, Int_t el_n, Int_t mu_n, Int_t jet_n, std::vector<float> * ph_pt, Float_t met_et, Float_t dphi_jetmet, Float_t dphi_gammet, Float_t dphi_gamjet){
		if (%s) return true;
		return false;
	}
	""" % (cuts)

	ROOT.gInterpreter.Declare(def_func)


lumi_dict = {
	'2015': 3219.56,
	'2016': 32965.30,
	'20152016': 36184.86,
	'2017': 44307.40,
	'2018': 59937.20,
	# 'fullR2': 140429.46,

}

campaign_tag = {
	'2015': 'mc16a',
	'2016': 'mc16a',
	'20152016': 'mc16a',
	'2017': 'mc16d',
	'2018': 'mc16e',
}

trainMethods = {
	'Cuts': ROOT.TMVA.Types.kCuts,
	'Likelihood': ROOT.TMVA.Types.kLikelihood,
	'PDERS': ROOT.TMVA.Types.kPDERS,
	'HMatrix': ROOT.TMVA.Types.kHMatrix,
	'Fisher': ROOT.TMVA.Types.kFisher,
	'KNN': ROOT.TMVA.Types.kKNN,
	'CFMlpANN': ROOT.TMVA.Types.kCFMlpANN,
	'TMlpANN': ROOT.TMVA.Types.kTMlpANN,
	'BDT': ROOT.TMVA.Types.kBDT,
	'DT': ROOT.TMVA.Types.kDT,
	'RuleFit': ROOT.TMVA.Types.kRuleFit,
	'SVM': ROOT.TMVA.Types.kSVM,
	'MLP': ROOT.TMVA.Types.kMLP,
	'BayesClassifier': ROOT.TMVA.Types.kBayesClassifier,
	'FDA': ROOT.TMVA.Types.kFDA,
	'Boost': ROOT.TMVA.Types.kBoost,
	'PDEFoam': ROOT.TMVA.Types.kPDEFoam,
	'LD': ROOT.TMVA.Types.kLD,
	'Plugins': ROOT.TMVA.Types.kPlugins,
	'Category': ROOT.TMVA.Types.kCategory,
	'DNN': ROOT.TMVA.Types.kDNN,
	'DL': ROOT.TMVA.Types.kDL,
	'PyRandomForest': ROOT.TMVA.Types.kPyRandomForest,
	'PyAdaBoost': ROOT.TMVA.Types.kPyAdaBoost,
	'PyGTB': ROOT.TMVA.Types.kPyGTB,
	'PyKeras': ROOT.TMVA.Types.kPyKeras,
	'PyTorch': ROOT.TMVA.Types.kPyTorch,
	'C50': ROOT.TMVA.Types.kC50,
	'RSNNS': ROOT.TMVA.Types.kRSNNS,
	'RSVM': ROOT.TMVA.Types.kRSVM,
	'RXGB': ROOT.TMVA.Types.kRXGB,
	'CrossValidation': ROOT.TMVA.Types.kCrossValidation,
	'MaxMethod': ROOT.TMVA.Types.kMaxMethod,
}


methodsRange = {
	'Cuts_GA': (0., 1.),
	'LikelihoodD': (0., 1.),
	'BDT': (-0.45, 0.45),
	'MLP': (0., 1., 3),
	'MLPBFGS': (0., 1.),
	'MLPBNN': (0., 1.),
	'Fisher': (-4., 6.),
	'FisherG': (-3., 4.),
	'BoostedFisher': (-1., 1.5),
}

def isdata(sample):

	if  'data15' in sample or \
		'data16' in sample or \
		'data17' in sample or \
		'data18' in sample or \
		'efake15' in sample or \
		'efake16' in sample or \
		'efake17' in sample or \
		'efake18' in sample or \
		'jfakeiso15' in sample or \
		'jfakeiso16' in sample or \
		'jfakeiso17' in sample or \
		'jfakeiso18' in sample or \
		'jfakeiso215' in sample or \
		'jfakeiso216' in sample or \
		'jfakeiso217' in sample or \
		'jfakeiso218' in sample or \
		'jfakeid15' in sample or \
		'jfakeid16' in sample or \
		'jfakeid17' in sample or \
		'jfakeid18' in sample or \
		'jfakeid215' in sample or \
		'jfakeid216' in sample or \
		'jfakeid217' in sample or \
		'jfakeid218' in sample:

		return True

	else:

		return False