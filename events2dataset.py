#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 12:41:28 2015

@author: Marina
"""

# thise script is to generate a list of dictionaries for the information relate to the events of a event-related design


from mvpa2.tutorial_suite import *
from events_variables import *
from variables2events import *
from mvpa2.misc.fsl.base import McFlirtParams
import numpy as np  #for arrays
import scipy.io as sp  #for manipulation of matlab files
import nibabel as nib
import os
import glob
import sys


verbose.level = 6


verbose(1, "Generating datasets")
for subject_dir in sys.argv[1:]:
    verbose(2, "Loading subject from %s" % subject_dir)

    def get_subj_files(pattern):
        return sorted(glob.glob((os.path.join(subject_dir, pattern))))

    def get_subj_file(pattern):
        return os.path.join(subject_dir, pattern)

    matfiles = get_subj_files("*T*.mat")
    assert (len(matfiles) == 4)

    all_ds = []
    #filename = os.path.join(os.getcwd(), subject_dir,"dataset_run%d.gzipped.hdf5" % f)

    for run in range(4):
        verbose(3, "Loading run %d" % run)
        f = run + 1
        run_number = run

        filename = os.path.join(os.getcwd(), subject_dir,"dataset_%s.hdf5" % subject_dir)  #,"dataset_run%d.hdf5" % f)

        stimulus = get_subj_file("at%d.txt" % f)
        imaginery = get_subj_file("co%d.txt" % f)
        response = get_subj_file("re%d.txt" % f)
        path_mat = matfiles[run]
        ffd = get_subj_file("run%d/filtered_func_data.nii.gz" % f)
        mc = McFlirtParams(get_subj_file("run%d/prefiltered_func_data_mcf.par" % f))
        data = nib.load(ffd).get_data()
        len_chunks = data.shape[3]
        del data
        #assert(len(ffd) == 1)
        stim = np.loadtxt(stimulus)  #loads text file
        re = np.loadtxt(response)
        ntim = np.loadtxt(imaginery)
        mat = sp.loadmat(path_mat, squeeze_me=True)  #load mat file
        e = mat['e']
        variables = events_variables(stim, ntim, re, e, run_number)  #generates the variables to produce the events
        #sphere_gnbsearchlight(GNB(), NFoldPartitioner())
        events = variables2events(*variables)

        verbose(4, "Generating datasets for run %d" % run)
        ds = fmri_dataset(ffd,
                          mask='/usr/share/fsl/data/standard/MNI152lin_T1_2mm_brain_mask.nii.gz',
                          #mask='./motor_cortex_mask.nii.gz',
                          #mask='./occipital_cortex_mask.nii.gz',
                          chunks=np.ones(len_chunks) * run_number,
                          add_fa={'at': './thresh_zstat1.nii.gz',
                                  'me': './thresh_zstat2.nii.gz',
                                  'si': './thresh_zstat3.nii.gz',
                                  'co': './thresh_zstat4.nii.gz',
                                  'fi': './finger_mask.hdr'})
        TR = 2
        ds.sa['time_coords'] = np.arange(0,len_chunks*TR,TR)

        for param in mc:
            ds.sa['mc_' + param] = mc[param]

        verbose(5, "Detrending")
        poly_detrend(ds, opt_regs=['mc_x', 'mc_y', 'mc_z',
                                   'mc_rot1', 'mc_rot2', 'mc_rot3'])

        verbose(5, "Fitting the hrf model for run%d" % run)
        evds = fit_event_hrf_model(ds, events, time_attr='time_coords',
                                   condition_attr=['targets',
                                                   'chunks',
                                                   'field_response_visual',
                                                   'final_angle',
                                                   'trial',
                                                   'task',
                                                   'direction',
                                                   'start_angle'],
                                   # regr_attrs=['mc_x',
                                   #             'mc_y',
                                   #             'mc_z',
                                   #             'mc_rot1',
                                   #             'mc_rot2',
                                   #             'mc_rot3'],
                                   design_kwargs=dict(drift_model='blank'))
        del ds

        all_ds.append(evds)
        del evds
        del events



        if f == 4:
            verbose(6, "Saving evds files from %s" % subject_dir)
            all_datasets = vstack(all_ds, a=0)
            #zscore(all_datasets)
            h5save(filename, all_datasets, compression=9)
            del all_datasets



