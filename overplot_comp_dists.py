import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc

#deason_file = './massdist_gibbons2014_gauss_illustris1.npy'
#gibbons_file = './massdist_gibbons2014_gauss_illustris1.npy'
#gibbons_file = './massdist_gibbons2014_gauss_illustrisdark1.npy'
#deasonData = np.load(deason_file)
#gibbonsData = np.load(gibbons_file)

file1 = './veldist_deason_e11-13_dm_illustris1_new.npy'
file2 = './veldist_deason_e11-13_gas_illustris1_new.npy'
file3 = './veldist_deason_e11-13_star_illustris1_new.npy'


data1 = np.load(file1)
data2 = np.load(file2)
data3 = np.load(file3)

labelArray = ['Dark Matter', 'Gas', 'Stars']

pl.figure(figsize=(8,7))
pl.errorbar(data1[0],data1[1], yerr = [data1[2],data1[3]], fmt = 's', markersize = 8,label=labelArray[0], elinewidth = 1.3, markeredgewidth = 1.3, color = 'k', fillstyle = 'none')
pl.errorbar(data2[0],data2[1], yerr = [data2[2],data2[3]], fmt = 'o', markersize = 8,label=labelArray[1], elinewidth = 1.3, markeredgewidth = 1.3, color = 'r', fillstyle = 'none')
pl.errorbar(data3[0],data3[1], yerr = [data3[2],data3[3]], fmt = '^', markersize = 8,label=labelArray[2], elinewidth = 1.3, markeredgewidth = 1.3, color = 'b', fillstyle = 'none')
pl.ylabel(r'$V_{\rm circ}(r)$  [km/s]',fontsize = 20)
pl.xlabel(r'$r$  [kpc]',fontsize = 20)
pl.xlim([0,310])
pl.ylim([0,220])
#pl.yscale('log')
pl.legend(labelArray, loc = 'upper right',fontsize = 18)

#pl.text(-35, 0.30, 'Fractional Differences', va = 'center', rotation = 'vertical', fontsize = 18)
pl.show()