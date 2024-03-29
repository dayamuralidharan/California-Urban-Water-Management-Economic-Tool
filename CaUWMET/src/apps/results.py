import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.optimizationPlot_Helper import displayOptimizationPlot
from src.pageUtilities.resultsPlots_Helper import displayOptimizedLongTermWMOResults, displayExpectedLosses, displaySystemOpsAndWaterMarketTransferCosts, displayResultsByWaterYearType

def app():
    with opt_echo():      
        st.title('CaUWMET Results Page')
        st.markdown("""
        :green[CaUWMET results are summarized below. Time series results can be found in the "outputData" folder of the model package.]""", unsafe_allow_html=True)
        st.write("")
        st.write("")

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)

        with st.expander("Optimization Plots"):
            st.write(optimizationExpanderText)
            displayOptimizationPlot(df=st.session_state.optimizationPlotData)

        with st.expander("Long-term Water Management Options Summary"):
            st.write(longtermWaterManagementOptionsExpanderText)
            displayOptimizedLongTermWMOResults(st.session_state.optimizedLongTermWMOs, 
                                               st.session_state.surfaceLongTermWMOCost,
                                               st.session_state.groundwaterLongTermWMOCost,
                                               st.session_state.desalinationLongTermWMOCost,
                                               st.session_state.recycledLongTermWMOCost,
                                               st.session_state.potableReuseLongTermWMOCost,
                                               st.session_state.XfersAndXchangesLongTermWMOCost,
                                               st.session_state.otherSupplyLongTermWMOCost,
                                               st.session_state.conservationLongTermWMOCost)

        with st.expander("Expected Losses"):
            st.write(expectedLossesExplanderText)
            displayExpectedLosses(st.session_state.totalAnnualCost_optimizedLongTermWMOs, 
                                  st.session_state.totalAnnualCost_zeroedLongTermWMOs, 
                                  st.session_state.totalEconomicLoss_optimizedLongTermWMOs)
        
        with st.expander("System Operations and Water Market Costs"):
            st.write(systemOperationsAndWaterMarketCostsExpanderText)
            displaySystemOpsAndWaterMarketTransferCosts(st.session_state.waterTreatmentCost, 
                                                        st.session_state.wastewaterTreatmentCost,
                                                        st.session_state.distributionCost, 
                                                        st.session_state.waterMarketTransferDeliveries, 
                                                        st.session_state.waterMarketTransferCost)
            
        with st.expander("Annual Average Results by Water Year Type"):
            st.write(annualAverageByWaterYearTypeExpanderText)
            displayResultsByWaterYearType(st.session_state.SWPCVPSupplyDelivery,
                                          st.session_state.excessSupply,
                                          st.session_state.unallocatedSWPCVPDeliveries,
                                          st.session_state.putSurface,
                                          st.session_state.putGroundwater,
                                          st.session_state.volumeSurfaceCarryover,
                                          st.session_state.volumeGroundwaterBank,
                                          st.session_state.waterMarketTransferDeliveries,
                                          st.session_state.totalShortage,
                                          st.session_state.hydrologyAssumptions,
                                          st.session_state.totalAnnualCost_optimizedLongTermWMOs)
            
optimizationExpanderText = """The plots below provide the resulting total expected cost and losses associated with the implementation of incremental volumes of long-term
water management options, as a result of CaUWMET's optimization method. The x-axis represents the total volume of implemented long-term water management options, which can
consist of a mix of different supply types and conservation that can be viewed by hovering over each dot. The y-axis represents the total annual cost and expected losses, particularly the average
over the simulation period. The colors represent the optimizer's iteration number, which increases as it reaches the optimized point.
"""

longtermWaterManagementOptionsExpanderText = """These results summarize the least-cost portfolio of long-term WMOs based on optimization of 
the total cost function. Volumes for each optimized long-term water management option are provided in thousands of acre-feet."""

expectedLossesExplanderText = """These results summarize components of the total cost function and other related values. These include 
optimized total costs, or the optimized value of the total cost function, and optimized economic loss due to shortage. Also summarized in 
this section is optimized avoided shortage loss, which represents the difference between economic losses due to shortage with and without 
the optimized portfolio of long-term WMOs in place."""

systemOperationsAndWaterMarketCostsExpanderText = """Results summarize the average annual system operations costs, which include water treatment 
and distribution costs. A summary of short-term water market deliveries and costs is also provided in the model results, including total 
deliveries over the 93-year hydrologic record and average water market deliveries over the same period. Total and average water market 
costs are also provided."""

annualAverageByWaterYearTypeExpanderText = """A summary of a range of water management variables is provided by hydrologic water year 
type for three categories: AN and wet years, BN years, and dry and critical years. Variables are summarized on an annual average basis, 
including:  
                    1) SWP/CVP Deliveries: SWP/CVP deliveries summarizes the average annual deliveries to each contractor.  
                    2) Excess (Net) Supply: If SWP/CVP deliveries are in excess of contractor demand, they are considered excess supply and are eligible for carryover storage, groundwater banking, or for returning to the turnback pool.  
                    3) Unallocated SWP/CVP Deliveries: Unallocated CWP/CVP deliveries represent the volume of excess supply that was not stored or delivered due to limited storage capacity or demand for these supplies was lower than the available supply volume entered by the user.  
                    4) Puts to Storage: Puts to storage are determined by each contractor’s storage options, available storage capacity, put capacity, and the amount of excess supply. Average annual puts to storage are summarized in this result field.  
                    5) Water Market Deliveries: Water market deliveries summarize the average annual volume of water that a contractor purchases on the short-term water market.  
                    6) Net User Shortage: Net user shortage is the average expected shortage over the hydrologic record. It is this shortage value that is used to calculate economic losses included in the total loss/cost value.  
                    7) Total Loss/Cost: Total loss/cost represents the total cost function at the optimized point of additional supply reliability, including both the cost of the additional long-term water management option and the economic loss associated with any remaining shortages."""