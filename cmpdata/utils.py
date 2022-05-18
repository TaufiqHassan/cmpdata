import os
import sys
import xesmf as xe
import xarray as xr
import numpy as np
import pandas as pd
import math
from dask.diagnostics import ProgressBar

class color:
   PURPLE = '\033[35m'
   CYAN = '\033[36m'
   BLUE = '\033[34m'
   LBLUE='\033[94m'
   GREEN = '\033[32m'
   LGREEN='\033[92m'
   YELLOW = '\033[33m'
   RED = '\033[31m'
   LRED='\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
   
class HidePrint:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._stdout

def _check_list(item):
    try:
        if (type(item.replace("'",'').strip('[]').split(','))==list):
            lm = str(item).replace("'",'').strip('[]').split(',')
            lm_nospace = [x.strip() for x in lm]
            item = str(lm_nospace).replace("'",'').strip('[]')
    except:
        pass
    return item

def _regrid(dr, ds_in=None,_var=None,regrid='rect'):
    if ds_in == None:
        try:
            ds_in = dr.rename({'longitude':'lon','latitude':'lat'})
        except:
            try:
                ds_in=dr.rename({'nav_lon':'lon','nav_lat':'lat'})
            except:
                ds_in = dr
    else:
        try:
            ds_in = ds_in.rename({'longitude':'lon','latitude':'lat'})
        except:
            try:
                ds_in=ds_in.rename({'nav_lon':'lon','nav_lat':'lat'})
            except:
                ds_in = ds_in
    if regrid!='rect':
        ds_out=xe.util.grid_global(1, 1)
    else:
        ds_out=xr.Dataset({'lat': (['lat'], np.arange(-89.5, 90.0, 1.0)),\
                               'lon': (['lon'], np.arange(0, 360, 1.0)),})
    try:
        regridder = xe.Regridder(ds_in, ds_out, 'bilinear',periodic=True, \
                                 reuse_weights=True)
    except:
        regridder = xe.Regridder(ds_in, ds_out, 'bilinear',periodic=True, \
                                 reuse_weights=True,ignore_degenerate=True)
    ds = regridder(dr)
    return ds

class concat_data(object):
    
    def __init__(self,fname1,fname2,**kwargs):
        self.fname1 = fname1
        self.fname2 = fname2
        self._var = kwargs.get('var', None)
        self.nc = kwargs.get('nc', 'yes')
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)
        self.out = kwargs.get('out', None)

    def _cExp(self):
        if type(self.fname1) is str:
            if self._var == None:
                var = self.fname1.split('/')[-1].split('_')[0]
            else:
                var = self._var
            data1 = xr.open_mfdataset(self.fname1)[var]
            data2 = xr.open_mfdataset(self.fname2)[var]
        else:
            data1 = self.fname1
            data2 = self.fname2
        data = xr.concat([data1,data2],dim='time')
        print('\nConcat shape:', data.shape)
        if self.nc == 'yes':
            with ProgressBar():
                if self.out !=None:
                    data.load().to_netcdf(self.out)
                else:
                    if (self.init != None) or (self.end != None):
                        data.load().to_netcdf(('_').join(self.fname1.split('/')[-1].split('_')[:4])+'_'+str(self.init)+'-'+str(self.end)+'_combined.nc')
                    else:
                        data.load().to_netcdf(('_').join(self.fname1.split('/')[-1].split('_')[:4])+'_combined.nc')
        else:
            return data  

