#!/usr/bin/env python
# coding: utf-8

# In[7]:

import os
import numpy as np
import xarray as xr
from configparser import ConfigParser
from datetime import datetime, timedelta
from netCDF4 import Dataset,num2date,date2num

config_object = ConfigParser()
config_object.read('namelist.pre')
folder = config_object['DIR']
variables = config_object['VAR']
path   = folder['dir_model']

# In[8]:

u    = xr.open_dataset(path + '/DATA/U_cun.nc') ; u = u.u10 
v    = xr.open_dataset(path + '/DATA/V_cun.nc') ; v = v.v10 


# In[9]:

vel_abs = np.sqrt(u**2 + v**2) 


# In[10]:


a = str(u.time[0].values)
b = str(u.time[len(u.time)-1].values)


# In[13]:


if os.path.exists(path + '/DATA/' + 'VEL_cun.nc' ):
    os.remove(path + '/DATA/' + 'VEL_cun.nc')

nyears = len(vel_abs);
unout = 'days since ' + (a[0:4]) + '-' + (a[5:7]) + '-' + (a[8:10])

nx, ny = (7, 8)
lon = u.longitude.values
lat = u.latitude.values

dataout  = vel_abs

datesout = list(np.arange(datetime(int(a[0:4]),int(a[5:7]),int(a[8:10]),0),
                          datetime(int(b[0:4]),int(b[5:7]),int(b[8:10]),23), timedelta(hours=6)).astype(datetime))

ncout = Dataset(path + '/DATA/' + 'VEL_cun.nc', 'w', 'NETCDF4')
ncout.createDimension('longitude',nx)
ncout.createDimension('latitude',ny)
ncout.createDimension('time',nyears);
lonvar = ncout.createVariable('longitude','float32',('longitude'));lonvar[:] = lon;
latvar = ncout.createVariable('latitude','float32',('latitude'));latvar[:] = lat;
timevar = ncout.createVariable('time','float64',('time'));timevar.setncattr('units',unout);timevar[:]=date2num(datesout,unout);
myvar = ncout.createVariable('vel','float32',('time','latitude','longitude'));myvar.setncattr('units','m/s');myvar[:] = dataout;
ncout.close();