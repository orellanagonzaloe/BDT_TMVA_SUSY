# Signal cross sections

import os
import json

import ROOT

_xs_db = dict()

def _create_xs_db():

    with open('/cvmfs/atlas.cern.ch/repo/sw/database/GroupData/dev/PMGTools/PMGxsecDB_mc16.txt') as f:
        
        for line in f:
            line = line.replace('\n', '')
            if not line or line.startswith('#'):
                continue

            try:
                dsid, name, gen_xs, filter_eff, kfact, unc_up, unc_dn, gen_name, etag = line.split()
            except:
                continue

            # effective cross-section and relative uncertainty
            xseff = float(gen_xs) * float(kfact) * float(filter_eff)

            _xs_db[int(dsid)] = xseff


def get_xs_from_did(did):

    if not _xs_db:
        _create_xs_db()

    if did in _xs_db:
        return _xs_db[did]

    raise Exception('ERROR: XS not found for DID=%s' % (did))


def get_EWK_xs_total(mN1):

    xs_file = 'lib/EWK_xs/EWK_xsec_%s.json' % mN1

    with open(xs_file) as f:
        json_tmp = json.load(f)

    return json_tmp['ChiChi']



def get_EWK_xs_event(mN1, h_susy_sumw):

    # h_susy_sumw.Print('all')

    d_fs = {
        # 111: 'N1N1',
        112: 'N1N2',
        # 113: 'N1N3',
        115: 'N1C1p',
        117: 'C1mN1',
        # 122: 'N2N2',
        # 123: 'N2N3',
        125: 'N2C1p',
        127: 'C1mN2',
        # 133: 'N3N3',
        # 135: 'C1pN3',
        # 137: 'C1mN3',
        157: 'C1mC1p',
    }

    xs_file = 'lib/EWK_xs/EWK_xsec_%s.json' % mN1

    with open(xs_file) as f:
        json_tmp = json.load(f)

    _def_func = ''

    for fs in d_fs:

        sumw = h_susy_sumw.GetBinContent(fs)

        xs = json_tmp[d_fs[int(fs)]]

        div = 1. * xs / sumw if sumw != 0 else 0.

        _def_func += 'if (fs==%i) return %.15f;\n' % (fs, div)

    def_func = """
    float get_EWK_xs_event(int fs) {
        %s
        std::cout<<"Final state not recognised: "<<fs<<std::endl;
        return 0.;
    }
    """ % (_def_func)

    ROOT.gInterpreter.Declare(def_func)