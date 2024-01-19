import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.summaryPlots_Helper import displaySummaryPlots


def app():
# "with" makes sure any memory resources used by this page gets closed so its not taking memory when the page is closed. 
    with opt_echo():

        #Set font styling (currently used for green text)

        st.title('System Operations Assumptions Page')

        st.markdown("""
        :green[There are six groups of system operations assumptions entered into CaUWMET including:  
                    1) Excess project supply management strategy  
                    2) Surface carryover storage operations  
                    3) Groundwater banking storage operations  
                    4) Storage hedging strategy  
                    5) Storage operations costs  
                    6) Delivery costs]""", unsafe_allow_html=True)
        st.write("")
        st.markdown("""
        :green[A detailed description of each of variable is provided in each expandable section below and Sections 3.5 of the model documentation.]""", unsafe_allow_html=True)

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """

        st.markdown(hide, unsafe_allow_html=True)
        
        with st.expander("Excess Project Supply Management Strategy"):
            st.write(excessWaterSwitchExplanationText)
            st.table(st.session_state.excessWaterSwitch)
        
        with st.expander("Surface Carryover Storage Operations"):
            displaySummaryPlots(st.session_state.surfaceCarryover, carryoverStorageExplanationText, "Surface Carryover", "total")
        
        with st.expander("Groundwater Banking Storage Operations"):
            displaySummaryPlots(st.session_state.groundwaterBank, groundwaterBankExplanationText, "Groundwater Banking", "total")
        
        with st.expander("Storage Hedging Strategy"):
            st.write(storageHedgingStrategyExplanationText)
            st.table(st.session_state.storageHedging)
        
        with st.expander("Storage Operations Costs"):
            displaySummaryPlots(st.session_state.storageCosts, storageCostsExplanationText, "Storage Operations Costs", "average")
        
        with st.expander("Delivery Costs"):
            displaySummaryPlots(st.session_state.deliveryCosts, deliveryCostsExplanationText, "Delivery Costs", "average")

excessWaterSwitchExplanationText = 'This input data informs the model on where to put excess SWP and/or CVP water when there is more supply than needed to meet demands. There are three options for how contractors can manage excess SWP: 1) put into a carryover reservoir system, 2) put into a groundwater bank,  3) take the excess SWP and reduce local groundwater pumping, or 4) send the excess SWP supply to the Turn Back Pool. If a contractor has both surface carryover and groundwater banking systems, both can be utilized and the model assumes the groundwater banking system is filled first until full, then the surface carryover system is filled. If both storage systems are full, water is sent to the Turn back Pool.'  
carryoverStorageExplanationText = 'Surface carryover storage operations can involve storage capacities within the region or external to the region. Information entered here include aggregated surface carryover storage operations for each contractor. These include the capacity which can be operated, the initial fill, the annual put capacity, the annual take capacity, and any losses associated with storage operations.' 
groundwaterBankExplanationText = 'Banked groundwater storage operations can involve storage capacities within the region or external to the region. Information entered here include aggregated groundwater bank storage operations for each contractor. These include the capacity which can be operated, the initial fill, the annual put capacity, the annual take capacity, recharge effectiveness, and any losses associated with storage operations. Default initial storage data was collected for dates as close to January 2021 as possible.' 
storageHedgingStrategyExplanationText = 'Takes from carryover can also be constrained by a hedging function within the model.  This hedging function can be assigned to any or all carryover operations but only on a total capacity basis. Note for the Storage Hedging Strategy Switch:  Enter 0 for no hedging stragey on neither surface carryover nor banked groundwater; 1 for hedging only on surface carryover storage; 2 for hedging only on banked groundwater; 3 for hedging on both surface carryover and banked groundwater.' 
storageCostsExplanationText = 'Cost of puts includes the operational costs to place the excess water into storage. Cost of takes includes any operational costs required to pull water from storage, e.g. groundwater pumping. Costs for groundwater banking may vary from base groundwater supply if they are exchanged, or depths to groundwater are different between banking and base supply sources.' 
deliveryCostsExplanationText = "Variable supply costs accounted for in the model include groundwater supply (for existing groundwater sources, new groundwater supplies related to water management options are detailed on the Long-Term Water Management Options page), SWP and/or CVP delivery costs, treatment, and distribution cost assumptions. Groundwater supply costs are input by hydrologic year type, and include a Base Cost assumption, as well as an Incremental Cost assumption, so that the total cost (y) is calculated as: y = mx+b where b = Base Cost and m = Incremental Cost. The delivery cost for SWP M&I deliveries include the variable OMP&R component plus the Off-Aqueduct charge. The delivery cost of CVP water is the O&M rate. Water treatment costs are based on the O&M portion of Metropolitan's 2021 Treatment Surcharge, in 2020 dollars. The surcharge is escalated according to average projected increase from 2021 to 2026 in Met's 2021 10-year financial forecast. Distribution costs are based on the fixed commodity portion (associated with meeting average demands as opposed to peak demand or emergency demand) of the System Access Rate. The cost is escalated to averaged projected increase in the SAR from 2021 to 2030 in Met's 2021 10-year financial forecast."
        
        