import streamlit as st
from src.globalUtilities import opt_echo
from src.pageUtilities.optimizationPlot_Helper import displayOptimizationPlot
from src.pageUtilities.resultsPlots_Helper import displayOptimizedLongTermWMOResults, displayExpectedLosses, displaySystemOpsAndWaterMarketTransferCosts, displayResultsByWaterYearType

def app():
    with opt_echo():      
        st.title('CaUWMET Results Page')
        st.markdown("""<div><span class='font'>
        There are ### results output by CaUWMET including:</span></div>""", unsafe_allow_html=True)
        st.write("")

        #HIDE EXPANDER BORDERS
        hide = """
        <style>
        ul.streamlit-expander {
        border: 0 !important;
        </style>
        """
        st.markdown(hide, unsafe_allow_html=True)

        with st.expander("Optimization Plots"): displayOptimizationPlot(df=st.session_state.optimizationPlotData)

        with st.expander("Long-term Water Management Options Summary"):
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
            displayExpectedLosses(st.session_state.totalAnnualCost_optimizedLongTermWMOs, 
                                  st.session_state.totalAnnualCost_zeroedLongTermWMOs, 
                                  st.session_state.totalEconomicLoss_optimizedLongTermWMOs)
        
        with st.expander("System Operations and Water Market Costs"):
            displaySystemOpsAndWaterMarketTransferCosts(st.session_state.waterTreatmentCost, 
                                                        st.session_state.wastewaterTreatmentCost,
                                                        st.session_state.distributionCost, 
                                                        st.session_state.waterMarketTransferDeliveries, 
                                                        st.session_state.waterMarketTransferCost)
            
        with st.expander("Annual Average Results by Water Year Type"):
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