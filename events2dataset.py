#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:41:28 2015

@author: Marina
"""

#thise script is to generate a list of dictionaries for the information relate to the events of a event-related design 


from mvpa2.tutorial_suite import *

#importing everything you need
import numpy as np #for arrays
import scipy.io as sp  #for manipulation of matlab files
#mport nibabel as nib
import os
#import glob as gb

verbose.level = 4

subj = sorted(os.listdir('.'))

verbose(1, "Generating datasets")
for i in range(9):
    verbose(2, "Loading subject %d" % i)
    def get_subj_files(pattern):
        return sorted(glob(os.path.join(subj[i], pattern))
    
    matfiles = get_subj_files("*T*.mat")
    assert(len(matfiles) == 4)
  
    for j in range(4):
        verbose(3, "Loading run %d" % j)
        f = j+1
        run_number = j
        
        #nib.load('/home/brain/Downloads/filtered_func_data.nii.gz')
        #ffd = bold.get_data()
        mask_at = os.path.join('803','thresh_zstat1.nii.gz')
        mask_me = os.path.join('803','thresh_zstat2.nii.gz')
        mask_si = os.path.join('803','thresh_zstat3.nii.gz')
        mask_co = os.path.join('803','thresh_zstat4.nii.gz')
        
        
        stimulus = get_subj_files("at?.txt")
        imaginery = os.path.join(subj[i], matfiles[7 + f])
        response = os.path.join(subj[i], matfiles[11 + f])
        path_mat = os.path.join(subj[i], matfiles[j])
        ffd = os.path.join(subj[i], "run%d" % f, 'filtered_func_data.nii.gz')
        
        stim = np.loadtxt(stimulus) #loads text file
        re = np.loadtxt(response)
        ntim = np.loadtxt(imaginery)
        mat = sp.loadmat(path_mat, squeeze_me = True) #load mat file
        e = mat['e']
        variables = events_variables(stim, ntim, re, e)  #generates the variables to produce the events
        #sphere_gnbsearchlight(GNB(), NFoldPartitioner())
        events = variables2events(*variables)
        verbose(4, "Generating datasets for run %d"  % j )        
        ds = fmri_dataset(ffd, 
                  mask='/usr/share/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz',
                  chunks= np.ones(280) * run_number,
                  add_fa = {'at': mask_at, 'me': mask_me, 'si': mask_si,'co' : mask_co})#, chunks= np.ones(280))

        #sub = fmri_dataset('filtered_func_data.nii.gz',add_fa = {'thresh_zstat1.nii.gz', 'thresh_zstat2.nii.gz','thresh_zstat3.nii.gz', 'thresh_zstat4.nii.gz'}, chunks= np.ones(280,))
        verbose(5, "Fitting the hrf model for run%d" % j )
        evds = fit_event_hrf_model(ds, events, time_attr ='time_coords',
                                   condition_attr=['targets', 'trial'])
        del ds
        
        verbose(6, "Saving evds file for run%d" % j)
        h5save()