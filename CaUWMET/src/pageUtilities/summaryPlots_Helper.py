import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from src.colors import colors
from src.globalUtilities import roundValues, load_CSV_data


#---------------------------------------------------------------#
# SUMMARY POSTER FOR VARIABLES INPUT BY PLANNING HORIZON YEAR
#---------------------------------------------------------------#

def displaySummaryPlots(df, explanationText, dataset):
    st.write(explanationText)

    # Set up total demand variables for summary poster plots
    plotInputData = df[['Variable', 'Study Region', 'Contractor', int(st.session_state.futurePlanningYear)]]
    plotInputData = pd.melt(plotInputData, id_vars=['Variable','Contractor', 'Study Region'])
    plotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    vars = df['Variable'].unique()

    varsCount = df['Variable'].nunique()
    numberOfVars = list(range(varsCount))
    selectBoxKey = dataset + " Selectbox"

    allOrSingleContractorSelector = st.selectbox('View ' + dataset + ' data for:', st.session_state.dropDownMenuList, )
    if allOrSingleContractorSelector == 'All Contractors':
        displayPieAndBarPlots(vars, numberOfVars, plotInputData, selectBoxKey)
    else:
        displayDataForOneContractor(allOrSingleContractorSelector, plotInputData)




# Functions to create the plots for all the input assumption pages

def summary_poster(contractor_df, color_dict, piePlotTitle, barPlotTitle, barPlotXAxisTitle):
    #MAKE SUBPLOTS
    fig = make_subplots(
        rows=1, cols=2, 
        column_widths=[0.35, 0.65],
        specs=[[{"type": "pie"}, {"type": "bar"}]],
            # [ {"type":"scatter", "colspan": 2}, None]],
            subplot_titles=(piePlotTitle, 
                            barPlotTitle), 
            vertical_spacing=0.1, horizontal_spacing= 0.1)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=18, family="Times New Roman")

    #PIE
    #data for pie
    pie_data = contractor_df.groupby('Study Region')['Value'].sum()

    fig.add_trace(go.Pie(labels = pie_data.index,
                            values = pie_data.values,
                            hole = 0.4,
                            legendgroup = 'grp1',
                            showlegend=True),
                row = 1, col = 1)
    fig.update_traces(hoverinfo = 'label+percent',
                        textinfo = 'value+percent',
                        textfont_color = 'white',
                        marker = dict(colors = pie_data.index.map(color_dict),
                                    line=dict(color='white', width=1)),
                        row = 1, col = 1)

    #BAR
    pivot_contractor_df = contractor_df.groupby(['Contractor','Type'])['Value'].sum()
    pivot_contractor_df = pivot_contractor_df.unstack()
    pivot_contractor_df.fillna(0, inplace = True)

    #plot params
    labels = pivot_contractor_df.columns

    for i, label_name in enumerate(labels):
        y = pivot_contractor_df.iloc[:,i].index
        fig.add_trace(go.Bar(x = pivot_contractor_df.iloc[:,i], 
                                y = y, orientation = 'h',
                                name = label_name,
                                marker_color = colors,
                                legendgroup = 'grp2',
                                showlegend=True),
                                row = 1, col = 2)
    fig.update_xaxes(title_text = barPlotXAxisTitle, linecolor = 'grey', mirror = True, 
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False, 
                        row = 1, col = 2)
    fig.update_yaxes(side = 'right', linecolor = 'grey', mirror = True, dtick = -5,
                     row = 1, col = 2)

    fig.update_layout( # customize font and margins
                        # barmode = 'stack',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        #plot_bgcolor = '#0E1117',#'black',
                        font_family= 'Times New Roman',#"Helvetica",
                        width=1100,
                        height=900,
                        template = 'plotly_dark',
                        legend=dict(title="", orientation = 'h', y = -0.15,
                                    font=dict(size = 10),
                                    bordercolor = 'LightGrey',
                                    borderwidth=0.5),
                        font=dict(size=12),
                        margin = dict(l = 0, t = 40, r = 40, b = 40, pad = 0.1)
                    )

    return fig

def displayPieAndBarPlots(vars, k_labelValues, plotInputData, selectBoxKey):
    color_map_df = load_CSV_data("src/inputData/color_map_df.csv")
    
    col1, col2 = st.columns(2)
    with col1:
        vars = pd.DataFrame({'Type' : vars}, index = k_labelValues)

        selectVariable = []
        selectVariable.append(st.selectbox('', vars, key= selectBoxKey, help="Select variable to display in plots below."))
        
    plot_df = plotInputData[plotInputData['Type'].isin(selectVariable)]
    barPlotTitle = 'By Contractor'
    piePlotTitle = 'By Study Region'
    barPlotXAxisLabel = str(selectVariable[0])
    
        
    # Setting up color palette dict
    color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))
    fig = summary_poster(plot_df, color_dict, piePlotTitle, barPlotTitle, barPlotXAxisLabel)
    st.write(fig)

    #Display table
    tableData = plotInputData[plotInputData['Type'].isin(selectVariable)]
    tableData = tableData.drop(columns = ['Year'])
    tableData['Value'] = tableData['Value'].apply(roundValues)
    st.table(data = tableData)

def displayDataForOneContractor(contractorName, dataFrameToDisplay):
    filteredDataToOneContractor = dataFrameToDisplay[dataFrameToDisplay['Contractor'].isin([contractorName])]
    filteredDataToOneContractor['Value'] = filteredDataToOneContractor['Value'].apply(roundValues)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=filteredDataToOneContractor['Type'],
        y=filteredDataToOneContractor['Value'],
    ))
    fig.update_layout(title_text = contractorName, title_x=0.45, width = 700)
    fig.update_traces(marker_color=['#EF553B', '#636EFA', '#AB63FA', '#00CC96', '#FFA15A', '#FF33E3', '#3336FF'])
    fig.update_xaxes(title_text="Type")
    fig.update_yaxes(title_text="Value")
    st.write(fig)
    st.table(filteredDataToOneContractor)