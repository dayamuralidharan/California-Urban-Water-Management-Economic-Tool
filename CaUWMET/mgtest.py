import numpy as np
from pprint import pprint
import timeit

from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize
from pymoo.termination import get_termination

#from tests.test_modelLogic.py import ModelLogic
#from tests.test_inputDataLocationsForTesting import InputDataLocationsForTesting
#from tests.test_storageOperations import StorageUtilities

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
from src.modelLogic.readLongTermWMOsAssumptions import LongTermWMOsAssumptions

### PyMoo Optimization Problem ###

class CostOptimizer(Problem):
    '''
    This class is a PyMoo problem class designed to simulate the effects of wmoSupply level...
    ...on water usage cost optimization across various sources.
    
    The objective function f(x) has an equality constraint g(x) = wmoSupply.
    The algorithm is a particle swarm optimizer with default settings. 
    
    https://pymoo.org/
    '''
    def __init__(self, 
                 wmoSupply: int,             # how much are we allocating to the longterm WMOs? int for now...
                 upperBounds: list,          # upper bound of each WMO type for a given scenario - len(list)=8
                 modelLogic: ModelLogic):    # prepared ModelLogic object with InputData and StorageUtilities
        '''
        Initializing the CostOptimizer class requires parameterizing a given CaUWMET model
        for a given contractor and requested wmoSupply.
        Inputs:
            wmoSupply :: integer (for now..., could later be a number)
            upperBounds :: list of numbers, length 8
            modelLogic :: ModelLogic object loaded with InputData, StorageUtilities, and Contractor
        '''
        self.wmoSupply = wmoSupply           # must be greater than 0
        self.upperBounds = upperBounds       # list length 8 upper bounding WMOs
        self.objectiveFunction = modelLogic.execute
        
        # parameterize the objective function
        super().__init__(
            n_var=8, n_obj=1, #n_eq_constr=1, 
            xl=[0]*8, xu=self.upperBounds    # xl and xu set f bounds 
        )


    def _evaluate(self, x, out, *args, **kwargs):
        '''
        Inputs:
           x :: list of numbers, length 8
        Returns objective function f(x) as execution of model logic
        Returns equality constraint h(x) as wmoSupply - sum(x) = 0
        '''
        tic = timeit.default_timer()
        out["F"] = self.objectiveFunction(x)
        toc = timeit.default_timer()
        print(f"Execution Time: {toc-tic:.2f}s")
#        print(f"{(self.wmoSupply - np.sum(x,axis=1)).shape}")
#        print(f"{self.wmoSupply - np.sum(x,axis=1)}")
        #out["H"] = self.wmoSupply - np.sum(x, axis=1)
        

### Optimization Test ###

def main():

    # instantiate CaUWMET model
    inputData = InputData(InputDataLocations())
    modelLogic = ModelLogic(inputData, StorageUtilities())
    modelLogic.contractor = 'Metropolitan Water District of Southern California'
    
    ltaWMO = LongTermWMOsAssumptions(InputDataLocations())
    year = '2045'
    
#    upperBounds = [
#        ltaWMO.longtermWMOSurfaceVolumeLimit[ltaWMO.longtermWMOSurfaceVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMOGroundwaterVolumeLimit[ltaWMO.longtermWMOGroundwaterVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMODesalinationVolumeLimit[ltaWMO.longtermWMODesalinationVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMORecycledVolumeLimit[ltaWMO.longtermWMORecycledVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMOPotableReuseVolumeLimit[ltaWMO.longtermWMOPotableReuseVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMOTransfersExchangesVolumeLimit[ltaWMO.longtermWMOTransfersExchangesVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMOOtherSupplyVolumeLimit[ltaWMO.longtermWMOOtherSupplyVolumeLimit.index==modelLogic.contractor][year][0],
#        ltaWMO.longtermWMOConservationVolumeLimit[ltaWMO.longtermWMOConservationVolumeLimit.index==modelLogic.contractor][year][0],
#    ]

    upperBounds = [50]*8
    wmoSupply = 500
    
    problem = CostOptimizer(wmoSupply=wmoSupply, upperBounds=upperBounds, modelLogic=modelLogic)
    algorithm = PSO(
        pop_size=50,
        w=0.9, c1=5.0, c2=1.0,
        adaptive=True,
        max_velocity_rate=0.2
    )
    termination = get_termination("n_gen", 10)
    
    res = minimize(
        problem, 
        algorithm, 
        termination, 
        seed=42, 
        verbose=True,
        save_history=False
    )
    
    print("Best solution found: \nX = %s\nF = %s" % (res.X, res.F))
    
    
