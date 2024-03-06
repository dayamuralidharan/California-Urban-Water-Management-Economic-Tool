from src.multiapp import MultiApp
from src.apps import home, demands, modeloverview, globalAssumptions, supplies, systemoperations, contingencyWatermanagementOptions, longtermWatermanagementOptions, results
from src.globalUtilities import fetch_data, selectSpecifiedRows
import copy

import streamlit as st

## This file is the entry point for the Streamlit app
## Streamlit pages and session state variables are defined here

st.set_page_config(layout="wide")

app = MultiApp()

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
    # CaUWMET
    California Urban Water Management Economic Tool
    """)

with col2: 
    st.image('src/pageUtilities/dwrlogo.jpg', width=90)

PAGES = {
    "Home": home,
    "Model Overview": modeloverview,
    "Input Global Assumptions": globalAssumptions,
    "Input Demand Assumptions": demands,
    "Input Supply Assumptions": supplies,
    "Input System Operation Assumptions": systemoperations,
    "Input Contingency Water Management Options Assumptions": contingencyWatermanagementOptions,
    "Input Long-term Water Management Options Assumptions": longtermWatermanagementOptions,
    "Results": results,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to",list(PAGES.keys()))
page = PAGES[selection]
page.app()

st.sidebar.write("")
inputDataFile = "src/inputData/CaUWMETInputData.xlsx"
outputDataFile_optimizedLTWMOs = "src/outputData/ModelOutputs_Optimal.xlsx"
outputDataFile_zeroedLTWMOS = "src/outputData/ModelOutputs_Zero.xlsx"

#---------------------------------------------------------------#
# INITIALIZE GLOBAL ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
simulationSettings = fetch_data(inputDataFile, sheet_name = 'Simulation Settings', nrows = 3, usecols = 'B')

if 'futurePlanningYear' not in st.session_state:
    st.session_state['futurePlanningYear'] = str(simulationSettings.columns.values[0])

if 'hydrologicReferencePeriodStartYear' not in st.session_state:
    st.session_state['hydrologicReferencePeriodStartYear'] = simulationSettings[simulationSettings.columns.values[0]][0]

if 'hydrologicReferencePeriodEndYear' not in st.session_state:
    st.session_state['hydrologicReferencePeriodEndYear'] = simulationSettings[simulationSettings.columns.values[0]][1]

if 'contractorInfo' not in st.session_state:
    st.session_state['contractorInfo'] = fetch_data(inputDataFile, sheet_name = 'Contractor Assumptions', skiprows = 4, nrows = 44, usecols = 'A:I')

contractorList = selectSpecifiedRows(st.session_state.contractorInfo, 'Include in model', 'Yes')['Contractor']
if 'contractorList' not in st.session_state:
    st.session_state['contractorList'] = contractorList

if 'dropDownMenuList' not in st.session_state: # Drop down menu used on all pages
    st.session_state['dropDownMenuList'] = copy.deepcopy(st.session_state.contractorList)
    st.session_state.dropDownMenuList.loc[0] = "All Contractors"
    st.session_state.dropDownMenuList.sort_index(inplace=True)

hydrologyAssumptions = fetch_data(inputDataFile, sheet_name = 'Hydrology Assumptions', skiprows = 3, nrows = 95, usecols = 'A:AR')
hydrologyAssumptions.reset_index(inplace=True)
hydrologyAssumptions.set_index('Year', inplace = True)
hydrologyAssumptions = hydrologyAssumptions.loc[:, hydrologyAssumptions.columns.isin(contractorList)]

if 'hydrologyAssumptions' not in st.session_state:
    st.session_state['hydrologyAssumptions'] = hydrologyAssumptions

#---------------------------------------------------------------#
# INITIALIZE DEMAND ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_TotalDemands = fetch_data(inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 19, nrows = 135, usecols = 'A:H')
inputData_DemandByUseType = fetch_data(inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 257, nrows = 319, usecols = 'A:H')
inputData_BaseLongTermConservation = fetch_data(inputDataFile, sheet_name = 'Demand Assumptions', skiprows = 582, nrows = 44, usecols = 'A:H')

# #### Initialize input datasets with input data 
if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = inputData_TotalDemands[inputData_TotalDemands['Contractor'].isin(st.session_state.contractorList)]

if 'useByTypedf' not in st.session_state:
    st.session_state['useByTypedf'] = inputData_DemandByUseType[inputData_DemandByUseType['Contractor'].isin(st.session_state.contractorList)]

if 'baseLongTermConservationdf' not in st.session_state:
    st.session_state['baseLongTermConservationdf'] = inputData_BaseLongTermConservation[inputData_BaseLongTermConservation['Contractor'].isin(st.session_state.contractorList)]

#---------------------------------------------------------------#
# INITIALIZE SUPPLY ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_LocalSupplies = fetch_data(inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 11, nrows = 965, usecols = 'A:I')
inputData_SWPCVP = fetch_data(inputDataFile, sheet_name = 'Supply Assumptions', skiprows = 984, nrows = 95, usecols = 'A:AR')

# #### Initialize input datasets with input data 
if 'localSuppliesdf' not in st.session_state:
    st.session_state['localSuppliesdf'] = inputData_LocalSupplies[inputData_LocalSupplies['Contractor'].isin(st.session_state.contractorList)]

if 'swpCVPSuppliesdf' not in st.session_state:
    st.session_state['swpCVPSuppliesdf'] = inputData_SWPCVP


#---------------------------------------------------------------#
# INITIALIZE SYSTEM OPERATIONS ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_excessWaterSwitch = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 6, nrows = 44, usecols = 'A:E')
inputData_surfaceCarryover = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 55, nrows = 229, usecols = 'A:I')
inputData_groundwaterBank = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 289, nrows = 227, usecols = 'A:I')
inputData_storageHedging = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 522, nrows = 181, usecols = 'A:E')
inputData_storageCosts = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 709, nrows = 89, usecols = 'A:I')
inputData_deliveryCosts = fetch_data(inputDataFile, sheet_name = 'System Operations Assumptions', skiprows = 804, nrows = 319, usecols = 'A:I')

# #### Initialize input datasets with input data 
if 'excessWaterSwitch' not in st.session_state:
    st.session_state['excessWaterSwitch'] = inputData_excessWaterSwitch[inputData_excessWaterSwitch['Contractor'].isin(st.session_state.contractorList)]

if 'surfaceCarryover' not in st.session_state:
    st.session_state['surfaceCarryover'] = inputData_surfaceCarryover[inputData_surfaceCarryover['Contractor'].isin(st.session_state.contractorList)]

if 'groundwaterBank' not in st.session_state:
    st.session_state['groundwaterBank'] = inputData_groundwaterBank[inputData_groundwaterBank['Contractor'].isin(st.session_state.contractorList)]

if 'storageHedging' not in st.session_state:
    st.session_state['storageHedging'] = inputData_storageHedging[inputData_storageHedging['Contractor'].isin(st.session_state.contractorList)]

if 'storageCosts' not in st.session_state:
    st.session_state['storageCosts'] = inputData_storageCosts[inputData_storageCosts['Contractor'].isin(st.session_state.contractorList)]

if 'deliveryCosts' not in st.session_state:
    st.session_state['deliveryCosts'] = inputData_deliveryCosts[inputData_deliveryCosts['Contractor'].isin(st.session_state.contractorList)]


#---------------------------------------------------------------#
# INITIALIZE CONTINGENT WMO ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_contingencyConservation = fetch_data(inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 5, nrows = 183, usecols = 'A:I')
inputData_waterMarketTransfers = fetch_data(inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 192, nrows = 458, usecols = 'A:I')
inputData_rationingProgram = fetch_data(inputDataFile, sheet_name = 'Contingent WMOs Assumptions', skiprows = 655, nrows = 183, usecols = 'A:I')

if 'contingencyConservation' not in st.session_state:
    st.session_state['contingencyConservation'] = inputData_contingencyConservation[inputData_contingencyConservation['Contractor'].isin(st.session_state.contractorList)]

if 'waterMarketTransfers' not in st.session_state:
    st.session_state['waterMarketTransfers'] = inputData_waterMarketTransfers[inputData_waterMarketTransfers['Contractor'].isin(st.session_state.contractorList)]

if 'rationingPrograms' not in st.session_state:
    st.session_state['rationingPrograms'] = inputData_rationingProgram[inputData_rationingProgram['Contractor'].isin(st.session_state.contractorList)]


#---------------------------------------------------------------#
# INITIALIZE LONG-TERM WMO ASSUMPTION SESSION STATE VARIABLES
#---------------------------------------------------------------#
inputData_longermWMOVolumes = fetch_data(inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 7, nrows = 366, usecols = 'A:I')
inputData_longtermWMOCosts = fetch_data(inputDataFile, sheet_name = 'Long-term WMOs Assumptions', skiprows = 378, nrows = 734, usecols = 'A:J')

if 'longermWMOVolumes' not in st.session_state:
    st.session_state['longermWMOVolumes'] = inputData_longermWMOVolumes[inputData_longermWMOVolumes['Contractor'].isin(st.session_state.contractorList)]

if 'longtermWMOCosts' not in st.session_state:
    st.session_state['longtermWMOCosts'] = inputData_longtermWMOCosts[inputData_longtermWMOCosts['Contractor'].isin(st.session_state.contractorList)]

#---------------------------------------------------------------#
# INITIALIZE OUTPUT SESSION STATE VARIABLES
#---------------------------------------------------------------#
outputData_optimizationPlotData = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='plotData', usecols='A:O')
outputData_optimizedWMOS = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='longtermWMOOptimizedVolumes', usecols='A:I')

longtermCostOutputs = ['surfaceLongTermWMOCost',
                       'groundwaterLongTermWMOCost',
                       'desalinationLongTermWMOCost', 
                       'recycledLongTermWMOCost',
                       'potableReuseLongTermWMOCost',
                       'XfersAndXchangesLongTermWMOCost',
                       'otherSupplyLongTermWMOCost',
                       'conservationLongTermWMOCost'
                       ]

# Get long-term WMO Cost output data
longTermCostOutputForName = {}
for var in longtermCostOutputs:
    varName = "outputData_" + var
    longTermCostOutputForName[varName] = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name=var)
    longTermCostOutputForName[varName].set_index('Year', inplace=True)
    if var not in st.session_state:
        st.session_state[var] = longTermCostOutputForName[varName]

if 'optimizationPlotData' not in st.session_state:
    st.session_state['optimizationPlotData'] = outputData_optimizationPlotData[outputData_optimizationPlotData['contractor'].isin(st.session_state.contractorList)]

if 'optimizedLongTermWMOs' not in st.session_state:
    st.session_state['optimizedLongTermWMOs'] = outputData_optimizedWMOS


# Get Expected Losses output data
outputData_zeroedLTWMOS = fetch_data(outputDataFile_zeroedLTWMOS, sheet_name='totalAnnualCost')
outputData_zeroedLTWMOS.set_index('Year', inplace=True)
if 'totalAnnualCost_zeroedLongTermWMOs' not in st.session_state:
    st.session_state['totalAnnualCost_zeroedLongTermWMOs'] = outputData_zeroedLTWMOS

outputData_optimizedLTWMOS = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='totalAnnualCost')
outputData_optimizedLTWMOS.set_index('Year', inplace=True)
if 'totalAnnualCost_optimizedLongTermWMOs' not in st.session_state:
    st.session_state['totalAnnualCost_optimizedLongTermWMOs'] = outputData_optimizedLTWMOS

outputData_optimizedLTWMOS = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='totalEconomicLoss')
outputData_optimizedLTWMOS.set_index('Year', inplace=True)
if 'totalEconomicLoss_optimizedLongTermWMOs' not in st.session_state:
    st.session_state['totalEconomicLoss_optimizedLongTermWMOs'] = outputData_optimizedLTWMOS

# Get System Operations and Water Market Transfers output data
outputData_waterTreatmentCosts = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='waterTreatmentCost')
outputData_wastewaterTreatmentCosts = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='wastewaterTreatmentCost')
outputData_distributionCosts = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='distributionCost')
outputData_waterMarketTransferDeliveries = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='waterMarketTransferDeliveries')
outputData_waterMarketTransferCost = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='waterMarketTransferCost')

outputData_waterTreatmentCosts.set_index('Year', inplace=True)
outputData_wastewaterTreatmentCosts.set_index('Year', inplace=True)
outputData_distributionCosts.set_index('Year', inplace=True)
outputData_waterMarketTransferDeliveries.set_index('Year', inplace=True)
outputData_waterMarketTransferCost.set_index('Year', inplace=True)

if 'waterTreatmentCost' not in st.session_state:
    st.session_state['waterTreatmentCost'] = outputData_waterTreatmentCosts

if 'wastewaterTreatmentCost' not in st.session_state:
    st.session_state['wastewaterTreatmentCost'] = outputData_wastewaterTreatmentCosts

if 'distributionCost' not in st.session_state:
    st.session_state['distributionCost'] = outputData_distributionCosts

if 'waterMarketTransferDeliveries' not in st.session_state:
    st.session_state['waterMarketTransferDeliveries'] = outputData_waterMarketTransferDeliveries

if 'waterMarketTransferCost' not in st.session_state:
    st.session_state['waterMarketTransferCost'] = outputData_waterMarketTransferCost

# Get results by water year type output data
outputData_SWPCVPDeliveries = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='SWPCVPSupplyDelivery')
outputData_excessSupply = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='excessSupply')
outputData_unallocatedSWPCVPDeliveries = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='unallocatedSWPCVPDeliveries')
outputData_putSurface = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='putSurface')
outputData_putGroundwater = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='putGroundwater')
outputData_volumeSurfaceCarryover = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='volumeSurfaceCarryover')
outputData_volumeGroundwaterBank = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='volumeGroundwaterBank')
outputData_totalShortage = fetch_data(outputDataFile_optimizedLTWMOs, sheet_name='totalShortage')

outputData_SWPCVPDeliveries.set_index('Year', inplace=True)
outputData_excessSupply.set_index('Year', inplace=True)
outputData_unallocatedSWPCVPDeliveries.set_index('Year', inplace=True)
outputData_putSurface.set_index('Year', inplace=True)
outputData_putGroundwater.set_index('Year', inplace=True)
outputData_volumeSurfaceCarryover.set_index('Year', inplace=True)
outputData_volumeGroundwaterBank.set_index('Year', inplace=True)
outputData_totalShortage.set_index('Year', inplace=True)

if 'SWPCVPSupplyDelivery' not in st.session_state:
    st.session_state['SWPCVPSupplyDelivery'] = outputData_SWPCVPDeliveries

if 'excessSupply' not in st.session_state:
    st.session_state['excessSupply'] = outputData_excessSupply

if 'unallocatedSWPCVPDeliveries' not in st.session_state:
    st.session_state['unallocatedSWPCVPDeliveries'] = outputData_unallocatedSWPCVPDeliveries

if 'putSurface' not in st.session_state:
    st.session_state['putSurface'] = outputData_putSurface

if 'putGroundwater' not in st.session_state:
    st.session_state['putGroundwater'] = outputData_putGroundwater

if 'volumeSurfaceCarryover' not in st.session_state:
    st.session_state['volumeSurfaceCarryover'] = outputData_volumeSurfaceCarryover

if 'volumeGroundwaterBank' not in st.session_state:
    st.session_state['volumeGroundwaterBank'] = outputData_volumeGroundwaterBank

if 'totalShortage' not in st.session_state:
    st.session_state['totalShortage'] = outputData_totalShortage
