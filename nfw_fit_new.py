import numpy as np
import matplotlib.pyplot as pl
import scipy.interpolate as si
import scipy.optimize as so
import cosmo_const as cc
import mpfit
"""
def mbk_mpfit(func, xdat, ydat, p0, err=None, quiet=False, return_error=False):
	if err is None:
		err=np.ones(xdat.size)
	def myfunc(p, fjac=None, x=None, y=None, err=None):
		model = func(x)#, p0[0], p0[1])
		status = 0
		return([status, (y-model)/err])
	fa={'x':xdat, 'y':ydat, 'err':err}
	fitn=mpfit.mpfit(myfunc, p0, functkw=fa, quiet=quiet)
	if not quiet:
		print 'errors:', fitn.perror
	if return_error:
		return fitn.params, fitn.perror
	else:
		return fitn.params
"""
def nfw(rad, nfwC, nfwMass):
	mcrit200 = nfwMass*(10.**12.)
	gC = 1./(np.log(1+nfwC)-(nfwC/(1+nfwC)))
	virialRadius = (3.*mcrit200/(800*np.pi*cc.rho_crit))**(1./3.)
	rS = rad/virialRadius
	nfwOut = mcrit200*gC*(np.log(1+nfwC*rS)-(nfwC*rS/(1+(nfwC*rS))))
	return nfwOut

def diffunct(p, fjac = None, x = None, y = None, err = None):
	model = np.log10(nfw(x, p[0], p[1]))
	status = 0
	return ([status, (y - model)/err])

fileIn = './massdist_deason_e11-13_total_illustrisdark1_new.npy'
#fileIn = './massdist_deason2012_gauss_illustris1_total_new.npy'
#fileIn = './massdist_deason2012_m100_illustrisdark1_total_new.npy'

data = np.load(fileIn)
x = data[0]
y = np.log10(data[1])
#err1 = data[2]
#err2 = data[3]
#err = np.apply_along_axis(np.max, 1, np.transpose(np.array([err1,err2])))
# (high - med) + (med-low) = high - low
#err = (err2 + err1)/2.
logErrHigh = np.log10(data[3]+data[1])
logErrLow = np.log10(data[1]-data[2])
err = (logErrHigh - logErrLow)/2.
print err
print len(err)
fa = {'x':x[3:], 'y':y[3:], 'err':err[3:]}

nfwFit = mpfit.mpfit(diffunct, [12.,1.1], functkw = fa)
print nfwFit.params
print nfwFit.perror

cFit = nfwFit.params[0]
massFit = nfwFit.params[1]
sigmaC = nfwFit.perror[0]
sigmaMass = nfwFit.perror[1]

fitX = np.linspace(10., 300., 100.)
nfwFitVals = nfw(fitX, cFit, massFit)

pl.figure(figsize=(8,7))
pl.errorbar(data[0],data[1], yerr = [data[2],data[3]], fmt = 's', markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5, markeredgewidth = 1.5, color = 'k', markeredgecolor = 'none')#,label=labelArray[0])
pl.plot(fitX,nfwFitVals, color = '0.7', linewidth = 3., linestyle = '-')
pl.yscale('log')
#pl.ylim([4.*10.**10., 2.*10.**12.])
pl.ylim([4.*10.**10., 2.5*10.**12.])
pl.xlim([0.,310.])
pl.xlabel(r'$r$ [kpc]', fontsize = 20)
pl.ylabel(r'$M$(< $r$) [$M_{\odot}$]',fontsize = 20)

cLabel = "c = " + "{0:.2f}".format(float(cFit)) + r" $\pm$ " +  "{0:.3f}".format(float(sigmaC))
massLabel = r"$M_{\rm 200,c}$ = " + "{0:.2f}".format(float(massFit)) + r" $\pm$ " +  "{0:.3f}".format(float(sigmaMass)) + r"$\times 10^{12} M_{\odot}$"
pl.text(10., 1.9*10.**12., 'Illustris-Dark-1', fontsize = 20)
pl.text(113., 8.5*10.**10., 'NFW Fit:', fontsize = 20)
pl.text(113., 6.5*10.**10., cLabel, fontsize = 20)
pl.text(110., 5.*10.**10., massLabel, fontsize = 20)

pl.show()