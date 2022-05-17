import argparse

from cmpdata.c6Data import get_data
from cmpdata.utils import _check_list
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
    parser.add_argument("-m", help="Model names", default=None)
    parser.add_argument("-e", help="Experiment names", default=None)
    parser.add_argument("-v", help="Variable names", default=None)
    parser.add_argument("-r", help="Realization", default=None)
    parser.add_argument("-out", help="Output file name", default=None)
    parser.add_argument("-f", help="Input filenames for stats", default=None)    
    parser.add_argument("-init", help="Initial year", default=None)
    parser.add_argument("-end", help="Ending year", default=None)
    parser.add_argument("-t", help="Temporal mean option", action='append_const', default=None, const='yes')
    parser.add_argument("-z", help="Zonal mean option", action='append_const', default=None, const='yes')
    parser.add_argument("-s", help="Seasonal mean option", default=None)
    parser.add_argument("-mm", help="Calculate model ensemble mean", action='store_true', default=None)
    parser.add_argument("-std", help="Calculate model std", action='store_true', default=None)
    parser.add_argument("-clim", help="Calculate monthly climatology", action='store_true', default=None)
    parser.add_argument("-anom", help="Calculate monthly anomaly", action='store_true', default=None)
    parser.add_argument("-manom", help="Calculate model anomaly", action='store_true', default=None)
    parser.add_argument("-trend", help="Calculate variable grid-by-grid trends", action='store_true', default=None)
    parser.add_argument("-aggr", help="Calculate model aggreement", action='store_true', default=None)
    parser.add_argument("-freq", help="Temporal mean frequency", choices=['annual','daily','monthly'] ,default='annual')
    parser.add_argument("-rm", help="Use the realization means", action='store_true', default=None)
    parser.add_argument("-curve", help="Regridding to curvilinear grids", action='store_true', default=None)
    parser.add_argument("-w", help="All model means as ens dim (used by -std, -mm, -aggr stats options)", action='store_true', default=None)
    parser.add_argument("-ci", help="confidence interval used in -trend and -aggr options", default=0.95)
    parser.add_argument("-regrid", help="regridding on/off", action='store_true', default=None)
    
    args = parser.parse_args()
    search_dir = args.dir
    mod = _check_list(args.m)
    var = _check_list(args.v)
    exp = _check_list(args.e)
    realization = args.r
    init = args.init
    end = args.end
    freq = args.freq
    season = args.s
    tmean = args.t
    zmean = args.z
    fname = args.f
    rm = args.rm
    mm = args.mm
    std = args.std
    clim = args.clim
    anom = args.anom
    manom = args.manom
    trend = args.trend
    aggr = args.aggr
    curve = args.curve
    w = args.w
    out = args.out
    ci = args.ci
    regrid = args.regrid
    
    output = args.output_options
        
    if output == 'info':
        data = get_data(dir_path=search_dir,rm=rm)
        if (var != None):
            data.variable=var
        if (mod != None):
            data.model=mod
        if (exp != None):
            data.experiment=exp
        if (realization != None):
            data.realization=realization
        data.get_info()
    elif output == 'rm':
        data = get_data(dir_path=search_dir,init=init,end=end,\
                        freq=freq,season=season,tmean=tmean,curve=curve,regrid=regrid)
        if (var != None):
            data.variable=var
        if (mod != None):
            data.model=mod
        if (exp != None):
            data.experiment=exp
        if (realization != None):
            data.realization=realization
        data.get_rm()
    elif output == 'mm':
        data = get_data(dir_path=search_dir,\
                 init=init,end=end,regrid=regrid, \
                 freq=freq,season=season,tmean=tmean,rm=rm,curve=curve,whole=w,out=out)
        if (var != None):
            data.variable=var
        if (mod != None):
            data.model=mod
        if (exp != None):
            data.experiment=exp
        if (realization != None):
            data.realization=realization
        data.get_mm()
    elif output == 'stats':
        data = data_resample(fname=fname,zonMean=zmean,dir_path=search_dir,\
                 freq=freq,init=init,end=end,regrid=regrid,modMean=mm,modStd=std, \
                 season=season,tmean=tmean,monAnom=anom,curve=curve,monClim=clim,\
                 modAnom=manom,out=out,ci=ci,trend=trend,aggr=aggr,variable=var)
        data._mod_mean()

    


