# -*- coding: utf-8 -*-
"""


Ideally, this script should
take (user?) inputs to determine x_predicted, y_predicte, and z_predicted arrays
take inputs from the second script to enter in data (that is, the temperature (T_time_avg_3d) and position (xyz_observed) data that was augmented in the second script).

TODO:
output the interpolated data. Specifically, T_prediction, y_prediction_MSE, and sigma.

Having at least the GP interpolation as a function


Created on Fri Feb 13 17:31:06 2015
@author: Richard Decal, decal@uw.edu
"""
from scipy.optimize import curve_fit
from sklearn import gaussian_process
import numpy as np
import matplotlib.pyplot as plt

import process_3D_data

def predictionLocations():
    """prediction locations, make ##finish your sentences, points deducted -Richard
    
    TODO: document what these magic numbers mean
    Do we want to feed any input into this fxn?"""
    
    x_predict = np.atleast_2d(np.linspace(0, 254, 25))       #2 mm prediction sites
    y_predict = np.atleast_2d(np.linspace(100, 850, 15))
    z_predict = np.atleast_2d(np.linspace(80, 280, 20))
    
    x1,x2,x3 = np.meshgrid(x_predict, y_predict, z_predict)
    xyz_predict = np.vstack([x1.reshape(x1.size), x2.reshape(x2.size), x3.reshape(x3.size)]).T #TODO: what is this line for?
    return xyz_predict

def noiseCalc(temp_stdev, Temp_time_avg_3D):
    nugget =  (temp_stdev/Temp_time_avg_3D)**2
    nugget = nugget       #deletes repeated measurment locations
    return nugget

def gaussianProcess(T_sd, T_time_avg_3d, xyz_observed):
    """
    TODO: feed params for gp (corr, thetas, etc) into the parent fxn?
    """
    xyz_predict = predictionLocations()
    mynugget = noiseCalc(T_sd, T_time_avg_3d)    
    
    gp = gaussian_process.GaussianProcess(corr = 'absolute_exponential',
                                          theta0 = 1./25, 
                                          thetaL = 1e-1,
                                          thetaU = .3,
                                          normalize = True,
                                          nugget = mynugget)
    #when height = 1, thetaL = .1, thetaU = .3
    #when height = 0, thetaL = 10e-2,thetaU = .3
    
    gp.fit(xyz_observed.T, T_time_avg_3d)
     
    #Target value error will come up with that last repeated row. It can't have 
    #multiple measurements at the same location. Consider deleting that repeated
    #last row of measurements or take a mean or stack the timeseries onto the 
    #first measurement, which will effectivly average the values.
    
    T_prediction, y_prediction_MSE = gp.predict(xyz_predict, eval_MSE = True)   #produce predicted y values
    sigma = np.sqrt(y_prediction_MSE)   #get SD of fit at each x_predicted location (for confidence interval)
    return T_prediction, y_prediction_MSE, sigma

def main():
    #load vars from second script
    T_sd, T_time_avg_3d, xyz_observed = process_3D_data.main()
    
    #run Gaussian process
    T_prediction, y_prediction_MSE, sigma = gaussianProcess(T_sd, T_time_avg_3d, xyz_observed)
    return T_prediction, y_prediction_MSE, sigma


if __name__ == "__main__":
    T_prediction, y_prediction_MSE, sigma = main()