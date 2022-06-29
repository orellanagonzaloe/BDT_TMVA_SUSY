
colors_dict = dict()
colors_dict['data']           = '#000000'
colors_dict['photonjet']      = '#dd4b39' #'#e03127'
colors_dict['photonjet_nnlo'] = '#dd4b39' #'#e03127'
colors_dict['wgamma']         = '#fcdd5d' #'#fcdd5d'
colors_dict['zgamma']         = '#9066b3'
colors_dict['ttgamma']        = '#32b422' #'#39dd4b' 
colors_dict['fakes']          = '#3b5998' #'#1e42d0'
colors_dict['zllgamma']       = '#fac9b4'
colors_dict['znunugamma']     = '#f7fab5'
colors_dict['vgamma']         = '#f8f59b'
colors_dict['efake']          = '#a4cee6'
colors_dict['jfake']          = '#348ABD'
colors_dict['multijet']       = '#348ABD'
colors_dict['wjets']          = '#BCBC93'
colors_dict['zjets']          = '#36BDBD'
colors_dict['vjets']          = '#a4cee6'
colors_dict['ttbar']          = '#8bc65a'
colors_dict['diphoton']       = '#ffa04d'
colors_dict['vgammagamma']    = '#e5ac49'
colors_dict['others']         = '#676363'
colors_dict['higgs']         = '#ff9491'
colors_dict['alldiph']         = '#ffa04d'

# ["ff9999","ffd199","fcffad","bbffad","70F3FF","99c0ff","baadff","ffc6ff","fffffc"]
# ["ff4343","ffab43","f9ff53","70ff53","23edff","438bff","7053ff","ff68ff","ffff90"]
# ["F5B400","F14F04","ff006e","8338ec","0A68FF"]

colors_dict['GGM_N1N2C1_phZ_150'] = '#F5B400'
colors_dict['GGM_N1N2C1_phZ_250'] = '#F14F04'
colors_dict['GGM_N1N2C1_phZ_350'] = '#fcffad'
colors_dict['GGM_N1N2C1_phZ_450'] = '#ff006e'
colors_dict['GGM_N1N2C1_phZ_550'] = '#044693'
colors_dict['GGM_N1N2C1_phZ_650'] = '#8338ec'
colors_dict['GGM_N1N2C1_phZ_750'] = '#044693'
colors_dict['GGM_N1N2C1_phZ_850'] = '#0A68FF'
colors_dict['GGM_N1N2C1_phZ_950'] = '#ff903b'
colors_dict['GGM_N1N2C1_phZ_1050'] = '#044693'
colors_dict['GGM_N1N2C1_phZ_1250'] = '#044693'
colors_dict['GGM_N1N2C1_phZ_1450'] = '#044693'

colors_dict['GGM_N1N2C1_phb_150'] = '#F5B400'
colors_dict['GGM_N1N2C1_phb_250'] = '#F14F04'
colors_dict['GGM_N1N2C1_phb_350'] = '#044693'
colors_dict['GGM_N1N2C1_phb_450'] = '#ff006e'
colors_dict['GGM_N1N2C1_phb_550'] = '#044693'
colors_dict['GGM_N1N2C1_phb_650'] = '#8338ec'
colors_dict['GGM_N1N2C1_phb_750'] = '#044693'
colors_dict['GGM_N1N2C1_phb_850'] = '#0A68FF'
colors_dict['GGM_N1N2C1_phb_950'] = '#41c8c2'
colors_dict['GGM_N1N2C1_phb_1050'] = '#044693'
colors_dict['GGM_N1N2C1_phb_1250'] = '#044693'
colors_dict['GGM_N1N2C1_phb_1450'] = '#044693'

def sig_color(sample):

	if 'GGM_' in sample:
		if sample.endswith('_250'):
			return '#3a92fa'
		elif sample.endswith('_1050'):
			return '#fa3a92'
		else:
			return '#8453fb'
	else:
		if 'mu_-250' in sample:
			# return '#044693'
			return '#3a92fa'
		elif 'mu_-1050' in sample:
			# return '#962257'
			return '#fa3a92'
		if 'mu_250' in sample:
			# return '#044693'
			return '#3a92fa'
		elif 'mu_1050' in sample:
			# return '#962257'
			return '#fa3a92'
		else:
			# return '#4f3196'
			return '#8453fb'


