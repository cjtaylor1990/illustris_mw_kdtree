#New Subcount for Illustris Hydro, designed for M(<R) output.  Currently configured to look primaries with 1sigma around Deason et al. 2012 with R = 50 kpc
#Deason et al. 2012 Range for M(<50kpc): 3.8-4.6e11
import sys
import numpy as np

#Taking weighing parameters from command line
if (len(sys.argv) != 4):
	print 'ERROR!  Must have three arguments (mean, sigma, constraint name) for halo weighing.'
	sys.exit()
	
mwMassMean = float(sys.argv[1])*(10.**12.)
#mwMassSigma = float(sys.argv[2])*(10.**12.)
mwMassSigma = (float(sys.argv[2]))*mwMassMean

#File paths to load
dmInFile = './kdTree_complete_10-300kpc_dm_bigdata_illustris-1.npy'
gasInFile = './kdTree_complete_10-300kpc_gas_bigdata_illustris-1.npy'
starInFile = './kdTree_complete_10-300kpc_star_bigdata_illustris-1.npy'

#File paths to save
saveFile = './halo_weighing_m80_sigma.npy'

#Unpacking arrays from DM file 7, 12, 27
dmData = np.transpose(np.load(dmInFile))
haloNum = dmData[0]
groupNum = dmData[1]
dmMassInside50 = dmData[7]
dmMassInside80 = dmData[10]
dmMassInside100 = dmData[12]
dmMassInside250 = dmData[27]
del dmData

#Unpacking arrays from gas file
gasData = np.transpose(np.load(gasInFile))
gasMassInside50 = gasData[7]
gasMassInside80 = gasData[10]
gasMassInside100 = gasData[12]
gasMassInside250 = gasData[27]
del gasData

#Unpacking arrays from star file
starData = np.transpose(np.load(starInFile))
starMassInside50 = starData[7]
starMassInside80 = starData[10]
starMassInside100 = starData[12]
starMassInside250 = starData[27]
del starData

#Calculating total mass inside
totalMassInside50 = dmMassInside50 + gasMassInside50 + starMassInside50
totalMassInside80 = dmMassInside80 + gasMassInside80 + starMassInside80
totalMassInside100 = dmMassInside100 + gasMassInside100 + starMassInside100
totalMassInside250 = dmMassInside250 + gasMassInside250 + starMassInside250

#Creating array that will give a Gaussian weighting to all halos (normalized so that same integral as 1 sigma top hat)
boolArray = (np.exp((-1.*((totalMassInside80- mwMassMean)**2.))/(2.*(mwMassSigma**2.))))*(1./(np.sqrt(2.*np.pi)*mwMassSigma))

saveArray = np.array([haloNum, groupNum, boolArray, totalMassInside50, totalMassInside80, totalMassInside100, totalMassInside250])
saveArray = np.transpose(saveArray)

np.save(saveFile, saveArray)