
from src.modelLogic.modelLogic import ModelLogic
from src.modelLogic.inputData import InputData
from src.modelLogic.storageUtilities import StorageUtilities
from src.modelLogic.inputDataLocations import InputDataLocations
from src.modelLogic.costOptimizer import CostOptimizer
import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.soo.nonconvex.pso import PSO
from pymoo.optimize import minimize
from src.modelLogic.pyMoo_Optimizer import ShortageCost

# inputData = InputData(InputDataLocations())
# modelLogic = ModelLogic(inputData, StorageUtilities())
# modelLogic.contractor = 'Metropolitan Water District of Southern California'
# print(modelLogic.executeModelLogicForContractor())

# costOptimizer = CostOptimizer(inputData, modelLogic)
# costOptimizer.optimizeWMOs()

# instantiate variables - play with these!
demands = 200
supplies = 100
w = np.array([20,20]) # cost/volume unit weights - rationing in position 0. Needs to be size 8 or 9
 
# instantiate algorithm
algorithm = PSO(pop_size=10) 
 
# instantiate problem
problem = ShortageCost(demands=demands,supplies=supplies,w=w)
 
# optimize
res = minimize(problem,
               algorithm,
               seed=42,
               verbose=False)
 
print("Best solution found: \nVolumes = %s\nCost = %s" % (np.append(problem.rationing([res.X]),res.X).round(3), res.F))
print("Completed running main file")