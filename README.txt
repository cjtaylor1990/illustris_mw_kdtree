The following is my original README that I wrote for these scripts in 2015. The codes were all written in Python 2.7 and do reference readsnapHDF5.py and readsubfHDF5.py which were codes produced by the Illustris team independently of myself (accessed in 2015). The results of this work were presented in Taylor et al. (2016), MNRAS 461, 3483. (arXiv link: https://arxiv.org/abs/1510.06409).

I will not be hosting the data necessary to run these scripts, nor the Illustris team's scripts, but these can be accessed via http://www.illustris-project.org/data/

------------

This is a how-to document on reproducing the plots and table values from Taylor et al. 2016.  If you have any questions or concerns, feel free to email me at cjtaylor@astro.umd.edu. 

Note that in almost all cases, brackets (i.e. []) represent some variable of input on the command line in this document, and are not actually typed.

1.) KD Tree codes

Names 
kdTree_10-300kpc.py 
kdTree_10-300kpc_dark.py 

Needed files: 
Need a txt file with the paths to all of the particle files, individually listed 
readsnapHDF5.py 
readsubfHDF5.py 
cosmo_const.py 

Running the script 
python [script name] [run] [snap_number] [search_r] [pType] [partFileTxt] 
run = Illustris-1, Illustris-Dark-1, etc 
snap_number = The number of the snap shot (135 for z = 0) 
search_r = Maximal radius that you’re searching at (in this case, 300kpc).  This is really redundant, but I haven’t taken the time to eliminate the variable 
pType = Dark Matter (dm), Stars (star), or Gas (gas) 
partFileTxt = The text file that contains the particle files paths 

Outputs: 
Numpy file called: 
'kdTree_10-300kpc_'+pType+'_'+run+'.npy' 
Inside are arrays for each central sub-halo in e11-13 for M200,c 
The first three indices of arrays are the sub halo numbers, the group numbers, and the sub halo mass (though, this will not be used in analysis.  This is a mass determined by sound binding condition rather than the typical M200,c or anything) 
After that, is M(<r) for r=10-300 kpc  


2.) Getting the masses of the halos (M200,c, M200,m, Mvir, Mstar)

Scripts: 
python get_mcrit200.py 
python get_mcrit200_dark.py 

Running: 
python [script-name] 

Files Needed: 
readsubfHDF5.py 
cosmo_const.py 
kdTree script output for run of interest (see #1) 

Output: 
Numpy array with arrays for each halo 
[groupNum, m_crit200, m_mean200, m_topHat200, m_star] 

Notes: 
m_topHat200 = mvir 
You will have to do this for each Illustris run.  You will have to change the output file name (outFile, line #32) and the data being loaded in (line 16 with variable massInsideData). 
Finally, everything is in units of solar masses. 

3.) Figure 1, Part A - Predicting M(<r)
Scripts 
mass_dist_10-300_weighting_new.py 
mass_dist_10-300_weighting_new_dark.py 

Files Needed 
kdTree output spy files (see 1) 
cosmo_const.py 

Running 
python [script] [weight type] [mass type] 

Weight type = tophat or gauss (we used the latter) 
Mass type = 0,1,2,3 
(0 = Total Mass, 1 = DM, 2 = Gas, 3 = Star) 

Output 
Two numpy files (examples) 
     massdist_deason_e11-13_[mass type]_illustris3.npy 
     veldist.. 
Where the first is the mass distribution and the other are the corresponding velocity curves. 
Note that it will show the curves on the screen, but you can exit and they’ll still save 
Also, note, will have to edit outFile1, outFile2 (lines 158 and 160) depending on constraint (D12 or G14) and simulation name 
Finally, will have to change lines 28-31 for mass constraint at 50 kpc and 48-50 to give the code the kdTree outputs that you are interested in 
out_arrays = [r, median, low68Err, high68Err] 

4.) Figure 1, Part B - Fitting M(<r) with NFW profile
Scripts: 
overplot_massdists.py 

Files needed: 
cosmo_const.py 
mpfit 
Outputs from #3 for Illustris-1,2,3 for particular constraint (e.g. D12) 

Running: 
python overplot_massdists.py 

Output: 
Will plot the two panel plot from the paper’s Figure 1 that you can then save 

Notes: 
Will have to change the variables file1,file2,file3, which are the mass distributions for Illustris-1,2,3 (lines 19-21) 


5.) Figure 2a - Velocity curves from total mass distributions
Script: 
overplot_vcirc.py 

Files Needed: 
cosmo_const.py 
Outputs from #3 for Illustris-1,2,3 for total mass 

Running: 
python overplot_vcirc.py 

Output: 
Will plot out Figure 2a (left panel) that you can then save. 

Notes: 
Need to change file1,file2 variables (lines 11&12) to be the D12 and G14 constraints massdist files (total mass; output from #3) 


6.) Figure 2b - Velocity curves from component mass distributions
Running: 
python overplot_comp_dists.py 

