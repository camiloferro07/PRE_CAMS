import os
import numpy as np
import xarray as xr
from configparser import ConfigParser

config_object = ConfigParser()
config_object.read('namelist.pre')
folder = config_object['DIR']
variables = config_object['VAR']
path   = folder['dir_model']

U_PRE    = xr.open_dataset(path + '/SALIDAS/' + 'prediccion_u10.nc')
U_PRE    = U_PRE.u10
    
V_PRE    = xr.open_dataset(path + '/SALIDAS/' + 'prediccion_v10.nc')
V_PRE    = V_PRE.v10
    

DIR_PRE  = np.degrees(np.arctan2(V_PRE,U_PRE))
DIR_CARDINAL = 90 - DIR_PRE

DIR_CARDINAL.attrs.update(DIR_CARDINAL.attrs)
DIR_CARDINAL.attrs['description'] = 'Wind direction'
DIR_CARDINAL.attrs['units'] = 'degrees'


if os.path.exists(path + '/SALIDAS/' + 'prediccion_dir.nc'):
    os.remove(path + '/SALIDAS/' + 'prediccion_dir.nc')

DIR_CARDINAL.to_netcdf(path + '/SALIDAS/' + 'prediccion_dir.nc')