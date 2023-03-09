import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
 
class ShortageCost(Problem):
    '''
    This class is a PyMoo problem class designed to simulate the effects of shortage level...
    ...on water usage cost optimization across various sources.
 
    The objective function f(x) has an equality constraint g(x) = shortage.
    The algorithm is a particle swarm optimizer with default settings. 
 
    https://pymoo.org/
    '''
    def __init__(self, demands, supplies, w):
        super().__init__(n_var=1, n_obj=1, n_eq_constr=1, xl=0.0, xu=50) # xl and xu set f bounds ## TODO: Need to make xl and xu array, set n_var = 8
        self.shortage = demands - supplies
        self.rc = w[0] # 'rationing coefficient'
        self.w = w[1:] # water source weights
        inputData = InputData(InputDataLocations())
        self.modelLogic = ModelLogic(inputData, StorageUtilities())
        self.modelLogic.contractor = 'Metropolitan Water District of Southern California'
 
    def rationing(self, x, *args, **kwargs): 
        '''
        Inputs:
	        x :: Array ;; volumes from water sources
	        shortage :: int
	    Computes rationing r = (shortage - sum(x)) '''

        try:
            r = (self.shortage-np.sum(x,axis=1))
            r[r<0] = 0 # Set lower bound constraint on rationing
        except IndexError:
            r = (self.shortage-np.sum(x,axis=0))
            if r<0:
                r=0
        return r
 
    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
            x :: Array of shape w[] * population size: The size of the swarm being used;; volumes from water sources
            w :: Array of shape w[0] ;; cost units for water sources
            rc :: int ;; cost unit for rationing
            shortage :: int
        Compute rationing r
        Returns f(x) as x dot w + rc * r
        Returns h(x) as shortage - sum(x) = 0

        ''' 
        r = self.rationing(x, self.shortage)
        f = x.dot(self.w) # 
        f += self.rc * r # 
        out["F"] = self.modelLogic.execute(x)
        h = self.shortage - np.sum(np.c_[x,r],axis=1)
        out["H"] = h

