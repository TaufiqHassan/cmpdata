import os
import sys
import xesmf as xe
import xarray as xr
import numpy as np
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
