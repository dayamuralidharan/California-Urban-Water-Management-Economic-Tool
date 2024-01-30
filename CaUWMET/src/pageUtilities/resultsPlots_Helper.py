import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
from src.colors import mapColorsByStudyRegion
from src.globalUtilities import roundValues

def displayOptimizedLongTermWMOResults(df):
    #Format dataframe for display
    for i in range (df.shape[1]):
        df.iloc[:,i] = df.iloc[:,i].apply(roundValues)
        old_column_name = df.columns[i]
        new_column_name = df.iloc[0, i]
        df.rename(columns={old_column_name: new_column_name}, inplace=True)
        
    old_column_name = df.columns[0]
    df.rename(columns={old_column_name: 'Contractor'}, inplace=True)
    df = df.drop(0)

    # Define a color blind friendly color palette
    colors = ["#D55E00", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#999999", "#CC79A7"]
    
    # Creating a bar plot using Plotly's graph_objs
    fig = go.Figure()

    # Adding traces for each column
    for i, column in enumerate(df.columns[1:]):
        fig.add_trace(go.Bar(
            x=df['Contractor'],
            y=df[column],
            name=column,
            marker_color = colors[i]
        ))

    # Updating layout
    fig.update_layout(
        title='Optimized Long-term Water Management Option by Contractor',
        xaxis=dict(title='Contractor'),
        yaxis=dict(title='Volume (acre-feet/year)'),
        barmode='stack',
        height=700
    )

    # Show the plot and table
    st.plotly_chart(fig)
    st.table(df)

def displayExpectedLosses(df_optimizedLTWMOs_totalAnnualCost, df_zeroedLTWMOs_totalAnnualCost, df_totalEconomicLoss_optimizedLongTermWMOs):
    #Format dataframes for display
    
    # Format Optimized Avoided Shortage Loss dataframe for display
    optimizedAvoidedShortageLoss = df_optimizedLTWMOs_totalAnnualCost.sub(df_zeroedLTWMOs_totalAnnualCost)
    average_optimizedAvoidedShortageLoss = optimizedAvoidedShortageLoss.mean()
    average_optimizedAvoidedShortageLoss = average_optimizedAvoidedShortageLoss.drop("totalAnnualCost ($)", axis=0)
    average_optimizedAvoidedShortageLoss = pd.DataFrame(average_optimizedAvoidedShortageLoss)
    average_optimizedAvoidedShortageLoss.columns = ['Optimized Avoided Shortage Loss ($)']
    average_optimizedAvoidedShortageLoss['Optimized Avoided Shortage Loss ($)'] = average_optimizedAvoidedShortageLoss['Optimized Avoided Shortage Loss ($)'].apply(roundValues)

    # Format Optimized Total Cost dataframe for display
    df_optimizedLTWMOs_totalAnnualCost = df_optimizedLTWMOs_totalAnnualCost.drop("totalAnnualCost ($)", axis=1)
    df_optimizedLTWMOs_totalAnnualCost = df_optimizedLTWMOs_totalAnnualCost.mean()
    df_optimizedLTWMOs_totalAnnualCost = pd.DataFrame(df_optimizedLTWMOs_totalAnnualCost)
    df_optimizedLTWMOs_totalAnnualCost.columns = ['Optimized Total Cost ($)']
    df_optimizedLTWMOs_totalAnnualCost['Optimized Total Cost ($)'] = df_optimizedLTWMOs_totalAnnualCost['Optimized Total Cost ($)'].apply(roundValues)

    df_totalEconomicLoss_optimizedLongTermWMOs = df_totalEconomicLoss_optimizedLongTermWMOs.drop("totalEconomicLoss ($)", axis=1)
    df_totalEconomicLoss_optimizedLongTermWMOs = df_totalEconomicLoss_optimizedLongTermWMOs.mean()
    df_totalEconomicLoss_optimizedLongTermWMOs = pd.DataFrame(df_totalEconomicLoss_optimizedLongTermWMOs)
    df_totalEconomicLoss_optimizedLongTermWMOs.columns = ['Optimized Economic Loss Due to Shortage']
    df_totalEconomicLoss_optimizedLongTermWMOs['Optimized Economic Loss Due to Shortage'] = df_totalEconomicLoss_optimizedLongTermWMOs['Optimized Economic Loss Due to Shortage'].apply(roundValues)
    #st.table(df_totalEconomicLoss_optimizedLongTermWMOs)
    
    # Format Optimized Economic Loss due to Shortage dataframe for display
    
    tableForDisplay = pd.concat([average_optimizedAvoidedShortageLoss, df_optimizedLTWMOs_totalAnnualCost, df_totalEconomicLoss_optimizedLongTermWMOs], axis = 1)
    st.table(tableForDisplay)

    