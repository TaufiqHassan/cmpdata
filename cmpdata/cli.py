# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 14:40:38 2020

@author: Taufiq
"""
import argparse

from cmpdata.c6Data import get_data
from cmpdata.file_system_util import _check_list

import warnings
warnings.filterwarnings("ignore")
        
def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-o","--output-options", help="Select an output option", choices=['info', 'rm', 'mm'], required=True)
    parser.add_argument("-dir", help="Download directory.", default=None)
    parser.add_argument("-dir2", help="Download directory for the 2nd experiment", default=None)
    parser.add_argument("-m", help="Model names", default=None)
    parser.add_argument("-e", help="Experiment names", default=None)
    parser.add_argument("-v", help="Variable names", default=None)
    parser.add_argument("-r", help="Realization", default=None)
    
    parser.add_argument("-init", help="Initial year", default=None)
    parser.add_argument("-end", help="Ending year", default=None)
    parser.add_argument("-e2", help="Secondary experiment name", default=None)
    parser.add_argument("-t", help="Temporal mean option", default=None)
    parser.add_argument("-s", help="Seasonal mean option", choices=['DJF', 'MAM', 'SON', 'JJA'], default=None)
    parser.add_argument("-f", help="Temporal mean frequency", choices=['annual','daily','monthly'],default='annual')
    parser.add_argument("-rm", help="Use the realization means", default=None)
    parser.add_argument("-curve", help="Regridding to curvilinear grids", default=None)
    
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
    
    out = args.output_options
    
    if out == 'info':
        get_data(dir_path=search_dir,model=model,variable=variable,\
                 experiment=experiment,realization=realization,rm=rm).get_info()
    elif out == 'rm':
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
    elif out == 'mm':
        data = get_data(dir_path=search_dir,variable=variable,experiment=experiment,\
                 init=init,end=end,\
                 freq=freq,season=season,tmean=tmean,rm=rm,curve=curve)
        if (model != None):
            data.extMod=model
        data.get_mm()

    


