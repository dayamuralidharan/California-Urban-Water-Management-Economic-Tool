import streamlit as st
from src.globalUtilities import opt_echo

def app():
    
    with opt_echo():

        st.title('Model Overview')
        st.markdown("""State Water Project (SWP) and Central Valley Project (CVP) water contractors (contractors) 
                    are often required to evaluate alternative local, regional, statewide, and federal water management 
                    strategies during water supply planning efforts. 
                    Economic impacts of changes in water service reliability are also generally required as part of an environmental 
                    impact study. 
                    
CaUWMET was developed to leverage major advancements made in open-source optimization methods. The tool 
includes analyses at the contractor level with a primary goal of being publicly available, free, open-source, 
and user friendly so that contractors can tailor the tool for their specific study needs. Its objective is to 
determine the economically optimal urban water management strategy using the least-cost planning criterion. 
This criterion is theoretically described on the bar plot figure below, which shows how two inversely related cost components 
are evaluated by the model: the cost of adding reliability enhancement measures and the expected costs and 
losses without the addition of the enhancements. The objective function minimizes the total of these two costs 
to determine the most economically efficient level of reliability enhancement and level of costs and losses to 
accept from shortage. """)
        
        st.image('src/pageUtilities/CaUWMETObjectiveFunctionGraphic.png', width=650)

        st.markdown("""A high-level overview of the water balance and cost simulation and its linkage to the 
                    optimization tool is summarized in the figure below. The water balance starts with a contractor’s total 
                    demands, which are first met by available base conservation and supply assumptions (that is, existing 
                    conservation and supply programs). Both the demand and supply assumptions vary year to year according to 
                    the sequence of hydrologic conditions that are input for each contractor. Carryover and groundwater banking 
                    storage operations are dynamically simulated as a part of the supplies available to meet demands, or for 
                    storage of CVP/SWP supplies in years they are in excess of the volume needed to meet demands. If there is 
                    still demand after supplies available from storage have been delivered, contingent options can be implemented, 
                    including contingency conservation programs, water market transfers, and lastly, rationing programs.""")

        st.markdown("""Costs are estimated annually in constant 2022 dollars, as a function of the dynamic water balance simulation. Operational costs 
                    are derived for variable cost components only, which are added to the capital and operational costs estimated
                     for the implementation of the new WMOs to determine the total reliability management cost (refer to figure above). The other key cost 
                    component is the economic loss associated with shortage, which is applied only if there is remaining shortage in any time step. 
                    An economic loss function as a result of shortage occurrences is applied, derived from studies of urban price elasticities and 
                    water agency retail rate, also in 2022 dollars. The reliability management cost is added to the economic loss to derive a total 
                    annual cost. This total annual cost is averaged over the entire simulation period.""")

                    
        st.markdown("""The optimization tool minimizes the total annual cost by iterating the water balance and cost simulation over various volume 
                    quantities of the long-term WMOs. The WMO volumes are set by the optimization tool, bounded by a maximum volume
                     assumption, then incorporated into the available base conservation and supply assumptions. The optimization 
                    tool outputs the total cost and losses associated with each long-term WMO volume quantity in each iteration of
                     the optimization space it explores, and ultimately the economically efficient level of reliability enhancement.
""")

        st.image('src/pageUtilities/CaUWMET Approach Overview.png', width=650)

        st.markdown("""The model is configured for all CVP and SWP contractors with urban (that is, municipal and industrial) uses, 
                    shown in the figure below. Additional details on the contractors can be found in the Global Assumptions page.""")
        st.image('src/pageUtilities/AgenciesInCaUWMET.png', width=650)
