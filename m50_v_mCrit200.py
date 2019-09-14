import sys
import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc
import mpfit

inFile  = str(sys.argv[1])
data = np.transpose(np.load(inFile))

def linear(m50, a, b, c):
	return (a*(m50**2.))+(b*m50)+c

def diffunct(p, fjac = None, x = None, y = None, err = None):
	model = linear(x, p[0], p[1], p[2])
	status = 0
	return ([status, (y - model)/err])
	
logErrHigh = np.log10(data[2]+data[1])
logErrLow = np.log10(data[1]-data[3])
err = (logErrHigh - logErrLow)/2.
	
fa = {'x':np.log10(data[0]/(4e11)), 'y':np.log10(data[1]), 'err':err}
linearFit = mpfit.mpfit(diffunct, [1.,1.,1.], functkw = fa)

print linearFit.params
print linearFit.perror

analyticX = np.log10(np.logspace(11., 12., 1000., base = 10)/(4e11))
#fitY = (linearFit.params[0]*(np.log10(analyticX)**2.))+(linearFit.params[1]*np.log10(analyticX))+linearFit.params[2]
fitYmed = (linearFit.params[0]*(analyticX**2.))+(linearFit.params[1]*analyticX)+linearFit.params[2]
fitY = (0.32509593*(analyticX**2.))+(1.61930511*analyticX)+ 12.04541389
xtest = np.log10((4.48*10.**11.)/(4e11))
#test1 = (0.43*(xtest**2.))+(1.61*xtest)+12.01
#test2 = (linearFit.params[0]*(xtest**2.)) + (linearFit.params[1]*xtest) + linearFit.params[2]
#print (10.**test1)/(10.**11.)
#print (10.**test2)/(10.**11.)
plotErrHigh = np.log10(data[2]+data[1]) - np.log10(data[1])
plotErrLow =  np.log10(data[1]) - np.log10(data[1]-data[3])

#print data[3]/(10.**10.)
#print data[2]/(10.**10.)

#scatterData = np.load('./m50_v_mCrit200_scatter_bins.npy')

pl.figure(figsize=(8,7))
pl.errorbar(np.log10(data[0]),np.log10(data[1]), yerr = [plotErrLow,plotErrHigh], fmt = 's', color = 'k', markersize = 8, elinewidth = 1.3, capsize = 5.0, capthick = 1.3, markeredgecolor = 'none', label = r'$M_{\rm 200,c}$ fit')
#pl.errorbar(scatterData[0],scatterData[1], yerr = [scatterData[1]-scatterData[2],scatterData[3]-scatterData[1]], fmt = 's', color = 'r', markersize = 8, elinewidth = 1.3, capsize = 5.0, capthick = 1.3,fillstyle = 'none', label = r'$M_{\rm 200,c}$ from scatter')
pl.plot(np.log10(np.logspace(11., 12., 1000., base = 10)),fitYmed, color = '0.7', linewidth = 3, linestyle = '-', label = 'Scatter Fit')
pl.plot(np.log10(np.logspace(11., 12., 1000., base = 10)),fitY, color = '0.7', linewidth = 3, linestyle = '--', label = 'Median Fit')
#pl.axvline(2.9*10.**11., color = 'y')
#pl.axvline(4.2*10.**11., color = 'm')
#pl.errorbar(data[0],data[1], yerr = [data[3],data[2]], fmt = 's', color = 'k', markersize = 8, elinewidth = 1.3, capsize = 3.0, capthick = 1.3)
pl.axvspan(np.log10(3.8*10.**11.), np.log10(4.6*10.**11.), facecolor = 'm', alpha = 0.2)
pl.axvspan(np.log10(2.4*10.**11.), np.log10(3.4*10.**11.), facecolor = 'y', alpha = 0.2)
pl.text(11.44, 12.7, 'G14', rotation = 270, fontsize = 24)
pl.text(11.6, 12.7, 'D12', rotation = 270, fontsize = 24)
#pl.legend(['Scatter Fit', 'Median Fit'], loc = 'upper left')
"""
pl.axhline(np.log10(1.11776294305e+12), color = 'r')
pl.axhline(np.log10(1.11776294305e+12 + 369608444109.0), color = 'r')
pl.axhline(np.log10(1.11776294305e+12 - 240499631292.0), color = 'r')
pl.axvline(np.log10(4.2*10.**11.),color = 'r')
"""
pl.xlabel(r'log$_{10}$[$M$(< 50 kpc) / $M_{\odot}$]', fontsize = 20)
pl.ylabel(r'log$_{10}$[$M_{\rm 200,c}$ / $M_{\odot}$]', fontsize = 20)
pl.xlim([11.,12.])
pl.ylim([11.,13.])
#pl.legend([r'$M_{\rm 200,c}$ fit',r'$M_{\rm 200,c}$ scatter'], loc = 'upper left')
#pl.xscale('log')
#pl.yscale('log')
pl.show()