class aave(object):
    
    def __init__(self, val, lat_i=-90, lat_e=90, lon_i=-180, lon_e=180):
        self.val = val
        self.lat_i = lat_i
        self.lat_e = lat_e
        self.lon_i = lon_i
        self.lon_e = lon_e

    def get_lat_lon(self):
        lat = self.val.lat.values
        self.val.coords['lon']=(self.val.coords['lon'] + 180) % 360 - 180
        sorted_val = self.val.sortby(self.val.lon)
        lon = sorted_val.lon.values
        
        late=list(lat).index(lat[lat<=self.lat_e][len(lat[lat<=self.lat_e])-1])
        lati=list(lat).index(lat[lat>=self.lat_i][0])
        lone=list(lon).index(lon[lon<=self.lon_e][len(lon[lon<=self.lon_e])-1])
        loni=list(lon).index(lon[lon>=self.lon_i][0])
        new_val = sorted_val[lati:late+1,loni:lone+1]
        return new_val


    def get_weight(self):
        
        lat=self.get_lat_lon().lat.values
        lon=self.get_lat_lon().lon.values
        
        jlat = lat.shape[0]
        rad = 4.0*math.atan(1.0)/180.0
        re = 6371220.0
        rr = re*rad
        dlon = abs(lon[2]-lon[1])*rr
        dx = dlon*np.cos(lat*rad)
        dy = np.zeros(jlat)
        dy[0] = abs(lat[2]-lat[1])*rr
        dy[1:jlat-1] = abs(lat[2:jlat]-lat[0:jlat-2])*rr*0.5 
        dy[jlat-1] = abs(lat[jlat-1]-lat[jlat-2])*rr
        
        multi = dx*dy
        area=xr.DataArray(multi)
        area=area.rename({'dim_0':'lat'})
        return area

    @staticmethod
    def average_da(var, dim=None, weights=None):
        if weights is None:
            return var.mean(dim)
        else:
            if not isinstance(weights, xr.DataArray):
                raise ValueError("weights must be a DataArray")
    
            if var.notnull().any():
                total_weights = weights.where(var.notnull()).sum(dim=dim)
            else:
                total_weights = weights.sum(dim)
    
            return (var * weights).sum(dim) / total_weights
    
    def spatial_avg(self):
        new_val = self.get_lat_lon()
        lon_avg = new_val.mean(dim='lon')
        area = self.get_weight()
        avg = self.average_da(lon_avg, dim='lat',weights=area)
        return avg.values

def get_area(val,area):
    if area=='global':
        out=aave(val).spatial_avg()
    if area=='tropic':
        out=aave(val,lat_i=-30,lat_e=30).spatial_avg()
    if area=='NH':
        out=aave(val,lat_i=0).spatial_avg()
    if area=='SH':
        out=aave(val,lat_e=0).spatial_avg()
    if area=='NA':
        out=aave(val,lat_i=0,lat_e=65,lon_i=-60,lon_e=-10).spatial_avg()
    if area=='EU':
        out=aave(val,lat_i=30,lat_e=45,lon_i=0,lon_e=30).spatial_avg()
    if area=='NH-mid':
        out=aave(val,lat_i=30,lat_e=60).spatial_avg()
    if area=='SPG':
        out=aave(val,lat_i=45,lat_e=65,lon_i=-60,lon_e=-10).spatial_avg()
    if area=='azores':
        out=aave(val,lat_i=25,lat_e=35,lon_i=-35,lon_e=5).spatial_avg()
    if area=='icelandic':
        out=aave(val,lat_i=50,lat_e=60,lon_i=-35,lon_e=5).spatial_avg()
    return out    

def get_rm_ts(path,models,variables,experiments,region='global',area_file=None):
    for exp in experiments:
        for var in variables:
            all_models=[]
            av_models=[]
            area_files=[]
            for model in models:
                print('\nFor variable / model / experiment: ', var,'/',model,'/',exp)
                try:
                    if area_file!=None:
                        area=xr.open_mfdataset(path+'/areacell*'+model+'*'+exp+'*.nc')['areacella']
                        area_files.append(area)
                    data=xr.open_mfdataset(path+'/'+var+'_rm_'+model+'_'+exp+'_RM_*.nc')[var]
                    all_models.append(data)
                    av_models.append(model)
                    print(model)
                except:
                    pass
            n=0
            mdata=pd.DataFrame()
            mdata_actual=pd.DataFrame()
            print('\nCalculating Spatial averages . . .')
            for avg in all_models:
                try:
                    avg=avg.rename_dims({'longitude':'lon','latitude':'lat'})
                except:
                    pass
                
                ts=[]
                if area_file!=None:
                    ts=(avg*area_files[n]).sum(['lat','lon'])/area_files[n].sum(['lat','lon'])
                else:
                    for i in range(len(avg.time)):
                        ts.append(get_area(avg[i,:,:],region))
                mdata_actual[av_models[n]]=pd.Series(ts)
                ser=(mdata_actual[av_models[n]]-mdata_actual[av_models[n]].mean())
                mdata[av_models[n]]=ser
                mdata.to_csv(path+'/'+var+'_'+exp+'_AllModels_'+region+'.csv', index=False)
                mdata_actual.to_csv(path+'/'+var+'_'+exp+'_AllModels_actual_'+region+'.csv', index=False)
                n=n+1
