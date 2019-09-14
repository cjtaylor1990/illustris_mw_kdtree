import sys
import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc

inFile1  = 'script_sigma_m50_mcrit200_deason.npy'#'script_sigma_m50_m100_deason.npy'
inFile2 = 'script_sigma_m80_mcrit200_deason.npy'#'script_sigma_m50_m100_gibbons.npy'
inFile3 = 'script_sigma_m100_mcrit200_deason.npy'
data1 = np.transpose(np.load(inFile1))
data2 = np.transpose(np.load(inFile2))
data3 = np.transpose(np.load(inFile3))
probWidth1 = ((data1[2]+data1[3])/data1[1])
probWidth2 = ((data2[2]+data2[3])/data2[1])
probWidth3 = ((data3[2]+data3[3])/data3[1])

#pl.errorbar(data1[0], data1[1], yerr = [data1[3],data1[2]])
#pl.errorbar(data2[0], data2[1], yerr = [data2[3],data2[2]])
#pl.yscale('log')

pl.figure(figsize=(8,7))
#labelArray = ['Deason et al. 2012', 'Gibbons, Belokurov, & Evans 2014']
labelArray = [r'$r$ = 50 kpc', r'$r$ = 80 kpc', r'$r$ = 100 kpc']
pl.plot((data1[0][1:]),probWidth1[1:]/2., marker = 'o', color = 'k', label = labelArray[0], markersize = 8, markeredgecolor = 'none')
pl.plot((data2[0][1:]),probWidth2[1:]/2., marker = 's', color = 'r', label = labelArray[1], markersize = 8, markeredgecolor = 'none')
pl.plot((data3[0][1:]),probWidth3[1:]/2., marker = '^', color = 'b', label = labelArray[2], markersize = 9, markeredgecolor = 'none')
pl.xlabel(r'Fractional Error on $M$(< $r$)')
#pl.ylabel(r'Fractional 68% Width ($M_{\rm 200,c}$)')
pl.ylabel(r'Fractional Error on $M_{\rm 200,c}$')
#pl.axvline(0.4*10., color = 'k', linewidth = 2.0)
pl.xlim([0.02,0.21])
#pl.ylim([0.05,0.35])
#pl.axhline(0.560555663784, color = 'b')
#pl.axhline(0.545829577905, color = 'r')
#pl.axhline(0.5315315315315315, color = 'r')
#pl.axvline((0.4/4.2), color = 'r')
#pl.axvline((0.4/2.9), color = 'b')
pl.legend(labelArray, loc = 'upper left')

pl.show()