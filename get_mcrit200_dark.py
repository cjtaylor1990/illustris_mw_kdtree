#Last updated: 1/18/15.
#importing libraries.  Got 1/5/15 version of readsnapHDF5 from Volgelsburger repo.
import readsubfHDF5  
import numpy as np
import cosmo_const as cc

#switch variable.  If = 0, then runs
this_task = 0

#loading in catalog of halos
if this_task==0:
	cat = readsubfHDF5.subfind_catalog('/n/hernquistfs1/Illustris/Runs/Illustris-Dark-1/output/', 135, keysel=['Group_M_Crit200', 'Group_M_Mean200', 'Group_M_TopHat200', 'SubhaloMassType'] )
else:
	cat = None

massInsideData = np.transpose(np.load('kdTree_bigdata_10-300kpc_dm_Illustris-Dark-1.npy'))
haloNum = np.array(massInsideData[0])
groupNum = np.array(massInsideData[1])
m_crit200 = np.empty(len(groupNum))
m_mean200 = np.empty(len(groupNum))
m_topHat200 = np.empty(len(groupNum))
m_star = np.empty(len(groupNum))
i = 0
while (i<len(groupNum)):
	m_crit200[i] = cat.Group_M_Crit200[groupNum[i]]*1e10*(cc.h_little**-1.)
	m_mean200[i] = cat.Group_M_Mean200[groupNum[i]]*1e10*(cc.h_little**-1.)
	m_topHat200[i] = cat.Group_M_TopHat200[groupNum[i]]*1e10*(cc.h_little**-1.)
	m_star[i] = (cat.SubhaloMassType[:,4])[haloNum[i]]*1e10*(cc.h_little**-1.)
	
	i += 1

outFile = 'm_crit200_bigdata_illustrisdark-1.npy'
outArray = np.transpose(np.array([groupNum, m_crit200, m_mean200, m_topHat200, m_star]))
np.save(outFile, outArray)
print "End!"
	
	


