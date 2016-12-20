""" Module for finding patterns in arc line spectra
"""
from __future__ import (print_function, absolute_import, division, unicode_literals)


import numpy as np
import pdb


def iterative_fitting(spec, tcent, ifit, IDs, llist, disp, plot_fil=None,
                      verbose=False):

    aparm = dict(llist='',
                    disp=disp,             # Ang/unbinned pixel
                    disp_toler=0.1,      # 10% tolerance
                    match_toler=3.,      # Matcing tolerance (pixels)
                    func='legendre',     # Function for fitting
                    n_first=3,           # Order of polynomial for first fit
                    n_final=4,           # Order of polynomial for final fit
                    nsig_rej=2.,         # Number of sigma for rejection
                    nsig_rej_final=3.0)  # Number of sigma for rejection (final fit)
    # PYPIT
    from pypit import pyputils
    msgs = pyputils.get_dummy_logger()
    from pypit import arutils
    from pypit import arqa
    arutils.dummy_settings()

    npix = spec.size

    # Setup for fitting
    sv_ifit = list(ifit) # Keep the originals
    all_ids = -999.*np.ones(len(tcent))
    all_idsion = np.array(['12345']*len(tcent))
    all_ids[ifit] = IDs

    # Fit
    n_order = aparm['n_first']
    flg_quit = False
    fmin, fmax = -1., 1.
    while (n_order <= aparm['n_final']) and (flg_quit is False):
        # Fit with rejection
        xfit, yfit = tcent[ifit], all_ids[ifit]
        mask, fit = arutils.robust_polyfit(xfit, yfit, n_order, function=aparm['func'], sigma=aparm['nsig_rej'], minv=fmin, maxv=fmax)

        rms_ang = arutils.calc_fit_rms(xfit[mask==0], yfit[mask==0],
                                       fit, aparm['func'], fmin=fmin, fmax=fmax)
        rms_pix = rms_ang/disp
        if verbose:
            print("RMS = {:g}".format(rms_pix))
        # DEBUG
        #if msgs._debug['arc']:
        #    debugger.xpcol(xfit,yfit)
            #wave = arutils.func_val(fit, np.arange(slf._msarc.shape[0]), aparm['func'], min=fmin, max=fmax)
            #xdb.xplot(xfit,yfit,scatter=True,xtwo=np.arange(slf._msarc.shape[0]), ytwo=wave)
        # Reject but keep originals (until final fit)
        ifit = list(ifit[mask == 0]) + sv_ifit
        # Find new points (should we allow removal of the originals?)
        twave = arutils.func_val(fit, tcent, aparm['func'], minv=fmin, maxv=fmax)
        for ss,iwave in enumerate(twave):
            mn = np.min(np.abs(iwave-llist['wave']))
            if mn/aparm['disp'] < aparm['match_toler']:
                imn = np.argmin(np.abs(iwave-llist['wave']))
                if verbose:
                    print('Adding {:g} at {:g}'.format(llist['wave'][imn],tcent[ss]))
                # Update and append
                all_ids[ss] = llist['wave'][imn]
                all_idsion[ss] = llist['ion'][imn]
                ifit.append(ss)
        # Keep unique ones
        ifit = np.unique(np.array(ifit,dtype=int))
        #if msgs._debug['arc']:
        #    debugger.set_trace()
        # Increment order
        if n_order < (aparm['n_final']+2):
            n_order += 1
        else:
            # This does 2 iterations at the final order
            flg_quit = True

    # Final fit (originals can now be rejected)
    fmin, fmax = 0., 1.
    xfit, yfit = tcent[ifit]/(npix-1), all_ids[ifit]
    mask, fit = arutils.robust_polyfit(xfit, yfit, n_order, function=aparm['func'], sigma=aparm['nsig_rej_final'], minv=fmin, maxv=fmax)#, debug=True)
    irej = np.where(mask==1)[0]
    if len(irej) > 0:
        xrej = xfit[irej]
        yrej = yfit[irej]
        if verbose:
            for imask in irej:
                msgs.info('Rejecting arc line {:g}'.format(yfit[imask]))
    else:
        xrej = []
        yrej = []
    xfit = xfit[mask==0]
    yfit = yfit[mask==0]
    ions = all_idsion[ifit][mask==0]
    # Final RMS
    rms_ang = arutils.calc_fit_rms(xfit, yfit, fit, aparm['func'],
                                   fmin=fmin, fmax=fmax)
    rms_pix = rms_ang/disp
    #
    '''
    if msgs._debug['arc']:
        msarc = slf._msarc[det-1]
        wave = arutils.func_val(fit, np.arange(msarc.shape[0])/float(msarc.shape[0]),
            'legendre', minv=fmin, maxv=fmax)
        debugger.xplot(xfit,yfit, scatter=True,
            xtwo=np.arange(msarc.shape[0])/float(msarc.shape[0]),
            ytwo=wave)
        debugger.xpcol(xfit*msarc.shape[0], yfit)
        debugger.set_trace()
    '''

        #debugger.xplot(xfit, np.ones(len(xfit)), scatter=True,
        #    xtwo=np.arange(msarc.shape[0]),ytwo=yprep)
        #debugger.xplot(xfit,yfit, scatter=True, xtwo=np.arange(msarc.shape[0]),
        #    ytwo=wave)
        #debugger.set_trace()
        #wave = arutils.func_val(fit, np.arange(msarc.shape[0])/float(msarc.shape[0]),
        #    'legendre', min=fmin, max=fmax)

    # Pack up fit
    final_fit = dict(fitc=fit, function=aparm['func'], xfit=xfit, yfit=yfit,
        ions=ions, fmin=fmin, fmax=fmax, xnorm=float(npix),
        xrej=xrej, yrej=yrej, mask=mask, spec=spec, nrej=aparm['nsig_rej_final'],
        shift=0., tcent=tcent, rms=rms_pix)
    # QA
    if plot_fil is not None:
        arqa.arc_fit_qa(None, final_fit, outfil=plot_fil)
    # Return
    return final_fit


