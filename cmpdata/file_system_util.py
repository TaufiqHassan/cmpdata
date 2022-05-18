import os
import pandas as pd
import xarray as xr
from dask.diagnostics import ProgressBar
from pathlib import Path

from cmpdata.c6Stats import data_resample
from cmpdata.utils import color, HidePrint, _regrid, get_rm_ts

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
        m,v,e,r=[],[],[],[]
        dpath=[]
        unknown=[]
        for file in files:
            if ('_MM_' not in file) and ('.nc' in file):
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
            v = "variable_id=="+str(self._var)
            ld.append(v)
        if self._mod != None:
            m = "source_id=="+str(self._mod)
            ld.append(m)
        if self._exp != None:
            e = "experiment_id=="+str(self._exp)
            ld.append(e)
        if self._rlzn != None:
            r = "realization=="+str(self._rlzn)
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

def _get_rm(df,mod,var,exp,realization=None,init=None,end=None,nc=None,\
            tmean=None,freq='annual',season=None,curve=None,regrid=None):
    
    if realization==None:
        rlzn = df['realization'][df.variable_id==var][df.experiment_id==exp][df.source_id==mod].unique()
    else:
        rlzn=realization
    print('\nAvailable realizations:', rlzn)
    ds_r=[0]*len(rlzn)
    m=0
    for r in rlzn:
        try:
            print('\ncalculating for: ', r)
            uri = df[(df.source_id == mod) & (df.realization == r) & (df.experiment_id == exp) & (df.variable_id == var)]['data'].values
            print(uri)
            if (init != None) or (end != None):
                ds_rr = xr.open_mfdataset(uri, combine='by_coords').sel(time=slice(str(init),str(end)))
            else:
                ds_rr = xr.open_mfdataset(uri, combine='by_coords')
            ds_r[m] = ds_rr[var]
            print('\nData shape:',ds_r[m].shape)
            m=m+1
        except:
            print('\nFound issue on',r,'realization of',mod)
            print('\nIgnoring',r)
            continue
    ds = sum(ds_r)/m
    if tmean != None:
        print('\nGetting tmean')
        ds = data_resample(ds,var=var,freq=freq,season=season,nc=None,tmean='yes')._mod_mean()
        print('new shape:',ds.shape)
    if regrid!= None:
        if curve == None:
            ds = _regrid(ds, ds_in=ds_rr)
        else:
            ds = _regrid(ds, ds_in=ds_rr, regrid='curv')
    print('\nEnsemble data shape:',ds.shape)
    ds.name = var
    if nc != None:
        with ProgressBar():
            if (init != None) or (end != None):
                ds.load().to_netcdf(var+'_rm_'+mod+'_'+exp+'_RM_'+str(init)+'-'+str(end)+'.nc')
            else:
                ds.load().to_netcdf(var+'_rm_'+mod+'_'+exp+'_RM_.nc')
    return ds

class get_means(object):
    
    def __init__(self, **kwargs):
        self.dir_path = kwargs.get('dir_path', None)
        self._var = kwargs.get('variable', None)
        self._mod = kwargs.get('model', None)
        self._exp = kwargs.get('experiment', None)
        self._rlzn = kwargs.get('realization', None)        
        self.to_nc = kwargs.get('nc', None)
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)
        self.curve = kwargs.get('curve', None)
        self._rm = kwargs.get('rm', None)
        self.freq = kwargs.get('freq', 'annual')
        self.season = kwargs.get('season', None)
        self.tmean = kwargs.get('tmean', None)
        self.whole = kwargs.get('whole', None)
        self.out = kwargs.get('out', None)
        self.regrid = kwargs.get('regrid', None)
        self.region = kwargs.get('region', 'global')
        self.area_file = kwargs.get('area_file', None)

    def time_ser(self):
        with HidePrint(): 
            df = search_dir(dir_path=self.dir_path, variable=self._var, \
                model=self._mod, experiment=self._exp, realization=self._rlzn).specific_data()
        exp = df['experiment_id'].unique()
        var = df['variable_id'].unique()
        mod = df['source_id'].unique()
        get_rm_ts(self.dir_path,mod,var,exp,region=self.region,\
                  area_file=self.area_file)


    def real_mean(self):
        with HidePrint(): 
            df = search_dir(dir_path=self.dir_path, variable=self._var, \
                model=self._mod, experiment=self._exp, realization=self._rlzn).specific_data()
        ds = []
        var = df['variable_id'].unique()
        exp = df['experiment_id'].unique()
        mod = df['source_id'].unique()
        for v in var:
            for m in mod:
                for e in exp:
                    print('\nFor variable / model / experiment: ', v,'/',m,'/',e)
                    ds1 = _get_rm(df,var=v,mod=m,exp=e,\
                       init=self.init,end=self.end,nc=self.to_nc,\
                       freq=self.freq,season=self.season,tmean=self.tmean, \
                       regrid=self.regrid,curve=self.curve,realization=self._rlzn)

                    ds.append(ds1)
        return ds
    
    def model_mean(self):
        with HidePrint(): 
            df = search_dir(dir_path=self.dir_path, variable=self._var, \
                model=self._mod, experiment=self._exp, rm=self._rm, \
                realization=self._rlzn).specific_data()
        ds_m = []
        var = df['variable_id'].unique()
        exp = df['experiment_id'].unique()
        mod = df['source_id'].unique()
        for e in exp:
            for v in var:
                for m in mod:
                    print('\nFor variable / model / experiment: ', v,'/',m,'/',e)
                    dr = _get_rm(df,var=v,mod=m,exp=e,\
                       init=self.init,end=self.end,nc=self.to_nc,\
                       freq=self.freq,season=self.season,tmean=self.tmean, \
                       regrid=self.regrid,curve=self.curve,realization=self._rlzn)
                    if self.regrid == None:
                        if self.curve == None:
                            ds_m.append(_regrid(dr))
                        else:
                            ds_m.append(_regrid(dr,regrid='curv'))
                    else:
                        ds_m.append(dr)
                    time = ds_m[0]['time'].values
                    for zz in range(len(ds_m)):
                        ds_m[zz]['time'] = time
                ds = xr.concat(ds_m,dim='ens')
                ds_mean=ds.mean(dim='ens')
                print('\nEnsemble data shape:',ds_mean.shape)
                ds_mean.name = v
                if self.to_nc != None:
                    with ProgressBar():
                        if self.out !=None:
                            if self.whole!=None:
                                ds.load().to_netcdf(self.out)
                            else:
                                ds_mean.load().to_netcdf(self.out)
                        else:
                            if (self.init != None) or (self.end != None):
                                if self.whole!=None:
                                    ds.load().to_netcdf(v+'_ens_ModMean_'+e+'_MM_'+str(self.init)+'-'+str(self.end)+'.nc')
                                else:
                                    ds_mean.load().to_netcdf(v+'_mm_ModMean_'+e+'_MM_'+str(self.init)+'-'+str(self.end)+'.nc')
                            else:
                                if self.whole!=None:
                                    ds.load().to_netcdf(v+'_ens_ModMean_'+e+'_MM_.nc')
                                else:
                                    ds_mean.load().to_netcdf(v+'_mm_ModMean_'+e+'_MM_.nc')
        return ds_mean
