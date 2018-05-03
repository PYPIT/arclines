""" Run the current, favored holy grail routine on a set of
standard input spectra.  Generate summary output
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)

import numpy as np
import json
import h5py
import warnings
import pdb

from pkg_resources import resource_filename

from arclines.holy import grail

#from xastropy.xutils import xdebug as xdb

test_arc_path = resource_filename('arclines','/data/test_arcs/')
outdir = 'TEST_SUITE_OUTPUT/'

def tst_holy(name, spec_file, lines, wv_cen, disp, score, fidx, test='semi_brute', debug=False):

    # Favored parameters (should match those in the defaults)
    siglev=20.
    min_ampl=1000.
    min_match = 10

    # Load spectrum
    exten = spec_file.split('.')[-1]
    if exten == 'json':
        with open(test_arc_path+spec_file,'r') as f:
            pypit_fit = json.load(f)
        # Allow for new PYPIT output
        if '0' in pypit_fit.keys():
            pypit_fit = pypit_fit['0']
        # Continue
        spec = np.array(pypit_fit['spec'])
    elif exten == 'hdf5':
        hdf = h5py.File(test_arc_path+spec_file,'r')
        spec = hdf['arcs/{:d}/spec'.format(fidx)].value
    else:
        pdb.set_trace()

    # Run
    outroot = outdir+name
    #if spec_file == 'deimos_830G_r_PYPIT.json':
    #    debug=True
    if test == 'semi_brute':
        best_dict, final_fit = grail.semi_brute(spec, lines, wv_cen, disp, debug=debug,
                             min_ampl=min_ampl, min_nmatch=min_match, outroot=outroot)
    elif test == 'general':
        best_dict, final_fit = grail.general(spec, lines, debug=debug,
                                                min_ampl=min_ampl, outroot=outroot)
    else:
        pdb.set_trace()

    # Score
    grade = 'PASSED'
    if final_fit['rms'] > score['rms']:
        grade = 'FAILED'
        warnings.warn("Solution for {:s} failed RMS!!".format(name))
    if len(final_fit['xfit']) < score['nxfit']:
        grade = 'FAILED'
        warnings.warn("Solution for {:s} failed N xfit!!".format(name))
    if best_dict['nmatch'] < score['nmatch']:
        grade = 'FAILED'
        warnings.warn("Solution for {:s} failed N match!!".format(name))

    # Warn
    return grade, best_dict, final_fit


def main(flg_tst):

    if flg_tst in [1]:
        test = 'semi_brute'
    elif flg_tst in [2]:
        test = 'general'

    # LRISb 600/4000 with the longslit
    names = ['LRISb_600_4000_longslit']
    src_files = ['lrisb_600_4000_PYPIT.json']
    all_lines = [['CdI','HgI','ZnI']]
    all_wvcen = [4400.]
    all_disp = [1.26]
    fidxs = [0]
    scores = [dict(rms=0.13, nxfit=13, nmatch=10)]


    '''
    # LRISb off-center
    # NeI lines are seen beyond the dicrhoic but are ignored
    names += ['LRISb_600_4000_red']
    src_files += ['LRISb_600_LRX.hdf5']  # Create with low_redux.py if needed
    all_wvcen += [5000.]
    all_disp += [1.26]
    all_lines += [['CdI','ZnI','HgI']]  #,'NeI']]
    fidxs += [18]
    scores += [dict(rms=0.08, nxfit=10, nmatch=10)]
    '''

    # LRISr 600/7500 longslit
    names += ['LRISr_600_7500_longslit']
    src_files += ['lrisr_600_7500_PYPIT.json']
    all_wvcen += [7000.]
    all_disp += [1.6]
    all_lines += [['ArI','HgI','KrI','NeI','XeI']]
    fidxs += [-1]
    scores += [dict(rms=0.08, nxfit=30, nmatch=50)]

    '''
    # LRISr 900/XX00 longslit -- blue
    names += ['LRISr_900_XX00_longslit']
    src_files += ['lrisr_900_XX00_PYPIT.json']
    all_wvcen += [5800.]
    all_disp += [1.08]
    all_lines += [['ArI','HgI','KrI','NeI','XeI','CdI','ZnI']]
    fidxs += [-1]
    scores += [dict(rms=0.08, nxfit=10, nmatch=10)]
    '''

    # LRISr 400/8500 longslit -- red
    names += ['LRISr_400_8500_longslit']
    src_files += ['lrisr_400_8500_PYPIT.json']
    all_wvcen += [8000.]
    all_disp += [2.382]
    all_lines += [['ArI','HgI','KrI','NeI','XeI']]
    fidxs += [-1]
    scores += [dict(rms=0.12, nxfit=40, nmatch=40)]  # Failing for semi-brute

    # Kastb 600 grism
    names += ['KASTb_600_standard']
    src_files += ['kastb_600_PYPIT.json']
    all_lines += [['CdI','HeI','HgI']]
    all_wvcen += [4400.]
    all_disp += [1.02]
    fidxs += [0]
    scores += [dict(rms=0.1, nxfit=13, nmatch=10)]

    # Kastr 600/7500 grating
    names += ['KASTr_600_7500_standard']
    src_files += ['kastr_600_7500_PYPIT.json']
    all_lines += [['ArI','NeI','HgI']]
    all_wvcen += [6800.]
    all_disp += [2.345]
    fidxs += [0]
    scores += [dict(rms=0.1, nxfit=20, nmatch=20)]

    # DEIMOS 830G grating (blue)
    names += ['DEIMOS_830g_blue']
    src_files += ['deimos_830G_b_PYPIT.json']
    all_lines += [['ArI','NeI','KrI','XeI']]
    all_wvcen += [7440.]
    all_disp += [0.468]
    fidxs += [0]
    scores += [dict(rms=0.05, nxfit=30, nmatch=40)]

    # DEIMOS 830G grating (red)
    names += ['DEIMOS_830g_red']
    src_files += ['deimos_830G_r_PYPIT.json']
    all_lines += [['ArI','NeI','KrI','XeI']]
    all_wvcen += [9300.]
    all_disp += [0.467]
    fidxs += [0]
    scores += [dict(rms=0.05, nxfit=15, nmatch=50)]

    # DEIMOS 1200G grating (red)
    names += ['DEIMOS_1200g']
    src_files += ['deimos_1200G_r_PYPIT.json']  # Original PYPIT format
    all_lines += [['ArI','NeI','KrI','XeI']]
    all_wvcen += [9400.]
    all_disp += [0.32]
    fidxs += [0]
    scores += [dict(rms=0.05, nxfit=14, nmatch=40)]

    # Run it
    sv_grade = [] # for the end, just in case
    for name,src_file,lines,wvcen,disp,score,fidx in zip(
            names,src_files,all_lines,all_wvcen,all_disp,scores,fidxs):
        #if '8500' not in name:
        #    continue
        grade, best_dict, final_fit = tst_holy(name, src_file, lines, wvcen, disp, score, fidx,
                                               test=test)
        sv_grade.append(grade)
        #if '900' in name:
        #    pdb.set_trace()

    # Report it
    print('==============================================================')
    for name,grade in zip(names,sv_grade):
        print("{:s} {:s}".format(name,grade))


# Test
if __name__ == '__main__':
    #flg_tst = 1   # Run em all with semi-brute
    flg_tst = 2   # Run em all with general

    main(flg_tst)