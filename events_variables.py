# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 18:44:01 2015

@author: Marina
"""

"""
This function takes the values of the 3 txt files (attention/synchronizacion:
memory/continuation:response) and the mat file to generate the variables needed
to generate the events """




def events_variables(stim,ntim,re,e,run_number):
    sonsets = stim[:,0]  #gets the events of 
    sduration = stim[:,1]   #soffset = sonsets + sduration
    #scorrect = stim[:,2]
    trials = range(len(stim))
    nonsets = ntim[:,0]
    nduration = ntim[:,1]#noffset = nonset + nduration 
    #ncorrect = ntim[:,2]
    ronsets = re[:,0]
    rduration = re[:,1]
    iscontrol = []
    task = []
    sphase = []
    nphase = []
    direction = []
    vis_field = []
    res_angle = []
    sta_angle = []
    for i in range(len(stim)):
        iscontrol.append(e['trial'][()][i][8])
        res_angle.append(e['trial'][()][i][6])
        if iscontrol[i] == 1 :      
            task.append('control')
            sphase.append('attention')
            nphase.append('memory')
        else:
            task.append('rhythm')
            sphase.append('synchronization')
            nphase.append('continuation')
   
        if sum(e['trial'][()][i][3])>365:
            vis_field.append('right')
        else:
            vis_field.append('left')
        
        if e['trial'][()][i][7] == -1:
            direction.append('cw')
        else:
            direction.append('ccw')
 
        if e['trial'][()][i][4] == 0 or 45 or 315:
            sta_angle.append('right')
        else:
            sta_angle.append('left')
            
    return (
        sonsets,
        nonsets,
        ronsets,
        trials,
        sduration,
        nduration,
        rduration,
        task,
        sphase,
        nphase,
        vis_field,
        direction,
        sta_angle,
        res_angle,
        run_number)
    
            
            
