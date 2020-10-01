# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 14:29:56 2020

@author: Taufiq
"""
import os
import pandas as pd
import sys
import xarray as xr
from dask.diagnostics import ProgressBar
from pathlib import Path
import xesmf as xe
import numpy as np

from cmpdata.c6Stats import data_resample

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

class search_dir(object):
    
    def __init__(self, **kwargs):
        self.dir_path = kwargs.get('dir_path', None)
        self._var = kwargs.get('variable', None)
        self._mod = kwargs.get('model', None)
        self._exp = kwargs.get('experiment', None)
        self._rlzn = kwargs.get('realization', None)
        self._rm = kwargs.get('rm', None)
    
    def get_data(self):
        if self.dir_path == None:
            p=Path('.')
            print('\nLooking through current directory:', p.absolute())
            self.dir_path = p.absolute()
        else:
            self.dir_path = Path(self.dir_path)
        files = os.listdir(self.dir_path)
        m=[]
        v=[]
        e=[]
        r=[]
        dpath=[]
        unknown=[]
        for file in files:
            if '_MM_' not in file:
                try:
                    if len(file.split('_'))>4:
                        m.append(file.split('_')[2])
                        v.append(file.split('_')[0])
                        e.append(file.split('_')[3])
                        r.append(file.split('_')[4])
                        dpath.append(self.dir_path / file)
                except:
                    unknown.append(file) 
        data=pd.DataFrame()
        data['variable_id']=v
        data['experiment_id']=e
        data['source_id']=m
        data['realization']=r
        data['data']=dpath
        if self._rm != None:
            data = data[data['realization'] == 'RM']
        else:
            data = data[data['realization'] != 'RM']
        var = data['variable_id'].unique()
        exp = data['experiment_id'].unique()
        rlzn = data['realization'].unique()
        mod = data['source_id'].unique()    
        print(color.LGREEN+'\nAvailable',len(var), 'variables:'+color.END,var)
        print(color.LGREEN+'\nAvailable',len(mod),'models:'+color.END,mod)
        print(color.LGREEN+'\nAvailable',len(exp),'experiments:'+color.END,exp)
        print(color.LGREEN+'\nAvailable', len(rlzn),'realizations:'+color.END,rlzn)
        print(color.LGREEN+'\nTotal number of files:'+color.END,len(data),'\n\n')
        if (len(unknown)!=0):
            print('\nUnknown file formats: ',unknown)
        
        return data
    
    def specific_data(self):
        with HidePrint():
            data = self.get_data()
        ld = []
        if self._var != None:
            v = "variable_id=='"+self._var+"'"
            ld.append(v)
        if self._mod != None:
            m = "source_id=='"+self._mod+"'"
            ld.append(m)
        if self._exp != None:
            e = "experiment_id=='"+self._exp+"'"
            ld.append(e)
        if self._rlzn != None:
            r = "realization=='"+self._rlzn+"'"
            ld.append(r)
        if len(ld)!=0:
            data_string = (' & ').join(ld)
            data = data.query(data_string)
            var = data['variable_id'].unique()
            exp = data['experiment_id'].unique()
            rlzn = data['realization'].unique()
            mod = data['source_id'].unique()    
            print(color.LGREEN+'\nAvailable',len(var), 'variables:'+color.END,var)
            print(color.LGREEN+'\nAvailable',len(mod),'models:'+color.END,mod)
            print(color.LGREEN+'\nAvailable',len(exp),'experiments:'+color.END,exp)
            print(color.LGREEN+'\nAvailable', len(rlzn),'realizations:'+color.END,rlzn)
            print(color.LGREEN+'\nTotal number of files:'+color.END,len(data),'\n\n')
        else:
            print('\n<<Showing all available data>>\n')
            self.get_data()
        return data

def _get_rm(df,mod,var,exp,init=None,end=None,nc=None,tmean=None,freq='annual',season=None,exdf2=pd.DataFrame()):
    if not exdf2.empty:
        rlzn1 = df['realization'][df.source_id == mod].unique()
        rlzn2 = exdf2['realization'][exdf2.source_id == mod].unique()
        rlzn = list(set(rlzn1) & set(rlzn2))
    else:
        rlzn = df['realization'][df.source_id == mod].unique()
    print('\nAvailable realizations:', rlzn)
    ds_r=[0]*len(rlzn)
    m=0
    for r in rlzn:
        try:
            print('\ncalculating for: ', r)
            uri = df[(df.source_id == mod) & (df.realization == r)]['data'].values
            if (init != None) or (end != None):
                ds_rr = xr.open_mfdataset(uri, combine='by_coords')[var].sel(time=slice(str(init),str(end)))
            else:
                ds_rr = xr.open_mfdataset(uri, combine='by_coords')[var]
            ds_r[m] = ds_rr
            print('\nData shape:',ds_r[m].shape)
            m=m+1
        except:
            print('\nFound issue on',r,'realization of',mod)
            print('\nIgnoring',r)
            continue
    ds_all = xr.concat(ds_r,dim='ens')
    ds=ds_all.mean(dim='ens')
    if tmean != None:
        ds = data_resample(ds,var=var,freq=freq,season=season,nc=None)._tmean()
    print('\nEnsemble data shape:',ds.shape)
    ds.name = var
    if nc != None:
        with ProgressBar():
            if (init != None) or (end != None):
                ds.load().to_netcdf(var+'_rm_'+mod+'_'+exp+'_RM_'+str(init)+'-'+str(end)+'.nc')
            else:
                ds.load().to_netcdf(var+'_rm_'+mod+'_'+exp+'_RM_.nc')
    return ds

def _rect_regrid(dr):
    try:
        ds_in = dr.rename({'longitude':'lon','latitude':'lat'})
    except:
        try:
            ds_in=dr.rename({'nav_lon':'lon','nav_lat':'lat'})
        except:
            ds_in = dr
    ds_out=xr.Dataset({'lat': (['lat'], np.arange(-89.5, 90.0, 1.0)),\
                           'lon': (['lon'], np.arange(0, 360, 1.0)),})
    regridder = xe.Regridder(ds_in, ds_out, 'bilinear')
    ds = regridder(dr)
    regridder.clean_weight_file()
    return ds

def _curv_regrid(dr):
    try:
        ds_in = dr.rename({'longitude':'lon','latitude':'lat'})
    except:
        try:
            ds_in=dr.rename({'nav_lon':'lon','nav_lat':'lat'})
        except:
            ds_in = dr
    ds_out=xe.util.grid_global(1, 1)
    regridder = xe.Regridder(ds_in, ds_out, 'bilinear')
    ds = regridder(dr)
    regridder.clean_weight_file()
    return ds


class concat_data(object):
    
    def __init__(self,fname1,fname2,**kwargs):
        self.fname1 = fname1
        self.fname2 = fname2
        self._var = kwargs.get('var', None)
        self.nc = kwargs.get('nc', 'yes')
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)

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
        if self.nc == 'yes':
            with ProgressBar():
                if (self.init != None) or (self.end != None):
                    data.load().to_netcdf(('_').join(self.fname1.split('/')[-1].split('_')[:4])+'_'+str(self.init)+'-'+str(self.end)+'_combined.nc')
                else:
                    data.load().to_netcdf(('_').join(self.fname1.split('/')[-1].split('_')[:4])+'_combined.nc')
        else:
            return data  


class get_means(object):
    
    def __init__(self, **kwargs):
        self.dir_path = kwargs.get('dir_path', None)
        self._var = kwargs.get('variable', None)
        self._mod = kwargs.get('model', None)
        self._exp = kwargs.get('experiment', None)
        self.to_nc = kwargs.get('nc', None)
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)
        self.extMod = kwargs.get('extMod', None)
        self.extExp = kwargs.get('extExp', None)
        self.extVar = kwargs.get('extVar', None)
        self.curve = kwargs.get('curve', None)
        self._rm = kwargs.get('rm', None)
        self.freq = kwargs.get('freq', 'annual')
        self.season = kwargs.get('season', None)
        self.tmean = kwargs.get('tmean', None)
        self.exp2 = kwargs.get('exp2', None)
        self.dir_path2 = kwargs.get('dir_path2', None)
        self.whole = kwargs.get('whole', None)
        self.out = kwargs.get('out', None)

    def real_mean(self):
        with HidePrint(): 
            df = search_dir(dir_path=self.dir_path, variable=self._var, \
                model=self._mod, experiment=self._exp).specific_data()
            if self.exp2 != None:
                if self.dir_path2 == None:
                    self.dir_path2 = self.dir_path
                df2 = search_dir(dir_path=self.dir_path2, variable=self._var, \
                                 model=self._mod, experiment=self.exp2).specific_data()
                if df2.empty:
                    print('\nNo experiment',self.exp2,'found in',self.dir_path2)
                    raise SystemExit
        if self.extVar!=None:
            var = self.extVar
        else:
            var = df['variable_id'].unique()
        if self.extExp!=None:
            exp = self.extExp
        else:
            exp = df['experiment_id'].unique()
        if self.extMod!=None:
            mod = self.extMod
        else:
            mod = df['source_id'].unique()

        ds = []
        for v in var:
            print('\nFor variable: ', v)
            for m in mod:
                print('\nFor model: ', m)
                if self.exp2 != None:
                    ds1 = _get_rm(df,var=v,mod=m,exp=exp[0],\
                       init=self.init,end=self.end,nc=None,\
                       freq=self.freq,season=self.season,tmean=self.tmean,exdf2=df2)

                    ds2 = _get_rm(df2,var=v,mod=m,exp=self.exp2,\
                       init=self.init,end=self.end,nc=None,\
                       freq=self.freq,season=self.season,tmean=self.tmean,exdf2=df)
                    ds1 = concat_data(ds1,ds2,nc='no')._cExp()
                else:
                    for e in exp:
                        print('\nFor experiment: ', e)
                        ds1 = _get_rm(df,var=v,mod=m,exp=e,\
                           init=self.init,end=self.end,nc=self.to_nc,\
                           freq=self.freq,season=self.season,tmean=self.tmean)

                ds.append(ds1)
        return ds
    
    def model_mean(self):
        with HidePrint(): 
            df = search_dir(dir_path=self.dir_path, variable=self._var, \
                model=self._mod, experiment=self._exp, rm=self._rm).specific_data()
        var = df['variable_id'].unique()[0]
        exp = df['experiment_id'].unique()[0]
        if self.extMod!=None:
            mod = self.extMod
        else:
            mod = df['source_id'].unique()

        ds_m = []
        for m in mod:
            print('\nFor model: ', m)
            dr = _get_rm(df,var=var,mod=m,exp=exp,\
                   init=self.init,end=self.end,freq=self.freq,\
                   season=self.season,tmean=self.tmean)
            if self.curve != None:
                ds_m.append(_curv_regrid(dr))
            else:
                ds_m.append(_rect_regrid(dr))
        time = ds_m[0]['time'].values
        for zz in range(len(ds_m)):
            ds_m[zz]['time'] = time
        ds = xr.concat(ds_m,dim='ens')
        ds_mean=ds.mean(dim='ens')
        print('\nEnsemble data shape:',ds_mean.shape)
        ds_mean.name = var
        if self.to_nc != None:
            with ProgressBar():
                if self.out !=None:
                    ds_mean.load().to_netcdf(self.out)
                else:
                    if (self.init != None) or (self.end != None):
                        if self.whole!=None:
                            ds.load().to_netcdf(var+'_ens_ModMean_'+exp+'_MM_'+str(self.init)+'-'+str(self.end)+'.nc')
                        else:
                            ds_mean.load().to_netcdf(var+'_mm_ModMean_'+exp+'_MM_'+str(self.init)+'-'+str(self.end)+'.nc')
                    else:
                        if self.whole!=None:
                            ds.load().to_netcdf(var+'_ens_ModMean_'+exp+'_MM_.nc')
                        else:
                            ds_mean.load().to_netcdf(var+'_mm_ModMean_'+exp+'_MM_.nc')
        return ds_mean

def _mod_help():
    print("\n"+color.PURPLE+"                <<You are using the STATS module now>>"+color.END+'\n')
    print(color.BOLD+color.UNDERLINE+"Usage:"+color.END+" cmpdata -o stats <input> <optional output> <optional args>\n")
    print(color.UNDERLINE+"stat options:"+color.END)
    print("\nmonClim = monthly climatology \
          \nmonAnom = monthly anomalies \
          \nmodAnom = model anomalies \
          \nzonMean = zonal mean \
          \nmodMean = ensemble model mean, where different models are saved under the 'ens' dimention.\
          \nmodStd = standard deviation within the models, where different models are saved under the 'ens' dimention.\
          \ntANN/tDJF/tMAM/tSON/tJJA = resample to yearly/seasonal mean data \
          \ntmon/tday = resample to monthly or daily mean data\
          \ntrend = calculate spatial grid by grid trends \
          \nmodAggr = estimate model aggreement on the sign of the signal, where different models are saved under the 'ens' dimention. \
          \n")    
