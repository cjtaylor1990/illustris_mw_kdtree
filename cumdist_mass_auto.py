import sys
import numpy as np
import numpy.ma as mask
import matplotlib.pyplot as pl
import scipy.interpolate as si
import cosmo_const as cc
import math
import csv

if (len(sys.argv) != 4):
	print 'ERROR! Wrong number of arguments.'
	sys.exit()
if (str(sys.argv[1]) == 'mcrit200'):
	massIndex = 1
elif (str(sys.argv[1]) == 'mmean200'):
	massIndex = 2
elif (str(sys.argv[1]) == 'mtophat'):
	massIndex = 3
elif (str(sys.argv[1]) == 'mstar'):
	massIndex = 4
elif (str(sys.argv[1]) == 'm100'):
	massIndex = 5
elif (str(sys.argv[1]) == 'm250'):
	massIndex = 6
else:
	print 'Error!  Wrong arguments'
	sys.exit()

inFile = str(sys.argv[2])
m50Value = float(sys.argv[3])*(10.**10.)
mcritInFile = './m_crit200_bigdata.npy'

#Unpacking data (groupNum, totalMassInside, allMassTotal, dmMassInside, gasMassInside, starMassInside, boolArray)
data = np.transpose(np.load(inFile))
haloNum = data[0]
groupNum = data[1]
boolArray = data[2]
mInside50 = data[3]
mInside100 = data[4]
mInside250 = data[5]
del data
if (massIndex == 6):
	testMass = mInside250
elif (massIndex == 5):
	testMass = mInside100
else:
	#Unpacking M_crit200, M_mean200, M_tophat200, or M_star data
	data = np.transpose(np.load(mcritInFile))
	testMass = data[massIndex]
	del data

#Getting indices for sorting
testMassSort = np.argsort(testMass)

testMass = testMass[testMassSort]
probVals = boolArray[testMassSort]
cumProb = np.cumsum(probVals)/np.sum(probVals)

#Creating 90% confidence range of cumulative prob distribution
massInterpolate = si.interp1d(cumProb, np.log10(testMass))
massConfLow90 = 10.**massInterpolate(0.05)
massConfHigh90 = 10.**massInterpolate(0.95)
massConfLow68 = 10.**massInterpolate(0.16)
massConfHigh68 = 10.**massInterpolate(0.84)
massMedian = 10.**massInterpolate(0.5)
#massPeak = np.log10(np.array(midMass)[np.where(posProb == np.max(posProb))])

#print str(massMedian/(10.**10.)) + ' + ' + str((massConfHigh68 - massMedian)/(10.**10.)) + ' - ' + str((massMedian - massConfLow68)/(10.**10.))
#print str((massConfHigh68-massConfLow68)/massMedian)
#print (0.4/4.2)
print str(m50Value)+ ' ' + str(massMedian) + ' ' + str((massConfHigh68 - massMedian)) + ' ' + str((massMedian - massConfLow68))


	