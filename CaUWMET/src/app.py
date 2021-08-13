import streamlit as st
from multiapp import MultiApp
# import your app modules here
from apps import home, demands, demandsmanagement, modeloverview, hydrologyassumptions, editcontractors, supplies, systemoperations, results, faq, returnTest, watermanagement


app = MultiApp()




col1, col2 = st.beta_columns([5, 1])
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
    "Demand Management Assumptions": demandsmanagement,
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