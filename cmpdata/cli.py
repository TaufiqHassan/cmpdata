# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:40:38 2020

@author: Taufiq
"""
import argparse

from cmpdata.c6Data import get_data
from cmpdata.file_system_util import _check_list, _mod_help
from cmpdata.c6Stats import data_resample

import warnings
warnings.filterwarnings("ignore")
       
def main():
    
    parser = argparse.ArgumentParser()
    def myerror(message):
        print(message)

    parser.error=myerror

    parser.add_argument("-o","--output-options", help="Select an output option", choices=['info', 'rm', 'mm','stats'], required=True)
    parser.add_argument("-dir", help="Select directory.", default=None)
    parser.add_argument("-dir2", help="Select directory for the second experiment", default=None)
    parser.add_argument("-m", help="Model names", default=None)
    parser.add_argument("-e", help="Experiment names", default=None)
    parser.add_argument("-v", help="Variable names", default=None)
    parser.add_argument("-r", help="Realization", default=None)
    parser.add_argument("-out", help="Output file name", default=None)
    parser.add_argument('stats',action='append',nargs=2,help=argparse.SUPPRESS,default=None)
    
    parser.add_argument("-init", help="Initial year", default=0)
    parser.add_argument("-end", help="Ending year", default=-1)
    parser.add_argument("-e2", help="Secondary experiment name", default=None)
    parser.add_argument("-t", help="Temporal mean option", action='store_true', default=None)
    parser.add_argument("-s", help="Seasonal mean option", choices=['DJF', 'MAM', 'SON', 'JJA'], default=None)
    parser.add_argument("-f", help="Temporal mean frequency", choices=['annual','daily','monthly'],default='annual')
    parser.add_argument("-rm", help="Use the realization means", default=None)
    parser.add_argument("-curve", help="Regridding to curvilinear grids", action='store_true', default=None)
    parser.add_argument("-w", help="Get all model means a single file (used for certain statistical analysis later)", action='store_true', default=None)
    parser.add_argument("-ci", help="confidence interval used in stats", default=0.95)
    
    args = parser.parse_args()
    search_dir = args.dir
    d2 = args.dir2
    model = _check_list(args.m)
    variable = _check_list(args.v)
    experiment = _check_list(args.e)
    exp2 = args.e2
    realization = args.r
    init = args.init
    end = args.end
    freq = args.f
    season = args.s
    tmean = args.t
    rm = args.rm
    curve = args.curve
    w = args.w
    out = args.out
    astat = args.stats
    ci = args.ci
    
    output = args.output_options
        
    if output == 'info':
        get_data(dir_path=search_dir,model=model,variable=variable,\
                 experiment=experiment,realization=realization,rm=rm).get_info()
    elif output == 'rm':
        data = get_data(dir_path=search_dir,\
                 init=init,end=end,\
                 exp2=exp2,dir_path2=d2,\
                 freq=freq,season=season,tmean=tmean)
        if (model != None):
            data.extMod=model
        if (variable != None):
            data.extVar=variable
        if (experiment != None):
            data.extExp=experiment
        data.get_rm()
    elif output == 'mm':
        data = get_data(dir_path=search_dir,variable=variable,experiment=experiment,\
                 init=init,end=end,\
                 freq=freq,season=season,tmean=tmean,rm=rm,curve=curve,whole=w,out=out)
        if (model != None):
            data.extMod=model
        data.get_mm()
    elif output == 'stats':
        try:
            print('\nSelected stat option:',astat[0][1])
            if astat[0][1] == 'modMean':
                data_resample(fname=astat[0][0],var=variable,out=out,modMean = 'modMean')._mod_mean()
            if astat[0][1] == 'zonMean':
                data_resample(fname=astat[0][0],var=variable,out=out,zonMean = 'zonMean')._mod_mean()
            if astat[0][1] == 'modStd':
                data_resample(fname=astat[0][0],var=variable,out=out,modStd = 'modStd')._mod_mean()
            if astat[0][1] == 'monClim':
                data_resample(fname=astat[0][0],var=variable,out=out,monClim = 'monClim')._mod_mean()
            if astat[0][1] == 'monAnom':
                data_resample(fname=astat[0][0],var=variable,out=out,monAnom = 'monAnom')._mod_mean()
            if astat[0][1] == 'modAnom':
                data_resample(fname=astat[0][0],var=variable,out=out,modAnom = 'modAnom',init=init,end=end)._mod_mean()
            if astat[0][1] == 'tANN':
                data_resample(fname=astat[0][0],var=variable,out=out)._tmean()
            if astat[0][1] == 'tDJF':
                data_resample(fname=astat[0][0],var=variable,out=out,season='DJF')._tmean()
            if astat[0][1] == 'tMAM':
                data_resample(fname=astat[0][0],var=variable,out=out,season='MAM')._tmean()
            if astat[0][1] == 'tJJA':
                data_resample(fname=astat[0][0],var=variable,out=out,season='JJA')._tmean()
            if astat[0][1] == 'tSON':
                data_resample(fname=astat[0][0],var=variable,out=out,season='SON')._tmean()
            if astat[0][1] == 'tmon':
                data_resample(fname=astat[0][0],var=variable,out=out,freq='monthly')._tmean()
            if astat[0][1] == 'tday':
                data_resample(fname=astat[0][0],var=variable,out=out,freq='daily')._tmean()
            if astat[0][1] == 'trend':
                data_resample(fname=astat[0][0],var=variable,trend='trend',out=out,init=init,end=end,ci=ci)._mod_mean()
            if astat[0][1] == 'modAggr':
                print('\nThis may take some time . . .')
                data_resample(fname=astat[0][0],var=variable,aggr='aggr',out=out,init=init,end=end,ci=ci)._mod_mean()
        except:
            _mod_help()
    


