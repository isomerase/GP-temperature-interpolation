# -*- coding: utf-8 -*-
"""
3D_data_processor

lines 48-85 of main code

Created on Fri Feb 13 14:24:19 2015
@author: Richard Decal, decal@uw.edu
"""

import fetch_3D_temp_data

mydir, T_raw, zpos, pos_data = fetch_3D_temp_data.main()

#TODO: average these repeated points, instead of deleting them with lim
lim = 199      #limit of points used (to remove repeat positions or unwanted positions)

#Make array of observed locations (x,y)
xy_observed = np.zeros((2,lim),dtype = float)
observed_data = np.zeros((3,lim), dtype = float)

#temperatures_time_avg = pos_data['s']      #time averaged temperature data
xy_observed[0,:] = pos_data['p_mm'][:lim,0]          #x (crosswind) axis, observed data
xy_observed[1,:] = pos_data['p_mm'][:lim,1] #Richard: is this the y axis?

#for 3d interpolation:
xyz_observed = np.zeros((3,len(xy_observed.T)),dtype = float)       #observed locations
xyz_observed[:2,:] = xy_observed
xyz_observed[2,:] = zpos[3]*np.ones((1,lim))
T_time_avg_3d = np.mean(T_raw[:lim,0,:],1)      #preallocate observed measurements variable
T_sd = np.std(T_raw[:lim,0,:],1)    #preallocate sd variable

for i in range(1,4):
    T_slice = np.mean(T_raw[:lim,i,:], 1)      #single height layer of temperature   
    T_slice_sd = np.std(T_raw[:lim,i,:],1)
    layer = len(xy_observed.T)      
    xy_slice = np.append(xy_observed,(np.ones((1,layer))*zpos[3-i]),axis = 0)     #single height layer of position data
    xyz_observed = np.append(xyz_observed, xy_slice, axis = 1)      #3d positions
    T_time_avg_3d = np.append(T_time_avg_3d, T_slice, axis = 1)       #resized tempearture data
    T_sd = np.append(T_sd,T_slice_sd,axis = 1)

#look for and remove nans () 
if np.any(np.isnan(T_time_avg_3d)):
    NaN_locations = np.where(np.isnan(T_time_avg_3d))      #find the indices of Nans
    T_time_avg_3d = np.delete(T_time_avg_3d, NaN_locations)
    xyz_observed = np.delete(xyz_observed, NaN_locations, axis = 1)
    T_sd = np.delete(T_sd, NaN_locations)

#fit all of the observed data into one array, for ease of use of fitting function
observed_data_3d = np.zeros((4,len(xyz_observed.T)), dtype = float)
observed_data_3d[:3,:] = xyz_observed
observed_data_3d[3,:] = T_time_avg_3d.T
