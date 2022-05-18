#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 14 02:30:18 2020

@author: taufiq
"""
from util_trend import _dir_path, sel_period, sel_models, _get_fig, _get_data, get_area, get_rho
import xarray as xr
import warnings
warnings.simplefilter("ignore")
from CMIP6Data import DataHandler as dh
import CMIPStats as cs
from pathlib import Path
import os
import pandas as pd

### get data
models=['MRI-ESM2-0','ACCESS-CM2', 'ACCESS-ESM1-5', 'BCC-CSM2-MR', 'CAMS-CSM1-0', 'CESM2',
       'CESM2-WACCM', 'CNRM-CM6-1', 'CNRM-ESM2-1', 'CanESM5', 'EC-Earth3-Veg',
       'GFDL-CM4', 'HadGEM3-GC31-LL', 'INM-CM4-8', 'INM-CM5-0', 'IPSL-CM6A-LR',
       'MIROC-ES2L', 'MIROC6', 'MPI-ESM1-2-HR', 'MPI-ESM1-2-LR', 'NESM3',
       'NorESM2-LM', 'NorESM2-MM', 'UKESM1-0-LL','EC-Earth3-AerChem', 'GISS-E2-1-G']
#models=['CESM2', 'CNRM-CM6-1', 'MIROC6', 'HadGEM3-GC31-LL', 
#        'NorESM2-LM', 'BCC-CSM2-MR', 'CanESM5', 'IPSL-CM6A-LR']
models=['EC-Earth3-AerChem', 'GISS-E2-1-G', 'MRI-ESM2-0','UKESM1-0-LL']
#models=['CanESM5', 'GFDL-CM4', 'CNRM-CM6-1', 'IPSL-CM6A-LR', 'HadGEM3-GC31-LL', 'MIROC6','NorESM2-LM']
#models=['MERRA2']
av_models=[]
#path='/Volumes/tCMIP/single_ncs/'
path='/Volumes/HD4/mechanism/SDF/'
csv_path='/Volumes/tCMIP/csv_files/'
#csv_path='/Volumes/HD2/SW/'
#variables=['tos','sos','ssd','sdf-total','sdf-hf','sdf-ff','sssdt','sssds']
#variables=['SW','LW','tos','sos']
variables=['rsds','rsut','rlut','rsdt','rsus','rlds','rlus']
exp='ssp370SST-lowNTCFCH4'
#exp2='ssp370'
seasons=['ANN']
masking=xr.open_dataset(path+'wfo_mm_ModMean_ssp370_MM_2015-2100.nc')['wfo']
mask_file=xr.open_dataset('/Volumes/CMIP6/VO/mask_1x1.nc')
mask=mask_file.REGION_MASK
for var in variables:
    print('\n<<'+var+'>>')
    for sea in seasons:
        print('\nGetting model data for:', sea)
        all_models=[]
        for model in models:
            try:
# mlotst_rm_MRI-ESM2-0_historical_RM_1850-2020.nc
               # all_models.append(xr.open_dataset(path+var+'_rm_'+model+'_'+exp+'_RM_.nc')[var]-xr.open_dataset(path+var+'_rm_'+model+'_'+exp2+'_RM_.nc')[var])
                data=xr.open_mfdataset(path+var+'_rm_'+model+'_'+exp+'_RM_*.nc')[var]
                #data=data.where(masking[0].notnull())
                print(data.shape)
                #data=data.where((mask==6)|(mask==8)|(mask==9)).where(data.lat>0).where(data.lat<61)
                all_models.append(data)
                av_models.append(model)
                print(model)
            except:
                pass
        ## For timeseries
        ts_model=pd.DataFrame()
        test=pd.DataFrame()
        spread=pd.DataFrame()
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
            try:
                for i in range(len(avg.time)):
                    ts.append(get_area(avg[i,:,:],'NA'))
                    #ts.append(get_area(avg[i,:,:],'azores')-get_area(avg[i,:,:],'icelandic'))
            except:
                for i in range(len(avg.time)):
                    ts.append(get_area(avg[i,:,:],'NA'))
                    #ts.append(get_area(avg[i,:,:],'azores')-get_area(avg[i,:,:],'icelandic'))
            ts_model[n]=pd.Series(ts)
            mdata_actual[av_models[n]]=ts_model[n]
            amoc_ser=(ts_model[n]-ts_model[n].mean())
            test[n]=(amoc_ser).rolling(window=10).mean()
            mdata[av_models[n]]=amoc_ser
            spread[n]=amoc_ser
            mdata.to_csv(csv_path+var+'_'+sea+'_'+exp+'_AllModels_NAT.csv', index=False)
            mdata_actual.to_csv(csv_path+var+'_'+sea+'_'+exp+'_AllModels_actual_NAT.csv', index=False)
            n=n+1
        ## get in csv
        data=pd.DataFrame()
        path_deviation=test.T.std()
        eavg=test.T.mean()
        actual_mean=ts_model.T.mean()
        path_deviation_actual=ts_model.T.std()
        year=list(range(1850,1850+len(eavg)))
        data['eavg']=eavg
        data['year']=year
        data['path_deviation']=path_deviation
        data['actual_mean']=actual_mean
        data['path_deviation_actual']=path_deviation_actual
        data.to_csv(csv_path+var+'_'+sea+'_'+exp+'.csv', index=False)
