import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
from src.colors import mapColorsByStudyRegion
from src.globalUtilities import roundValues

#---------------------------------------------------------------#
# DISPLAY LONG-TERM WATER MANAGEMENT OPTIONS SUMMARY RESULTS
#---------------------------------------------------------------#
def displayOptimizedLongTermWMOResults(df_optimizedLTWMOVolumes, 
                                       surfaceLongTermWMOCost, 
                                       groundwaterLongTermWMOCost, 
                                       desalinationLongTermWMOCost, 
                                       recycledLongTermWMOCost,
                                       potableReuseLongTermWMOCost,
                                       XfersAndXchangesLongTermWMOCost,
                                       otherSupplyLongTermWMOCost,
                                       conservationLongTermWMOCost
                                       ):

    #Format optimized long-term WMO volumes dataframe for display
    for i in range (df_optimizedLTWMOVolumes.shape[1]):
        df_optimizedLTWMOVolumes.iloc[:,i] = df_optimizedLTWMOVolumes.iloc[:,i].apply(roundValues)
        old_column_name = df_optimizedLTWMOVolumes.columns[i]
        new_column_name = df_optimizedLTWMOVolumes.iloc[0, i]
        df_optimizedLTWMOVolumes.rename(columns={old_column_name: new_column_name}, inplace=True)
        
    old_column_name = df_optimizedLTWMOVolumes.columns[0]
    df_optimizedLTWMOVolumes.rename(columns={old_column_name: 'Optimized Long-term Water Management Option Volume (acre-feet/year)'}, inplace=True)
    df_optimizedLTWMOVolumes = df_optimizedLTWMOVolumes.drop(0)

    # Format long-term WMO costs for display
    dfSurfaceLongTermWMOCost = formatAverageTables(surfaceLongTermWMOCost, 'surfaceLongTermWMOCost ($)', 'Surface Average Annual Cost ($/AF)' )
    dfGroundwaterLongTermWMOCost = formatAverageTables(groundwaterLongTermWMOCost,'groundwaterLongTermWMOCost ($)' , 'Groundwater Average Annual Cost ($/AF)' )
    dfDesalinationLongTermWMOCost = formatAverageTables(desalinationLongTermWMOCost, 'desalinationLongTermWMOCost ($)', 'Desalination Average Annual Cost ($/AF)' )
    dfRecycledLongTermWMOCost = formatAverageTables(recycledLongTermWMOCost, 'recycledLongTermWMOCost ($)', 'Recycled Average Annual Cost ($/AF)' )
    dfPotableReuseLongTermWMOCost = formatAverageTables(potableReuseLongTermWMOCost, 'potableReuseLongTermWMOCost ($)', 'Potable Reuse Average Annual Cost ($/AF)' )
    dfXfersAndXchangesLongTermWMOCost = formatAverageTables(XfersAndXchangesLongTermWMOCost,'transfersAndExchangesLongTermWMOCost ($)' , 'Transfers and Exchanges Average Annual Cost ($/AF)' )
    dfOtherSupplyLongTermWMOCost = formatAverageTables(otherSupplyLongTermWMOCost, 'otherSupplyLongTermWMOCost ($)', 'Other Supply Average Annual Cost ($/AF)' )
    dfconservationLongTermWMOCost = formatAverageTables(conservationLongTermWMOCost, 'conservationLongTermWMOCost ($)', 'Conservation Average Annual Cost ($/AF)' )


    longtermWMOCostTableForDisplay = pd.concat([dfSurfaceLongTermWMOCost, 
                                                dfGroundwaterLongTermWMOCost, 
                                                dfDesalinationLongTermWMOCost,
                                                dfRecycledLongTermWMOCost,
                                                dfPotableReuseLongTermWMOCost,
                                                dfXfersAndXchangesLongTermWMOCost,
                                                dfOtherSupplyLongTermWMOCost,
                                                dfconservationLongTermWMOCost], axis = 1)
    
    longtermWMOCostTableForDisplay = longtermWMOCostTableForDisplay.reset_index()
    longtermWMOCostTableForDisplay = longtermWMOCostTableForDisplay.rename(columns={'index': 'Long-term Water Management Option Annual Average Cost ($/acre-foot)'})
    
    # #TODO: make sure colors are the same for each supply source type in bar plot
    # formatAndDisplayBarPlots(df_optimizedLTWMOVolumes, 'Optimized Long-term Water Management Option Volume (acre-feet/year)', 'Optimized Long-term Water Management Option Volume by Contractor', 'Volume (acre-feet/year)')
    # formatAndDisplayBarPlots(longtermWMOCostTableForDisplay, 'Long-term Water Management Option Annual Average Cost ($/acre-foot)', 'Optimized Long-term Water Management Option Cost by Contractor', 'Cost ($/acre-foot)')
    st.table(df_optimizedLTWMOVolumes)
    st.table(longtermWMOCostTableForDisplay)

