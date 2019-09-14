import sys
import numpy as np
import cosmo_const as cc
import matplotlib.pyplot as pl
import scipy.interpolate as si

#File paths to load
darkInFile = './kdTree_bigdata_10-300kpc_dm_Illustris-Dark-1.npy'
hydroDMInFile = './kdTree_complete_10-300kpc_dm_bigdata_illustris-1.npy'
hydroStarInFile = './kdTree_complete_10-300kpc_star_bigdata_illustris-1.npy'
hydroGasInFile = './kdTree_complete_10-300kpc_gas_bigdata_illustris-1.npy'
mcritInFile = 'm_crit200_bigdata_Illustris-1.npy'

#Comparison files to load
comparisonFile = './comparisonArrays_illustris1.npy'

#Loading in files
darkDMData = np.load(darkInFile)
hydroDMData = np.load(hydroDMInFile)
hydroStarData = np.load(hydroStarInFile)
hydroGasData = np.load(hydroGasInFile)
comparisonData = np.load(comparisonFile)
mcrit200Data = np.load(mcritInFile)[:,1]

print len(darkDMData)
print len(mcrit200Data)

#Doing a mass cut of halos (68% confidence Deason M_crit200)
#mwHigh = (4.2+0.4)*10.**11.
#mwLow = (4.2-0.4)*10.**11.
#m50forCut = (hydroDMData + hydroStarData + hydroGasData)[:,7]
#iMassCut = np.where(np.logical_and(m50forCut > mwLow, m50forCut < mwHigh))
mwHigh = (111.776294305 + 36.9608444109)*(10.**10.)
mwLow = (111.776294305 - 24.0499631292)*(10.**10.)
iMassCut = np.where(np.logical_and(mcrit200Data > mwLow, mcrit200Data < mwHigh))
darkDMData = darkDMData[iMassCut]
hydroDMData = hydroDMData[iMassCut]
hydroStarData = hydroStarData[iMassCut]
hydroGasData = hydroGasData[iMassCut]
print len(darkDMData)

#Specifying index for subhalo number
subhaloNumIndex = 0

#Specify first and last index with mass value
firstMassIndex = 3
finalMassIndex = len(hydroDMData)-1

#Specify M(<R) index that will determine weighting
mRindex = 7-(firstMassIndex) #Index for M(<50) which will be compared to Deason et al. 2012

#Finding dark versions of hydro halos (and vice-versa)
#Note that comparison DM numbers is not in original order, but rearranged when matching the halos
iInHydroSample = np.in1d(comparisonData[0], hydroDMData[:,0])
iInDarkSample = np.in1d(comparisonData[1], darkDMData[:,0])
iConsistent = np.equal(iInHydroSample,iInDarkSample)
iHydroConsistent = np.in1d(comparisonData[0][iConsistent], hydroDMData[:,0])
iDarkConsistent = np.in1d(comparisonData[1][iConsistent], darkDMData[:,0])
darkVersionHydro = (comparisonData[1][iConsistent])[iDarkConsistent]
hydroVersionDark = (comparisonData[0][iConsistent])[iHydroConsistent]

#Looking for these other versions in hydro and dark sub-samples
iDark = np.in1d(darkDMData[:,0], darkVersionHydro)#consistentDark)
iHydro = np.in1d(hydroDMData[:,0], hydroVersionDark)#consistentHydro)

darkDMDataMatched = darkDMData[iDark]
hydroDMDataMatched = hydroDMData[iHydro]
hydroStarDataMatched = hydroStarData[iHydro]
hydroGasDataMatched = hydroGasData[iHydro]

i = 0
darkDMDataCorrected = np.empty([len(darkDMDataMatched),len(darkDMDataMatched[0])])
while (i < len(darkVersionHydro)):
	findingNum = np.equal(darkDMDataMatched[:,0], darkVersionHydro[i])
	findingArray = darkDMDataMatched[findingNum]
	darkDMDataCorrected[i] = findingArray
	i+=1

darkDMDataCorrected = np.transpose(darkDMDataCorrected)[firstMassIndex::]

#np.save('test_hydro_v_dark.npy', np.array([darkDMDataMatched[:,0],hydroDMDataMatched[:,0]]))

#Creating total mass distribution for Hydro
massDistMatched = np.transpose(hydroDMDataMatched)[firstMassIndex::] + np.transpose(hydroStarDataMatched)[firstMassIndex::] + np.transpose(hydroGasDataMatched)[firstMassIndex::]

#Creating cumulative mass distribution
resMassDist = (massDistMatched - darkDMDataCorrected)/massDistMatched
resMassDistMed = np.apply_along_axis(np.median, 1, resMassDist)
resMassLow = np.apply_along_axis(np.sort, 1, resMassDist)[:,np.floor(0.16*len(resMassDist[0]))]
resMassHigh = np.apply_along_axis(np.sort, 1, resMassDist)[:,np.ceil(0.84*len(resMassDist[0]))]

#Creating differential mass distributions
subtractArrayHydro = np.concatenate((np.array([np.zeros(len(massDistMatched[0]))]),massDistMatched[0:len(massDistMatched)-1]))
subtractArrayDark = np.concatenate((np.array([np.zeros(len(darkDMDataCorrected[0]))]),darkDMDataCorrected[0:len(darkDMDataCorrected)-1]))

differentialMassHydro = massDistMatched - subtractArrayHydro
differentialMassDark = darkDMDataCorrected - subtractArrayDark
resMassDifferential = (differentialMassHydro - differentialMassDark)/differentialMassHydro

resMassDifferentialMed = np.apply_along_axis(np.median, 1, resMassDifferential)
resMassDifferentialLow = np.apply_along_axis(np.sort, 1, resMassDifferential)[:,np.floor(0.16*len(resMassDifferential[0]))]
resMassDifferentialHigh = np.apply_along_axis(np.sort, 1, resMassDifferential)[:,np.ceil(0.84*len(resMassDifferential[0]))]

#Creating error arrays for cumulative
highErr = (resMassHigh - resMassDistMed)
lowErr = (resMassDistMed - resMassLow)

#Creating error arrays for differential
highErrDiff = resMassDifferentialHigh - resMassDifferentialMed
lowErrDiff = resMassDifferentialMed - resMassDifferentialLow

#Creating linear array of galactocentric radii (kpc)
deltaR = 10
maxR = 300
minR = 10
radArray = np.arange(minR,maxR+deltaR,deltaR)
pl.figure(figsize=(8.,7.))
#pl.errorbar(radArray,resMassDistMed, yerr = [lowErr,highErr],fmt = 's', color = 'k', markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5, markeredgewidth = 1.5, markeredgecolor = 'none')
pl.errorbar(radArray,resMassDifferentialMed, yerr = [lowErrDiff,highErrDiff],fmt = 's', color = 'k', markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5, markeredgewidth = 1.5, markeredgecolor = 'none')
pl.xlabel(r'$r$ [kpc]')
#pl.ylabel(r'1 - $M_{\rm DMO}$(<$r$) / $M$(<$r$)')
pl.ylabel(r'1 - $\rho_{\rm DMO}$($r$) / $\rho$($r$)')
pl.xlim([0.,310.])
pl.axhline(0., color = '0.5', linestyle = '--', linewidth = 3)
pl.show()

print 'End!'