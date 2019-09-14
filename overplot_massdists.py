import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc
import mpfit

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

file1 = './data/massdist_deason_e11-13_total_illustris1_new.npy'
file2 = './data/massdist_deason_e11-13_total_illustris2_new.npy'
file3 = './data/massdist_deason_e11-13_total_illustris3_new.npy'

data1 = np.load(file1)
data2 = np.load(file2)
data3 = np.load(file3)

x = data1[0]
y = np.log10(data1[1])
logErrHigh = np.log10(data1[3]+data1[1])
logErrLow = np.log10(data1[1]-data1[2])
err = (logErrHigh - logErrLow)/2.


fa = {'x':x[3:], 'y':y[3:], 'err':err[3:]}
nfwFit = mpfit.mpfit(diffunct, [12.,0.6], functkw = fa)
print nfwFit.params
print nfwFit.perror

cFit = nfwFit.params[0]
massFit = nfwFit.params[1]
sigmaC = nfwFit.perror[0]
sigmaMass = nfwFit.perror[1]

fitX = np.linspace(10., 300., 100.)

nfwFitVals = nfw(fitX, cFit, massFit)

labelArray = ['Illustris-2', 'Illustris-3']

#pl.figure(figsize=(8,7))
pl.figure(figsize=(8,10))

ax1 = pl.subplot2grid((10,1), (0,0), rowspan = 7)
pl.errorbar(data1[0],data1[1], yerr = [data1[2],data1[3]], fmt = 's', color = 'k', markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5, markeredgecolor = 'none')
pl.plot(fitX, nfwFitVals, color = '0.7', linestyle = '-', linewidth = 3)
pl.ylabel(r'$M$(< $r$)  [$M_{\odot}$]',fontsize = 18)
pl.xlim([0,310])
#pl.ylim([3.*10.**10., 1.2*10**12.])
pl.ylim([3.*10.**10.,2.*10**12.])
pl.setp(ax1.get_xticklabels(), visible = False)
pl.yscale('log')
cLabel = "c = " + "{0:.1f}".format(float(cFit)) + r" $\pm$ " +  "{0:.2f}".format(float(sigmaC))
massLabel = r"$M_{\rm 200,c}$ = " + "{0:.2f}".format(float(massFit)) + r" $\pm$ " +  "{0:.3f}".format(float(sigmaMass)) + r"$\times 10^{12} M_{\odot}$"
pl.text(128., 7.0*10.**10., 'NFW Fit:', fontsize = 20)
pl.text(128., 5.5*10.**10., cLabel, fontsize = 20)
pl.text(125., 4.*10.**10., massLabel, fontsize = 20)
pl.text(10., 1.3*10.**12., 'D12', fontsize = 24)
#pl.text(280.,4.*10.**10.,'A', fontsize = 18)

ax2 = pl.subplot2grid((10,1), (7,0), sharex = ax1, rowspan = 3)
pl.plot(data1[0], ((data2[1]/data1[1])-1.), 'ko', markersize = 8, label = labelArray[0])
pl.plot(data1[0], ((data3[1]/data1[1])-1.), color = '0.5', marker = '^', linestyle = ' ', markeredgecolor = '0.5', markersize = 9, label = labelArray[1])
#pl.ylim([-0.2,0.2])
pl.ylim([-0.2,0.1])
pl.xlim([0,310])
#pl.text(280.,-0.15,'B', fontsize = 18)
#pl.text(280.,-0.175,'B', fontsize = 18)
#pl.yticks([-0.2,-0.1, 0.0, 0.1, 0.2])
pl.yticks([-0.2,-0.1, 0.0, 0.1])#, 0.2])
pl.xlabel(r'$r$ [kpc]', fontsize = 20)
pl.axhline(0.0, color = 'k', linestyle = ':', linewidth = 3)
pl.ylabel(r'$\Delta M$ / $M_{\rm 1}$', fontsize = 20)
pl.legend(labelArray, loc = 'lower right')

pl.tight_layout()
pl.subplots_adjust(hspace = 0.0)

"""
ax3 = pl.subplot2grid((5,1),(4,0), sharex = ax1)
pl.plot(data1[0], ((data3[1]/data1[1])-1.), 'ks')#, yerr = [err21Low,err21High], fmt = 's')#,label=labelArray[0])
pl.ylim([-0.2,0.2])
pl.text(280.,0.05,'C', fontsize = 18)
pl.yticks([-0.2, -0.1, 0.0, 0.1, 0.2])
pl.xlabel('R (kpc)', fontsize = 18)
"""

#pl.text(-35, 0.30, 'Fractional Differences', va = 'center', rotation = 'vertical', fontsize = 18)
pl.show()