#---------------------------------------------------------------#
# DISPLAY EXPECTED LOSSES RESULTS
#---------------------------------------------------------------#

def displayExpectedLosses(df_optimizedLTWMOs_totalAnnualCost, df_zeroedLTWMOs_totalAnnualCost, df_totalEconomicLoss_optimizedLongTermWMOs):
    #Format dataframes for display
    
    
    optimizedAvoidedShortageLoss = df_zeroedLTWMOs_totalAnnualCost.sub(df_optimizedLTWMOs_totalAnnualCost)
    
    # Calculate simulation averages and format tables
    average_optimizedAvoidedShortageLoss = formatAverageTables(optimizedAvoidedShortageLoss, "totalAnnualCost ($)", 'Optimized Avoided Shortage Loss ($)')
    average_optimizedLTWMOs_totalAnnualCost = formatAverageTables(df_optimizedLTWMOs_totalAnnualCost, "totalAnnualCost ($)", 'Optimized Total Annual Cost ($)')
    average_totalEconomicLoss_optimizedLongTermWMOs = formatAverageTables(df_totalEconomicLoss_optimizedLongTermWMOs, "totalEconomicLoss ($)", 'Optimized Economic Loss Due to Shortage')
    
    tableForDisplay = pd.concat([average_optimizedAvoidedShortageLoss, average_optimizedLTWMOs_totalAnnualCost, average_totalEconomicLoss_optimizedLongTermWMOs], axis = 1)
    st.table(tableForDisplay)

#---------------------------------------------------------------#
# DISPLAY SYSTEM OPERATIONS AND WATER MARKET COST RESULTS
#---------------------------------------------------------------#
def displaySystemOpsAndWaterMarketTransferCosts(dfwaterTreatmentCost,
                                                dfwastewaterTreatmentCost,
                                                dfdistributionCost, 
                                                dfwaterMarketTransferDeliveries, 
                                                dfwaterMarketTransferCost):
    
    systemOperationsCost = dfwaterTreatmentCost + dfdistributionCost + dfwastewaterTreatmentCost
    systemOperationsCost = systemOperationsCost.drop(['waterTreatmentCost ($)', 'distributionCost ($)'], axis =1)
    
    average_systemOperationsCost = formatAverageTables(systemOperationsCost, 'skip', 'Average System Operations Cost')
    total_WaterMarketTransferDeliveries = formatTotalSumTables(dfwaterMarketTransferDeliveries, 'waterMarketTransferDeliveries (acre-feet/year)', 'Total Contingent Water Market Deliveries (acre-feet/year)')
    average_WaterMarketTransferDeliveries = formatAverageTables(dfwaterMarketTransferDeliveries, 'waterMarketTransferDeliveries (acre-feet/year)', 'Average Contingent Water Market Deliveries (acre-feet/year)')
    average_WaterMarketTransferCost = formatAverageTables(dfwaterMarketTransferCost, 'waterMarketTransferCost ($)', 'Average Annual Contingent Water Market Cost ($/year)')
    
    tableForDisplay = pd.concat([average_systemOperationsCost, total_WaterMarketTransferDeliveries, average_WaterMarketTransferDeliveries, average_WaterMarketTransferCost], axis=1)
    st.table(tableForDisplay)

