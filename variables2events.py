# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 19:07:59 2015

@author: Marina
"""

import numpy as np


def variables2events(sonsets, nonsets, ronsets, trials, sduration, nduration,
                     rduration, task, sphase, nphase, vis_field, direction, sta_angle,
                     res_angle, run_number, res_field, final_angle,stim_anlge):
    response_events = []
    events = []
    for ensayos in trials:
        hand_response = np.isfinite(ronsets[ensayos])
        event_base = {'chunks': run_number,
                      'trial': ensayos,
                      'task': task[ensayos],
                      'direction': direction[ensayos],
                      'start_angle': sta_angle[ensayos]}

        event_sample_intervals = event_base.copy()
        event_sample_intervals.update({'duration': sduration[ensayos],
                                       'onset': sonsets[ensayos],
                                       'targets': sphase[ensayos],
                                       'field_response_visual':vis_field[ensayos],
                                       'final_angle': stim_anlge[ensayos] })
        events.append(event_sample_intervals)

        event_test_intervals = event_base.copy()
        event_test_intervals.update({'duration': nduration[ensayos],
                                     'onset': nonsets[ensayos],
                                     'targets': nphase[ensayos],
                                     'field_response_visual':vis_field[ensayos],
                                     'final_angle': final_angle[ensayos]})
        events.append(event_test_intervals)

        if hand_response:
            event_response_ejecution = event_base.copy()
            event_response_ejecution.update({'duration': rduration[ensayos],
                                             'onset': ronsets[ensayos],
                                             'targets': 'response',
                                             'field_response_visual':res_field[ensayos],
                                             'final_angle': res_angle[ensayos]})
            events.append(event_response_ejecution)



    return events

