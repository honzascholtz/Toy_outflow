#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 15:54:34 2021

@author: jansen
"""

#importing modules
import numpy as np
import matplotlib.pyplot as plt; plt.ioff()

from astropy.io import fits as pyfits
from astropy import wcs
from astropy.table import Table, join, vstack
from matplotlib.backends.backend_pdf import PdfPages
import pickle
from scipy.optimize import curve_fit

nan= float('nan')

pi= np.pi
e= np.e

plt.close('all')
c= 3.*10**8
h= 6.62*10**-34
k= 1.38*10**-23

Ken98= (4.5*10**-44)
Conversion2Chabrier=1.7 # Also Madau
Calzetti12= 2.8*10**-44
arrow = u'$\u2193$' 


import Outflow_module as Out
from Outflow_module import Outflow

plt.close('all')

mph = '/Users/jansen/Downloads/test'

model = Outflow(v_launch=400, dispersion=500, PA=150, inclination=45,npixel=64, mypath= mph)
model.graph_format()

model.print_info()

model.Flux, model.Vel = model.create_model_grid()
model.Flux_rot, model.Vel_rot = model.rotation(model.Flux, model.Vel)
model.Plotting_rot(model.Flux, model.Flux_rot)

model.Deconvolved_cube = model.Spectral_matrix(model.Flux_rot, model.Vel_rot)


model.Phys_resize_cube = model.Physical_resize(model.Deconvolved_cube)
model.Convolved_cube = model.Convolution(model.Phys_resize_cube)

model.Convolved_cube_flux = model.Flux_calibration_ALMA(model.Convolved_cube)

#model.Convolved_cube_flux = model.Nosie_addition(model.Convolved_cube_flux,2000)

model.Save_fits(model.Convolved_cube_flux)


model.Fast_analyses(model.Convolved_cube_flux, boundry_up=1000., boundry_do=-1000.)
      


plt.show()



