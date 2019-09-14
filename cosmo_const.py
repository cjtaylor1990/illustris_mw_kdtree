#Cosmo Constants for Illustris
import numpy as np
omega_b = 0.0456
omega_lam = 0.7274
omega_m = 0.2726

h_little = 0.704

grav_const = 4.301*(10.**-9.) #km^2MpcMsun^-1s^-2 (taken from https://www.cfa.harvard.edu/~dfabricant/huchra/ay145/constants.html

rho_crit = (3.*((h_little*100.)**2.)/(8.*np.pi*grav_const))*((1./1000.)**3.) #Msun per cubic kpc