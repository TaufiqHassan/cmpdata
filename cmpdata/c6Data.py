from cmpdata.file_system_util import search_dir, get_means
from cmpdata.c6Stats import data_resample

class get_data(object): 
    
    def __init__(self, **kwargs):
        self.dir_path = kwargs.get('dir_path', None)
        self._var = kwargs.get('variable', None)
        self._mod = kwargs.get('model', None)
        self._exp = kwargs.get('experiment', None)
        self._rlzn = kwargs.get('realization', None)
        self._rm = kwargs.get('rm', None)
        self.to_nc = kwargs.get('nc', 'yes')
        self.init = kwargs.get('init', None)
        self.end = kwargs.get('end', None)
        self.curve = kwargs.get('curve', None)
        self.freq = kwargs.get('freq', 'annual')
        self.season = kwargs.get('season', None)
        self.tmean = kwargs.get('tmean', None)
        self.whole = kwargs.get('whole', None)
        self.fname = kwargs.get('fname', None)
        self.modMean = kwargs.get('modMean', None)
        self.modStd = kwargs.get('modStd', None)
        self.monClim = kwargs.get('monClim', None)
        self.monAnom = kwargs.get('monAnom', None)
        self.modAnom = kwargs.get('modAnom', None)
        self.trend = kwargs.get('trend', None)
        self.aggr = kwargs.get('aggr', None)
        self.zonMean = kwargs.get('zonMean', None)
        self.ci = kwargs.get('ci', 0.95)
        self.out = kwargs.get('out', None)
        self.regrid = kwargs.get('regrid', None)
        self.region = kwargs.get('region', 'global')
        self.area_file = kwargs.get('area_file', None)
        
    @property
    def model(self):
        return self._mod

    @model.setter
    def model(self, val):
        self._mod=[0]
        mods = [x.strip() for x in val.split(',')]
        for zz in range(len(mods)):
            self._mod.append(mods[zz])
        self._mod.remove(0)

    @property
    def experiment(self):
        return self._exp

    @experiment.setter
    def experiment(self, val):
        self._exp = [0]
        exps = [x.strip() for x in val.split(',')]
        for zz in range(len(exps)):
            self._exp.append(exps[zz])
        self._exp.remove(0)
            
    @property
    def variable(self):
        return self._var

    @variable.setter
    def variable(self, val):
        self._var = [0]
        vars = [x.strip() for x in val.split(',')]
        for zz in range(len(vars)):
            self._var.append(vars[zz])
        self._var.remove(0)
        
    @property
    def realization(self):
        return self._rlzn

    @realization.setter
    def realization(self, val):
        self._rlzn = [0]
        rlzns = [x.strip() for x in val.split(',')]
        for zz in range(len(rlzns)):
            self._rlzn.append(rlzns[zz])
        self._rlzn.remove(0)


    def get_info(self):
        info = search_dir(dir_path=self.dir_path,model=self._mod,variable=self._var,\
                          experiment=self._exp,realization=self._rlzn,rm=self._rm).specific_data()
        return info
            
    def get_rm(self):
        rm = get_means(dir_path=self.dir_path, variable=self._var, model=self._mod, \
                       experiment=self._exp, realization=self._rlzn,\
                       init=self.init,end=self.end,nc=self.to_nc,\
                       freq=self.freq,season=self.season,tmean=self.tmean,\
                       regrid=self.regrid, curve=self.curve).real_mean()
        return rm
    
    def get_ts(self):
        ts = get_means(dir_path=self.dir_path, variable=self._var, model=self._mod, \
                       experiment=self._exp,region=self.region,\
                       realization=self._rlzn,area_file=self.area_file).time_ser()
        return ts

    
    def get_mm(self):
        mm = get_means(dir_path=self.dir_path, variable=self._var, model=self._mod, \
                       experiment=self._exp,regrid=self.regrid,init=self.init,\
                       end=self.end,nc=self.to_nc,curve=self.curve,rm=self._rm,\
                       freq=self.freq,season=self.season,tmean=self.tmean,\
                       whole=self.whole,out=self.out,realization=self._rlzn).model_mean()
        return mm

    def get_stats(self):
        r = data_resample(fname=self.fname,season=self.season,var=self._var,\
                          nc=self.to_nc,freq=self.freq,tmean=self.tmean,\
                          modMean=self.modMean,modStd=self.modStd,monClim=self.monClim,\
                          monAnom=self.monAnom,modAnom=self.modAnom,out=self.out,\
                          init=self.init,end=self.end,trend=self.trend,aggr=self.aggr,\
                          ci=self.ci,regrid=self.regrid)._mod_mean()
        return r

