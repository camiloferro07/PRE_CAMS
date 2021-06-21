#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
import xarray as xr
import numpy as np
from keras.models import load_model
from configparser import ConfigParser
from datetime import datetime, timedelta
from netCDF4 import Dataset,num2date,date2num


# In[2]:


config_object = ConfigParser()
config_object.read('namelist.pre')
folder = config_object['DIR']
variables = config_object['VAR']
path   = folder['dir_model']


# In[3]:


tem = xr.open_dataset(path + '/DATA/V_cun.nc')
model = load_model(path + '/MODELOS/modelo_v10.h5')
model.load_weights(path + '/MODELOS/modelo_v10_pesos.h5')


# In[4]:


tem = tem.v10
div = np.max(tem.values)
tem = tem/div


# In[5]:


x = np.array(tem[-56:,:,:])


# In[6]:


x = np.reshape(x, (1,x.shape[0], x.shape[1],x.shape[2], 1))


# In[7]:


pre_tem = model.predict(x, verbose=0)


# In[8]:


pre_tem  = pre_tem.reshape(1,28,len(tem.latitude),len(tem.longitude)); pre_tem = pre_tem * div
pre_dia  = pre_tem[0,:,:,:]




if os.path.exists(path + '/SALIDAS/' + 'prediccion_v10.nc' ):
    os.remove(path + '/SALIDAS/' + 'prediccion_v10.nc')



nyears = 28;
unout = 'days since ' + str(tem.time[len(tem.time)-1].values)[:19]

nx, ny = (7, 8)
lon = tem.longitude.values
lat = tem.latitude.values
dataout  = pre_dia


fecha_hoy = datetime.strptime(variables['fecha_hoy'], '%Y-%m-%d')
fecha_inicial = fecha_hoy + timedelta(days = -4)
fecha_final = fecha_hoy + timedelta(days = 3)

a = str(fecha_inicial)
b = str(fecha_final)

datesout = np.arange(datetime(int(a[0:4]),int(a[5:7]),int(a[8:10]),0),
                            datetime(int(b[0:4]),int(b[5:7]),int(b[8:10]),0), timedelta(hours=6)).astype(datetime)
datesout = list(datesout + timedelta(hours = -5))

ncout = Dataset(path + '/SALIDAS/' + 'prediccion_v10.nc','w','NETCDF4')
ncout.createDimension('lon',nx)
ncout.createDimension('lat',ny)
ncout.createDimension('time',nyears);
lonvar = ncout.createVariable('lon','float32',('lon'));lonvar[:] = lon;
latvar = ncout.createVariable('lat','float32',('lat'));latvar[:] = lat;
timevar = ncout.createVariable('time','float64',('time'));timevar.setncattr('units',unout);timevar[:]=date2num(datesout,unout);
myvar = ncout.createVariable('v10','float32',('time','lat','lon'));myvar.setncattr('units','m/s');myvar[:] = dataout;
ncout.close();