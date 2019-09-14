import numpy as np
import matplotlib.pyplot as plt
import csv
import sys

inFile  = str(sys.argv[1])
outFile = str(sys.argv[2])

table = open(inFile, 'r')
data = csv.reader(table, delimiter = ' ')

m50 = []
mCrit200 = []
highErr = []
lowErr = []
deltaM = 0.1
for column in data:
	m50.append(10.**(np.log10(1.5*10.**11.) + ((float(column[0])/1e10)*deltaM)))
	mCrit200.append(float(column[1]))
	highErr.append(float(column[2]))
	lowErr.append(float(column[3]))
    
mCrit200 = np.array(mCrit200)
highErr = np.array(highErr)
lowErr = np.array(lowErr)

outArray = np.array([m50, mCrit200, highErr, lowErr])
outArray = np.transpose(outArray)

np.save(outFile, outArray)
