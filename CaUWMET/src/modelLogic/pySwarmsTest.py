import sys
import numpy as np
from pyswarms.single.global_best import GlobalBestPSO
from pyswarms.utils.functions import single_obj as fx

from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
from src.modelLogic.readLongTermWMOsAssumptions import LongTermWMOsAssumptions



class CostOptimizer:

    def __init__(self, inputData: InputData, modelLogic: ModelLogic):
        self.inputData = inputData
        self.modelLogic = modelLogic


x_max = [10]
x_min = [1, 1]
bounds = (x_min, x_max)

# Set-up hyperparameters
options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
optimizer = GlobalBestPSO(n_particles=1, dimensions=1, options=options) #, bounds=bounds) 

cost, pos = optimizer.optimize(objectiveFunction, 1000)

# print("cost:")
# print(cost)
# print("pos:")
# print(pos)
