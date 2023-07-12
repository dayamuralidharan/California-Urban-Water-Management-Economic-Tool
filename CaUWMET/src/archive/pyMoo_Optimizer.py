import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
 
class CostOptimizer(Problem):
    '''
    This class is a PyMoo problem class designed to simulate the effects of wmoSupply level...
    ...on water usage cost optimization across various sources.
 
    The objective function f(x) has an equality constraint g(x) = wmoSupply.
    The algorithm is a particle swarm optimizer with default settings. 
 
    https://pymoo.org/
    '''
    def __init__(self, 
                 wmoSupply: int,        # how much are we allocating to the WMOs? int for now...
                 contractor: str,       # which subcontractor? e.g. 'Metropolitan Water District of Southern California'
                 upperBounds: list,     # upper bound of each WMO for a given scenario - len(list)=8
                 inputData: InputData, inputDataLocations: InputDataLocations, 
                 storageUtilities: StorageUtilities, modelLogic: ModelLogic):
        '''
        Initializing the CostOptimizer class requires parameterizing a given CaUWMET model
        for a given contractor and requested wmoSupply.
        '''
        self.wmoSupply = wmoSupply      # must be greater than 0
        self.upperBounds = upperBounds  # list length 8 upper bounding WMOs
        self.inputData = inputData
        self.inputDataLocations = inputDataLocations
        self.storageUtilities = storageUtilities
        self.modelLogic = modelLogic
        self.modelLogic = self.modelLogic(
            self.inputData(self.inputDataLocations()), 
            self.storageUtilities()
        )
        self.modelLogic.contractor = contractor
        
        # parameterize the objective function
        super().__init__(
            n_var=8, n_obj=1, n_eq_constr=1, 
            xl=[0]*8, xu=self.upperBounds    # xl and xu set f bounds 
        )
    
    
    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
           wmoSupply :: int
        Returns objective function f(x) as execution of model logic
        Returns equality constraint h(x) as wmoSupply - sum(x) = 0
        ''' 
        out["F"] = self.modelLogic.execute(x)
        out["H"] = self.wmoSupply - np.sum(x)
        

