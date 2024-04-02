import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots

def app():

    with opt_echo():

        st.title('Contingency Water Management Options Assumptions')
        st.markdown("""
        :green[There are three groups of contingency water management option assumptions entered into CaUWMET including:  
                    1) Contingency conservation campaigns  
                    2) Water market transfers  
                    3)  Rationing programs]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Section 3.6.2 of the model documentation.]""", unsafe_allow_html=True)
        
        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Contingency Conservation Campaigns"):
            displaySummaryPlots(st.session_state.contingencyConservation, contingencyConservationExplanationText, "Contingency Conservation Campaigns", "average")
        
        with st.expander("Water Market Transfers"):
            displaySummaryPlots(st.session_state.waterMarketTransfers, waterMarketTransfersExplanationText, "Water Market Transfers", "average")

        with st.expander("Rationing Programs"):
            displaySummaryPlots(st.session_state.rationingPrograms, rationingProgramExplanationText, "Rationing Programs", "average")

contingencyConservationExplanationText = """The model assumes contingency conservation campaigns are initiated whenever there is a 
shortage in available water supplies compared to current quantity demanded or in response to low carryover storage availability. 
Here users define the sse reduction with contingency conservation campaign,  the ratio of that reduction that is cut from interior 
use, the cost for contingency conservation campaigns, the demand hardening adjustment factor, population, 
and storage volume threshold to trigger contingency conservation management options."""

waterMarketTransfersExplanationText = ("""If supplies are less than demand in the dry or critical year type, and the marginal 
                                       water supply for the provider is a water transfer, then end-use shortages up to a percentage
                                        are applied first. Then, providers can acquire transfer supplies to eliminate shortfalls 
                                       up to the maximum transfer limit indicated on the System Operations Assumptions page. 
                                       These supplies have unit costs specific to the dry and critical condition. Thereafter it 
                                       is assumed that end-users must take additional shortage. 
                                       Water Transfer costs represent the cost each water district faces in acquiring water through a market transfer in a
                                        given water year. Costs are based on the unit values developed for the Water Storage 
                                       Investment Program's technical guidance, which modelled values by region (Sacramento Valley,
                                        Delta Export, Friant Service Area, and Eastside San Joaquin), water year type (wet, above 
                                       normal, below normal, dry, and critical), and future condition (2030, and 2045 after full 
                                       SGMA implementation). In the model, years 2035 and 2040 are interpolated values between the 
                                       2030 and 2045 future conditions. 2025 unit values are set at 2030 values to avoid 
                                       extrapolation. Single dry year or wetter transfer costs are set at the dry year unit value, 
                                       and multi-dry year transfer costs are set at the critical year unit value.>""")


rationingProgramExplanationText = ("""“Rationing” is shorthand for a water allocation method designed to minimize the overall 
                                   economic costs of a shortage by “balancing” the costs of forgone use among customer classes. 
                                   The allocation method in LCPSIM is intended to mimic water agencies by maintaining provisions for 
                                   exemptions due to serious adverse economic impacts, especially for businesses. 
                                   Here the user can enter the cost of a rationing program, the storage volume threshold to
                                    trigger rationing program, Cut Ratios by Use Type, Elasticity Variables and Upper and Lower 
                                   Loss Boundaries, and Retail Prices. 
                                   Retail prices are from the American Water Works Association 2020 California Water Survey, 
                                   where available. Those agencies not covered in the survey were collected from rate information 
                                   published on agency websites. All costs are in 2020 dollars, and presented as cost per acre-foot.>""")