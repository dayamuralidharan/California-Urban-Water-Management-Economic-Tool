import pandas as pd #TODO only import functionalities needed?
import numpy as np
from src.modelLogic.inputData import InputData
from src.modelLogic.modelLogic import ModelLogic

# Find water management portfolio option that has the least cost

# Loop through incremental volumes of supply/demand options input by user for each contractor - j
# Calculate average annual cost for each contractor - k
# Total average annual cost for all contractors - j
# Fit a curve to total annual average cost from each incremental volume loop
# Calculate global minimum on curve
# Return supply volume increments that correspond to that global min

class CostOptimizer:
    
    def __init__(self, inputData: InputData, modelLogic: ModelLogic):
        self.inputData = inputData
        self.modelLogic = modelLogic

    def loopThroughWmoIncrementalVolumes(self):
        self.objectiveFunction = []
        # Get number of WMO loops
        self.numberOfWMOLoops = int(round(1 / self.inputData.wmoSupplyVolumeIncrement, 0))
        self.numberOfWMOLoopsList = [None] * self.numberOfWMOLoops
        for self.j in range(len(self.numberOfWMOLoopsList)):
            if self.j == 0:
                self.wmoIncrement = self.inputData.wmoSupplyVolumeIncrement
            else:
                self.wmoIncrement = self.inputData.wmoSupplyVolumeIncrement + (self.j * self.inputData.wmoSupplyVolumeIncrement)
            
            self.modelLogic.executeModelLogic(self.wmoIncrement)
            self.objectiveFunction.append(self.modelLogic.systemwideAverageAnnualCost)
            
        self.objectiveFunction = pd.DataFrame(self.objectiveFunction)
        
        #TODO extract to another function?
        self.numberOfPortfolios = range(self.j + 1)
        self.deg = 3 #TODO make degree user defined
        self.polyCoefficients = np.polyfit(self.numberOfPortfolios, self.objectiveFunction, deg = self.deg) 
        def polynomialFunction(x):
            return self.polyCoefficients[0][0]*x**self.deg + self.polyCoefficients[1][0]*x**(self.deg - 1) + self.polyCoefficients[2][0]*x**(self.deg - 2) + self.polyCoefficients[3][0]*x
        
        x0 = range(1,10)
        bounds = [(0, None)] * len(x0)
        #leastCostPoly = minimize(polynomialFunction, x0=x0, bounds = bounds)
        
        #print("objectiveFunction: ", self.objectiveFunction)
        # print(polyCoefficients[1][0])
        #print("leastCostPoly: ", leastCostPoly)
    #def optimize(self):
        #for volume in waterManagementVolumes:
            #self.modelLogic.executeModelLogic(volume)