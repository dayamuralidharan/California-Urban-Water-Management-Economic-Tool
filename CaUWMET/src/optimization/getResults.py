# Script defining the GetResults class

import pandas as pd

from src.modelLogic.modelLogic import ModelLogic

### GetResults Data Writer Class ###

class GetResults():
    '''
    This class appends the results of OptimizeWMOs.exportResults and provides a mechanism to export these data to excel. 
    This class is instantiated by first passing the modelLogic - no contractor required.
    The appendResults method, appends successive dicts of 1 x n dataframes.
    These are then written to excel by writeResults
    Note: 
        The dataframes passed to this class should be of the same shape. 
    '''
    def __init__(self, modelLogic=ModelLogic):
        self.aggregatedOutputs = {}
        self.modelLogic = modelLogic
        self.longtermWMO_df = pd.DataFrame(data={'LongtermWMO':[
            'Conservation', 
            'Surface', 
            'Groundwater', 
            'Desalination',
            'Recycled', 
            'Potable Reuse', 
            'Transfers and Exchanges', 
            'Other'
        ]})

        self.shortenSheetNames = {
            'transfersAndExchangesLongTermWMOCost': 'XfersAndXchangesLongTermWMOCost',
            'demandsToBeMetByContingentOptions': 'demandsToBeMetByContingentOpts',
            'contingentConservationReductionVolume': 'contingentConservationReductVol'
        }

        self.indexLabelUnits = {
            'SWPCVPSupplyDelivery': 'acre-feet/year',
            'excessSupply': 'acre-feet/year',
            'unallocatedSWPCVPDeliveries': 'acre-feet/year',
            'putSurface': 'acre-feet/year',
            'putGroundwater': 'acre-feet/year',
            'volumeSurfaceCarryover': 'acre-feet',
            'volumeGroundwaterBank': 'acre-feet',
            'waterMarketTransferDeliveries': '$',
            'totalShortage': 'acre-feet/year',
            # Total Costs
            'totalAnnualCost': '$',
            'totalEconomicLoss': '$',
            'totalReliabilityMgmtCost': '$',
            # WMO Costs
            'waterMarketTransferCost': '$',
            'surfaceLongTermWMOCost': '$',
            'groundwaterLongTermWMOCost': '$',
            'desalinationLongTermWMOCost': '$',
            'recycledLongTermWMOCost': '$',
            'potableReuseLongTermWMOCost': '$',
            'transfersAndExchangesLongTermWMOCost': '$',
            'otherSupplyLongTermWMOCost': '$',
            'conservationLongTermWMOCost': '$',
            # System operations costs
            'swpCVPDeliveryCost': '$',
            'putGroundwaterBankCost': '$',
            'takeGroundwaterBankCost': '$',
            'groundwaterPumpingSavings': '$',
            'waterTreatmentCost': '$',
            'distributionCost': '$',
            'wastewaterTreatmentCost': '$',
            # QAQC data
            'totalAnnualCost': '$',
            'totalEconomicLoss': '$',
            'appliedDemands': 'acre-feet/year',
            'demandsToBeMetByStorage': 'acre-feet/year',
            'volumeGroundwaterBank': 'acre-feet/year',
            'takeGroundwater': 'acre-feet/year',
            'putGroundwater': 'acre-feet/year',
            'demandsToBeMetByContingentOptions': 'acre-feet/year',
            'contingentConservationReductionVolume': 'acre-feet/year',
            'waterMarketTransferDeliveries': 'acre-feet/year',
            'totalShortage': 'acre-feet/year',
        }


    def appendResults(self, output=dict):
        '''
        This method iterates through a dict of 1 x n dataframes and appends them based on their key values to a singular dict with the aggregated results. 
        Essentially, column binding the results for each contractor to a single aggregated dataframe. 
        '''
        if self.aggregatedOutputs == {}:
            self.aggregatedOutputs = { k: pd.DataFrame() for k in output.keys() }
        
        for k in self.aggregatedOutputs.keys():
            if k == 'plotData':
                self.aggregatedOutputs[k] = pd.concat([self.aggregatedOutputs[k],output[k]],axis=0)
            else:
                self.aggregatedOutputs[k] = pd.concat([self.aggregatedOutputs[k],output[k]],axis=1)


    def writeResults(self, filename=str):
        '''
        This method writes the aggregatedOutputs to an excel file of a given name.
        It parses the length of each df and adds a reference column depending on the result type index (as longtermWMO categories or historic hydrology years).
        Note:
            Must be run after .appendResults method!
        '''
        historicHydrologyYear_df = pd.DataFrame(data={'Year': self.modelLogic.inputData.historicHydrologyYears})
        
        with pd.ExcelWriter(path=filename, engine='openpyxl') as writer:
            self.modelLogic.inputData.hydroYearType.to_excel(
                writer, 
                sheet_name="HydroYearType", 
                index_label="Hydrologic Year Type"
            )
            for k, df in self.aggregatedOutputs.items():
                if len(df)==len(self.longtermWMO_df):
                    # TODO: re-index by ltWMO name to remove numbered column names
                    out_df = pd.concat([self.longtermWMO_df,df],axis=1).transpose()
                    out_df.to_excel(writer, sheet_name=k, index_label=k)
                elif len(df)==len(historicHydrologyYear_df):
                    out_df = pd.concat([historicHydrologyYear_df,df],axis=1)
                    if k in self.shortenSheetNames.keys():
                        out_df.to_excel(
                            writer, 
                            sheet_name=self.shortenSheetNames[k], 
                            index_label=k+f" ({self.indexLabelUnits[k]})"
                        )
                    else:
                        out_df.to_excel(writer, sheet_name=k, index_label=k+f" ({self.indexLabelUnits[k]})")
                elif k=='plotData':
                    df.to_excel(writer, sheet_name=k, index=None)