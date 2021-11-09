import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np
from colors import colors

def load_data(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def summary_poster(contractor_df, color_dict, piePlotTitle, barPlotTitle, barPlotXAxisTitle):
    #MAKE SUBPLOTS
    fig = make_subplots(
        rows=1, cols=2, 
        column_widths=[0.35, 0.65],
        specs=[[{"type": "pie"}, {"type": "bar"}]],
            subplot_titles=(piePlotTitle, 
                            barPlotTitle), 
            vertical_spacing=0.1, horizontal_spacing= 0.04)

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

    #STACKED BAR
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
                                # hovertemplate='<b>Year: %{x}</b><br>#Songs: %{y}',
                                marker_color = colors,
                                legendgroup = 'grp2',
                                showlegend=True),
                                row = 1, col = 2)
    fig.update_xaxes(title_text = barPlotXAxisTitle,linecolor = 'grey', mirror = True, 
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False, 
                        row = 1, col = 2)
    fig.update_yaxes(side = 'right', linecolor = 'grey', mirror = True, dtick = -5,
                     row = 1, col = 2)

    fig.update_layout( # customize font and margins
                        barmode = 'stack',
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        #plot_bgcolor = '#0E1117',#'black',
                        font_family= 'Times New Roman',#"Helvetica",
                        width=1400,
                        height=700,
                        template = 'plotly_dark',
                        legend=dict(title="", orientation = 'v', x = 1.45,
                                    font=dict(size = 10),
                                    bordercolor = 'LightGrey',
                                    borderwidth=0.5),
                        font=dict(size=12),
                        margin = dict(l = 40, t = 40, r = 40, b = 40)
                    )
    
    return fig

def displayPieAndBarPlots(vars, varsForLabel, k_labelValues, plotInputData, selectBoxKey, piePlotTitle, barPlotTitle, barPlotXAxisLabel, colors):
    color_map_df = load_data("inputData/color_map_df_demands.csv")
    plotInputData['k_labels'] = np.select(varsForLabel, k_labelValues)
    
    plotInputData['colors'] = np.select(varsForLabel, colors) 

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### **Select Variable to Display in Plot Below:**")
        
        vars = pd.DataFrame({'Type' : vars}, index = k_labelValues)

        selectVariable = []
        selectVariable.append(st.selectbox('', vars, key= selectBoxKey, help="Select variable to display in plots below."))
        
        plot_df = plotInputData[plotInputData['Type'].isin(selectVariable)]

    # Setting up color palette dict
    color_dict = dict(zip(color_map_df['Study Region'], color_map_df['colors']))
    fig = summary_poster(plot_df, color_dict, piePlotTitle, barPlotTitle, barPlotXAxisLabel)
    st.write(fig)

localSuppliesExplanationText = ("""Local supply data includes all existing and planned sources of water available for 
                                each supplier excluding supplies sourced from the State Water and Central Valley Projects (SWP and CVP). 
                                SWP and CVP supplies are input separately via the second variable on this page. Local supplies are input for
                                anticipated availability under a normal or better water year, single dry, and multiple dry year conditions. Local supplies
                                are input separately by type to account for the varying costs associated with each supply type. 
                                Default data was developed utilizing information reported in each supplier's 2020 Urban Water Management Plan.
                                Local supplies reported on this page should only include verified supplies. Any local supplies that are still 
                                undergoing feasibility assessments should be input in the Water Management Options Assumptions page.""")

swpCVPExplanationText = ("""State Water Project (SWP) and Central Valley Project (CVP) sourced supplies are input separately from the local supplies to account for
                         the operational costs associated with each. Default data for these supplies were developed from CA DWR and U.S. Bureau of Reclamation's Calsim II 
                         and Calsim 3 water resources planning models. These
                         models. These models simulate operations of the SWP and CVP and much of the water resources infrastructure in the Central 
                         Valley of California and the Sacramento-San Joaquin Delta regions. The default Calsim II dataset was developed from the U.S. Bureau's 2020 Benchmark study
                         which simulated delivery capabilities under 1922 - 2003 historic hydrologic conditions. The default Calsim 3 dataset was developed from DWR's <TBD> study
                         which simulated delivery capabilities under 1922 - 2015 historic hydrologic conditions. More details on these Calsim models and associated studies can be found
                         in Section X of the model documentation.""")

costBySupplyTypeExplanationText = ("""...""")

supplyPriorityTypeExplanationText = ("""...""")