Files needed: 
cosmo_const.py 
Outputs from #3 for Illustris-1,2,3. In particular, the “veldist” files for each component types (dm, gas, star) 

Notes: 
Will have to change file1,2,3 variables (lines 11-13) which are the file paths to the veldist files 

Output: 
Will plot out Figure 2b 

7.) Table 1&2 part 1 - weighing each individual halo by M(<50 kpc)
Script: 
halo_weighing_m50.py 
halo_weighing_m50_dark.py 

Files needed: 
kdTree output files for simulation that you are interested in (see #1) 

Running: 
python [script] [constraint_mass] [constraint_sigma] [constraint_name] 
constraint_mass = mean mass of constraint (peak of gaussian) 
constraint_sigma = standard deviation of constraint 
constraint_name = name of constraint being used (e.g. D12) 

Output: 
saves array with name given by saveFile variable 
array = transpose([haloNum, groupNum, boolArray, totalMassInside50, totalMassInside80, totalMassInside100, totalMassInside250]) 
where boolArray is the weights given to each halo 

Notes: 
May need to change the inFile variables  in order to suit the simulation being weighed 

8.) Table 1, 2, 3 - Getting the confidence intervals (and individual posteriors)
Scripts: 
probdist_mass_new_illustris.py 

Files Needed: 
cosmo_const.py 
Files from #2 and #7 (given by variables on line 12 and 13 

Running 
python [script] [constraint_name] [mass_type] [simulation] 

constraint_name = name of constraint (e.g. D12 or G14) 
mass_type = mass over which the posterior will be made 
sim = simulation name 

Output: 
Will print out confidence intervals in units of 10^10 solar mass for 68% and 90% ranges 
Will plot the posterior over [mass_type] space 
Will save an array named by the variable outFile (line 138) 
array = [mass, likelihood] 

Notes: Will have to do this for all of the simulations and all masses that you would like to get the confidence interval of.  
Mass types are: mcrit200, mmean200, mvir, mstar, m100, and m250 


9.) Figure 3 - Posterior distributions for M(<100kpc)
Script: 
overplot_likelihood_new_m100.py 

Files needed: 
cosmo_const.py 
Illustris-1,2,3 posteriors for m100 for season and gibbons (see #8) 

Running: 
python [script] [constraint_name] [mass_type] [simulation] 

Output: 
Will plot all of the posteriors for M(<100) over-plotted, which then can then be saved. 

Notes: 
May have to change illustris#_file# variables (lines 6-12)  

10.) Figure 4 part 1 - Calculating M200,c from general M(<50 kpc) constraint
Scripts: 
script_m50_mCrit200_auto 
halo_weighing_m50_auto.py 
cumdist_mass_auto.py 

Running: 
./script_m50_mCrit200_auto 

Output: 
This will produce an output .txt file with columns: mean_number, M_crit200 mean, M_crit200 high error bar, M_crit200 low error bar.  Name = script_m50_mCrit200.txt 

The mean_number is used by the script to automatically generate evenly spaced mean constraints on M(<50kpc): 

mwMassMean = 10.**(np.log10(1.5*10.**11.) + (mean_number)*deltaM) 

Note that, in cumdist_mass_auto.py, mean_number is given the name m50Value due to the cannibalized nature of the code (this could obviously be changed) 

Finally, the errors are in the form of mean +upper -lower, and assume a relative standard deviation of 10%. 

Notes: 
You can edit the script script_m50_mCrit200_auto by changing the name to the same thing but .txt as an extension. 

11.) Figure 4 part 2 - Converting .txt to .npy file
Scripts: 
txt_to_npy_auto.py 

Running: 
python txt_to_npy_auto.py [input_name] [output_name] 

input_name = .txt output file from #10 
output_name = name of .npy file  

Output: 
An .npy file with a name given by ‘output_name’ inputted by the user 

[m50, mCrit200, highError, lowError] 


12.) Figure 4 part 3 - Fitting the scatter
Scripts: 
m50_v_mCrit200_scatter.py 

Running: 
python m50_v_mCrit200_scatter.py 

Output: 
Will print out the best fit values of a quadratic fit to the scatter of x = log10(m50/4e11) to y = log10(M200,c): y = Ax^2 + Bx + C 

Example of output 
[  0.32509592   1.6193051   12.04541389] (results using curve_fit) 
[ 0.00630671  0.00424532  0.00108466] (uncertainty from curve_fit) 
[  0.32509593   1.61930511  12.04541389] (results using leastsq) 

Finally, it will plot the fit to the scatter, over plotted over the scatter plot of m50 v. mCrit200 


13.) Figure 4 part 4 - Final plotting of Figure 4 + Median Fit
Script: 
m50_v_mCrit200.py 

Running: 
python m50_v_mCrit200.py [m50_weighting_npy] 

