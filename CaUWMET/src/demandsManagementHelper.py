import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

def load_data(filename):
    df = pd.read_csv(filename, index_col=0)
    return df

def summary_poster(contractor_df, color_dict):
    #MAKE SUBPLOTS
    fig = make_subplots(
        rows=1, cols=2, 
        column_widths=[0.35, 0.65],
        specs=[[{"type": "pie"}, {"type": "bar"}]],
            # [ {"type":"scatter", "colspan": 2}, None]],
            subplot_titles=('Conservation by Study Region', 
                            'Conservation by Year'), 
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
    fig.update_xaxes(title_text = 'Conservation (acre-feet/year)',linecolor = 'grey', mirror = True, 
                        title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1,
                        zeroline = False, 
                        row = 1, col = 2)
    fig.update_yaxes(side = 'right', linecolor = 'grey', mirror = True, dtick = -5,
                     row = 1, col = 2)

    # #SCATTER
    # fig.add_trace(go.Scatter(
    #             x=contractor_df['Contractor'],
    #             y=contractor_df['Rank'],
    #             mode = 'markers',
    #             marker_color = contractor_df['Demands'].map(color_dict),
    #             customdata = contractor_df.loc[:,['Year','Rank']],
    #             # hovertemplate='<b>Year: %{customdata[0]}</b><br>Rank: %{customdata[1]} <br>Title: %{customdata[2]}',
    #             legendgroup = 'grp1',
    #             showlegend=False
    #             ),
    #             row = 2, col = 1
    #             )
    # fig.update_traces(marker = dict(symbol = 'circle', size = 7
    #                                 #,line = dict(color = 'grey', width = 0.5)
    #                                 ),
    #                   name = "",
    #                   row = 2, col =1)
    # fig.update_yaxes(autorange = 'reversed',title = 'Rank',showgrid=True, 
    #                 mirror = True, zeroline = False, linecolor = 'grey', 
    #                 title_standoff = 0, gridcolor = 'grey', gridwidth = 0.1, 
    #                 row = 2, col = 1)
    # fig.update_xaxes(title="",showgrid=True, mirror = True,
    #                 linecolor = 'grey', 
    #                 gridcolor = 'grey', gridwidth = 0.1,
    #                 row = 2, col =1)

    fig.update_layout( # customize font and margins
                        # barmode = 'stack',
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