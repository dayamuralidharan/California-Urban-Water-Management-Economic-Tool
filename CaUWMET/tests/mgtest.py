# This script explores a closed form solution to optimizing the WMO unit costs
# Also explores ModelLogic class, getting weight vector from WMO UnitCosts
# gist - lines to be run in terminal, not executable
# Mark Green 4/1/23

import numpy as np
from pprint import pprint
from random import sample

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations

random.seed(42)

### ModelLogic Exploration ###

# instantiate CaUWMET model
inputData = InputData(InputDataLocations())
modelLogic = ModelLogic(inputData, StorageUtilities())
modelLogic.contractor = 'Metropolitan Water District of Southern California'

# assign weights
w = []

w += [ modelLogic.inputData.longtermWMOSurfaceUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMOGroundwaterUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMODesalinationUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMORecycledUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMOPotableReuseUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMOTransfersExchangesUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMOOtherSupplyUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

w += [ modelLogic.inputData.longtermWMOConservationUnitCost.loc[modelLogic.contractor][inputData.futureYear] ]

### Bucket Testing ###

# TODO: Need to complete evaluation of inputs and constraints
# randomish 1x8 variables for testing inputs
# could replace wt with w

wt = sample(list(range(1,5))*2, k=8)  # weights
lb = [0]*8                            # lower bound
ub = sample([50,40,30,20]*2, k=8)     # upper bound
wmo = [                               # wmo names
    'Surface',
    'Groundwater',
    'Desalination',
    'Recycled',
    'PotableReuse',
    'TransfersExchanges',
    'OtherSupply',
    'Conservation'
]

# TODO: integrate the lower bound variable into the bucket filling logic
# TODO: verify optimal solutions

class Optimizer:
    '''
    Contraint Model determines optimal WMO allocation by minimizing cost.
    First ranks WMOs by weight then "fills" the lower weighted WMO "buckets" first.
    Tied WMO buckets are filled equally, all buckets filled as constrained by bounds.    
    '''
    def __init__(self, wmo:list, wt:list, lb:list, ub:list, a:int):
        self.wmo = wmo  # names
        self.wt = wt    # weights
        self.lb = lb    # lower bounds
        self.ub = ub    # upper bounds
        self.a = a      # allowance
        self.__OptimizeLongtermWMOs()
    
    def OptimizeLongtermWMOs(self):
        # bounded constraint model
        cmod = [ 
            {'wmo':i,'wt':j,'lb':k,'ub':l} for i,j,k,l in 
            list(zip(self.wmo,self.wt,self.lb,self.ub)) 
        ]
        
        # sort by weights
        cmod_sort = sorted(cmod, key=lambda d: d['wt'])
        
        # cmod_sort to nested dict keyed by rank
        rank = 0
        cmod_rank = {}
        while rank < len(cmod_sort):
            cmod_rank[rank] = [ d for d in cmod_sort if d['wt'] == cmod_sort[rank]['wt'] ]
            rank += len(cmod_rank[rank])
        
        # fill buckets equally by rank
        for rank in cmod_rank.values():
            for d in rank:
                d['fill'] = 0
            
            b = sum([ d['ub'] for d in rank ])        # capacity
            
            if self.a > b:                            # determine rank allowance
                ra = b
            else: 
                ra = self.a
            
            self.a -= ra                              # decrement total allowance
            
            i = 0
            while ra > 0:
                if rank[i]['fill'] != rank[i]['ub']:  # fill if ub not met
                    rank[i]['fill'] += 1
                    ra -= 1
                
                if i >= len(rank) - 1:  # cycle through variables sharing rank
                    i = 0
                else:
                    i += 1
        
        # solved system and cost
        self.solution = [ i for items in cmod_rank.values() for i in items ] 
        amounts =[ d['fill'] for d in self.solution ]
        weights = [ d['wt'] for d in self.solution ]
        self.cost = np.dot(amounts, weights)
    
    __OptimizeLongtermWMOs = OptimizeLongtermWMOs


# run
opt = Optimizer(wmo=wmo,wt=wt,lb=lb,ub=ub,a=178)

print('Constrained Model Solution')
pprint(opt.solution)
print('---')
print(f'Cost: {opt.cost}')
print('---')

