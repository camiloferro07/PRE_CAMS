#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import xarray as xr
import numpy as np
from configparser import ConfigParser


# In[2]:


config_object = ConfigParser()
config_object.read('namelist.pre')
folder = config_object['DIR']
path   = folder['dir_model']


# In[3]:

TEM_PRE       = xr.open_dataset(path + '/SALIDAS/' + 'prediccion_tem.nc')
TEM_PRE       = TEM_PRE.t2m

POIND_PRE     = xr.open_dataset(path + '/SALIDAS/' + 'prediccion_dew.nc')
POIND_PRE     = POIND_PRE.d2m
        
HUM_PRE       = 100 * (np.exp((17.625 * POIND_PRE)/(243.04 + POIND_PRE))/np.exp((17.625 * TEM_PRE)/(243.04 + TEM_PRE)))

HUM_PRE.attrs.update(HUM_PRE.attrs)
HUM_PRE.attrs['description'] = '2 metre relative humidity'
HUM_PRE.attrs['units'] = '%'

# In[4]:

if os.path.exists(path + '/SALIDAS/' + 'prediccion_hum.nc'):
    os.remove(path + '/SALIDAS/' + 'prediccion_hum.nc')

HUM_PRE.to_netcdf(path + '/SALIDAS/' + 'prediccion_hum.nc')