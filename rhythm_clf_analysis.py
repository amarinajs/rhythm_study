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



verbose.level = 5

sys.argv[1:]

verbose(1, "Loading  h5 files")
for subject_dir in sys.argv[1:]:

        filename = os.path.join(os.getcwd(), subject_dir, "dataset_%s.hdf5" % subject_dir)
        
        data = h5load(filename)
        verbose(2, "Creating dataset for response ")
        response = data[data.targets == 'response']
        ds = dataset_wizard(response.samples,targets=response.sa.response_hand, chunks=response.sa.chunks)
        verbose(3, "Creating classifier")
        clf = kNN(k=1,
                  dfx=one_minus_correlation,
                  voting='majority')
        verbose(4, "Starting Crossvalidation")
        cvte = CrossValidation(clf,
                             NFoldPartitioner(),
                             errorfx = lambda p,
                             t: np.mean(p == t),
                             enable_ca = ['stats'])
        cv_results = cvte(ds)
        verbose(5, "Printing results")
        print cvte.ca.stats.as_string(description=True)
        print cvte.ca.stats.matrix
        cvte.ca.stats.plot(labels = ['left', 'right'])
        pylab.show()