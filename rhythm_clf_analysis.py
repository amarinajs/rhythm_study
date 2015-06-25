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
import glob 
import sys
import numpy as np
import pylab



verbose.level = 6

sys.argv[1:]

verbose(1, "Loading  h5 files")
for subject_dir in sys.argv[1:]:

        filename = os.path.join(os.getcwd(), subject_dir, "dataset_%s.hdf5" % subject_dir)
        
        data = h5load(filename)
        verbose(2, "Creating dataset for response ")
        fingers  = data[:, data.fa.si>0]
        response = fingers[fingers.targets == 'response']
        res_cor = response[response.sa.field_response_visual != 'none']
        evds = dataset_wizard(res_cor.samples,targets=res_cor.sa.field_response_visual, chunks=res_cor.sa.chunks)
        verbose(3, "Creating classifier")
        clf = kNN(k=1,
                  dfx=one_minus_correlation,
                  voting='majority')
        verbose(3, "Starting Balancer")
        Bal = Balancer(amount='equal', attr='targets', limit='chunks',apply_selection=True)
        evds = Bal(evds)
        verbose(4, "Starting Crossvalidation with kNN")
        cvte = CrossValidation(clf,
                             NFoldPartitioner(),
                             errorfx = lambda p,
                             t: np.mean(p == t),
                             #postproc=mean_sample(),
                             enable_ca = ['stats'])
        cv_results = cvte(evds)
        verbose(5, "Printing Cross Validation results")
        print cvte.ca.stats
        verbose(3, "Creating classifier")
        clf = LinearCSVMC()
        verbose(4, "Starting Crossvalidation with LinearCSVMC")
        cvte = CrossValidation(clf,
                             NFoldPartitioner(),
                             errorfx = lambda p,
                             t: np.mean(p == t),
                             #postproc=mean_sample(),
                             enable_ca = ['stats'])
        cv_results = cvte(evds)
        verbose(5, "Printing Cross Validation results")
        print cvte.ca.stats

        #sl = Searchlight(cvte,
        #         IndexQueryEngine(voxel_indices=Sphere(1),
        #                          event_offsetidx=Sphere(2)),
        #         postproc=mean_sample())
        #res = sl(evds)
        #verbose(6, "Printing Searchlight results")
        #print res
        #print cvte.ca.stats.matrix
        #cvte.ca.stats.plot(labels = ['left', 'right'])
        #pylab.show()
        #cvte = CrossValidation(GNB(), NFoldPartitioner(),
            #                   postproc=mean_sample())