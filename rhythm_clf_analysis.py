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



verbose.level = 6

sys.argv[1:]

verbose(1, "Loading  h5 files")
for subject_dir in sys.argv[1:]:
    
      
    
    
    for run in np.arange(1,5):
        
        filename = os.path.join(os.getcwd(), subject_dir,"dataset_run%d.hdf5" % run)
        
        loaded = h5load(filename)
        clf = kNN(k=1, dfx=one_minus_correlation, voting='majority')
        cv = CrossValidation(clf, NFoldPartitioner(attr='targets'))
        cv_glm = cv(evds)
        print '%.2f' % np.mean(cv_glm)