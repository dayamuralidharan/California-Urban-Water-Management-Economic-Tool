from bokeh.plotting import figure, save
from bokeh.models import ColumnDataSource, CustomJS, ColorBar, HoverTool, Label, Div, Span
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

    # hover tool
    # JS callback
    hover_callback = """
    var data = source.data;
    var indices = cb_data.index.indices;
    var alpha = data['alpha'];
    var originalAlpha = data['original_alpha'];
    var size = data['size'];
    var originalSize = data['original_size'];

    // Initialize originalAlpha if not already present
    if (!originalAlpha) {
        data['original_alpha'] = alpha.slice();
        originalAlpha = data['original_alpha'];
    }

    // Reset alpha to original for all circles
    for (var i = 0; i < alpha.length; i++) {
        alpha[i] = originalAlpha[i];
    }

    // Initialize originalSize if not already present
    if (!originalSize) {
        data['original_size'] = size.slice(); 
        originalSize = data['original_size'];
    }

    // Reset size to original for all circles
    for (var i = 0; i < size.length; i++) {
        size[i] = originalSize[i];
    }

    // Set alpha to 1 and size x2 for the top-most hovered circle
    if (indices.length > 0) {
        alpha[indices[0]] = 1.0;
        size[indices[0]] = originalSize[indices[0]] * 2;
    }

    // Update the source data
    source.change.emit();
    """
    
    # HTML tooltip insets
    # https://github.com/bokeh/bokeh/issues/9087
    # tooltips as text
#    tooltips = """
#    <div>
#    Conservation: @{conservation}{0.2f} <br>
#    Surfacewater: @{surface}{0.2f} <br>
#    Groundwater: @{groundwater}{0.2f} <br>
#    Desalination: @{desalination}{0.2f} <br>
#    Recycled: @{recycled}{0.2f} <br>
#    Potable Reuse: @{potable_reuse}{0.2f} <br>
#    Transfers and Exchanges: @{transfers_exchanges}{0.2f} <br>
#    Other Sources: @{other}{0.2f}
#    </div>
#    <style>
#    div.bk-tooltip-content > div > div:not(:last-child) {
#        display:none !important;
#    } 
#    </style>
#    """

    # tooltips as bars
    tooltips = """
    <body>
      <h2>Total Cost: @{cost}</h2>
      <table>
        <tr>
          <td>Conservation</td>
          <td>
            <div style="background-color: lightblue; width: @{conservation_bar}px">
              <strong style="color: black;">@{conservation}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Surfacewater</td>
          <td>
            <div style="background-color: darkorange; width: @{surface_bar}px">
              <strong style="color: black;">@{surface}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Groundwater</td>
          <td>
            <div style="background-color: lightgreen; width: @{groundwater_bar}px">
              <strong style="color: black;">@{groundwater}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Desalination</td>
          <td>
            <div style="background-color: violet; width: @{desalination_bar}px">
              <strong style="color: black;">@{desalination}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Recycled</td>
          <td>
            <div style="background-color: cyan; width: @{recycled_bar}px">
              <strong style="color: black;">@{recycled}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Potable Reuse</td>
          <td>
            <div style="background-color: pink; width: @{potable_reuse_bar}px">
              <strong style="color: black;">@{potable_reuse}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Transfers and Exchanges</td>
          <td>
            <div style="background-color: gray; width: @{transfers_exchanges_bar}px">
              <strong style="color: black;">@{transfers_exchanges}{0.2f}</strong>
            </div>
          </td>
        </tr>
        <tr>
          <td>Other Sources</td>
          <td>
            <div style="background-color: brown; width: @{other}{0.2f}px">
              <strong style="color: black;">@{other}{0.2f}</strong>
            </div>
          </td>
        </tr>
      </table>
    </body>   
    <style>
        div.bk-tooltip-content > div > div:not(:last-child) {
            display:none !important;
        } 
    </style>
    """

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
    contractor = st.selectbox('View Optimization Results for:', st.session_state.dropDownMenuList, )
    st.bokeh_chart = use_file_for_bokeh
    if contractor == 'All Contractors':
        p = "Select a contractor from the dropdown..."
        st.write(p)
    else:
        source = ColumnDataSource(data=df[df['contractor']==contractor])
        
        # shrink the inset bar sizes
        bar_scale = 5
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

