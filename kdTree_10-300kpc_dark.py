#Last updated: 11/13/15.
#importing libraries.  Got 1/5/15 version of readsnapHDF5 from Volgelsburger repo.
import readsnapHDF5 as rs
import readsubfHDF5 
import sys 
import numpy as np
import cosmo_const as cc
from mpi4py import MPI
import scipy.spatial as sp

#arguments from command line when ran
run  = str(sys.argv[1])
snap = int(sys.argv[2])
search_r = float(sys.argv[3])
pType = str(sys.argv[4])
partFileTxt = str(sys.argv[5])

if (pType == "dm"):
	pNum = 1
elif (pType == "star"):
	pNum = 4
elif (pType == "gas"):
	pNum = 0
else:
	print "ERROR!  Unknown particle type!"
	sys.exit()
	
#radii (r) at which M(<r) will be calculated
search_r_array = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200,210,220,230,240,250,260,270,280,290,search_r]

boxsize=75000.0*(cc.h_little**-1.) #length of box side (kpc)
search_r2 = search_r * search_r

#switch variable.  If = 0, then runs
this_task = 0

#prints arguments from initial command line
print sys.argv
print snap

ext = '000'+str(snap)
ext = ext[-3:]

#loading in txt file with all particle files listed
partFileArray = np.genfromtxt(partFileTxt, dtype='str')
print partFileArray


#loading in catalog of halos
if this_task==0:
	cat = readsubfHDF5.subfind_catalog('/n/hernquistfs1/Illustris/Runs/'+run+'/output/', snap, keysel=['SubhaloPos', 'SubhaloMass', 'GroupFirstSub', 'SubhaloGrNr', 'Group_M_Crit200'] )
else:
	cat = None
print "Loaded In Halo Catalog"

groupFirstSub = cat.GroupFirstSub[np.where(cat.GroupFirstSub != -1)]
all_subhalo_nrs = np.arange(cat.SubhaloMass.shape[0])	#making an array of values 0 to the number of halos - 1 (index number array)
subhalo_masses = cat.SubhaloMass * 1e10 * (cc.h_little**-1.)	#correcting array of halo masses to be in units of Msun
groupNum = cat.SubhaloGrNr
groupMcrit200 = cat.Group_M_Crit200[np.where(cat.GroupFirstSub != -1)]*(cc.h_little**-1.)*(10.**10.)

#finding primary halos within mass range (e11.5-e12.5)
#groupFirstSub = groupFirstSub[(subhalo_masses[groupFirstSub] > (10.**11.5)) & (subhalo_masses[groupFirstSub] < (10.**12.5))]
groupFirstSub = groupFirstSub[(groupMcrit200 > (10.**11.)) & (groupMcrit200 < (10.**13.))]
print groupFirstSub

print cat.SubhaloMass.shape
print cat.SubhaloMass.shape[0]
print subhalo_masses
print subhalo_masses.shape

#loading in halo positions as cat_[dimension] variable
catPos = (cat.SubhaloPos.astype(float)[groupFirstSub])*(cc.h_little**-1.)
n_subs = cat.SubhaloMass.shape[0]

print len(catPos)
print len(groupFirstSub)

#finding halos that are too close to edges
badHaloIndexX1 = np.where(catPos[:,0] < search_r)
badHaloIndexX2 = np.where(catPos[:,0] > (boxsize-search_r))
badHaloIndexY1 = np.where(catPos[:,1] < search_r)
badHaloIndexY2 = np.where(catPos[:,1] > (boxsize-search_r))
badHaloIndexZ1 = np.where(catPos[:,2] < search_r)
badHaloIndexZ2 = np.where(catPos[:,2] > (boxsize-search_r))
badHaloIndex = np.concatenate((badHaloIndexX1[0],badHaloIndexX2[0],badHaloIndexY1[0],badHaloIndexY2[0],badHaloIndexZ1[0],badHaloIndexZ2[0]))
badHaloIndex = np.unique(badHaloIndex)

#creating array of transformed bad halo positions
badHaloTransformed = (cat.SubhaloPos.astype(float)[groupFirstSub])*(cc.h_little**-1.)
(badHaloTransformed[:,0])[badHaloIndexX1] += boxsize
(badHaloTransformed[:,0])[badHaloIndexX2] -= boxsize
(badHaloTransformed[:,1])[badHaloIndexY1] += boxsize
(badHaloTransformed[:,1])[badHaloIndexY2] -= boxsize
(badHaloTransformed[:,2])[badHaloIndexZ1] += boxsize
(badHaloTransformed[:,2])[badHaloIndexZ2] -= boxsize
badHaloPos = badHaloTransformed[badHaloIndex]
del badHaloTransformed

#Clearing un-needed arrays
del cat

print len(badHaloIndex)
print len(catPos)
print len(catPos) - len(badHaloIndex)
print len(groupFirstSub)

#Creating output array (to be saved into numpy file)
outArray = np.zeros([len(groupFirstSub), 3+len(search_r_array)])
outArray[:,0] = groupFirstSub
outArray[:,1] = groupNum[groupFirstSub]
outArray[:,2] = subhalo_masses[groupFirstSub]

badHaloMass = np.zeros([len(badHaloPos),len(search_r_array)])

i = 0
while (i < len(partFileArray)):
	#loading in particle positional data
	partPos = rs.read_block(partFileArray[i], 'POS ', parttype=pNum, verbose=True).astype('float')
	partPos = partPos*(cc.h_little**-1.)
	#loading in particle mass data
	partMass = rs.read_block(partFileArray[i], 'MASS', parttype=pNum, verbose=True).astype('float')
	partMass = np.reshape(partMass, partMass.shape[0])*1e10*(cc.h_little**-1.)
	
	print "Number of Particles: " + str(len(partMass))
	
	
	#Setting up the the KD Tree
	kdTree = sp.cKDTree(partPos)

	j = 0
	while (j < len(groupFirstSub)):
		k = 0
		while (k < len(search_r_array)):
			iPartInR = kdTree.query_ball_point(catPos[j], search_r_array[k])
			mInR = np.sum(partMass[iPartInR])
			outArray[j,3+k] += mInR
			k+=1
		j += 1
	
	j = 0
	while (j < len(badHaloIndex)):
		k = 0
		while (k < len(search_r_array)):
			iPartInR = kdTree.query_ball_point(badHaloPos[j], search_r_array[k])
			mInR = np.sum(partMass[iPartInR])
			badHaloMass[j,k] += mInR
			k+=1
		j += 1
	print i
	i += 1

m = 0
while (m<len(search_r_array)):
	(outArray[:,3+m])[badHaloIndex] += badHaloMass[:,m]
	m += 1

outFile = 'kdTree_10-300kpc_'+pType+'_'+run+'.npy'
np.save(outFile, outArray)

print (groupNum[groupFirstSub])[badHaloIndex]
print badHaloPos[np.where((groupNum[groupFirstSub])[badHaloIndex] == 5255.)]
print catPos[np.where(groupNum[groupFirstSub] == 5255.)]
print boxsize

print "End!"
	
	


