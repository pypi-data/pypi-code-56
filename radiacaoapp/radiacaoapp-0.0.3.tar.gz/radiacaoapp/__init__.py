import numpy as np
import numpy.linalg as lg
import copy
from numpy import array
from numpy import power
from scipy.constants import sigma

class suprad:
    """Create a new Radiant Surface.
        
    e (float between 0 and 1) - Emissivity of the Radiant Surface
    
    A (float greater than 0) - Area of the Surface
    
    bound:
    0 - Temperature given;
    1 - Heat Flow given; and
    2 - Surface belgons to a coupling to be defined;
    
    bound_param:
    If bound = 0 or 1 It will be the temperature of the heat flow (if not filled the value will be zero!!!)
    for any other values The entry will not be used
    """
    total = 0
    list = []
    def __init__(self,e,A,bound,bound_param=0):
        self.num=suprad.total
        self.e=e
        self.A=A
        self.bound=bound
        # emissive power
        if bound==0:
            self.bound_param = sigma*power(bound_param,4)
        # heat flow
        elif bound==1:
            self.bound_param = bound_param
        else:
            self.bound_param = None
        suprad.total=suprad.total+1
        suprad.list.append(self)
    @staticmethod
    def get(num):
        """ Returns a Radiant Surface by its number.
        
        num - number of the Radiant Surface"""
        if isinstance(num, list):
            ret = []
            for i in num:
                ret.append(suprad.get(i))
            return ret
        for i in suprad.list:
            if i.num==num:
                return suprad.list[num]
    @staticmethod
    def K(num):
        """ Returns the 1st set of equation coefficient of a Radiant Surface by its number.

        num - number of the Radiant Surface"""
        sup = suprad.get(num)
        if sup.e==1:
            return 1
        else:
            return (sup.e*sup.A)/(1-sup.e)
    @staticmethod
    def clear():
        """ Clears all Radiant Surfaces, Views and Couplings."""
        ans = input('All views and couplings will be cleared to, are you sure? (y/n)')
        if ans=='y':
            view.clear()
            cpl.clear()
            suprad.list = []
            suprad.total = 0
            print('All data cleared!')
        else:
            print('Kept all data without erasing anything')

class view:
    """Create a new view between two Radiant Surfaces (RDs).
        
    num_suprad_dep: Number of the departure RD
    
    num_suprad_arr: Number of the arrival RD
    
    F : The view factor from the departure RD to the arrival RD
    """
    total = 0
    list = []
    def __init__(self,num_suprad_dep,num_suprad_arr,F):
        self.num = view.total
        self.dep=suprad.get(num_suprad_dep)
        self.arr=suprad.get(num_suprad_arr)
        self.F=F
        view.total=view.total+1
        view.list.append(self)
    @staticmethod
    def get(num):
        """ Returns a view by its number.
        
        num - number of the view"""
        for i in view.list:
            if i.num==num:
                return view.list[num]
    @staticmethod
    def K(num):
        """ Returns the 2nd set of equation coefficient of a view by its number.

        num - number of the view"""
        vw = view.get(num)
        return vw.dep.A*vw.F
    @staticmethod
    def clear():
        """ Clears all Views."""
        view.list = []
        view.total = 0

class cpl:
    """Create a new coupling between multiple Radiant Surfaces (RDs).
        
    num_suprad_list: List of the RDs numbers that belongs to the coupling
    
    q_gen: Heat generated inside de coupling (if not filled will be zero!)
    """
    total = 0
    list = []
    def __init__(self,num_suprad_list,q_gen=0):
        self.num = cpl.total
        self.suprad_list = suprad.get(num_suprad_list)
        self.q_gen = q_gen
        cpl.total=cpl.total+1
        cpl.list.append(self)
    @staticmethod
    def get(num):
        """Returns a coupling by its number."""
        for i in cpl.list:
            if i.num==num:
                return cpl.list[num]
    @staticmethod
    def clear():
        """Clears all couplings. """
        cpl.list = []
        cpl.total = 0

import numpy as np
import numpy.linalg as lg
import copy
from numpy import array
from numpy import power
from scipy.constants import sigma

def solve():
    """Solves the Linear System (LS) with all Radiant Surfaces (RDs), view and couplings declared.

    Returns:

    A - A Matrix
    B - B independent vector of the LS
    X - X vector solved
    X_temperatures - X vector solved with the RDs temperatures placed in its emissive powers
    """
    n = suprad.total
    A = np.zeros([3*n,3*n])
    B = np.zeros([3*n])
    for i in suprad.list:
        # first set of equations
        A[i.num,i.num] = suprad.K(i.num)
        A[i.num,1*n+i.num] = - suprad.K(i.num)
        if i.e!=1:
            A[i.num,2*n+i.num] = 1
        # second set of equations
        for j in view.list:
            if i.num==j.dep.num:
                A[1*n+i.num,j.dep.num] += view.K(j.num)
                A[1*n+i.num,j.arr.num] -= view.K(j.num)
            if i.num==j.arr.num:
                A[1*n+i.num,j.dep.num] -= view.K(j.num)
                A[1*n+i.num,j.arr.num] += view.K(j.num)
        A[1*n+i.num,2*n+i.num] = -1
        # third set of equations
        if i.bound==0:
            # temperature boundary condition
            A[2*n+i.num,1*n+i.num] = 1
            B[2*n+i.num] = i.bound_param
        elif i.bound==1:
            # heat flow boundary condition
            A[2*n+i.num,2*n+i.num] = 1
            B[2*n+i.num] = i.bound_param
        elif i.bound==2:
            # coupling boundary condition
            for j in cpl.list:
                num_suprads_coupled = len(j.suprad_list)
                for k in range(0,num_suprads_coupled-1):
                    A[2*n+j.suprad_list[k].num,1*n+j.suprad_list[k].num] = 1
                    A[2*n+j.suprad_list[k].num,1*n+j.suprad_list[k+1].num] = -1
                    A[2*n+j.suprad_list[num_suprads_coupled-1].num,2*n+j.suprad_list[k].num] = 1
                A[2*n+j.suprad_list[num_suprads_coupled-1].num,2*n+j.suprad_list[num_suprads_coupled-1].num] = 1
                B[2*n+j.suprad_list[num_suprads_coupled-1].num] = j.q_gen
    # transformation from emissive power to temperature back again
    X = lg.solve(A,B)
    X_temperatures = copy.copy(X)
    for i in range(0,n):
        X_temperatures[i+n] = power(X[i+n]/sigma,1/4)
    return [A,B,X,X_temperatures]