#---------------------------------------------------------------#
# DISPLAY RESULTS FOR ANNUAL AVERAGES BY WATER YEAR TYPE
#---------------------------------------------------------------#
def displayResultsByWaterYearType(SWPCVPSupplyDelivery,
                                  excessSupply,
                                  unallocatedSWPCVPDeliveries,
                                  putSurface,
                                  putGroundwater,
                                  volumeSurfaceCarryover,
                                  volumeGroundwaterBank,
                                  waterMarketDeliveries,
                                  totalShortage,
                                  hydroYearType, 
                                  totalCost):
    
    
    
    # Calculate total storage variables
    totalStoragePuts = putSurface + putGroundwater
    totalStorageVolume = volumeSurfaceCarryover + volumeGroundwaterBank
    changeInStorageVolume = totalStorageVolume.diff().fillna(0) # Calculates differences between adjacent rows and sets first row to zero

    totalStoragePuts.drop(columns = ['putGroundwater (acre-feet/year)', 'putSurface (acre-feet/year)'], inplace=True)
    changeInStorageVolume.drop(columns=['volumeGroundwaterBank (acre-feet/year)', 'volumeSurfaceCarryover (acre-feet)'], inplace=True)

    # Format variables for tables by year type
    # Annual Average for Above Normal or Wet Year Results
    aboveNormalOrWet_SWPCVPSupplyDelivery = formatVariablesByHydroYearType(SWPCVPSupplyDelivery, hydroYearType, 'SWPCVPSupplyDelivery (acre-feet/year)', ['AN', 'W'], 'SWP and/or CVP Delivery (TAF)')
    aboveNormalOrWet_excessSupply = formatVariablesByHydroYearType(excessSupply, hydroYearType, 'excessSupply (acre-feet/year)', ['AN', 'W'], 'Excess SWP and/or CVP Supply (TAF)')
    aboveNormalOrWet_unallocatedSWPCVPDeliveries = formatVariablesByHydroYearType(unallocatedSWPCVPDeliveries, hydroYearType, 'unallocatedSWPCVPDeliveries (acre-feet/year)', ['AN', 'W'], 'Unallocated SWP and/or CVP Deliveries (TAF)')
    aboveNormalOrWet_storagePuts = formatVariablesByHydroYearType(totalStoragePuts, hydroYearType, 'skip', ['AN', 'W'], 'Puts to Storage (TAF)')
    aboveNormalOrWet_changeInStorageVolume = formatVariablesByHydroYearType(changeInStorageVolume, hydroYearType, 'skip', ['AN', 'W'], 'Change in Storage Volume (TAF)')
    aboveNormalOrWet_waterMarketDeliveries = formatVariablesByHydroYearType(waterMarketDeliveries, hydroYearType, 'waterMarketTransferDeliveries (acre-feet/year)', ['AN', 'W'], 'Water Market Transfer Deliveries (TAF)')
    aboveNormalOrWet_totalShortage = formatVariablesByHydroYearType(totalShortage, hydroYearType, 'totalShortage (acre-feet/year)', ['AN', 'W'], 'Net User Shortage (TAF)')
    aboveNormalOrWet_totalCostAndLoss = formatVariablesByHydroYearType(totalCost, hydroYearType, 'totalAnnualCost ($)', ['AN', 'W'], 'Total Cost and Loss ($/1000)')

    # Annual Average for Below Normal Results
    belowNormal_SWPCVPSupplyDelivery = formatVariablesByHydroYearType(SWPCVPSupplyDelivery, hydroYearType, 'SWPCVPSupplyDelivery (acre-feet/year)', ['BN'], 'SWP and/or CVP Delivery (TAF)')
    belowNormal_excessSupply = formatVariablesByHydroYearType(excessSupply, hydroYearType, 'excessSupply (acre-feet/year)', ['BN'], 'Excess SWP and/or CVP Supply (TAF)')
    belowNormal_unallocatedSWPCVPDeliveries = formatVariablesByHydroYearType(unallocatedSWPCVPDeliveries, hydroYearType, 'unallocatedSWPCVPDeliveries (acre-feet/year)', ['BN'], 'Unallocated SWP and/or CVP Deliveries (TAF)')
    belowNormal_storagePuts = formatVariablesByHydroYearType(totalStoragePuts, hydroYearType, 'skip', ['BN'], 'Puts to Storage (TAF)')
    belowNormal_changeInStorageVolume = formatVariablesByHydroYearType(changeInStorageVolume, hydroYearType, 'skip', ['BN'], 'Change in Storage Volume (TAF)')
    belowNormal_waterMarketDeliveries = formatVariablesByHydroYearType(waterMarketDeliveries, hydroYearType, 'waterMarketTransferDeliveries (acre-feet/year)', ['BN'], 'Water Market Transfer Deliveries (TAF)')
    belowNormal_totalShortage = formatVariablesByHydroYearType(totalShortage, hydroYearType, 'totalShortage (acre-feet/year)', ['BN'], 'Net User Shortage (TAF)')
    belowNormal_totalCostAndLoss = formatVariablesByHydroYearType(totalCost, hydroYearType, 'totalAnnualCost ($)', ['BN'], 'Total Cost and Loss ($/1000)')

    # Annual Average for Dry and Critically Dry Results
    dryCriticallyDry_SWPCVPSupplyDelivery = formatVariablesByHydroYearType(SWPCVPSupplyDelivery, hydroYearType, 'SWPCVPSupplyDelivery (acre-feet/year)', ['D', 'C'], 'SWP and/or CVP Delivery (TAF)')
    dryCriticallyDry_excessSupply = formatVariablesByHydroYearType(excessSupply, hydroYearType, 'excessSupply (acre-feet/year)', ['D', 'C'], 'Excess SWP and/or CVP Supply (TAF)')
    dryCriticallyDry_unallocatedSWPCVPDeliveries = formatVariablesByHydroYearType(unallocatedSWPCVPDeliveries, hydroYearType, 'unallocatedSWPCVPDeliveries (acre-feet/year)', ['D', 'C'], 'Unallocated SWP and/or CVP Deliveries (TAF)')
    dryCriticallyDry_storagePuts = formatVariablesByHydroYearType(totalStoragePuts, hydroYearType, 'skip', ['D', 'C'], 'Puts to Storage (TAF)')
    dryCriticallyDry_changeInStorageVolume = formatVariablesByHydroYearType(changeInStorageVolume, hydroYearType, 'skip', ['D', 'C'], 'Change in Storage Volume (TAF)')
    dryCriticallyDry_waterMarketDeliveries = formatVariablesByHydroYearType(waterMarketDeliveries, hydroYearType, 'waterMarketTransferDeliveries (acre-feet/year)', ['D', 'C'], 'Water Market Transfer Deliveries (TAF)')
    dryCriticallyDry_totalShortage = formatVariablesByHydroYearType(totalShortage, hydroYearType, 'totalShortage (acre-feet/year)', ['D', 'C'], 'Net User Shortage (TAF)')
    dryCriticallyDry_totalCostAndLoss = formatVariablesByHydroYearType(totalCost, hydroYearType, 'totalAnnualCost ($)', ['D', 'C'], 'Total Cost and Loss ($/1000)')

    # Display table for Above Normal or Wet Year Results
    st.markdown("Annual Average for Above Normal or Wet Year Results")
    st.markdown("Note: TAF = thousand acre-feet")
    aboveNormalOrWet_tableForDisplay = pd.concat([aboveNormalOrWet_SWPCVPSupplyDelivery, 
                                 aboveNormalOrWet_excessSupply, 
                                 aboveNormalOrWet_unallocatedSWPCVPDeliveries, 
                                 aboveNormalOrWet_storagePuts, 
                                 aboveNormalOrWet_changeInStorageVolume, 
                                 aboveNormalOrWet_waterMarketDeliveries,
                                 aboveNormalOrWet_totalShortage,
                                 aboveNormalOrWet_totalCostAndLoss], 
                                  axis=1)
    st.table(aboveNormalOrWet_tableForDisplay)

    # Display table for Below Normal Year Results
    st.markdown("Annual Average for Below Normal Results")
    st.markdown("Note: TAF = thousand acre-feet")
    belowNormal_tableForDisplay = pd.concat([belowNormal_SWPCVPSupplyDelivery, 
                                 belowNormal_excessSupply, 
                                 belowNormal_unallocatedSWPCVPDeliveries, 
                                 belowNormal_storagePuts, 
                                 belowNormal_changeInStorageVolume, 
                                 belowNormal_waterMarketDeliveries,
                                 belowNormal_totalShortage,
                                 belowNormal_totalCostAndLoss], 
                                  axis=1)
    st.table(belowNormal_tableForDisplay)

    # Display table for Dry and Critically Dry Results
    st.markdown("Annual Average for Dry and Critically Dry Results")
    st.markdown("Note: TAF = thousand acre-feet")
    dryCriticallyDry_tableForDisplay = pd.concat([dryCriticallyDry_SWPCVPSupplyDelivery, 
                                 dryCriticallyDry_excessSupply, 
                                 dryCriticallyDry_unallocatedSWPCVPDeliveries, 
                                 dryCriticallyDry_storagePuts, 
                                 dryCriticallyDry_changeInStorageVolume, 
                                 dryCriticallyDry_waterMarketDeliveries,
                                 dryCriticallyDry_totalShortage,
                                 dryCriticallyDry_totalCostAndLoss], 
                                  axis=1)
    st.table(dryCriticallyDry_tableForDisplay)