var_plots = dict()
# var_plots['ph_pt[0]'] = ('p_{T}^{#gamma} [GeV]',130.,1500.)
var_plots['ph_pt[0]'] = ('p_{T}^{lead-#gamma} [GeV]',50.,1050.)
var_plots['jet_n'] = ('N_{jets}',0.,13.)
var_plots['bjet_n'] = ('N_{bjets}',0.,13.)
var_plots['el_n+mu_n'] = ('N_{lep}',0.,4.)
var_plots['met_et'] = ('E_{T}^{miss} [GeV]',0.,800.)
var_plots['mt_gam'] = ('M_{T}^{#gamma, E_{T}^{miss}} [GeV]',0., 2000.)
var_plots['dphi_jetmet'] = ('#Delta#varphi(E_{T}^{miss}, j)',0.,3.2)
var_plots['dphi_gammet'] = ('#Delta#varphi(E_{T}^{miss}, #gamma)',0.,3.2)
var_plots['ht'] = ('H_{T} [GeV]',0.,2200.)
var_plots['meff'] = ('m_{eff} [GeV]',0.,4000.)
var_plots['rt4'] = ('R_{T}^{4}',0.3,1.1)
var_plots['met_sig'] = ('E_{T}^{miss} Significance [GeV^{1/2}]',0.,30.)
var_plots['met_sig2'] = ('E_{T}^{miss} Significance (obj) [GeV^{1/2}]',0.,30.)
var_plots['ph_n'] = ('N_{#gamma}',0.,10.)

# Extra
var_plots['met_et/sqrt(ht)'] = ('E_{T}^{miss}/sqrt(H_{T}) [GeV^{1/2}]', 0., 50.)
var_plots['met_et/meff'] = ('E_{T}^{miss}/m_{eff}', 0., 1.)
var_plots['jet_pt[0]'] = ('p_{T}^{lead-jet} [GeV]',50.,1050.)
var_plots['met_et/(met_et+ph_pt[0]+jet_pt[0])'] = ('E_{T}^{miss}/(E_{T}^{miss}+p_{T}^{lead-#gamma}+p_{T}^{lead-jet})', 0., 1.)
var_plots['met_et/ht'] = ('E_{T}^{miss}/H_{T}', 0., 5.)
var_plots['meff/met_et'] = ('m_{eff}/E_{T}^{miss}', 0., 20.)
var_plots['ht0'] = ('H0_{T} [GeV]',0.,2200.)


# Friends
var_plots['m_jj'] = ('M_{jj} [GeV]',0.,300.)
var_plots['bbmass_w'] = ('M_{b#bar{b}}(w) [GeV]',0.,300.)
var_plots['bbmass_lead'] = ('M_{b#bar{b}}(lead) [GeV]',0.,300.)
var_plots['bbmass_hmass'] = ('M_{b#bar{b}}(Higgs) [GeV]',0.,300.)
var_plots['m_yy'] = ('M_{#gamma#gamma} [GeV]',0.,300.)
var_plots['st_gam'] = ('S_{T}^{#gamma} [GeV]',0.,2300.)

# 2D
var_plots['ph_pt[0]:met_et'] = (50., 1050., 50., 600.)
var_plots['ht:met_et'] = (0., 3000., 50., 600.)
var_plots['meff:met_et'] = (0., 2200., 50., 600.)
var_plots['mt_gam:met_et'] = (0., 1000., 50., 600.)
var_plots['ph_pt[0]:meff'] = (50., 1050., 0., 2200.)
var_plots['ph_pt[0]:ht'] = (50., 1050., 0., 3000.)
var_plots['ph_pt[0]:mt_gam'] = (50., 1050., 0., 1000.) 
var_plots['meff:mt_gam'] = (0., 2200., 0., 1000.) 
var_plots['ht:mt_gam'] = (0., 3000., 0., 1000.) 
var_plots['met_et/meff:met_et'] = (0.2, 0.9, 50., 600.)
var_plots['met_sig2:met_et'] = (0., 20., 50., 600.)

var_plots['ht0:met_et'] = (0., 3000., 50., 600.) 
var_plots['ph_pt[0]:ht0'] = (50., 1250., 0., 3000.) 
var_plots['jet_pt[0]:met_et'] = (50., 1250., 50., 600.)
var_plots['jet_pt[0]:ht0'] = (50., 1250., 0., 3000.)

# Diagnostic Plots
var_plots['ph_phi[0]'] = ('#phi^{lead #gamma}',-3., 3.)
var_plots['jet_phi[0]'] = ('#phi^{lead jet}',-3., 3.)
var_plots['ph_eta[0]'] = ('#eta^{lead #gamma}',-3., 3.)
var_plots['jet_eta[0]'] = ('#eta^{lead jet}',-3., 3.)
var_plots['met_phi'] = ('#phi^{E_{T}^{miss}}',-3., 3.)
var_plots['met_phi:met_et']  = (-3.14, 3.14, 0., 300.) 
var_plots['jet_phi[0]:jet_eta[0]']  = (-3.14, 3.14, -3., 3.) 
var_plots['ph_phi[0]:ph_eta[0]']  = (-3.14, 3.14, -3., 3.) 

