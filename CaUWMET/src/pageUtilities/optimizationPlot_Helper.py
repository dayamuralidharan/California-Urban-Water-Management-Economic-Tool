from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, ColorBar, HoverTool, Label, Div, Span
from bokeh.transform import linear_cmap
from bokeh.palettes import Viridis256
from bokeh.io import output_file

from pandas import DataFrame
import streamlit as st
import streamlit.components.v1 as components


def optimizationPlot(source: ColumnDataSource):
    """
    This function plots interactive plots of the optimization results in bokeh
    Takes the ColumnSourceData from the optPlotData as the source argument
    """
    # https://github.com/bokeh/bokeh/issues/9087
    tooltips = """
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
    df = source._property_values['data'] 
    colors = df['colors']
    optx = df['x'][-1]
    opty = df['y'][-1]
    
    xmin = min(df['x'])*0.1
    xmax = max(df['x'])*1.5
    f_zero = max(df['f_zero'])
    
    mapper = linear_cmap(field_name='colors', palette=Viridis256, low=min(colors), high=max(colors))
    
    p = figure(tools="pan,zoom_in,zoom_out,box_zoom,reset,save", 
               toolbar_location="below", toolbar_sticky=False,
               x_axis_type='log', x_range=(xmin, xmax),
               y_axis_type='log')
    
    hline = Span(location=f_zero, dimension='width',
                 line_color='red', line_width=2, line_alpha=0.5)
    p.add_layout(hline)
    
    scatter = p.scatter(x='x', y='y', size=10, source=source, 
                        fill_color=mapper, line_color='black', line_width=0.5)

    scatter2 = p.scatter(x=optx, y=opty, size=11,
                         fill_color='red', line_color='black', line_width=0.5)

    optlabel = Label(x=optx, y=opty, 
                     text="Optimized", text_font_size="10pt", 
                     x_offset=0, y_offset=-20)
    p.add_layout(optlabel)
    
    zerolabel = Label(x=xmin, y=f_zero, 
                      text="Cost of 0 LTWMOs", text_font_size="10pt", 
                      x_offset=0, y_offset=0)
    p.add_layout(zerolabel)

    hover = HoverTool(renderers=[scatter], tooltips=tooltips)
    p.add_tools(hover)

    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0),
                         title='Optimizer Iteration')
    p.add_layout(color_bar, 'right')

    p.yaxis.axis_label = 'Total Economic Loss ($)'
    p.xaxis.axis_label = 'Sum of Longterm Water Management Option Allocations'

    return p


# https://github.com/streamlit/streamlit/issues/5858
def use_file_for_bokeh(chart: figure, height=800, width=600):
    """
    Streamlit 1.27 only works with Bokeh 2.4.3, so this is used for compatibility.
    """
    output_file('graphics/optimization_plot.html')
    save(chart)
    with open("graphics/optimization_plot.html", 'r', encoding='utf-8') as f:
        html = f.read()
    components.html(html, height=height, width=width)


def displayOptimizationPlot(df: DataFrame):
    """
    Dropdown to selectively filter contractors for the Bokeh plot of optimization results
    If All contractors, it displays a dummy plot prompting to choose a single contractor
    https://docs.streamlit.io/library/api-reference/charts/st.bokeh_chart
    """
    contractor = st.selectbox('View Optimization Results for:', st.session_state.dropDownMenuList, )
    st.bokeh_chart = use_file_for_bokeh
    if contractor == 'All Contractors':
        p = "Select a contractor from the dropdown..."
        st.write(p)
    else:
        source = ColumnDataSource(data=df[df['contractor']==contractor])
        p = optimizationPlot(source)
        st.bokeh_chart(p)

