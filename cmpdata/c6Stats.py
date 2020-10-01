# -*- coding: utf-8 -*-
"""
Created on Sun Aug 30 01:48:57 2020

@author: Taufiq
"""

import xarray as xr
from dask.diagnostics import ProgressBar
from scipy import stats
import numpy as np


def do_ttest(x,ci=0.95):
    rgr= stats.linregress(np.r_[1:len(x)+1],x)
    trnd=rgr.slope
    tsig = (rgr.pvalue<(1 - ci))
    stderr = rgr.stderr
    ci = 1.96*stderr
    return (trnd, tsig, ci )

def trend_calc(var,init,end,ci=0.95):
    tru = np.ma.masked_all(var.shape[1:])
    var=var.values
    for yy in range(tru.shape[0]):
        for xx in range(tru.shape[1]):
            mask = ~np.isnan(var[init:end,yy,xx])
            if np.isnan(var[init:end,yy,xx][:5].mean()) or np.isnan(var[init:end,yy,xx][-5:].mean()):
                m,s,c=do_ttest(var[init:end,yy,xx],ci=ci)
            else:
                m,s,c=do_ttest(var[init:end,yy,xx][mask],ci=ci)
            tru.data[yy,xx]=m
            tru.mask[yy,xx]= ~s
    return tru.data, tru.mask

def get_aggr(var,init,end,ci=0.95):
    tru = np.zeros(var[0].shape[1:])
    for jj in range(len(var)):
        v=trend_calc(var[jj],init,end,ci=ci)[0]
        v = xr.DataArray(v,dims=['lat','lon'],coords={'lat':var[0].lat,'lon':var[0].lon})
        tru=tru+v.where(v<0,1).where(v>0,0)
    tru=tru.where(tru>=(len(var)/2)-1,(len(var)-tru)*(-1))
    tru=(tru/len(var))*100
    return tru    

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
        self.trend = kwargs.get('trend', None)
        self.aggr = kwargs.get('aggr', None)
        self.zonMean = kwargs.get('zonMean', None)
        self.ci = kwargs.get('ci', 0.95)
        
    def _tmean(self):
        SeaMon = {'DJF':[12,1,2],'MAM':[3,4,5],'JJA':[6,7,8],'SON':[9,10,11]}
        if type(self.fname) is str:
            if self._var == None:
                try:
                    varbl = self.fname.split('/')[-1].split('_')[0]
                except:
                    varbl = 'Unknown'
            else:
                varbl = self._var
            data = xr.open_mfdataset(self.fname)[varbl]
        else:
            data = self.fname
            varbl = self._var
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
        data.name = varbl
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
                try:
                    varbl = self.fname.split('/')[-1].split('_')[0]
                except:
                    varbl = 'Unknown'
            else:
                varbl = self._var
            data = xr.open_mfdataset(self.fname)[varbl]
        else:
            data = self.fname
            varbl = self._var
        if self.modMean != None:
            ds=data.mean(dim='ens')
            name_string = 'modMean'
        if self.zonMean != None:
            ds=data.mean(dim=data.dims[-1])
            name_string = 'zonMean'
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
        elif self.trend != None:
            trend = trend_calc(data,int(self.init),int(self.end),ci=float(self.ci))
            t = xr.DataArray(trend[0],dims=['lat','lon'],coords={'lat':data.lat,'lon':data.lon})
            t.name = 'trend'
            s = xr.DataArray(trend[1],dims=['lat','lon'],coords={'lat':data.lat,'lon':data.lon})
            s.name = 'sig'
            ds = xr.merge([t,s])
            name_string = 'trend'
        elif self.aggr != None:
            ds = get_aggr(data,int(self.init),int(self.end),ci=float(self.ci))
            ds.name = 'model_agreement'
            name_string = 'model_agreement'
        if self.nc == 'yes':
            with ProgressBar():
                if self.out !=None:
                    ds.load().to_netcdf(self.out)
                else:
                    try:
                        ds.load().to_netcdf(self.fname.split('.nc')[0]+'_'+name_string+'.nc')
                    except:
                        ds.load().to_netcdf(name_string+'.nc')
        else:
            return ds


## mean, std, climatology, anomaly, agreement, trendmap, correlation map
