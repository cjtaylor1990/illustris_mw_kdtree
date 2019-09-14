import sys
import numpy as np
import cosmo_const as cc
import matplotlib.pyplot as pl
import scipy.interpolate as si

#Getting input from command line
if len(sys.argv) != 3:
	print "ERROR!  Improper amount of declarations!"
	sys.exit()
if (str(sys.argv[1]) == 'tophat'):
	weightType = 1
elif (str(sys.argv[1]) == 'gauss'):
	weightType = 2
else:
	print "ERROR!  Need to declare weighting type as either 'tophat' or 'gauss'!"
	sys.exit()

"""
Need two inputs: the weighting type and the mass component
0 = Total Mass
1 = DM
2 = Gas
3 = Star
"""

#Weighting information (from Deason et al. 2012)
mwMassMean = 4.2*(10.**11.)
mwMassSigma = 0.4*(10.**11.)
mwMassHigh = 4.6*(10.**11.)
mwMassLow = 3.8*(10.**11.)

"""
#Weighting information (from Gibbons et al. 2014)
mwMassMean = 2.9*(10.**11.)
mwMassSigma = 0.4*(10.**11.)
mwMassHigh = 3.3*(10.**11.)
mwMassLow = 2.5*(10.**11.)
"""
"""
#Weighing information (from Williams & Evans 2015)
mwMassMean = 4.48*(10.**11.)
mwMassSigma = 0.15*(10.**11.)
mwMassHigh = (4.48+0.15)*(10.**11.)
mwMassLow = (4.48-0.14)*(10.**11.)
"""
#File paths to load
dmInFile = './kdTree_complete_10-300kpc_dm_bigdata_illustris-3.npy'
gasInFile = './kdTree_complete_10-300kpc_gas_bigdata_illustris-3.npy'
starInFile = './kdTree_complete_10-300kpc_star_bigdata_illustris-3.npy'

#Loading in files
dmData = np.transpose(np.load(dmInFile))
gasData = np.transpose(np.load(gasInFile))
starData = np.transpose(np.load(starInFile))

#Specify first and last index with mass value
firstMassIndex = 3
finalMassIndex = len(dmData)-1

#Specify M(<R) index that will determine weighting
mRindex = 7-(firstMassIndex) #Index for M(<50) which will be compared to Deason et al. 2012

#Creating mass distribution array
dmMassDist = dmData[firstMassIndex:finalMassIndex+1]
starMassDist = starData[firstMassIndex:finalMassIndex+1]
gasMassDist = gasData[firstMassIndex:finalMassIndex+1]
massDistArray = dmMassDist + starMassDist + gasMassDist

#Creating weighting array
if (weightType == 1):
	weightArray = np.zeros(len(massDistArray[0]))
	i = 0
	while (i < len(weightArray)):
		if ((massDistArray[mRindex,i] > mwMassLow) & (massDistArray[mRindex,i] < mwMassHigh)):
			weightArray[i] = 1.
		else:
			weightArray[i] = 0.
		i+=1
else:
	weightArray = (np.exp((-1.*((massDistArray[mRindex] - mwMassMean)**2.))/(2.*(mwMassSigma**2.))))*(np.sqrt(2./np.pi))


#Creating confidence interval array (currently empty)
confIntervalArray = np.zeros([len(massDistArray),3])

#Main processing loop to find confidence intervals
j = 0
while (j < len(massDistArray)):
	#massArray = dmMassDist[j]
	if str(sys.argv[2]) == '0':
		massArray = massDistArray[j]
	elif str(sys.argv[2]) == '1':
		massArray = dmMassDist[j]
	elif str(sys.argv[2]) == '2':
		massArray = gasMassDist[j]
	elif str(sys.argv[2]) == '3':
		massArray = starMassDist[j]
		
	#Getting indices for sorting
	massSort = np.argsort(massArray)
	
	#Sorting mass arrays
	sortedMass = massArray[massSort]
	
	#Creating arrays of sorted galaxy weightings
	probVals = weightArray[massSort]
	
	#Creating cumulative probability distributions
	cumProb = np.cumsum(probVals)/np.sum(probVals)
	
	#Creating 90% confidence range of posterior (Total Mass)
	massInterpolate = si.interp1d(cumProb, np.log10(sortedMass))
	massConfLow = massInterpolate(0.16)
	massConfHigh = massInterpolate(0.84)
	massMedian = massInterpolate(0.5)
	
	#Putting median, low, and high of confidence interval into array
	confIntervalArray[j] = [10.**(massMedian),10.**(massConfLow),10.**(massConfHigh)]
	print j
	j+=1

#Creating linear array of galactocentric radii (kpc)
deltaR = 10
maxR = 300
minR = 10
radArray = np.arange(minR,maxR+deltaR,deltaR)

#Creating error arrays
lowErr = confIntervalArray[:,0] - confIntervalArray[:,1]
highErr = confIntervalArray[:,2] - confIntervalArray[:,0]

pl.errorbar(radArray,confIntervalArray[:,0], yerr = [lowErr,highErr], fmt = 's')
pl.xlabel('R (kpc)')
pl.ylabel(r'M(<R) (M$_{\odot}$)')
#pl.ylabel(r'P($M(<50kpc)|M_{tot}$)')
#pl.xscale('log')
pl.yscale('log')
pl.xlim([0,310])
pl.title('Illustris-1 Mass Distribution (Deason et al. 2012; Gauss Weighting)')
pl.show()

vCircArray = np.sqrt(cc.grav_const*confIntervalArray[:,0]/(radArray*(10.**-3.)))
print vCircArray
vCircLowErr = (0.5*cc.grav_const*lowErr/(radArray*(10.**-3)))*(vCircArray**-1.)
vCircHighErr = (0.5*cc.grav_const*highErr/(radArray*(10.**-3.)))*(vCircArray**-1.)

if str(sys.argv[2]) == '0':
	fileLabel = 'total'
elif str(sys.argv[2]) == '1':
	fileLabel = 'dm'
elif str(sys.argv[2]) == '2':
	fileLabel = 'gas'
elif str(sys.argv[2]) == '3':
	fileLabel = 'star'

outArray1 = [radArray, confIntervalArray[:,0],lowErr,highErr]
outFile1 = './data/massdist_deason_e11-13_'+fileLabel+'_illustris3_new.npy'
outArray2 = [radArray, vCircArray,vCircLowErr,vCircHighErr]
outFile2 = './data/veldist_deason_e11-13_'+fileLabel+'_illustris3_new.npy'
np.save(outFile1, outArray1)
np.save(outFile2, outArray2)
print 'End!'
