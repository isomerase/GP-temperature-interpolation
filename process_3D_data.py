# -*- coding: utf-8 -*-
"""
3D_data_processor

Created on Fri Feb 13 14:24:19 2015
@author: Richard Decal, decal@uw.edu
"""
import pickle
import numpy as np

def load_obj(name ):
    """load Python pickle files"""
    with open('saved_objects/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def load_our_objects():
    """I got sick of re-running the first script, so I saved it's output to pickle files"""
    T_raw =  load_obj('T_raw')
    zpos =  load_obj('zpos')
    pos_data =  load_obj('pos_data')
    return T_raw, zpos, pos_data

#TODO: average these repeated points, instead of deleting them with lim
lim = 199      #limit of points used (to remove repeat positions or unwanted positions)

def main():
    """doing this so that we can call this file as a module. Would be way more ideal if this entire page
    was broken up into unit functions and made Pythonic"""
    T_raw, zpos, pos_data = load_our_objects() #load all our variables from the first script
    
    #Make array of observed locations (x,y)
    xy_observed = np.zeros((2,lim), dtype = float)
#    observed_data = np.zeros((3,lim), dtype = float) #commented out because was not being used... vestigial code?
    
    #temperatures_time_avg = pos_data['s']      #time averaged temperature data
    xy_observed[0,:] = pos_data['p_mm'][:lim,0]          #x (crosswind) axis, observed data
    xy_observed[1,:] = pos_data['p_mm'][:lim,1] #Is this the y axis? -Richard
    
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
    #TODO (maybe): turn this into a function
    if np.any(np.isnan(T_time_avg_3d)):
        NaN_locations = np.where(np.isnan(T_time_avg_3d))      #find the indices of Nans
        T_time_avg_3d = np.delete(T_time_avg_3d, NaN_locations)
        xyz_observed = np.delete(xyz_observed, NaN_locations, axis = 1)
        T_sd = np.delete(T_sd, NaN_locations)
    
    #fit all of the observed data into one array, for ease of use of fitting function
    observed_data_3d = np.zeros((4,len(xyz_observed.T)), dtype = float)
    observed_data_3d[:3,:] = xyz_observed
    observed_data_3d[3,:] = T_time_avg_3d.T
    
    #send off our variables to the GP script
    return T_sd, T_time_avg_3d, xyz_observed


if __name__ == "__main__":
    main()