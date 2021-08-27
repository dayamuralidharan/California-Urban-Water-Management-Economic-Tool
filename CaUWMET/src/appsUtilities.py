import base64
import streamlit as st
import altair as alt
from itertools import cycle
import traceback
from load_css import local_css
from demandsHelper import load_data, summary_poster
from contextlib import contextmanager
from streamlit.hashing import _CodeHasher
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
import pandas as pd

# Class with feature to show source code
# This is a mega-hack!
# And it's also not thread-safe. Don't use this if you have threaded
# code that depends on traceback.extract_stack
class opt_echo:
    def __init__(self):
        self.checkbox = st.sidebar.checkbox("Show source code")

        self.orig_extract_stack = traceback.extract_stack

        if self.checkbox:
            traceback.extract_stack = lambda: self.orig_extract_stack()[:-2]
            self.echo = st.echo()

    def __enter__(self):
        if self.checkbox:
            return self.echo.__enter__()

    def __exit__(self, type, value, traceback):
        if self.checkbox:
            self.echo.__exit__(type, value, traceback)

        import traceback

        traceback.extract_stack = self.orig_extract_stack

def fetch_data(inputDataLocation):
    data = pd.read_csv(inputDataLocation)
    return pd.DataFrame(data)

class editableTableWithFuturePlanningYearsForColumns:

    gb = GridOptionsBuilder.from_dataframe(st.session_state.totalDemandsdf)

    #customize gridOptions
    gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

    gb.configure_column("2025", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
    gb.configure_column("2030", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
    gb.configure_column("2035", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
    gb.configure_column("2040", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
    gb.configure_column("2045", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
    gb.configure_column("Notes", type=["textColumn"])

    selection_mode = 'multiple'
    gb.configure_selection(selection_mode, use_checkbox=False, rowMultiSelectWithClick=False, suppressRowDeselection=False)

    gb.configure_grid_options(domLayout='normal')
    gridOptions = gb.build()

    #Display the grid
    return_mode = 'FILTERED'
    return_mode_value = DataReturnMode.__members__[return_mode]
    update_mode = 'MODEL_CHANGED'
    update_mode_value = GridUpdateMode.__members__[update_mode]

    grid_response = AgGrid(
        st.session_state.totalDemandsdf, 
        gridOptions=gridOptions,
        # height=grid_height, 
        width='100%',
        data_return_mode=return_mode_value, 
        update_mode=update_mode_value,
        # fit_columns_on_grid_load=fit_columns_on_grid_load,
        allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected
        )
    
    st.session_state.totalDemandsdf = grid_response['data']
    selected = grid_response['selected_rows']
    selected_df = pd.DataFrame(selected)

    #downloading the dataframe data to a .csv file
    def download_link(object_to_download, download_filename, download_link_text):
        # Generates a link to download the given object_to_download.

        # object_to_download (str, pd.DataFrame):  The object to be downloaded.
        # download_filename (str): filename and extension of file. e.g. mydata.csv, some_txt_output.txt
        # download_link_text (str): Text to display for download link.

        if isinstance(object_to_download,pd.DataFrame):
            object_to_download = object_to_download.to_csv(index=False)
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
        return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'
        
    if st.button('Download Dataframe to CSV format', key = "Total Demand Scenarios"):
        tmp_download_link = download_link(st.session_state.totalDemandsdf, 'Total_Demand_Scenarios.csv', 'Click here to download your data!')
        st.markdown(tmp_download_link, unsafe_allow_html=True)

    with st.spinner("Displaying results..."):
        #displays the bar chart
        chart_data = st.session_state.totalDemandsdf.loc[:,['Contractor','2025','2030','2035', '2040', '2045']].assign(source='total')

        if not selected_df.empty:
            selected_data = selected_df.loc[:,['Contractor','2025','2030','2035','2040', '2045']].assign(source='selection')
            chart_data = pd.concat([chart_data, selected_data])


        chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name="Water Demand (acre-feet/year)")

        #st.dataframe(chart_data)
        chart = alt.Chart(data=chart_data).mark_bar().encode(
            x=alt.X("Year:O", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("sum(Water Demand (acre-feet/year)):Q", stack=False),
            color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
        ).configure_axis(
            labelFontSize=13,
            titleFontSize=13
        )

    st.markdown("""
    Users can select multiple agencies from the table above to highlight in the chart below:
    """)

    st.altair_chart(chart, use_container_width=True) 