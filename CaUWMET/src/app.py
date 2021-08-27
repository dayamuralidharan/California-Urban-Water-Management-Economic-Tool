import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, demands, modeloverview, hydrologyassumptions, editcontractors, supplies, systemoperations, results, faq, returnTest, watermanagement
from appsUtilities import fetch_data


app = MultiApp()

col1, col2 = st.columns([5, 1])
with col1:
    st.markdown("""
    # CaUWMET
    California Urban Water Management Economic Tool
    """)

with col2: 
    st.image('dwrlogo.jpg', width=90)

PAGES = {
    "Home": home,
    "Model Overview": modeloverview,
    "Contractor Assumptions": editcontractors,
    "Hydrology Assumptions": hydrologyassumptions,
    "Demand Assumptions": demands,
    "Supply Assumptions": supplies,
    "System Operation Assumptions": systemoperations,
    "Water Management Assumptions": watermanagement,
    "Results": results,
    "FAQ and Support": faq,
    "Return Test": returnTest,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to",list(PAGES.keys()))
page = PAGES[selection]
page.app()

# Initialize session state variables on Demand Assumptions page
if 'totalDemandScenarioRadioButtonIndex' not in st.session_state:
    st.session_state['totalDemandScenarioRadioButtonIndex'] = 0

if 'useBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['useBySectorRadioButtonIndex'] = 0

if 'intExtUseBySectorRadioButtonIndex' not in st.session_state:
    st.session_state['intExtUseBySectorRadioButtonIndex'] = 0

if 'baseLongTermConservationRadioButtonIndex' not in st.session_state:
    st.session_state['baseLongTermConservationRadioButtonIndex'] = 0

if 'totalDemandsdf' not in st.session_state:
    st.session_state['totalDemandsdf'] = fetch_data("inputData/totalDemandsData.csv")