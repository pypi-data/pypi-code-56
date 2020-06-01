import multiprocessing as mp
import numpy as np
import itertools
from functools import partial

class BulkSimulator:
    '''
    This class iterates over a parameter space, simulating for each set of parameters

    BulkSimulator(simulation,params,procs,kwargs,returnnames=['Result'])

    simulation: function which carries out the simulation

    params: dictionary of parameters with the names of the parameters and list containing values to be iterated over

    procs: number of processes to be ran on

    kwargs: other parameters

    '''
    def __init__(self,simulation,params,procs,kwargs,returnnames=['Result']):
        self.simulation = simulation
        self.kwargs = kwargs
        self.params = list(params.values())
        self.procs = procs
        self.param_names = params.keys()
        self.returnnames = returnnames

        grid = np.meshgrid(*self.params)
        self.gridsize = list(np.array(grid).shape)
        grid = tuple([gr.ravel() for gr in list(grid)])
        mesh = np.c_[grid]
        self.params = []
        
        self.params = [list(col) for col in mesh.T]
        self.N = len(self.params[0])
        self.args = [[val] * self.N for val in self.kwargs.values()]
        self.args = self.params + self.args 
        self.args = list(zip(*tuple(self.args)))  


    def run(self):
        '''
        This method runs the simulation for all parameters choices chosen on the number of processes speficied
        '''
        with mp.Pool(processes=self.procs) as pool:
            self.results = pool.starmap(self.simulation, self.args)
        if not isinstance(self.results, tuple):
            self.results = (self.results,)
    

    def to_csv(self,filename,sep=','):
        '''
        Given a filename and optional separator character, this function saves the parameters and results to a csv file.
        '''
        with open(filename,'w') as file:
            header = [f'idx{sep}']
            for name in self.param_names:
                header.append(f'{name}{sep}')
            for name in self.returnnames:
                header.append(f'{name}{sep}')
            header_str = ''.join(header)[:-1]
            file.write(header_str+'\n')

            for i,row in enumerate(zip(*(self.params+list(self.results)))):
                param_txt = [f'{val}{sep}' for val in row]
                row_txt = f'{i}{sep}' + ''.join(param_txt)[:-1] + '\n'
                file.write(row_txt)


    def save_metadata(self,filename,sep=','):
        '''
        Saves the extra "kwargs" to a csv file so all settings for a run can be saved
        '''
        with open(filename,'w') as file:
            header = []
            for name in self.kwargs.keys():
                header.append(f'{name}{sep}')
            header_str = ''.join(header)[:-1]
            file.write(header_str+'\n')

            line = [f'{val}{sep}' for val in self.kwargs.values()]
            line_str = ''.join(line)[:-1]
            file.write(line_str+'\n')


    def __str__(self):
        header = ['idx,']
        for name in self.param_names:
            header.append(f'{name},')
        for name in self.returnnames:
            header.append(f'{name},')
        header_str = ''.join(header)[:-1]
        row_txt = []
        for i,row in enumerate(zip(*(self.params+list(self.results)))):
            param_txt = [f'{val},' for val in row]
            row_txt.append(f'{i},' + ''.join(param_txt)[:-1] + '\n')
        res_string = ''.join(row_txt)
        return f'''
simulation = {self.simulation.__name__}
procs = {self.procs}
kwargs: {self.kwargs}
number of results: {self.N}
{header_str}
{res_string}'''