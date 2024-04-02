import streamlit as st
from src.globalUtilities import opt_echo
import plotly.express as px

def app():

    with opt_echo():
        st.title('Global Assumption Inputs')

        st.markdown("""
        :green[There are three groups of global assumptions entered into CaUWMET including:  
                    1) Time settings including the future planning horizon year and hydrologic reference period applied in the simulation  
                    2) List of contractors that are included in the model simulation, their study regions, additional details, and Calsim delivery arcs  
                    3) Annual hydrology assumptions for each contractor]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Sections 3.1 and 3.2 of the model documentation.]""", unsafe_allow_html=True)

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)

        with st.expander("Time Settings"):
            st.markdown(""":green[The planning horizon is set to:]""", unsafe_allow_html=True)
            st.write(st.session_state.futurePlanningYear)
            st.markdown(""":green[The hydrologic reference period is set to:]""", unsafe_allow_html=True)
            st.write(str(st.session_state.hydrologicReferencePeriodStartYear) + " - " + str(st.session_state.hydrologicReferencePeriodEndYear))

        with st.expander("Contractor Assumptions"):
            st.write("""The first input assumption CaUWMET’s Python code processes is which contractor(s) to run the simulation and 
            optimization processes for. The contractor list is provided as a table in the “Contractor Assumptions” sheet of the input 
                     spreadsheet file. Users can update this table to add or leave out contractors from a simulation, 
                     modify the study region grouping, update the CalSim delivery arcs, or keep track of other relevant 
                     details associated with a contractor.""")
            data1 = st.session_state.contractorInfo
            #TODO format table
            st.table(data = data1)

        with st.expander("Hydrology Assumptions"):
            st.write("""The water balance is conducted on an annual time step, spanning the period input by the user in the Hydrology 
                     Assumptions input table. An annual time series is entered into the Hydrology Assumptions sheet of the input data 
                     file by the contractor as Wet, Above Normal, Below Normal, Dry, and Critically Dry. The contractor’s total demand 
                     and supply assumptions (except CVP and SWP deliveries) can be input by hydrologic year type and these hydrology 
                     assumptions serve as a point of reference for which demand and supply values to assume for each time step.""")
            
            plotDataMapping = {
                'C':1,
                'D': 2,
                'BN': 3,
                'AN': 4,
                'W': 5
            }



            plotData = st.session_state.hydrologyAssumptions.copy(deep=True)
            plotData.replace(plotDataMapping, inplace=True)
            
            contractorView = st.selectbox("Select contractor to view hydrology assumptions for", st.session_state.contractorList)
            
            fig = px.scatter(plotData, x=st.session_state.hydrologyAssumptions.index, y=contractorView, title='Annual Hydrologic Year Type Assumptions', color=contractorView)
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text='Hydrologic Year Type', tickvals=[1, 2, 3, 4, 5], ticktext=['C', 'D', 'BN', 'AN', 'W'])
            fig.update(layout_coloraxis_showscale=False)

            # Show the interactive plot in your browser
            st.write(fig)
            st.table(data = st.session_state.hydrologyAssumptions)