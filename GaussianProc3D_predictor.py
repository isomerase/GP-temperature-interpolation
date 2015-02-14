# -*- coding: utf-8 -*-
"""


Ideally, this script should
take (user?) inputs to determine x_predicted, y_predicte, and z_predicted arrays (again, cool with augmenting lines in code, especially this one, which probably won't need to change much in the next 4-5 days I'll be using it).
take inputs from the second script to enter in data (that is, the temperature (T_time_avg_3d) and position (xyz_observed) data that was augmented in the second script).
output the interpolated data. Specifically, T_prediction, y_prediction_MSE, and sigma.

Having at least the GP interpolation as a function


Created on Fri Feb 13 17:31:06 2015
@author: Richard Decal, decal@uw.edu
"""


#prediction locations, make 

x_predict = np.atleast_2d(np.linspace(0, 254, 25))       #2 mm prediction sites
y_predict = np.atleast_2d(np.linspace(100, 850, 15))
z_predict = np.atleast_2d(np.linspace(80, 280, 20))

x1,x2,x3 = np.meshgrid(x_predict, y_predict, z_predict)
xyz_predict = np.vstack([x1.reshape(x1.size), x2.reshape(x2.size), x3.reshape(x3.size)]).T

#calculate noise (required)
nugget =  (T_sd/T_time_avg_3d)**2
nugget = nugget       #deletes repeated measurment locations
  
#TODO: make section into separate function
   
gp = gaussian_process.GaussianProcess(corr = 'absolute_exponential',
                                      theta0 = 1./25, 
                                      thetaL = 1e-1,
                                      thetaU = .3,
                                      normalize = True,
                                      nugget = nugget)
#when height = 1, thetaL = .1, thetaU = .3
#when height = 0, thetaL = 10e-2,thetaU = .3

gp.fit(xyz_observed.T, T_time_avg_3d)
 
#Target value error will come up with that last repeated row. It can't have 
#multiple measurements at the same location. Consider deleting that repeated
#last row of measurements or take a mean or stack the timeseries onto the 
#first measurement, which will effectivly average the values.

T_prediction, y_prediction_MSE = gp.predict(xyz_predict, eval_MSE = True)   #produce predicted y values
sigma = np.sqrt(y_prediction_MSE)   #get SD of fit at each x_predicted location (for confidence interval)

