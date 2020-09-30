# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 01:48:57 2020

@author: Taufiq
"""

import xarray as xr
from dask.diagnostics import ProgressBar


class data_resample(object):
    
    def __init__(self,fname,**kwargs):
        self.fname = fname
        self.season = kwargs.get('season', None)
        self._var = kwargs.get('var', None)
        self.nc = kwargs.get('nc', 'yes')
        self.freq = kwargs.get('freq', 'annual')
        self.modMean = kwargs.get('modMean', None)
        self.modStd = kwargs.get('modStd', None)
        self.monClim = kwargs.get('monClim', None)
        self.monAnom = kwargs.get('monAnom', None)
        self.modAnom = kwargs.get('modAnom', None)
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)
        self.out = kwargs.get('out', None)
        
    def _tmean(self):
        SeaMon = {'DJF':[12,1,2],'MAM':[3,4,5],'JJA':[6,7,8],'SON':[9,10,11]}
        if type(self.fname) is str:
            if self._var == None:
                var = self.fname.split('/')[-1].split('_')[0]
            else:
                var = self._var
            data = xr.open_mfdataset(self.fname)[var]
        else:
            data = self.fname
        if self.freq == 'monthly':
            data = data.resample(time="1MS").mean(dim='time')
        elif self.freq == 'daily':
            data = data.resample(time="1D").mean(dim='time')
        elif self.season != None:
            data_sea = data.where((data['time.month'] == SeaMon[self.season][0]) | \
                                  (data['time.month'] == SeaMon[self.season][1]) | \
                                  (data['time.month'] == SeaMon[self.season][2]))
            data_sea = data_sea.rolling(min_periods=3, center=True, time=3).mean()
            data = data_sea.groupby('time.year').mean('time')
            data = data.rename({'year':'time'})
        else:
            try:
                data = data.resample(time="1AS").mean(dim='time')
            except:
                data = data.groupby('time.year').mean('time')
                data = data.rename({'year':'time'})
        if self.nc == 'yes':
            with ProgressBar():
                if self.out !=None:
                    data.load().to_netcdf(self.out)
                else:
                    try:
                        data.load().to_netcdf(self.fname.split('.nc')[0]+'_'+self.season+'.nc')
                    except:
                        data.load().to_netcdf(self.fname.split('.nc')[0]+'_'+self.freq+'.nc')
        else:
            return data
        
    def _mod_mean(self):
        if type(self.fname) is str:
            if self._var == None:
                var = self.fname.split('/')[-1].split('_')[0]
            else:
                var = self._var
            data = xr.open_mfdataset(self.fname)[var]
        else:
            data = self.fname
        if self.modMean != None:
            ds=data.mean(dim='ens')
            name_string = 'modMean'
        elif self.modStd != None:
            ds=data.std(dim='ens')
            name_string = 'modStd'
        elif self.monClim != None:
            ds=data.groupby('time.month').mean('time')
            name_string = 'monClim'
        elif self.monAnom != None:
            climatology=data.groupby('time.month').mean('time')
            ds = data.groupby('time.month') - climatology
            name_string = 'monAnom'
        elif self.modAnom != None:
            name_string = 'modAnom'
            if self.init!= None or self.end!=None:
                sub=data.sel(time=slice(str(self.init),str(self.end))).mean(dim='time')
                ds = data - sub
            else:
                ds = data - data.mean(dim='time')
        if self.nc == 'yes':
            with ProgressBar():
                if self.out !=None:
                    data.load().to_netcdf(self.out)
                else:
                    ds.load().to_netcdf(self.fname.split('.nc')[0]+'_'+name_string+'.nc')
        else:
            return ds


## mean, std, climatology, anomaly, agreement, trendmap, correlation map
