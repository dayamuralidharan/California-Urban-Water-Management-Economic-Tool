import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
import numpy as np

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
                                # hovertemplate='<b>Year: %{x}</b><br>#Songs: %{y}',
                                marker_color = pd.Series([label_name]*len(y)).map(color_dict),
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
                        height=700,
                        template = 'plotly_dark',
                        legend=dict(title="", orientation = 'h', y = -0.15,
                                    font=dict(size = 10),
                                    bordercolor = 'LightGrey',
                                    borderwidth=0.5),
                        font=dict(size=12),
                        margin = dict(l = 0, t = 40, r = 40, b = 40)
                    )

    return fig

def displayPieAndBarPlots(vars, varsForLabel, k_labelValues, plotInputData, selectBoxKey, piePlotTitle, barPlotTitle, barPlotXAxisLabel, colors):
    color_map_df = load_data("src/inputData/color_map_df_demands.csv")
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

demandsExplainationText = """Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can 
be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>"""

useByTypeExplainationText = ("""Total demands reported here are by customer sector, including all interior and exterior consumption by sector. Demands are disaggregated by sector to account for 
demand management actions (i.e. conservation and rationing) that target specific sectors, and to account for economic loss assumptions for each sector.
Most residential indoor use includes sanitation, bathing, laundry, cooking and drinking. Most residential outdoor use includes landscape irrigation with other minor outdoor 
uses such as car washing, surface cleaning and similar activities. Industrial water use consists of a wide range of uses including product processing, equipment cooling, 
air conditioning, etc. Commercial water use are associated with the operation of a business or institution including drinking, sanitation and landscape irrigation. 
Commercial water users include service industries, car washes, laundries, and golf courses. Governmental use includes infrastructure uses such as fire suppression, 
street cleaning, line flushing, construction meters, conveyance losses, etc. Agriculture use represents the agricultural related demands within a contractor's service area, such as irrigation. 
Landscape irrigation includes nonresidential irrigation for areas such as schools and parks, but excludes golf courses which are incorporated in the commercial use sector. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")

intExtUseByTypeExplainationText = ("""The model accounts for interior and exterior uses in discerning how conservation and rationing reductions are applie, as well as water available for reuse assumptions. 
Various conservation programs target demand reductions specifically by sector and by interior versus exterior consumption. Rationing programs typically cut back interior 
use at a lower rate than exterior use during shortage events. Adjustments in the use associated with conservation and rationing programs impact the amount of water available 
for reuse and wastewater treatment costs. Interior use that results in water available for reuse includes urban wastewater that is deep percolated from septic tanks, while 
exterior use includes irrigation infiltrated to groundwater systems. More information can be found in the model documentation <add hyperlink to interior and exterior use section of model documentation.>""")

baseLongTermConservationText = ("""Long-term conservation is incorporated into the model as it is an important component of each contractor's long-term strategy to increase 
their water supply reliability. These demand reductions typically include programs that target water use efficiency in each sector, turf replacement programs, 
conservation outreach and communications, reducing conveyance losses, and more. Long-term demand management measures that are adopted by water users can 
have a demand hardening effect. Although they can increase reliability by reducing the size, frequency and duration of shortage events, they can make these 
events relatively more costly when they do occur.  A hardening factor can be set to simulate this effect.>""")