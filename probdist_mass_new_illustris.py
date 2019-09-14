import numpy as np
import numpy.ma as mask
import matplotlib.pyplot as pl
import scipy.interpolate as si
import cosmo_const as cc
import math
import csv
import sys

constraint = str(sys.argv[1])
sim = str(sys.argv[3])
mcritInFile = 'm_crit200_bigdata_'+sim+'.npy'
inFile = './halo_weighing_e11-13_'+constraint+'_'+sim+'.npy'

#Unpacking data [haloNum, groupNum, boolArray, totalMassInside50, totalMassInside80, totalMassInside100, totalMassInside250]
data = np.transpose(np.load(inFile))
haloNum = data[0]
groupNum = data[1]
boolArray = data[2]
mInside50 = data[3]
mInside80 = data[4]
mInside100 = data[5]
mInside250 = data[6]
del data

#Unpacking other data [groupNum, m_crit200, m_mean200, m_topHat200, m_star]
data = np.transpose(np.load(mcritInFile))
mCrit200 = data[1]
mMean200 = data[2]
mVir = data[3]
mStar = data[4]
del data
print np.where(mStar < 1.0)
#Designating test mass (one that will be estimated)
if (str(sys.argv[2]) == 'mcrit200'):
	testMass = mCrit200
elif (str(sys.argv[2]) == 'mmean200'):
	testMass = mMean200
elif (str(sys.argv[2]) == 'mvir'):
	testMass = mVir
elif (str(sys.argv[2]) == 'mstar'):
	testMass = mStar
elif (str(sys.argv[2]) == 'm100'):
	testMass = mInside100
elif (str(sys.argv[2]) == 'm250'):
	testMass = mInside250
else:
	print 'Error!  Wrong arguments'
	sys.exit()

#Create mass binning array
massMin = np.min(testMass)
massMax = np.max(testMass)
#print massMin
#deltaLogM = 0.04
#print np.log10(massMax)
#nBins = np.ceil((13.-11.)/deltaLogM)
nBins = 50.
#massLeftLims = np.logspace(11., 13. ,nBins, endpoint = False,base = 10.)
massLeftLims = np.logspace(np.log10(massMin), np.log10(massMax), nBins, endpoint = False,base = 10.)
#binSize = (13.-11.)/nBins

#print massLeftLims
#print massMax

iMassBins = np.digitize(testMass,massLeftLims)
iMassUnique = np.unique(iMassBins)
totInside = np.empty(len(iMassUnique))
trueInside = np.empty(len(iMassUnique))
midMass = np.empty(len(iMassUnique))
k = 0
for i in iMassUnique:
	bin = np.where(iMassBins == i)
	totInside[k] = float(len(testMass[bin]))
	trueInside[k] = float(np.sum(boolArray[bin]))
	#midMass[k] = 10.**(np.log10(massLeftLims[k]) + (binSize/2.))
	midMass[k] = np.median(testMass[bin])
	k += 1
#print midMass

likelihood = trueInside

#Sorting test mass to do confidence ranges
#Getting indices for sorting
testMassSort = np.argsort(testMass)

testMass = testMass[testMassSort]
probVals = boolArray[testMassSort]
cumProb = np.cumsum(probVals)/np.sum(probVals)

#Creating confidence ranges of cumulative prob distribution
massInterpolate = si.interp1d(cumProb, np.log10(testMass))
massConfLow90 = 10.**massInterpolate(0.05)
massConfHigh90 = 10.**massInterpolate(0.95)
massConfLow68 = 10.**massInterpolate(0.16)
massConfHigh68 = 10.**massInterpolate(0.84)
massConfHigh99 = 10.**massInterpolate(0.995)
massConfLow99= 10.**massInterpolate(0.005)
massConfHigh999 = 10.**massInterpolate(0.9995)
massConfLow999 = 10.**massInterpolate(0.0005)
massConfHigh9995 = 10.**massInterpolate(0.99975)
massConfLow9995 = 10.**massInterpolate(0.00025)
limit45 = massInterpolate(0.45)
limit55 = massInterpolate(0.55)
print len(testMass[np.where(np.logical_and(np.log10(testMass) > limit45, np.log10(testMass) < limit55))])
massMedian = 10.**massInterpolate(0.5)

print str(massMedian/(10.**10.)) + " + " + str((massConfHigh68 - massMedian)/(10.**10.)) + " - " +str((massMedian - massConfLow68)/(10.**10.))
print str(massMedian/(10.**10.)) + " + " + str((massConfHigh90 - massMedian)/(10.**10.)) + " - " +str((massMedian - massConfLow90)/(10.**10.))
#print str(massMedian/(10.**10.)) + " + " + str((massConfHigh99 - massMedian)/(10.**10.)) + " - " +str((massMedian - massConfLow99)/(10.**10.))
#print str(massMedian/(10.**10.)) + " + " + str((massConfHigh999 - massMedian)/(10.**10.)) + " - " +str((massMedian - massConfLow999)/(10.**10.))
#print str(massMedian/(10.**10.)) + " + " + str((massConfHigh9995 - massMedian)/(10.**10.)) + " - " +str((massMedian - massConfLow9995)/(10.**10.))
#print massPeak

pl.figure(figsize=(8,7))
pl.plot(np.log10(midMass), likelihood/np.sum(likelihood), marker = 'o', color = 'k')#, label = 'Posterior (P(M|X))')
#pl.plot(np.log10(midMass), totInside/np.sum(totInside), color = 'r')
#pl.plot(np.log10(testMass), cumProb, color = 'k')
#pl.axvline(limit45, color = 'r')
#pl.axvline(limit55, color = 'r')
#pl.axhline(0.16, color = 'b')
#pl.axhline(0.84, color = 'b')
#pl.axhline(0.5, color = 'b')
#pl.axvspan(np.log10((1.24-0.18)*10.**12.), np.log10((1.24+0.35)*10.**12.), facecolor = 'r', alpha = 0.2)
pl.xlabel(r'$M$')
pl.ylabel(r'Likelihood')
#pl.ylabel(r'P($M(<50kpc)|M_{tot}$)')
#pl.xscale('log')
#pl.yscale('log')
#pl.title('Illustris-1 Likelhood of M$_ Using Deason et al. 2012 (Top Hat Weighting)')
#pl.xlim([11., 13.])
#pl.ylim([-0.01,0.2])
pl.show()

outArray = [midMass, likelihood]
#print np.max(likelihood)/np.sum(likelihood)
#outFile = './mcrit200_likelihood_illustris1_lowSigma2_gauss.npy'
outFile = './'+str(sys.argv[2])+'_likelihood_e11-13_'+constraint+'_'+sim+'.npy'
np.save(outFile, outArray)
print 'End!'

	