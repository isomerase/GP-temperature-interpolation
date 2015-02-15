# -*- coding: utf-8 -*-
"""
This script opens data files and extracts relevant data. 

Note to Sharri: this should work if you put z-positions.mat in your data file and keep hitting enter

Input:
User input filename strings
 
Output:
temperature data
positional data
elevation data

TODO:
(maybe) save data to txt files so we don't have to re-run this code every time?

Created on Fri Feb 13 11:19:31 2015
@author: Richard Decal, decal@uw.edu
"""

import scipy.io as io
import os.path
import numpy as np
import pickle #for saving Python files as pickle binaries

def load_temp_data(mydir):
    print "Loading temperature data"
    print "--------------------------- \n"
    print """Please enter temperature data file name. If none entered, default is %s """ % "lhstore2.mat  \n"
    Temp_data_file = raw_input("Input temperature data file dir: \n")
    if Temp_data_file == '':
        print "EMPTY INPUT! Using lhstore2.mat \n"
        Temp_data_file = os.path.join(mydir, "data", 'lhstore2.mat')
    Temp_data = io.loadmat(Temp_data_file)
    #pull out temp data 
    T_raw = Temp_data['store2'].T
    return T_raw

def load_elevation_data(mydir):
    print "Loading elevation data" , " \n --------------------------- \n"
    print """Please enter elevation data file name. If none entered, default is %s """ % "z-positions.mat  \n"
    
    z_data_file = raw_input("Input elevation data file dir: \n")
    if z_data_file == '':
        print "EMPTY INPUT! Using z-positions.mat \n"
        z_data_file = os.path.join(mydir, "data", 'z-positions.mat')
    z = io.loadmat(z_data_file)
    
    #then pull out elevation data (z)
    zpos = z['y'][0]
    return zpos

def load_positional_data(mydir):
    print "Loading positional data"
    print "--------------------------- \n"
    print """Please enter positional data file name. If none entered, default is %s """ % "final-lh50.mat  \n"
    pos_data_file = raw_input("Input positional data file dir: \n")
    if pos_data_file == '':
        print "EMPTY INPUT! Using final-lh50.mat \n"
        pos_data_file = os.path.join(mydir, 'data', 'final-lh50.mat')
    pos_data = io.loadmat(pos_data_file) #x,y positional data
    return pos_data

def save_obj(obj, name ):
    """
    Pickle files are binary blobs you can use for saving any Python object of any type
    and then be able to load that pickle and it work exactly as expected.
    Using this to replace numpy.savetxt(), which was throwing errors because it wanted to save the NaNs as floats. 
    The pickles are also sweet because I can mindlessly save any variable without worrying if it's a numpy object, or Python dict, or whatever.
    """
    with open('saved_objects/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

#==============================================================================
# lh50_data.keys() ==> ['p_in', 'p_mm', 'p', 's', 'store', '__header__', '__globals__',  '__version__']
# 'p_in' => x,y positions in inches
# 'p_mm' = > x,y positions in mm
# 'p' => x,y positions in grid
# 's' => time averaged temperature
# 'store' => raw temp data
# 'z' => elevation positions
#==============================================================================

def main():
    mydir = os.path.dirname(__file__)
    print "Current directory is: \n", mydir, "\n \n"
    T_raw = load_temp_data(mydir)
    save_obj(T_raw, "T_raw")
    zpos = load_elevation_data(mydir)
    save_obj(zpos, "zpos")
    pos_data = load_positional_data(mydir)
    save_obj(pos_data, "pos_data")
    return mydir, T_raw, zpos, pos_data

    
if __name__ == "__main__":
    mydir, T_raw, zpos, pos_data = main()