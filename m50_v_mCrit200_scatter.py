import sys
import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc
import mpfit
import scipy.optimize as so

def linear(m50, a, b, c):
	return (a*(m50**2.))+(b*m50)+c


def diffunct(p, fjac = None, x = None, y = None, err = None):
	model = linear(x, p[0], p[1], p[2])
	status = 0
	return ([status, (y - model)/err])

def diffunctTest(tpl,x,y):
	return 	linear(x, tpl[0], tpl[1], tpl[2]) - y

mcritInFile = 'm_crit200_bigdata_illustris-1.npy'
inFile = './halo_weighing_e11-13_deason_illustris-1.npy'


#Unpacking data (groupNum, totalMassInside, allMassTotal, dmMassInside, gasMassInside, starMassInside, boolArray)
data = np.transpose(np.load(inFile))
haloNum = data[0]
groupNum = data[1]
boolArray = data[2]
mInside50 = data[3]
mInside80 = data[4]
mInside100 = data[5]
mInside250 = data[6]
del data

data = np.transpose(np.load(mcritInFile))
mCrit200 = data[1]
del data

m50Sort = np.argsort(mInside50)

err = np.log10(0.001*mCrit200)[m50Sort]

fa = {'x':np.log10(mInside50[m50Sort]/(4e11)), 'y':np.log10(mCrit200[m50Sort]), 'err':err}
linearFit = mpfit.mpfit(diffunct, [1.,1.,1.], functkw = fa)
linearFitTest = so.leastsq(diffunctTest, (0.331,1.62,12.), args = (np.log10(mInside50[m50Sort]/(4e11)),np.log10(mCrit200[m50Sort])), full_output = 1)
curveFitTest = so.curve_fit(linear, np.log10(mInside50[m50Sort]/(4e11)), np.log10(mCrit200[m50Sort]))
print curveFitTest[0]
print np.sqrt(np.diag(curveFitTest[1]))
print linearFitTest[0]
#print np.sqrt(np.diag(linearFitTest[1]))
#print linearFit.params
#print linearFit.perror

x = np.log10(mInside50[m50Sort]/(4e11))

#fitYRMS = ((linearFitTest[0])[0]*(x**2.))+((linearFitTest[0])[1]*x)+((linearFitTest[0])[2])
#fitYRMS = ((linearFitTest[0][0]*(x**2.))+(linearFitTest[0][1]*x)+linearFitTest[0][2])
#fitYRMS = ((0.373)*(x**2.))+(1.60*x)+(12.0)
#print np.sqrt(np.mean((fitYRMS - np.log10(mCrit200[m50Sort]))**2.))
#varRes = np.var(fitYRMS - np.log10(mCrit200[m50Sort]))
#print np.sqrt(linearFitTest[1]*varRes)
analyticX = np.linspace(10.**10.5,10.**12.5, 1000.)/(4e11)

pl.figure(figsize=(8,7))
fitY = (linearFit.params[0]*(np.log10(analyticX)**2.))+(linearFit.params[1]*np.log10(analyticX))+linearFit.params[2]
#fitYmed = (0.33*(np.log10(analyticX)**2.))+(1.62*(np.log10(analyticX)))+12.01
#fitY = (0.43272887*(np.sort(np.log10(mInside50))**2.))+(-8.42371545*(np.sort(np.log10(mInside50))))+51.4956988
pl.scatter(np.log10(mInside50), np.log10(mCrit200), color = '0.5', edgecolor = 'none')
pl.plot(np.sort(np.log10(analyticX*4e11)), fitY, color = 'b', linewidth = 3, linestyle = '--', label = 'Scatter Fit')
#pl.plot(np.sort(np.log10(analyticX*4e11)), fitYmed, color = 'r', linewidth = 3, linestyle = '--', label = 'Median Fit')
pl.ylim([10.8,13.2])
pl.xlim([10.5,12.3])
pl.xlabel(r'log$_{10}$[$M$(< 50 kpc) / $M_{\odot}$]', fontsize = 20)
pl.ylabel(r'log$_{10}$[$M_{\rm 200,c}$ / $M_{\odot}$]', fontsize = 20)
#pl.legend(['Scatter Fit', 'Median Fit'], loc = 'upper left')
pl.show()

	