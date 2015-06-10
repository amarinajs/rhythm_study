# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:07:59 2015

@author: Marina
"""

import numpy as np

def variables2events(sonsets,nonsets,ronsets,trials,sduration,nduration,
                     rduration,task,sphase,nphase,vis_field,direction,sta_angle):
 events = []
 for ensayos in trials: 
     had_response = np.isfinite(ronsets[ensayos])
     event_base = {'chunks': run_number,
                   'trial': ensayos,
                   'task': task[ensayos],
                   'direction': direction[ensayos],
                   'vis_field': vis_field[ensayos],
                   'res_angle': res_angle[ensayos],
                   'sta_angle': sta_angle[ensayos],
                   'had_response': had_response }

     event_1 = event_base.copy()
     event_1.update({'duration': sduration[ensayos],
     'onset': sonsets[ensayos],
     'targets': sphase[ensayos]})
     events.append(event_1)

     event_2 = event_base.copy()
     event_2.update({'duration': nduration[ensayos],
     'onset': nonsets[ensayos],
     'targets': nphase[ensayos]})
     events.append(event_2)

     if had_response:
         event_3 = event_base.copy()
         event_3.update({'duration': rduration[ensayos],
         'onset': ronsets[ensayos],
         'targets': 'response'})
         events.append(event_3)  
         
         
 return events       