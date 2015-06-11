#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:41:28 2015

@author: Marina
"""

#thise script is to generate a list of dictionaries for the information relate to the events of a event-related design 


from mvpa2.tutorial_suite import *
from events_variables import *
from variables2events import *
#importing everything you need
import numpy as np #for arrays
import scipy.io as sp  #for manipulation of matlab files
import nibabel as nib
import os
import glob 
import sys

verbose.level = 6

sys.argv[1:]

verbose(1, "Generating datasets")
for subject_dir in sys.argv[1:]:
    verbose(2, "Loading subject from %s" % subject_dir)

    def get_subj_files(pattern):
        return sorted(glob.glob((os.path.join(subject_dir, pattern))))
        
    def get_subj_file(pattern):
        return os.path.join(subject_dir, pattern)
    
    matfiles = get_subj_files("*T*.mat")
    assert(len(matfiles) == 4)
    
    #filename = os.path.join(os.getcwd(), subject_dir,"dataset_run%d.gzipped.hdf5" % f)
        
    for run in range(4):
        verbose(3, "Loading run %d" % run)
        f = run+1        
        run_number = run

        filename = os.path.join(os.getcwd(), subject_dir,"dataset_run%d.hdf5" % f)

        #nib.load('/home/brain/Downloads/filtered_func_data.nii.gz')
        #ffd = bold.get_data()
        #mask_at = os.path.join('803','thresh_zstat1.nii.gz')
        #mask_me = os.path.join('803','thresh_zstat2.nii.gz')
        #mask_si = os.path.join('803','thresh_zstat3.nii.gz')
        #mask_co = os.path.join('803','thresh_zstat4.nii.gz')
        
        
        stimulus = get_subj_file("at%d.txt" % f)
        imaginery = get_subj_file("co%d.txt" % f)
        response = get_subj_file("re%d.txt" %f)
        path_mat = matfiles[run]
        ffd = get_subj_file("run%d/filtered_func_data.nii.gz" % f)
        data = nib.load(ffd).get_data()
        len_chunks = data.shape[3]
        del data
        #assert(len(ffd) == 1)
        stim = np.loadtxt(stimulus) #loads text file
        re = np.loadtxt(response)
        ntim = np.loadtxt(imaginery)
        mat = sp.loadmat(path_mat, squeeze_me = True) #load mat file
        e = mat['e']
        variables = events_variables(stim, ntim, re, e, run_number)  #generates the variables to produce the events
        #sphere_gnbsearchlight(GNB(), NFoldPartitioner())
        events = variables2events(*variables)
        verbose(4, "Generating datasets for run %d"  % run )        
        ds = fmri_dataset(ffd, 
                  mask='/usr/share/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz',
                  chunks= np.ones(len_chunks) * run_number,
                  add_fa = {'at': './thresh_zstat1.nii.gz', 'me': './thresh_zstat2.nii.gz', 'si': './thresh_zstat3.nii.gz','co' : './thresh_zstat4.nii.gz'})
                  #add_fa = {'at': mask_at, 'me': mask_me, 'si': mask_si,'co' : mask_co})

        #sub = fmri_dataset('filtered_func_data.nii.gz',add_fa = {'thresh_zstat1.nii.gz', 'thresh_zstat2.nii.gz','thresh_zstat3.nii.gz', 'thresh_zstat4.nii.gz'}, chunks= np.ones(280,))
        verbose(5, "Fitting the hrf model for run%d" % run )
        evds = fit_event_hrf_model(ds, events, time_attr ='time_coords',
                                   condition_attr=['targets', 'trial'])
        del ds
        
        verbose(6, "Saving evds file for run%d" % run)
        h5save(filename, evds,compression=9)