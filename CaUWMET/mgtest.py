#from IPython.core.debugger import set_trace

import time
import numpy as np
import warnings

from pymoo.core.problem import ElementwiseProblem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.termination import get_termination
from pymoo.optimize import minimize

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

warnings.filterwarnings('ignore')

### PyMoo Optimization Problem Class ###

class CostOptimizer(ElementwiseProblem): 
    '''
    This class is a PyMoo problem class
    
    The objective function f(x) has an equality constraint g(x) = wmoSupply.
    The algorithm is a particle swarm optimizer with default settings. 
    
    https://pymoo.org/
    '''
    def __init__(self, 
                 modelLogic: ModelLogic,     # prepared ModelLogic object with InputData and StorageUtilities
                 lowerBounds: list,          # lower bound of each WMO type for a given scenario - len(list)=8
                 upperBounds: list,          # upper bound of each WMO type for a given scenario - len(list)=8
                 wmoFloor=None,              # how low are we constraining the sum longterm WMOs?
                 wmoSupply=None,             # how high are we constraining the sum longterm WMOs?
                 **kwargs):    
        '''
        Initializing the CostOptimizer class requires parameterizing a CaUWMET model for a given contractor and(?) wmoSupply.
        Inputs:
            wmoFloor/wmoSupply :: number > 0, max sum of the longtermWMO allocations
            lowerBounds/upperBounds :: list of numbers, length 8
            modelLogic :: ModelLogic object loaded with InputData, StorageUtilities, and Contractor
        '''
        self.wmoFloor = wmoFloor if wmoFloor is not None else None
        self.wmoSupply = wmoSupply if wmoSupply is not None else None
        self.n_ieq_constr = sum([i != None for i in [self.wmoFloor, self.wmoSupply]])
        self.lowerBounds = lowerBounds
        self.upperBounds = upperBounds
        self.objectiveFunction = modelLogic.executeModelLogicForContractor
        
        # parameterize the objective function
        super().__init__(
            n_var=8, n_obj=1, n_ieq_constr=self.n_ieq_constr, 
            xl=self.lowerBounds, xu=self.upperBounds,  # xl and xu set f bounds 
            **kwargs
        )


    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
           x :: list of numbers, length 8
        Returns objective function f(x) as execution of model logic
        Returns inequality constraints g(x)
        '''
        tic = time.perf_counter()
        if self.n_ieq_constr > 0:
            out["F"] = self.objectiveFunction(x)
            G1 = self.wmoFloor - np.sum(x)
            G2 = np.sum(x) - self.wmoSupply
            out["G"] = [G1, G2]
        else:
            out["F"] = self.objectiveFunction(x)
        toc = time.perf_counter()
        

### instantiate CaUWMET model and execute MOO problem ###

class OptimizeWMOs:

    def __init__(self, 
                 year='2045', 
                 contractor='Metropolitan Water District of Southern California',
                 wmoFloor=None, 
                 wmoSupply=None, 
                 lowerBounds=[0]*8, 
                 upperBounds='longtermWMOVolumeLimits'):
        
        self.inputData = InputData(InputDataLocations())
        self.modelLogic = ModelLogic(self.inputData, StorageUtilities())
        self.modelLogic.contractor = contractor
        self.wmoFloor = wmoFloor
        self.wmoSupply = wmoSupply
        self.lowerBounds = lowerBounds
        self.upperBounds = upperBounds if upperBounds != 'longtermWMOVolumeLimits' else [
            self.inputData.longtermWMOSurfaceVolumeLimit[self.inputData.longtermWMOSurfaceVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOGroundwaterVolumeLimit[self.inputData.longtermWMOGroundwaterVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMODesalinationVolumeLimit[self.inputData.longtermWMODesalinationVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMORecycledVolumeLimit[self.inputData.longtermWMORecycledVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOPotableReuseVolumeLimit[self.inputData.longtermWMOPotableReuseVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOTransfersExchangesVolumeLimit[self.inputData.longtermWMOTransfersExchangesVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOOtherSupplyVolumeLimit[self.inputData.longtermWMOOtherSupplyVolumeLimit.index==contractor][year][0],
            self.inputData.longtermWMOConservationVolumeLimit[self.inputData.longtermWMOConservationVolumeLimit.index==contractor][year][0],
        ]
        
    
    def optimize(self):
        # parameterize the problem
        problem = CostOptimizer(
            modelLogic=self.modelLogic,
            wmoFloor=self.wmoFloor, wmoSupply=self.wmoSupply, 
            lowerBounds=self.lowerBounds, upperBounds=self.upperBounds
        )
        # parameterize algorithm
        algorithm = PSO(
            pop_size=10,
            w=0.9, c1=5.0, c2=1.0,
            adaptive=True,
            max_velocity_rate=0.2
        )
        # parameterize the termination criteria
        termination = get_termination("n_gen", 5)
        
        # execute optimization
        self.res = minimize(
            problem, 
            algorithm, 
            termination, 
            seed=42, 
            verbose=True,
            save_history=True
        )

        print("Best solution found: \nX = %s\nF = %s" % (self.res.X, self.res.F))
        
        
    def visualization_a(self):
        
        