# Script defining the CostProblem class

import numpy as np
import warnings

from pymoo.core.problem import ElementwiseProblem

from src.modelLogic.modelLogic import ModelLogic

warnings.filterwarnings('ignore')  # turn off warnings

### PyMoo Optimization Problem Class ###

class CostProblem(ElementwiseProblem): 
    '''
    This class is a PyMoo problem class designed to simulate the effects of longtermWMOSupply levels...
    ...on water usage cost optimization (economicLoss) for a given contractor. 
    The objective space of F(X) is mapped by an algorithm, within the u/l bounds for each dimension of X.
    Optionally, F(X) can be constrained by inequality constraints G(X): 
       + g1(x) > wmoFloor  :: defines a floor value of the sum( longtermWMOSupply ) 
       + g2(x) < wmoCeiling :: defines a ceiling value of the sum( longtermWMOSupply )
    https://pymoo.org/
    '''
    def __init__(self, 
                 lowerBounds: list,          # lower bound of each longtermWMO - len(list)=8
                 upperBounds: list,          # upper bound of each longtermWMO - len(list)=8
                 modelLogic: ModelLogic,     # prepared ModelLogic object with InputData and StorageUtilities
                 wmoFloor=None,              # how low are we constraining the sum longtermWMOs?
                 wmoCeiling=None,            # how high are we constraining the sum longtermWMOs?
                 zero_threshold=1,           # the zero_threshold minimizes all values below it to 0
                 **kwargs):    
        '''
        Initializing the CostProblem class requires parameterizing a CaUWMET model for a given contractor.
        Inputs:
            wmoFloor/wmoCeiling :: number > 0, max sum of the longtermWMO allocations
            lowerBounds/upperBounds :: list of numbers, length 8
            modelLogic :: ModelLogic object loaded with InputData, StorageUtilities, and Contractor
            zero_threshold :: number to send all values below to 0
        '''
        self.zero_threshold = zero_threshold
        self.wmoFloor = wmoFloor if wmoFloor is not None else None
        self.wmoCeiling = wmoCeiling if wmoCeiling is not None else None
        self.n_ieq_constr = sum([ i != None for i in [self.wmoFloor, self.wmoCeiling] ]) #TODO: Recommend making name clearer
        self.lowerBounds = lowerBounds
        self.upperBounds = [ ub if ub>0 else self.zero_threshold for ub in upperBounds ]
        self.objectiveFunction = modelLogic.execute
        
        # parameterize the objective function
        super().__init__(
            n_var=8, n_obj=1, n_ieq_constr=self.n_ieq_constr, 
            xl=self.lowerBounds, xu=self.upperBounds,  # xl and xu set longtermWMOSupply bounds 
            **kwargs
        )


    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
           x :: list of numbers, length 8
        Returns objective function f(x)
        Returns inequality constraints g(x)
        The zero_threshold 0s out the values below it in the X vector.
        This is also reflected in the OPtimizeWMOs.optimize() method.
        This is done as a workaround to Nonetype errors when pymoo args xl and xu are both 0.
        '''
        x = [ xi if xi>self.zero_threshold else 0 for xi in x ]
        if self.n_ieq_constr > 0:
            out["F"] = self.objectiveFunction(x)
            G1 = self.wmoFloor - np.sum(x) if self.wmoFloor is not None else None  # np.sum(x)>=self.wmoFloor
            G2 = np.sum(x) - self.wmoCeiling if self.wmoCeiling is not None else None  # self.wmoCeiling>=np.sum(x)
            out["G"] = [ g for g in [G1,G2] if g is not None ]
        else:
            out["F"] = self.objectiveFunction(x)


