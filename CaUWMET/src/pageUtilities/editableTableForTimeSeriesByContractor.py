import streamlit as st
import pandas as pd 
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def editableTableForTimeSeriesByContractor(dataframeInput, setDataframeFunction, dataFrameTitle):
    with st.expander(dataFrameTitle):

        #Infer basic colDefs from dataframe types
        contractorList = ['City of Folsom', 'City of Redding', 'City of Roseville', 'City of West Sacramento', 'Yuba City','El Dorado Irrigation District', 
                          'Napa County Flood Control & Water Conservation District', 'Placer County Water Agency', 'Sacramento County Water Agency', 
                          'San Juan Water District', 'Shasta Contractors', 'Solano County Water Agency', 'City of Avenal', 'City of Coalinga',
                          'City of Fresno', 'City of Huron', 'City of Lindsay', 'City of Orange Cove', 'City of Tracy', 'Kern County Water Agency',
                          'Other Friant-Kern M&I Contractors', 'Stockton-East Water District', 'Alameda County Flood Control and Water Conservation District, Zone 7',
                          'Alameda County Water District', 'Contra Costa Water District', 'East Bay Municipal Utilities District', 'San Benito County Water District, Zone 6',
                          'Santa Clara Valley Water District', 'San Luis Obispo County Flood Control & Water Conservation District', 'Santa Barbara County Flood Control & Water Conservation District',
                          'Antelope Valley-East Kern Water Agency', 'Santa Clarita Water Division', 'Coachella Valley Water District', 'Crestline-Lake Arrowhead Water Agency',
                          'Desert Water Agency', 'Metropolitan Water District of Southern California', 'Mojave Water Agency', 'Palmdale Water District & Littlerock Creek Irrigation District',
                          'San Bernardino Valley Municipal Water District', 'San Gabriel Valley Municipal Water District', 'San Gorgonio Pass Water Agency', 'Ventura County Watershed Protection District']
        dataframe = dataframeInput
        gb = GridOptionsBuilder.from_dataframe(dataframe[['Year',*contractorList]])

        #customize gridOptions
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True, maintainColumnOrder = True)
        
        #gb.configure_column('Year', type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')

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
            dataframe, 
            gridOptions=gridOptions,
            # height=grid_height, 
            width='100%',
            data_return_mode=return_mode_value, 
            update_mode=update_mode_value,
            # fit_columns_on_grid_load=fit_columns_on_grid_load,
            allow_unsafe_jscode=True, #Set it to True to allow jsfunction to be injected,
            )
        
        setDataframeFunction(grid_response['data'])
        selected = grid_response['selected_rows']
        selected_df = pd.DataFrame(selected)

        #downloading the dataframe data to a .csv file                
        if st.button('Download Dataframe to CSV format', key = dataFrameTitle):
            tmp_download_link = download_link(dataframe, dataFrameTitle + '.csv', 'Click here to download your data!')
            st.markdown(tmp_download_link, unsafe_allow_html=True)