if __name__ == "__main__":
    main()


### old ###

# # assign weights
# w = []
# 
# w += [ modelLogic.inputData.longtermWMOSurfaceUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMOGroundwaterUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMODesalinationUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMORecycledUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMOPotableReuseUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMOTransfersExchangesUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMOOtherSupplyUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# w += [ modelLogic.inputData.longtermWMOConservationUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]
# 
# ### Bucket Testing ###
# 
# # TODO: Need to complete evaluation of inputs and constraints
# # randomish 1x8 variables for testing inputs
# # could replace wt with w
# 
# wt = random.sample(list(range(1,5))*2, k=8)  # weights
# lb = [0]*8                            # lower bound
# ub = random.sample([50,40,30,20]*2, k=8)     # upper bound
# wmo = [                               # wmo names
#     'Surface',
#     'Groundwater',
#     'Desalination',
#     'Recycled',
#     'PotableReuse',
#     'TransfersExchanges',
#     'OtherSupply',
#     'Conservation'
# ]
# 
# 
# 
# # TODO: integrate the lower bound variable into the bucket filling logic
# # TODO: verify optimal solutions
# 
# class Optimizer:
#     '''
#     Contraint Model determines optimal WMO allocation by minimizing cost.
#     First ranks WMOs by weight then "fills" the lower weighted WMO "buckets" first.
#     Tied WMO buckets are filled equally, all buckets filled as constrained by bounds.    
#     '''
#     def __init__(self, wmo:list, wt:list, lb:list, ub:list, a:int):
#         self.wmo = wmo  # names
#         self.wt = wt    # weights
#         self.lb = lb    # lower bounds
#         self.ub = ub    # upper bounds
#         self.a = a      # allowance
#         self.__OptimizeLongtermWMOs()
#     
#     def OptimizeLongtermWMOs(self):
#         # bounded constraint model
#         cmod = [ 
#             {'wmo':i,'wt':j,'lb':k,'ub':l} for i,j,k,l in 
#             list(zip(self.wmo,self.wt,self.lb,self.ub)) 
#         ]
#         
#         # sort by weights
#         cmod_sort = sorted(cmod, key=lambda d: d['wt'])
#         
#         # cmod_sort to nested dict keyed by rank
#         rank = 0
#         cmod_rank = {}
#         while rank < len(cmod_sort):
#             cmod_rank[rank] = [ d for d in cmod_sort if d['wt'] == cmod_sort[rank]['wt'] ]
#             rank += len(cmod_rank[rank])
#         
#         # fill buckets equally by rank
#         for rank in cmod_rank.values():
#             for d in rank:
#                 d['fill'] = 0
#             
#             b = sum([ d['ub'] for d in rank ])        # capacity
#             
#             if self.a > b:                            # determine rank allowance
#                 ra = b
#             else: 
#                 ra = self.a
#             
#             self.a -= ra                              # decrement total allowance
#             
#             i = 0
#             while ra > 0:
#                 if rank[i]['fill'] != rank[i]['ub']:  # fill if ub not met
#                     rank[i]['fill'] += 1
#                     ra -= 1
#                 
#                 if i >= len(rank) - 1:  # cycle through variables sharing rank
#                     i = 0
#                 else:
#                     i += 1
#         
#         # solved system and cost
#         self.solution = [ i for items in cmod_rank.values() for i in items ] 
#         amounts =[ d['fill'] for d in self.solution ]
#         weights = [ d['wt'] for d in self.solution ]
#         self.cost = np.dot(amounts, weights)
#     
#     __OptimizeLongtermWMOs = OptimizeLongtermWMOs
# 
# 
# # run
# opt = Optimizer(wmo=wmo,wt=wt,lb=lb,ub=ub,a=178)
# 
# print('Constrained Model Solution')
# pprint(opt.solution)
# print('---')
# print(f'Cost: {opt.cost}')
# print('---')

