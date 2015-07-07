#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 15:22:35 2015

@author: Marina
"""

"""
Script to make the classification analysis """

from mvpa2.tutorial_suite import *
import os
import sys
import numpy as np



verbose.level = 5

verbose(1, "Loading  h5 files")
print "Loading  h5 files"
for subject_dir in sys.argv[1:]:

        former, sys.stdout = sys.stdout, open(os.path.join(os.getcwd(), subject_dir, 'log.txt'), 'w')

        filename = os.path.join(os.getcwd(), subject_dir, "dataset_%s.hdf5" % subject_dir)
        
        data = h5load(filename)
        verbose(2, "Creating dataset for response ")
        print "Creating dataset for response "
        fingers  = data[:, data.fa.fi>0]
        response = fingers[fingers.targets == 'response']
        res_cor = response[response.sa.field_response_visual != 'none']
        res_cor.targets = res_cor.sa.field_response_visual
        #evds = dataset_wizard(res_cor.samples,targets=res_cor.sa.field_response_visual, chunks=res_cor.sa.chunks)
        evds = res_cor
        print evds.summary()
        verbose(3, "Starting Balancer")
        print "Starting Balancer"
        Bal = Balancer(amount='equal', attr='targets', limit='chunks', apply_selection=True)
        evds = Bal(evds)
        print evds.summary()
        verbose(3, "Creating classifier")
        print "Creating classifier"
        clf = LinearCSVMC()
        verbose(4, "Starting Crossvalidation with LinearCSVMC")
        print "Starting Crossvalidation with LinearCSVMC"
        cvte = CrossValidation(clf,
                             NFoldPartitioner(),
                             errorfx = lambda p,
                             t: np.mean(p == t),
                             #postproc=mean_sample(),
                             enable_ca = ['stats'])
        cv_results = cvte(evds)
        verbose(4, "Starting SearchLight")
        print "Starting SearchLight"
        sl = sphere_searchlight(cvte, radius=3, postproc=mean_sample())
        sl_results = sl(evds)
        verbose(5, "Printing Cross Validation amd SearchLight results")
        print "Printing Cross Validation amd SearchLight results"
        print cvte.ca.stats
        print 'Best performing sphere error:', np.min(sl_results.samples)
        map2nifti(evds, sl_results).to_filename(os.path.join(os.getcwd(), subject_dir, "fingers_sl_motor.gz"))
        verbose(1, "saving log file")
        print "saving log file"
        results, sys.stdout = sys.stdout, former
        results.close()


