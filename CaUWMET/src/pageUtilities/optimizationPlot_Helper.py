# Script defining functions to plot the optimization particles and final result

from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, CustomJS, ColorBar, HoverTool, Label, Span
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
    # get variables and data source
    df = source._property_values['data'] 
    colors = df['colors'][:-1]
    optx = df['x'][-1]
    opty = df['y'][-1]
    xmin = min(df['x'])*0.1
    xmax = max(df['x'])*1.5
    f_zero = max(df['f_zero'])
    ymin = min(df['y'])*0.95
    ymax = max(max(df['y']), f_zero)*1.05
    
    # init plot   
    p = figure(tools="pan,zoom_in,zoom_out,box_zoom,reset,save", 
               toolbar_location="below", toolbar_sticky=False,
               height=600, width=1000,
               x_axis_type='log', x_range=(xmin, xmax),
               y_axis_type='log', y_range=(ymin, ymax))
    
    # zero LTWMO line
    hline = Span(location=f_zero, dimension='width',
                 line_color='red', line_width=2, line_alpha=0.5)
    p.add_layout(hline)
    
    # scatter points
    mapper = linear_cmap(field_name='colors', palette=Viridis256, 
                         low_color='red', low=min(colors), high=max(colors))
 
    scatter = p.scatter(x='x', y='y', size='size', source=source, 
                        fill_alpha='alpha', marker='marker',
                        fill_color=mapper, line_color='black', line_width=0.5)
    
    # plot labels
    optlabel = Label(x=optx, y=opty, 
                     text="Optimized", text_font_size="10pt", 
                     x_offset=0, y_offset=-20)
    p.add_layout(optlabel)
    
    zerolabel = Label(x=xmin, y=f_zero, 
                      text="Cost of 0 LTWMOs", text_font_size="10pt", 
                      x_offset=0, y_offset=0)
    p.add_layout(zerolabel)

    # hover tool via JS callback
    with open("src/pageUtilities/hover_callback.js", 'r') as file:
        hover_callback = file.read()
    
    # HTML tooltip insets
    # https://github.com/bokeh/bokeh/issues/9087
    # tooltips as bars
    with open("src/pageUtilities/tooltips.html", "r") as file:
        tooltips = file.read()

    hover = HoverTool(renderers=[scatter], tooltips=tooltips)
    hover.callback = CustomJS(args={'source': source}, code=hover_callback)
    p.add_tools(hover)
    
    # color bar
    color_bar = ColorBar(color_mapper=mapper['transform'], width=8, location=(0,0),
                         title='Optimizer Iteration')
    p.add_layout(color_bar, 'right')

    # axis labels
    p.yaxis.axis_label = 'Expected Costs and Losses ($ Millions)'
    p.xaxis.axis_label = 'Sum of Longterm Water Management Option Fixed Yield Augmentation (acre-feet/year)'

    return p


# https://github.com/streamlit/streamlit/issues/5858
def use_file_for_bokeh(chart: figure, height=800, width=2000):
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
    contractor = st.selectbox('View Optimization Results for:', st.session_state.dropDownMenuList[1:], )
    st.bokeh_chart = use_file_for_bokeh

    if contractor == 'All Contractors':
        p = "Select a contractor from the dropdown..."
        st.write(p)
    else:
        source = ColumnDataSource(data=df[df['contractor']==contractor])
        
        # shrink the inset bar sizes
        bar_scale = 5
        source.data['shortage_bar'] = source.data['shortage'] / bar_scale
        source.data['conservation_bar'] = source.data['conservation'] / bar_scale
        source.data['surface_bar'] = source.data['surface'] / bar_scale
        source.data['groundwater_bar'] = source.data['groundwater'] / bar_scale
        source.data['desalination_bar'] = source.data['desalination'] / bar_scale
        source.data['recycled_bar'] = source.data['recycled'] / bar_scale
        source.data['potable_reuse_bar'] = source.data['potable_reuse'] / bar_scale
        source.data['transfers_exchanges_bar'] = source.data['transfers_exchanges'] / bar_scale
        source.data['other_bar'] = source.data['other'] / bar_scale

    # different default appearance for optimized value
    alpha_vals = [0.25] * len(source.data['x'])
    alpha_vals[-1] = 0.5
    source.add(alpha_vals, 'alpha')
    
    marker_vals = ['circle'] * len(source.data['x'])
    marker_vals[-1] = 'star'
    source.add(marker_vals, 'marker')

    size_vals = [10] * len(source.data['x'])
    size_vals[-1] = 30
    source.add(size_vals, 'size')

    source.data['colors'][-1] = -1
    
    # get cost and scale y values
    source.data['cost'] = [f"${value:,.0f}" for value in source.data['y']]
    source.data['y'] = [value / 1000000 for value in source.data['y']]
    source.data['f_zero'] = [value / 1000000 for value in source.data['f_zero']]

    p = optimizationPlot(source)
    st.bokeh_chart(p)

