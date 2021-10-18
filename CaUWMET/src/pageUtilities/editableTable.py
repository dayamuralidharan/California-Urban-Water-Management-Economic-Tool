import streamlit as st
import pandas as pd 
import altair as alt
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def editableTable(dataframeInput, futurePlanningYearInput, setDataframeFunction, dataFrameTitle, dataColumnTitle):
    with st.expander(dataFrameTitle):

        #Infer basic colDefs from dataframe types
        dataframe = dataframeInput
        gb = GridOptionsBuilder.from_dataframe(dataframe[['Variable','Study Region', 'Contractor', str(futurePlanningYearInput), 'Notes']])

        #customize gridOptions
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True, maintainColumnOrder = True)
        
        #TODO make contractor column non-editable, this doesn't seem to be working.
        gb.configure_column("Contractor", type=["nonEditableColumn"])

        gb.configure_column(str(futurePlanningYearInput), type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=0, aggFunc='sum')
        #gb.configure_column("Notes", type=["textColumn"])

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

        with st.spinner("Displaying results..."):
            #displays the bar chart
            chart_data = dataframe.loc[:,['Contractor',str(futurePlanningYearInput)]].assign(source='total')

            if not selected_df.empty:
                selected_data = selected_df.loc[:,['Contractor',str(futurePlanningYearInput)]].assign(source='selection')
                chart_data = pd.concat([chart_data, selected_data])

            #TODO: fix statement so it's not summing all year types, should only show one year type at a time.
            chart_data = pd.melt(chart_data, id_vars=['Contractor','source'], var_name="Year", value_name = dataColumnTitle)

            chart = alt.Chart(data=chart_data).mark_bar().encode(
                x=alt.X("Year", axis=alt.Axis(labelAngle=0)),
                y=alt.Y("sum(" + dataColumnTitle + "):Q", stack=False),
                color=alt.Color('source:N', scale=alt.Scale(domain=['total','selection'])),
            ).configure_axis(
                labelFontSize=13,
                titleFontSize=13
            )

        st.markdown("""
        Users can select multiple agencies from the table above to highlight in the chart below:
        """)

        st.altair_chart(chart, use_container_width=True)