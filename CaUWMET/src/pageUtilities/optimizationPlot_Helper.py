from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, Label, Div
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256

from pandas import DataFrame
import streamlit as st

def optimizationPlot(source: ColumnDataSource):
    """
    This function plots interactive plots of the optimization results in bokeh
    Takes the ColumnSourceData from the optPlotData as the source argument
    """
    # https://github.com/bokeh/bokeh/issues/9087
    TOOLTIPS = """
    <div>
    Conservation: @conservation <br>
    Surfacewater: @surface <br>
    Groundwater: @groundwater <br>
    Desalination: @desalination <br>
    Recycled: @recycled <br>
    Potable Reuse: @potable_reuse <br>
    Transfers and Exchanges: @transfers_exchanges <br>
    Other Sources: @other
    </div>
    <style>
    div.bk-tooltip-content > div > div:not(:first-child) {
        display:none !important;
    } 
    </style>
    """
    colors = source._property_values['data']['colors']
    optx = source._property_values['data']['x'][-1]
    opty = source._property_values['data']['y'][-1]
    mapper = linear_cmap(field_name='colors', palette=Viridis256, low=min(colors), high=max(colors))
    p = figure(tools="pan,zoom_in,zoom_out,box_zoom,reset,save", 
               toolbar_location="below", toolbar_sticky=False,
               x_axis_type='log', y_axis_type='log')

    scatter = p.scatter(x='x', y='y', size=10, source=source, 
                        fill_color=mapper, line_color='black', line_width=0.5)

    scatter2 = p.scatter(x=optx, y=opty, size=11,
                        fill_color='red', line_color='black', line_width=0.5)

    label = Label(x=optx, y=opty, 
                  text="Optimized", text_font_size="12pt", 
                  x_offset=-15, y_offset=-20)
    p.add_layout(label)

    hover = HoverTool(renderers=[scatter], tooltips=TOOLTIPS)
    p.add_tools(hover)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0))
    p.add_layout(color_bar, 'right')

    return p


def displayOptimizationPlot(df: DataFrame):
    """
    Dropdown to selectively filter contractors for the Bokeh plot of optimization results
    If All contractors, it displays a dummy plot prompting to choose a single contractor
    https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart
    """
    contractor = st.selectbox('View Optimization Results for:', st.session_state.dropDownMenuList, )
    if contractor == 'All Contractors':
        p = Div(text="Select a contractor...", width=400, height=50)
        st.bokeh_chart(p)
    else:
        source = ColumnDataSource(data=df)
        p = optimizationPlot(source)
        source.data['contractor'] = source.data[contractor]
        st.bokeh_chart(p)