m50_weighting_npy = output from #11 

Output: 
Will plot Figure 4, along with printing out the results from fitting the medians of m50 v. mCrit200 (obtained from #10) 

Example of output: 
[  0.37301615   1.60312584  12.01361125]  (best fit from mpfit) 
[ 0.60983036  0.16185792  0.05504208] (error from mpfit) 

Note: 
Will have to change the values in calculating fitY (line 31) to be whatever the output best-fit parameters from the scatter fit (see #12) 


14.) Figure 5 - NFW fit to Illustris-Dark
Scripts: 
nfw_fit_new.py 

Running: 
python nfw_fit_new.py 

Output: 
Will plot the M(<r) distribution from Illustris-Dark (Illustris-Dark-1 as currently written) 

Note: 
On line 37, there is a line that defines the name of the input data (as given by the output of #3 for Illustris-Dark) that will be loaded in to be fit and plotted 


15.) Figure 6 - Illustris v. Illustris-Dark M(<r) and dM(<r)/dr
Script: 
res_hydro_v_dark_new.py 

Running: 
python res_hydro_v_dark_new.py 

Output: 
Will output a plot of either the left or right panel of Figure 6, depending on if you have line 118 or 119 commented out 

Note: 
Will have to change file paths on lines 8-12 for: 
8: Illustris-Dark output from KD-Tree code (see #1) 
9: Illustris output from KD-Tree code for dark matter particles (see #1) 
10: Illustris output from KD-Tree code for star particles (see #1) 
11: Illustris output from KD-Tree code for gas particles (see #1) 
12: Illustris output from #2 

Also, may have change lines 33-34 as the range of masses you are comparing (in this case, within the 68% interval for the Illustris-1 M200,c result) 

16.) Figure 7 - M50 v. Mstar v. M200,c color scatter plot
Script: 
probdist_illustris1_colorscat.py 

Running: 
python probdist_illustris1_colorscat.py 

Output: 
Will plot out Figure 7, which can be saved using the python GUI 

Notes: 
May want to change line 10 and line 29 for the file paths/names 
10: gives the name of the output of halo weighing (see #7) 
29: loads in the data from the output of #2 (the string in np.load is the file path) 


17.) Figure 8 Part A - Getting M200,c based on M50, M80, M100 with varying relative uncertainty
Scripts: 
script_sigma_auto 

Running 
./script_sigma_auto 

Output 
Will output a .txt file with the relative uncertainty in M50 (or M80, or M100) along with M200,c and upper and lower uncertainty (68%) 

Note: 
Will have to do this for M50, M80, and M100.  Will also have to change the two lines within the loop depending on if you want M50, M50, or M100.  You can do this by adding a .txt extension. 

M50: 
python halo_weighing_m50.py [m50_value] $s 
python cumdist_mass_sigma_new.py mcrit200 halo_weighing_m50_sigma.npy $s >> script_sigma_m50_mcrit200_deason.txt 

M80: 
python halo_weighing_m80.py [m80_value] $s 
python cumdist_mass_sigma_new.py mcrit200 halo_weighing_m80_sigma.npy $s >> script_sigma_m80_mcrit200_deason.txt 

M100: 
python halo_weighing_m100.py [m100_value] $s 
python cumdist_mass_sigma_new.py mcrit200 halo_weighing_m100_sigma.npy $s >> script_sigma_m100_mcrit200_deason.txt 


18.) Figure 8 Part B - Converting the .txt files to .npy files
Scripts: 
txt_to_npy_sigma_auto.py 

Running: 
python txt_to_npy_sigma_auto.py [txt_sigma_file] [outfile] 

txt_sigma_file = output from #17 
outfile = .npy version of txt_sigma_file 

Output: 
Will produce an .npy file that has 
[massUncertainty, mCrit200, highError, lowError]  

Note: 
Will have to do this for M50, M80, and M100 


19.) Figure 8 Part C - Plotting M200,c based on M50, M80, M100 with varying relative uncertainty
Scripts: 
plot_sigma_auto.py 

Running: 
python plot_sigma_auto.py 

Output: 
Will output Figure 8 

Note: May want to change lines 6,7,&8 to match names of your outputs from #18 for m50,m80,m100 

20.) Table 4 - Joint Constraint From M50 & Mstar
Scripts: 
halo_weighing_mstar+m50.py 

Running: 
python halo_weighing_mstar+m50.py [mstar_value] [mstar_sigma] [m50_value] [m50_sigma] [constraint_name] 

mstar/m50_value = constraint on m50/mstar 
…sigma = uncertainty on m50/mstar 
constraint_name = name to label file (usually use constraint name; e.g. D12+LN15) 

Output: 
Will produce .npy files similar to halo_weighing_m50.py, but weighed with both M50 and Mstar preferred values 

Note: 
You can then produce confidence intervals using probdist_mass_new_illustris.py 