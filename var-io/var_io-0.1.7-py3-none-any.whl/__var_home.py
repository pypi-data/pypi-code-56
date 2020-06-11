from .__ioFunc import save_dictionary,load_dictionary
from .__var_filter import get_var_inf,varname
import __main__ as _main_module
import sys
from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics
import pandas as pd




class VarHome:
    def __init__(self,method = 'filter'):
        assert method in ['filter','choose']
        self.method = method
        if self.method == 'filter':
            self.__exclude_list = []
        elif self.method == 'choose':
            self.__choose_list = []
        self.__exclude_module = True
        self.__exclude_function = True
        self.__exclude_unsupported = True
        self._jupyterlab_variableinspector_nms = NamespaceMagics()
        self._jupyterlab_variableinspector_Jupyter = get_ipython()
        self._jupyterlab_variableinspector_nms.shell = self._jupyterlab_variableinspector_Jupyter.kernel.shell
        self.__init_var_list = self.__update_var_list()
        print(self.__init_var_list)

    def __var_base(self):
        need_list = [i for i in self.__update_var_list() if i not in self.__init_var_list]
        self.__name_space = _main_module.__dict__.copy()
        self.__var_inf = {i:get_var_inf(self.__name_space[i]).copy() for i in need_list}
        if self.__exclude_module == True:
            self.__filter_module()
        if self.__exclude_function == True:
            self.__filter_function()
        if self.__exclude_unsupported == True:
            self.__filter_unsupported()
        if self.method == 'filter':
            self.__var_inf = {k:v for k,v in self.__var_inf.items() if k not in  self.__exclude_list}
        elif self.method == 'choose':
            self.__var_inf = {k:v for k,v in self.__var_inf.items() if k  in  self.__choose_list}

    def vars(self):
        self.__var_base()
        show_df = pd.DataFrame(self.__var_inf).T
        if len(show_df)>0: 
            return show_df[['is_supported','type','size','memory usage']]

    def __filter_module(self):
        self.__var_inf = {k:v for k,v in self.__var_inf.items() if v['type'] != 'module'}
    def __filter_function(self):
        self.__var_inf = {k:v for k,v in self.__var_inf.items() if v['type'] != 'function'}
    def __filter_function(self):
        self.__var_inf = {k:v for k,v in self.__var_inf.items() if v['type'] != 'function'}
    def __filter_unsupported(self):
        self.__var_inf = {k:v for k,v in self.__var_inf.items() if v['is_supported'] == True}





    def __update_var_list(self):
        return self._jupyterlab_variableinspector_nms.who_ls()
    
    def clear_list(self):
        self.__init_var_list = self.__update_var_list()
    
    def save_data(self,filename):
        self.__var_base()
        data = {i:self.__name_space[i] for i in self.__var_inf.keys() if self.__var_inf[i]['is_supported'] == True}
        save_dictionary(data,filename)
        print(list(data.keys()))
        return True
    def load_data(self,filename):
        data = load_dictionary(filename)[0]
        for k,v in data.items():
            _main_module.__dict__[k] = v
        print(list(data.keys()))

    def exclude_var(self,var_name):
        if varname not in self.__exclude_list:
            self.__exclude_list.append(var_name)
        print('屏蔽变量：'+var_name)
    def choose_var(self,var_name):
        if varname not in self.__choose_list and var_name in self.__update_var_list():
            self.__choose_list.append(var_name)
        print('选定变量：'+var_name)