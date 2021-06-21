import os
import numpy
import pandas
import xarray
import calendar, datetime
from configparser import ConfigParser
from datetime import datetime, timedelta

config_object = ConfigParser()
config_object.read('namelist.pre')
variables = config_object['VAR']
folder = config_object['DIR']
path   = folder['dir_model']

parametros = ['167.128', '168.128', '165.128', '166.128']
nombres    = ['TEM', 'DEW', 'U', 'V']

def last_day_of_month(d: datetime.date) -> datetime.date:
    return (d.replace(day=calendar.monthrange(d.year, d.month)[1]))

def arreglar(inicial,final):
    fecha_vacio = []
    fecha_str   = str(inicial)[0:10] + str('/to/') + str(final)[0:10]
    fecha_vacio = numpy.append(fecha_vacio,fecha_str) ; numpy.append(fecha_vacio,fecha_str)
    return(fecha_vacio)
    

def descargar(fecha, nombre,parametro):
    #!/usr/bin/env python
    from ecmwfapi import ECMWFDataServer
    server = ECMWFDataServer()
    server.retrieve({
        'dataset': 'cams_nrealtime',
        'class': 'mc',
        'type': 'an',
        'stream': 'oper',
        'expver': '0001',
        'repres': 'sh',
        'date': fecha,
        'levtype': 'sfc',
        'param': parametro,
        'step': '0',
        'domain': 'g',
        'resol':'auto',
        'time': '00:00:00/06:00:00/12:00:00/18:00:00',
        'area':'6.5/-75/3.5/-72.5',
        'grib':'0.4/0.4',
        'format':'netcdf',
        'target': nombre,
    })


fecha_hoy     = datetime.strptime(variables['fecha_hoy'], '%Y-%m-%d')
fecha_inicial = fecha_hoy + timedelta(days = -5 -14)
fecha_final   = fecha_hoy + timedelta(days = -5)

for i in numpy.arange(0,len(parametros),1):
    if str(fecha_final)[5:7] == str(fecha_inicial)[5:7]:
        print('Descargando datos para un mes')
        inicial = fecha_inicial.replace(day=1)
        final   = fecha_final
        fecha_descargar = arreglar(inicial,final)
        descargar(fecha = fecha_descargar[0], nombre = path + '/DATA/' + nombres[i] + '_1.nc',
            parametro = parametros[i])
        
    if str(fecha_final)[5:7] != str(fecha_inicial)[5:7]:
        print('Descargando datos para dos meses')
        inicial_1 = fecha_inicial.replace(day=1)
        final_1   = last_day_of_month(fecha_inicial)
        fecha_descargar = arreglar(inicial_1,final_1)
        descargar(fecha = fecha_descargar[0], nombre = path + '/DATA/' + nombres[i] + '_1.nc',
            parametro = parametros[i])
        
        inicial_2  = fecha_final.replace(day=1)
        final_2    = fecha_final
        fecha_descargar = arreglar(inicial_2,final_2)
        descargar(fecha = fecha_descargar[0], nombre = path + '/DATA/' + nombres[i] + '_2.nc',
            parametro = parametros[i])
        

    if os.path.exists(path + '/DATA/' + nombres[i] + '_cun.nc'):
        os.remove(path + '/DATA/' + nombres[i] + '_cun.nc')

    aaa = xarray.open_mfdataset(path + '/DATA/'+ nombres[i] + '*')

    if nombres[i] == 'TEM':
        aaa = aaa - 273.15
        aaa.attrs.update(aaa.attrs)
        aaa.t2m.attrs['description'] = '2 metre temperature'
        aaa.t2m.attrs['units'] = '°C'

    if nombres[i] == 'DEW':
        aaa = aaa - 273.15
        aaa.attrs.update(aaa.attrs)
        aaa.d2m.attrs['description'] = '2 metre dewpoint temperature'
        aaa.d2m.attrs['units'] = '°C'


    aaa.to_netcdf( path + '/DATA/' + nombres[i] + '_cun.nc')