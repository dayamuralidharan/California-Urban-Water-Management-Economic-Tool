# Script defining the GetResults class

import pandas as pd

from src.modelLogic.modelLogic import ModelLogic

### GetResults Data Writer Class ###

class GetResults():
    '''
    This class appends the results of OptimizeWMOs.exportResults and provides a mechanism to export these data to excel. 
    This class is instantiated by first passing a dict of 1xn dataframes.
    The appendResults method, appends successive dicts of 1xn dataframes. 
    Note: 
        The dataframes passed to this class should be of the same shape. 
    '''
    def __init__(self, modelLogic=ModelLogic):
        self.aggregatedOutputs = {}
        self.modelLogic = modelLogic


    def appendResults(self, output=dict):
        if self.aggregatedOutputs == {}:
            d = {'year': self.modelLogic.inputData.historicHydrologyYears}
            self.aggregatedOutputs = { k: pd.DataFrame(data=d) for k in output.keys() }

        for k in self.aggregatedOutputs.keys():
            self.aggregatedOutputs[k] = pd.concat([self.aggregatedOutputs[k], output[k]], axis=1)


    def returnResults(self):
        return self.aggregatedOutputs


