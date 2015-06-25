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
    res_field = []
    final_angle = []
    stim_angle = []
    for i in range(len(stim)):
        iscontrol.append(e['trial'][()][i][8])
        stim_angle.append(e['trial'][()][0][3][2])
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
            #if all(e['trial'][()][i][3] == [180,45,315]) or all(e['trial'][()][i][3] == [45,315,180]) or all(e['trial'][()][i][3] == [315,180,45]):
            if list(e['trial'][()][i][3]) in [[180, 45, 315], [45, 315, 180], [315, 180, 45]]:
                direction.append('cw')
            elif list(e['trial'][()][i][3]) in [[180, 315, 45], [315, 45, 180], [45, 180, 315]]: #[180, 45, 315], [45, 315, 180], [315, 180, 45]]:
                direction.append('ccw')
            else:
                direction.append('none')
        else:
            vis_field.append('left')
            if list(e['trial'][()][i][3]) in [[225, 135, 0], [135, 0, 225], [0, 225, 135]]:
                direction.append('cw')
            elif list(e['trial'][()][i][3]) in [[225, 0, 135], [135, 225, 0], [0, 135, 225]]:
                direction.append('ccw')
            else:
                direction.append('none')

        if e['trial'][()][i][4] in [0, 45, 315]:
            sta_angle.append('right')
        elif e['trial'][()][i][4] in [180, 225, 135]:
            sta_angle.append('left')
        else:
            sta_angle.append('none')

        if e['trial'][()][i][6] in [0, 45, 315]:
            res_field.append('right')
        elif e['trial'][()][i][6] in [225, 180, 135]:
            res_field.append('left')
        elif e['trial'][()][2][6] == 'NaN':
            res_field.append('none')
        else:
            res_field.append('none')

        if e['trial'][()][i][6] == 0:
            res_angle.append('0')
        elif e['trial'][()][i][6] == 45:
            res_angle.append('45')
        elif e['trial'][()][i][6] == 315:
            res_angle.append('315')
        elif e['trial'][()][i][6] == 135:
            res_angle.append('135')
        elif e['trial'][()][i][6] == 225:
            res_angle.append('225')
        elif e['trial'][()][i][6] == 180:
            res_angle.append('180')
        else:
            res_angle.append('none')

        if e['trial'][()][i][5] == 0:
            final_angle.append('0')
        elif e['trial'][()][i][5] == 45:
            final_angle.append('45')
        elif e['trial'][()][i][5] == 315:
            final_angle.append('315')
        elif e['trial'][()][i][5] == 135:
            final_angle.append('135')
        elif e['trial'][()][i][5] == 225:
            final_angle.append('225')
        elif e['trial'][()][i][5] == 180:
            final_angle.append('180')
        else:
            final_angle.append('none')



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
        run_number,
        res_field,
        final_angle,
        stim_angle)
    
            

