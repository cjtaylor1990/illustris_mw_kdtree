import numpy as np
import numpy.ma as mask
import matplotlib.pyplot as pl
import matplotlib
import scipy.interpolate as si
import cosmo_const as cc
import math
import csv

inFile = './halo_weighing_e11-13_deason_illustris-1.npy'

#Error Info
errorPercent = 0.90
highErrPercent = 1.-(0.5-(errorPercent/2.))
lowErrPercent = 0.5-(errorPercent/2.)

#Unpacking data (groupNum, totalMassInside, allMassTotal, dmMassInside, gasMassInside, starMassInside, boolArray)
data = np.transpose(np.load(inFile))
haloNum = data[0]
groupNum = data[1]
boolArray = data[2]
mInside50 = data[3]
mInside80 = data[4]
mInside100 = data[5]
mInside250 = data[6]
data = False

#Unpacking M_crit200 Data [groupNum, m_crit200, m_mean200, m_topHat200, m_Star]
mCrit200Data = np.transpose(np.load('./m_crit200_bigdata_illustris-1.npy'))
mCrit200 = mCrit200Data[1]
mStar = mCrit200Data[4]
mCrit200Data = False

pl.rcParams['axes.linewidth'] = 1.5
pl.rcParams['axes.labelsize'] = 'large'
#pl.rcParams['axes.labelweight'] = 'bold'
pl.rcParams['xtick.major.size'] = 8.0
pl.rcParams['xtick.minor.size'] = 4.0
pl.rcParams['ytick.major.size'] = 8.0
pl.rcParams['ytick.minor.size'] = 4.0
pl.figure(figsize=(8.5,7.5))
#pl.scatter(totalMassInside, mInside100, c = np.log10(mInside250), cmap = pl.cm.coolwarm, lw=0)
pl.scatter(mInside50, mStar, c = np.log10(mCrit200), cmap = pl.cm.coolwarm, lw=0, edgecolor = 'none')#, norm = matplotlib.colors.LogNorm())
pl.axvspan(3.8*10.**11., 4.6*10.**11., facecolor = 'm', alpha = 0.2)
pl.axvspan(2.4*10.**11., 3.4*10.**11., facecolor = 'y', alpha = 0.2)
pl.axhspan(4.94*10.**10., 7.22*10.**10., facecolor = 'g', alpha = 0.2)
pl.xlabel(r'$M$(< 50 kpc) [$M_{\odot}]$', fontsize = 20)
pl.ylabel(r'$M_{\star}$ [$M_{\odot}]$', fontsize = 20)
pl.xscale('log')
pl.yscale('log')
pl.xlim([3.5*10.**10.,2.*10.**12.])
pl.ylim([2.*10.**8.,1.*10.**12.])
pl.text(10.**11.40, (1.5*2.*10.**11.), 'G14', rotation = 270, fontsize = 20)
pl.text(10.**11.57, (1.5*2.*10.**11.), 'D12', rotation = 270, fontsize = 20)
pl.text((5.5*10.**10.), (5.3*10.**10.), 'LN 15', rotation = 0, fontsize = 20)
pl.text(5.5*10.**12., (4.*10.**10.), r'log$_{10}$[$M_{\rm 200,c}$ / $M_{\odot}$]', rotation = 270, fontsize = 20)
#pl.title(r'Illustris-2 M(<50kpc) v. M$_{*}$ (Color: log$_{10}$(M$_{crit200}$))')
pl.colorbar()
#pl.savefig('/Users/cjtaylor/Dropbox/fig17b.pdf', transparent = True)
pl.show()

	