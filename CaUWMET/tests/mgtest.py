# This script explores a closed form solution to optimizing the WMO unit costs...
# ...via ranking WMOs by weight and "bucket filling" the lower cost WMOs first
# Tied WMO buckets are filled equally, all filled as constrained by bounds
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

inputData = InputData(InputDataLocations())
modelLogic = ModelLogic(inputData, StorageUtilities())
modelLogic.contractor = 'Metropolitan Water District of Southern California'

### ModelLogic Exploration ###

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
# randomish 1x8 variables
wt = sample(list(range(1,5))*2, k=8)  # weights
lb = [0]*8                           # lower bound
ub = sample([50,40,30,20]*2, k=8)     # upper bound
wmo = [                              # wmo names
    'Surface',
    'Groundwater',
    'Desalination',
    'Recycled',
    'PotableReuse',
    'TransfersExchanges',
    'OtherSupply',
    'Conservation'
]

# lb/ub constraint model cmod
cmod = [ {'wmo':i,'wt':j,'lb':k,'ub':l} for i,j,k,l in list(zip(wmo,wt,lb,ub)) ]

# sort by weights
cmod_sort = sorted(cmod, key=lambda d: d['wt'])

# cmod_sort to nested dict keyed by rank
rank = 0
cmod_rank = {}
while rank < len(cmod_sort):
    cmod_rank[rank] = [ d for d in cmod_sort if d['wt'] == cmod_sort[rank]['wt'] ]
    rank += len(cmod_rank[rank])


# fill buckets equally by rank
a = 178                                 # allowance
for rank in cmod_rank.values():
    for d in rank:
        d['fill'] = 0
    
    b = sum([ d['ub'] for d in rank ])  # capacity
    
    if a > b:                           # determine rank allowance
        ra = b
    else: 
        ra = a
    
    a -= ra                             # decrement total allowance
    
    i = 0
    while ra > 0:
        if rank[i]['fill'] != rank[i]['ub']:  # fill if ub not met
            rank[i]['fill'] += 1
            ra -= 1
        
        if i >= len(rank) - 1:  # cycle through variables sharing rank
            i = 0
        else:
            i += 1


# solved system
cmod_solved = [ i for items in cmod_rank.values() for i in items ]

# cost
amounts =[ d['fill'] for d in cmod_solved ]
weights = [ d['wt'] for d in cmod_solved ]
cost = np.dot(amounts, weights)

print('Constrained Model Solution')
pprint(cmod_solved)
print('---')
print(f'Cost: {cost}')
print('---')

### more basic reprex ###

# fill buckets
# a = 178 # allowance
# for wmo in cmod_sort:
#     if a - wmo['ub'] < 0:
#         wmo['fill'] = a
#         a=0
#     else:
#         wmo['fill'] = wmo['ub']
#         a -= wmo['ub']
# 
# weights = [d['wt'] for d in cmod_sort]
# amounts = [d['fill'] for d in cmod_sort]
# 
# cost = np.dot(weights,amounts)

