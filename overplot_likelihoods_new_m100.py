import numpy as np
import matplotlib.pyplot as pl
import cosmo_const as cc

#'./'+str(sys.argv[2])+'_likelihood_e11-13_'+constraint+'_'+sim+'.npy'
illustris1_file1 = './m100_likelihood_e11-13_deason_illustris-1.npy'
illustris2_file1 = './m100_likelihood_e11-13_deason_illustris-2.npy'
illustris3_file1 = './m100_likelihood_e11-13_deason_illustris-3.npy'

illustris1_file2 = './m100_likelihood_e11-13_gibbons_illustris-1.npy'
illustris2_file2 = './m100_likelihood_e11-13_gibbons_illustris-2.npy'
illustris3_file2 = './m100_likelihood_e11-13_gibbons_illustris-3.npy'

#Loading in Deason files
i1MidMass1 = np.load(illustris1_file1)[0]
i1Likelihood1 = np.load(illustris1_file1)[1]
i1Likelihood1 = i1Likelihood1/np.sum(i1Likelihood1)

i2MidMass1 = np.load(illustris2_file1)[0]
i2Likelihood1 = np.load(illustris2_file1)[1]
i2Likelihood1 = i2Likelihood1/np.sum(i2Likelihood1)

i3MidMass1 = np.load(illustris3_file1)[0]
i3Likelihood1 = np.load(illustris3_file1)[1]
i3Likelihood1 = i3Likelihood1/np.sum(i3Likelihood1)

#Loading in Gibbons files
i1MidMass2 = np.load(illustris1_file2)[0]
i1Likelihood2 = np.load(illustris1_file2)[1]
i1Likelihood2 = i1Likelihood2/np.sum(i1Likelihood2)

i2MidMass2 = np.load(illustris2_file2)[0]
i2Likelihood2 = np.load(illustris2_file2)[1]
i2Likelihood2 = i2Likelihood2/np.sum(i2Likelihood2)

i3MidMass2 = np.load(illustris3_file2)[0]
i3Likelihood2 = np.load(illustris3_file2)[1]
i3Likelihood2 = i3Likelihood2/np.sum(i3Likelihood2)

pl.figure(figsize=(8,7))
pl.plot(np.log10(i1MidMass1),i1Likelihood1,marker = 'o', markeredgecolor = 'none', markersize = 8, color = 'k')
pl.plot(np.log10(i2MidMass1),i2Likelihood1,marker = 'o', markeredgecolor = 'none', markersize = 8, color = 'b')
pl.plot(np.log10(i3MidMass1),i3Likelihood1,marker = 'o', markeredgecolor = 'none', markersize = 8, color = 'r')
pl.plot(np.log10(i1MidMass2),i1Likelihood2,marker = 's', markeredgecolor = 'none', markersize = 8, color = 'k', linestyle = '--')
pl.plot(np.log10(i2MidMass2),i2Likelihood2,marker = 's', markeredgecolor = 'none', markersize = 8, color = 'b', linestyle = '--')
pl.plot(np.log10(i3MidMass2),i3Likelihood2,marker = 's', markeredgecolor = 'none', markersize = 8, color = 'r', linestyle = '--')
pl.ylabel(r'Probability',fontsize = 20)
pl.xlabel(r'log$_{10}$[$M$(< 100 kpc)/$M_{\odot}$]',fontsize=20)
pl.xlim([11.3, 12.1])

pl.show()