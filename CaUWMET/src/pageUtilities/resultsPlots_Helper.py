import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
from src.colors import mapColorsByStudyRegion
from src.globalUtilities import roundValues

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
    
    #TODO: make sure colors are the same for each supply source type in bar plot
    formatAndDisplayBarPlots(df_optimizedLTWMOVolumes, 'Optimized Long-term Water Management Option Volume (acre-feet/year)', 'Optimized Long-term Water Management Option Volume by Contractor', 'Volume (acre-feet/year)')
    formatAndDisplayBarPlots(longtermWMOCostTableForDisplay, 'Long-term Water Management Option Annual Average Cost ($/acre-foot)', 'Optimized Long-term Water Management Option Cost by Contractor', 'Cost ($/acre-foot)')
    st.table(df_optimizedLTWMOVolumes)
    st.table(longtermWMOCostTableForDisplay)






def displayExpectedLosses(df_optimizedLTWMOs_totalAnnualCost, df_zeroedLTWMOs_totalAnnualCost, df_totalEconomicLoss_optimizedLongTermWMOs):
    #Format dataframes for display
    
    
    optimizedAvoidedShortageLoss = df_optimizedLTWMOs_totalAnnualCost.sub(df_zeroedLTWMOs_totalAnnualCost)
    
    # Calculate simulation averages and format tables
    average_optimizedAvoidedShortageLoss = formatAverageTables(optimizedAvoidedShortageLoss, "totalAnnualCost ($)", 'Optimized Avoided Shortage Loss ($)')
    average_optimizedLTWMOs_totalAnnualCost = formatAverageTables(df_optimizedLTWMOs_totalAnnualCost, "totalAnnualCost ($)", 'Optimized Total Annual Cost ($)')
    average_totalEconomicLoss_optimizedLongTermWMOs = formatAverageTables(df_totalEconomicLoss_optimizedLongTermWMOs, "totalEconomicLoss ($)", 'Optimized Economic Loss Due to Shortage')
    
    tableForDisplay = pd.concat([average_optimizedAvoidedShortageLoss, average_optimizedLTWMOs_totalAnnualCost, average_totalEconomicLoss_optimizedLongTermWMOs], axis = 1)
    st.table(tableForDisplay)


def displaySystemOpsAndWaterMarketTransferCosts(dfwaterTreatmentCost,
                                                dfdistributionCost, 
                                                dfwaterMarketTransferDeliveries, 
                                                dfwaterMarketTransferCost):
    
    systemOperationsCost = dfwaterTreatmentCost + dfdistributionCost
    systemOperationsCost = systemOperationsCost.drop(['waterTreatmentCost ($)', 'distributionCost ($)'], axis =1)
    average_systemOperationsCost = formatAverageTables(systemOperationsCost, 'skip', 'Average System Operations Cost')
    st.table(average_systemOperationsCost)
    
    total_WaterMarketTransferDeliveries = formatTotalSumTables(dfwaterMarketTransferDeliveries, 'waterMarketTransferDeliveries (acre-feet/year)', 'Total Contingent Water Market Deliveries (acre-feet/year)')
    average_WaterMarketTransferDeliveries = formatAverageTables(dfwaterMarketTransferDeliveries, 'waterMarketTransferDeliveries (acre-feet/year)', 'Average Contingent Water Market Deliveries (acre-feet/year)')
    average_WaterMarketTransferCost = formatAverageTables(dfwaterMarketTransferCost, 'waterMarketTransferCost ($)', 'Average Annual Contingent Water Market Cost ($/year)')
    
    waterMarketTransfers_TableForDisplay = pd.concat([total_WaterMarketTransferDeliveries, average_WaterMarketTransferDeliveries, average_WaterMarketTransferCost], axis=1)
    st.table(waterMarketTransfers_TableForDisplay)



def formatAverageTables(df, oldTitle, newTitle):
    if oldTitle != 'skip':
        df = df.drop(oldTitle, axis =1)
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