#---------------------------------------------------------------#
# HELPER FUNCTIONS
#---------------------------------------------------------------#
def formatVariablesByHydroYearType(df, hydrodf, columnNameToDrop, hydroYearTypes, newColumnName):
    if columnNameToDrop != 'skip':
        df = df.drop(columnNameToDrop, axis=1)
    dfByYearType = df[hydrodf.apply(lambda x: x.isin(hydroYearTypes))]
    dfByYearType = dfByYearType.mean()
    dfByYearType = dfByYearType / 1000
    dfByYearType = pd.DataFrame(dfByYearType.apply(roundValues))
    dfByYearType.rename(columns={dfByYearType.columns[0]: newColumnName}, inplace=True)
    return dfByYearType

def formatAverageTables(df, columnNameToDrop, newTitle):
    if columnNameToDrop != 'skip':
        df = df.drop(columnNameToDrop, axis =1)
    df = pd.DataFrame(df.mean())
    df.columns = [newTitle]
    df[newTitle] = df[newTitle].apply(roundValues)
    return df

def formatTotalSumTables(df, oldTitle, newTitle):
    if oldTitle != 'skip':
        df = df.drop(oldTitle, axis =1)
    df = pd.DataFrame(df.sum())
    df.columns = [newTitle]
    df[newTitle] = df[newTitle].apply(roundValues)
    return df

def formatAndDisplayBarPlots(df, title1, title2, title3):

    # Define a color blind friendly color palette
    colors = ["#00CC96", "#AE62E5", "#EF553B", "#636EFA", "#FFA15A", "#19D3F3", "#999999", "#FF6692"]
    
    
    # Creating a bar plot using Plotly's graph_objs
    fig = go.Figure()

    # Adding traces for each column
    for i, column in enumerate(df.columns[1:]):
        fig.add_trace(go.Bar(
            x=df[title1],
            y=df[column],
            name=column,
            marker_color = colors[i]
        ))

    # Updating layout
    fig.update_layout(
        title=title2,
        xaxis=dict(title='Contractor'),
        yaxis=dict(title=title3),
        barmode='stack',
        height=700
    )

    # Show the plot and table
    return st.plotly_chart(fig)