labels_dict = dict()
labels_dict['data']           = 'Data'
labels_dict['photonjet']      = '#gamma + jets'
labels_dict['photonjet_nnlo'] = '#gamma + jets'
labels_dict['ttgamma']        = 't#bar{t}#gamma' # /single-t \\gamma'
labels_dict['vgamma']         = 'W#gamma/Z#gamma'
labels_dict['zgamma']         = 'Z#gamma'
labels_dict['wgamma']         = 'W#gamma'
labels_dict['zllgamma']       = 'Z(ll)#gamma'
labels_dict['znunugamma']     = 'Z(#nu#nu)#gamma'
labels_dict['efake']          = 'e#rightarrow#gamma fake'
labels_dict['jfake']          = 'jet#rightarrow#gamma fake'
labels_dict['fakes']          = 'jet/e#rightarrow#gamma fake'
labels_dict['multijet']       = 'Multijet'
labels_dict['wjets']          = 'W + jets'
labels_dict['zjets']          = 'Z + jets'
labels_dict['vjets']          = 'W/Z + jets'
labels_dict['ttbar']          = 't#bar{t}'
labels_dict['higgs']          = 'ttH(#gamma#gamma/Z#gamma)'
labels_dict['vgammagamma']    = 'W#gamma#gamma/Z#gamma#gamma' # #gamma#gamma/W#gamma#gamma/Z#gamma#gamma
labels_dict['diphoton']       = '#gamma#gamma'
labels_dict['alldiph']          = '#gamma#gamma/W#gamma#gamma/Z#gamma#gamma'
labels_dict['allMC']          = ''

mn1_text = 'm_{#tilde{#chi} #kern[-0.8]{#lower[1.2]{#scale[0.6]{1}}} #kern[-1.6]{#lower[-0.6]{#scale[0.6]{0}}}}'

labels_dict['GGM_N1N2C1_phZ_150'] = '#gamma+Z, %s = 150 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_250'] = '#gamma+Z, %s = 250 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_350'] = '#gamma+Z, %s = 350 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_450'] = '#gamma+Z, %s = 450 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_550'] = '#gamma+Z, %s = 550 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_650'] = '#gamma+Z, %s = 650 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_750'] = '#gamma+Z, %s = 750 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_850'] = '#gamma+Z, %s = 850 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_950'] = '#gamma+Z, %s = 950 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_1050'] = '#gamma+Z, %s = 1050 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_1250'] = '#gamma+Z, %s = 1250 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phZ_1450'] = '#gamma+Z, %s = 1450 GeV' % 'mN1'

labels_dict['GGM_N1N2C1_phb_150'] = '#gamma+h, %s = 150 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_250'] = '#gamma+h, %s = 250 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_350'] = '#gamma+h, %s = 350 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_450'] = '#gamma+h, %s = 450 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_550'] = '#gamma+h, %s = 550 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_650'] = '#gamma+h, %s = 650 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_750'] = '#gamma+h, %s = 750 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_850'] = '#gamma+h, %s = 850 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_950'] = '#gamma+h, %s = 950 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_1050'] = '#gamma+h, %s = 1050 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_1250'] = '#gamma+h, %s = 1250 GeV' % 'mN1'
labels_dict['GGM_N1N2C1_phb_1450'] = '#gamma+h, %s = 1450 GeV' % 'mN1'

lumi_label = {
	'2015': 3.2,
	'2016': 33.0,
	'20152016': 36.2,
	'2017': 44.3,
	'2018': 58.5,
	'fullR2' : 139.0,
}

def sig_label(sample):

	mn1_text = 'm_{#tilde{#chi} #kern[-0.8]{#lower[1.2]{#scale[0.6]{1}}} #kern[-1.6]{#lower[-0.6]{#scale[0.6]{0}}}}'

	m_go = ''
	m_n1 = ''

	if 'GGM_' in sample:

		m_go = sample.split('_')[3]
		m_n1 = sample.split('_')[4]

	else:

		s_tmp = sample.split('_')
		m_go_i = s_tmp.index('go')+1
		m_n1_i = s_tmp.index('mu')+1
		m_go = s_tmp[m_go_i]
		m_n1 = s_tmp[m_n1_i]

	m_n1 = m_n1.replace('-', '')

	return 'm_{#tilde{g}} = %s, %s = %s GeV'  % (m_go, mn1_text, m_n1)
