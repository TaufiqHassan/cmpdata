import xarray as xr
from dask.diagnostics import ProgressBar
from scipy import stats
import numpy as np

from cmpdata.utils import _regrid

def do_ttest(x,ci=0.95):
    rgr= stats.linregress(np.r_[1:len(x)+1],x)
    trnd=rgr.slope
    tsig = (rgr.pvalue<(1 - ci))
    stderr = rgr.stderr
    ci = 1.96*stderr
    return (trnd, tsig, ci )

def trend_calc(var,init,end,ci=0.95):
    var = var.sel(time=slice(str(init),str(end)))
    init = 0
    end = len(var.time)
    tru = np.ma.masked_all(var.shape[1:])
    var=var.values
    for yy in range(tru.shape[0]):
        for xx in range(tru.shape[1]):
            mask = ~np.isnan(var[init:end,yy,xx])
            if np.isnan(var[init:end,yy,xx][:5].mean()) or np.isnan(var[init:end,yy,xx][-5:].mean()):
                m,s,c=do_ttest(var[init:end,yy,xx],ci=ci)
            else:
                m,s,c=do_ttest(var[init:end,yy,xx][mask],ci=ci)
            tru.data[yy,xx]= m
            tru.mask[yy,xx]= s
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

def smean(data):
    month_length = data.time.dt.days_in_month
    weights = (month_length.groupby("time.season") / month_length.groupby("time.season").sum())
    np.testing.assert_allclose(weights.groupby("time.season").sum().values, np.ones(4))
    seasons = (data * weights).groupby("time.season").sum(dim="time")
    return seasons

def amean(data):
    month_length = data.time.dt.days_in_month
    weights = (month_length.groupby("time.year") / month_length.groupby("time.year").sum())
    np.testing.assert_allclose(weights.groupby("time.year").sum().values, np.ones(1))
    seasons = (data * weights).groupby("time.year").sum(dim="time")
    return seasons

class data_resample(object):
    
    def __init__(self,fname,**kwargs):
        self.fname = fname
        self.season = kwargs.get('season', None)
        self._var = kwargs.get('variable', None)
        self.nc = kwargs.get('nc', 'yes')
        self.freq = kwargs.get('freq', 'annual')
        self.tmean = kwargs.get('tmean', None)
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
        self.regrid = kwargs.get('regrid', None)
        
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
            try:
                seaInd = {'DJF':0,'MAM':2,'JJA':1,'SON':3}
                data = smean(data)[seaInd[self.season]]
            except:
                try:
                    data_sea = data.where(data['time.season'] == self.season)
                    data = data_sea.groupby('time.year').mean('time')
                    data = data.rename({'year':'time'})
                except:
                    data_sea = data.where((data['time.month'] == SeaMon[self.season][0]) | \
                                          (data['time.month'] == SeaMon[self.season][1]) | \
                                          (data['time.month'] == SeaMon[self.season][2]))
                    data_sea = data_sea.rolling(min_periods=3, center=True, time=3).mean()
                    data = data_sea.groupby('time.year').mean('time')
                data = data.rename({'year':'time'})
        else:
            try:
                data = amean(data)
            except:
                try:
                    data = data.resample(time="1AS",restore_coord_dims=True).mean(dim='time')
                except:
                    data = data.groupby('time.year').mean('time')
                    data = data.rename({'year':'time'})
        data.name = varbl
        return data,self.freq,self.season
        
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
        if self.tmean!=None:
            dt=self._tmean()
            data = dt[0]
            if self.season!=None:
                name_string = dt[2]
            else:
                name_string = dt[1]
        if self.regrid!=None:
            data=_regrid(data)
        if self.modMean != None:
            ds=data.mean(dim='ens')
            name_string = 'modMean'
        if self.zonMean != None:
            ds=data.mean(dim=data.dims[-1])
            name_string = 'zonMean'
        if self.modStd != None:
            ds=data.std(dim='ens')
            name_string = 'modStd'
        if self.monClim != None:
            ds=data.groupby('time.month').mean('time')
            name_string = 'monClim'
        if self.monAnom != None:
            climatology=data.groupby('time.month').mean('time')
            ds = data.groupby('time.month') - climatology
            name_string = 'monAnom'
        if self.modAnom != None:
            name_string = 'modAnom'
            if self.init!= None or self.end!=None:
                sub=data.sel(time=slice(str(self.init),str(self.end))).mean(dim='time')
                ds = data - sub
            else:
                ds = data - data.mean(dim='time')
        if self.trend != None:
            trend = trend_calc(data,int(self.init),int(self.end),ci=float(self.ci))
            t = xr.DataArray(trend[0],dims=['lat','lon'],coords={'lat':data.lat,'lon':data.lon})
            t.name = 'trend'
            s = xr.DataArray(trend[1],dims=['lat','lon'],coords={'lat':data.lat,'lon':data.lon})
            s.name = 'sig'
            ds = xr.merge([t,s])
            name_string = 'trend'
        if self.aggr != None:
            ds = get_aggr(data,int(self.init),int(self.end),ci=float(self.ci))
            ds.name = 'model_agreement'
            name_string = 'model_agreement'
        if (self.nc == 'yes'):
            with ProgressBar():
                if self.out !=None:
                    try:
                        ds.load().to_netcdf(self.out)
                    except:
                        data.load().to_netcdf(self.out)
                else:
                    try:
                        try:
                            ds.load().to_netcdf(self.fname.split('.nc')[0]+'_'+name_string+'.nc')
                        except:
                            ds.load().to_netcdf(name_string+'.nc')
                    except:
                        try:
                            data.load().to_netcdf(self.fname.split('.nc')[0]+'_'+name_string+'.nc')
                        except:
                            data.load().to_netcdf(name_string+'.nc')
        else:
            try:
                return ds
            except:
                return data
