import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc

#deason_file = './massdist_gibbons2014_gauss_illustris1.npy'
#gibbons_file = './massdist_gibbons2014_gauss_illustris1.npy'
#gibbons_file = './massdist_gibbons2014_gauss_illustrisdark1.npy'
#deasonData = np.load(deason_file)
#gibbonsData = np.load(gibbons_file)

file1 = './massdist_deason_e11-13_total_illustris1_new.npy'
file2 = './massdist_gibbons_e11-13_total_illustris1_new.npy'

data1 = np.load(file1)
data2 = np.load(file2)

vCircArray1 = np.sqrt(cc.grav_const*data1[1]/(data1[0]*(10.**-3.)))
vCircLowErr1 = (0.5*vCircArray1**-1.)*(cc.grav_const*data1[2]/(data1[0]*(10.**-3.)))
vCircHighErr1 = (0.5*vCircArray1**-1.)*(cc.grav_const*data1[3]/(data1[0]*(10.**-3.)))

vCircArray2 = np.sqrt(cc.grav_const*data2[1]/(data2[0]*(10.**-3.)))
vCircLowErr2 = (0.5*vCircArray2**-1.)*(cc.grav_const*data2[2]/(data2[0]*(10.**-3.)))
vCircHighErr2 = (0.5*vCircArray2**-1.)*(cc.grav_const*data2[3]/(data2[0]*(10.**-3.)))

labelArray = ['D12', 'G14']

pl.figure(figsize=(8,7))

pl.errorbar(data1[0],vCircArray1, yerr = [vCircLowErr1,vCircHighErr1], fmt = 's', color = 'k', label = labelArray[0], markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5)
pl.errorbar(data1[0],vCircArray2, yerr = [vCircLowErr2,vCircHighErr2], fmt = 'o', color = '0.5', label=labelArray[1], markeredgecolor = '0.5', markersize = 8, elinewidth = 1.5, capsize = 5.0, capthick = 1.5)
#pl.errorbar(data2[0],data2[1], yerr = [data2[2],data2[3]], fmt = 's',label=labelArray[0])
#pl.errorbar(data3[0],data3[1], yerr = [data3[2],data3[3]], fmt = 's',label=labelArray[0])

pl.xlabel('$r$  [kpc]', fontsize = 20)
pl.ylabel(r'$V_{\rm circ}(r)$  [km/s]',fontsize = 20)
#pl.ylabel(r'P($M(<50kpc)|M_{tot}$)')
#pl.xscale('log')
#pl.yscale('log')
pl.xlim([0,310])
pl.ylim([0,220])
#pl.title('Illustris-1 Mass Distribution (Gauss Weighting)')
pl.legend(labelArray, loc = 'lower right', fontsize = 18)
#pl.savefig('/Users/cjtaylor/Dropbox/fig11a.pdf', transparent = True)
pl.show()