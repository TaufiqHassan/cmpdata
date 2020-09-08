# -*- coding: utf-8 -*-
"""
Created on Wed Aug 26 17:57:21 2020

@author: Taufiq
"""

from file_system_util import search_dir, get_means

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
        self._extMod = kwargs.get('extMod', None)
        self._extExp = kwargs.get('extExp', None)
        self._extVar = kwargs.get('extVar', None)
        self.curve = kwargs.get('curve', None)
        self.freq = kwargs.get('freq', 'annual')
        self.season = kwargs.get('season', None)
        self.tmean = kwargs.get('tmean', None)
        self.exp2 = kwargs.get('exp2', None)
        self.dir_path2 = kwargs.get('dir_path2', None)

    @property
    def extMod(self):
        return self._extMod

    @extMod.setter
    def extMod(self, val):
        self._extMod=[0]
        mods = [x.strip() for x in val.split(',')]
        for zz in range(len(mods)):
            self._extMod.append(mods[zz])
        self._extMod.remove(0)

    @property
    def extExp(self):
        return self._extExp

    @extExp.setter
    def extExp(self, val):
        self._extExp = [0]
        exps = [x.strip() for x in val.split(',')]
        for zz in range(len(exps)):
            self._extExp.append(exps[zz])
        self._extExp.remove(0)
            
    @property
    def extVar(self):
        return self._extVar

    @extVar.setter
    def extVar(self, val):
        self._extVar = [0]
        vars = [x.strip() for x in val.split(',')]
        for zz in range(len(vars)):
            self._extVar.append(vars[zz])
        self._extVar.remove(0)

    def get_info(self):
        info = search_dir(dir_path=self.dir_path,variable=self._var,model=self._mod,\
                          experiment=self._exp,realization=self._rlzn,rm=self._rm).specific_data()
        return info
    
    def get_rm(self):
        rm = get_means(dir_path=self.dir_path, variable=self._var, model=self._mod, experiment=self._exp,\
                         extMod=self._extMod,extExp=self._extExp,extVar=self._extVar,\
                         init=self.init,end=self.end,nc=self.to_nc,\
                         freq=self.freq,season=self.season,tmean=self.tmean,\
                         exp2=self.exp2,dir_path2=self.dir_path2).real_mean()
        return rm
    
    def get_mm(self):
        mm = get_means(dir_path=self.dir_path, variable=self._var, model=self._mod, experiment=self._exp,\
                         extMod=self._extMod,\
                         init=self.init,end=self.end,nc=self.to_nc,curve=self.curve,\
                         rm=self._rm,freq=self.freq,season=self.season,tmean=self.tmean).model_mean()
        return mm

