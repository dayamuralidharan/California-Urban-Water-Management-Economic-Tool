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
            # [ {"type":"scatter", "colspan": 2}, None]],
            subplot_titles=('Supplies by Study Region', 
                            'Supplies by Year'), 
                            # 'Demand data by Year'),
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
    fig.update_xaxes(title_text = 'Supplies (acre-feet/year)',linecolor = 'grey', mirror = True, 
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

localSurfaceWaterExplanationText = ("""...""")

groundwaterExplanationText = ("""...""")

desalinationExplanationText = ("""...""")

recyclingExplanationText = ("""...""")

potableReuseExplanationText = ("""...""")

contractualTransfersExplanationText = ("""...""")

otherImportedSuppliesExplanationText = ("""...""")

swpCVPExplanationText = ("""...""")

costBySupplyTypeExplanationText = ("""...""")

supplyPriorityTypeExplanationText = ("""...""")