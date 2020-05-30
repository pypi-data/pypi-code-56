import numpy as np
from .peak_shape import (PseudoVoigtModel, LorentzianModel, GaussianModel,
                         DPseudoVoigtModel, DLorentzianModel, DGaussianModel,
                         HDPseudoVoigtModel, HDLorentzianModel, HDGaussianModel,
                         HPseudoVoigtModel, HLorentzianModel, HGaussianModel, BkgModel)
from lmfit.models import LinearModel

from functools import reduce


c_ln2 = np.log(2.0)
c_ln2pi = c_ln2 / np.pi


class MossMod(object):
    def __init__(self, *args, **kwargs):
        self.FitModel = BkgModel(prefix='bkg_')
        self.FitParams = self.FitModel.make_params()

    def pre2mod(self, sprefix):
        prefixl = [i.prefix for i in self.FitModel.components]
        return self.FitModel.components[prefixl.index(sprefix)]

    def add_comp(self, PS, MULT, MAG, prefix, center, maxi, H, **kwargs):
        prefixl = [i.prefix for i in self.FitModel.components]
        if prefix in prefixl:
            print('prefix already used \n Please change')
            return
        qs_nomin = False
        if PS == "PseudoVoig":
            if MAG == 'sextet':
                if MULT == 'singlet':
                    Smod_type = HPseudoVoigtModel
                elif MULT == 'doublet':
                    Smod_type = HDPseudoVoigtModel
                    qs_nomin = True
            elif MAG == 'singlet':
                if MULT == 'singlet':
                    Smod_type = PseudoVoigtModel
                elif MULT == 'doublet':
                    Smod_type = DPseudoVoigtModel
        if PS == "Lorentzian":
            if MAG == 'sextet':
                if MULT == 'singlet':
                    Smod_type = HLorentzianModel
                elif MULT == 'doublet':
                    Smod_type = HDLorentzianModel
                    qs_nomin = True
            elif MAG == 'singlet':
                if MULT == 'singlet':
                    Smod_type = LorentzianModel
                elif MULT == 'doublet':
                    Smod_type = DLorentzianModel
        if PS == "Gaussian":
            if MAG == 'sextet':
                if MULT == 'singlet':
                    Smod_type = HGaussianModel
                elif MULT == 'doublet':
                    Smod_type = HDGaussianModel
                    qs_nomin = True
            elif MAG == 'singlet':
                if MULT == 'singlet':
                    Smod_type = GaussianModel
                elif MULT == 'doublet':
                    Smod_type = DGaussianModel

        mod = Smod_type.fromAdd(maxi, center, H, prefix, **kwargs)
        if qs_nomin:
            del mod.param_hints['qs']['min']
        self.FitModel += mod
        self.FitParams += self.FitModel.make_params()

    def remove_comp(self, sprefix):
        if sprefix == 'bkg_':
            print('backgroung could not removed')
            return

        comps = self.FitModel.components[:]
        index = [i.prefix for i in comps].index(sprefix)
        del comps[index]
        self.FitModel = reduce(lambda x, y: x + y, comps)
        self.FitParams = self.FitModel.make_params()
        print(self.FitModel)

    def FitModelEval(self, x, params=None):
        if params is None:
            self.FitParam = self.FitModel.make_params()
            params = self.FitParam
        return self.FitModel.eval(x=x, params=params)

    def Fit(self, y, x, yerr):
        params = self.FitModel.make_params()
        prefixl = [i.prefix for i in self.FitModel.components][1:]
        list_sum = '+'.join([f'{i}amplitude' for i in prefixl])
        for i, pr_comp in enumerate(prefixl):
            name = f'{pr_comp}conc'
            expression = f'{pr_comp}amplitude / ({list_sum})'
            params.add(name, expr=expression)
        out = self.FitModel.fit(y, params, x=x, weights=1 / yerr)
        self.FitParams = out.params
        for par_n, val in out.best_values.items():
            self.FitModel.set_param_hint(par_n, value=val)
        return out

    def loadFitmodel(self, info):
        self.FitModel = info[0][0]
        for comp in info[0][1:]:
            self.FitModel + comp
        self.FitModel.param_hints = info[2]

    def bkg_val(self):
        return self.FitModel.components[0].param_hints['val']['value']
