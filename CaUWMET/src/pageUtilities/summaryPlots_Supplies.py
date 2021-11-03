from suppliesHelper import displayPieAndBarPlots, localSurfaceWaterExplanationText, groundwaterExplanationText, desalinationExplanationText, recyclingExplanationText, potableReuseExplanationText, contractualTransfersExplanationText, otherImportedSuppliesExplanationText, swpCVPExplanationText, costBySupplyTypeExplanationText, supplyPriorityTypeExplanationText
import streamlit as st
import pandas as pd 

def displaySummaryPlots(): 
    st.header("Supply Assumptions Overview")
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR LOCAL SURFACE WATER
    #---------------------------------------------------------------#

    st.subheader("Local Surface Water Scenarios")
    st.write(localSurfaceWaterExplanationText)

    # Set up total demand variables for summary poster plots
    localSurfaceWaterPlotInputData = st.session_state.localSurfaceWaterdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    localSurfaceWaterPlotInputData = pd.melt(localSurfaceWaterPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    localSurfaceWaterPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    localSurfaceWaterVars = ['Surface']

    localSurfaceWaterVarsForLabel = [
        localSurfaceWaterPlotInputData['Type'] == localSurfaceWaterVars[0],
        ]
    localSurfaceWaterNumberOfVars = [0]
    localSurfaceWaterBoxKey = "Supplies Selectbox"
    localSurfaceWaterPiePlotLabel = "Supplies by Study Region"
    localSurfaceWaterBarPlotLabel = "Supplies by Contractor"
    localSurfaceWaterBarPlotXAxisLabel = "Supplies (acre-feet/year)"
    localSurfaceWaterColors = ['#F63366']

    displayPieAndBarPlots(localSurfaceWaterVars, localSurfaceWaterVarsForLabel, localSurfaceWaterNumberOfVars, localSurfaceWaterPlotInputData, localSurfaceWaterBoxKey, localSurfaceWaterPiePlotLabel, localSurfaceWaterBarPlotLabel, localSurfaceWaterBarPlotXAxisLabel, localSurfaceWaterColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR GROUNDWATER
    #---------------------------------------------------------------#

    st.subheader("Groundwater Scenarios")
    st.write(groundwaterExplanationText)

    # Set up total demand variables for summary poster plots
    groundwaterPlotInputData = st.session_state.groundwaterdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    groundwaterPlotInputData = pd.melt(groundwaterPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    groundwaterPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    groundwaterVars = ['Groundwater']

    groundwaterVarsForLabel = [
        groundwaterPlotInputData['Type'] == groundwaterVars[0],
        ]
    groundwaterNumberOfVars = [0]
    groundwaterBoxKey = "Groundwater Supplies Selectbox"
    groundwaterPiePlotLabel = "Groundwater Supplies by Study Region"
    groundwaterBarPlotLabel = "Groundwater Supplies by Contractor"
    groundwaterBarPlotXAxisLabel = "Groundwater (acre-feet/year)"
    groundwaterColors = ['#F63366']

    displayPieAndBarPlots(groundwaterVars, groundwaterVarsForLabel, groundwaterNumberOfVars, groundwaterPlotInputData, groundwaterBoxKey, groundwaterPiePlotLabel, groundwaterBarPlotLabel, groundwaterBarPlotXAxisLabel, groundwaterColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR DESALINATION
    #---------------------------------------------------------------#

    st.subheader("Desalination Scenarios")
    st.write(desalinationExplanationText)

    # Set up total demand variables for summary poster plots
    desalinationPlotInputData = st.session_state.desalinationdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    desalinationPlotInputData = pd.melt(desalinationPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    desalinationPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    desalinationVars = ['Desalination']

    desalinationVarsForLabel = [
        desalinationPlotInputData['Type'] == desalinationVars[0],
        ]
    desalinationNumberOfVars = [0]
    desalinationBoxKey = "Desalination Supplies Selectbox"
    desalinationPiePlotLabel = "Desalination Supplies by Study Region"
    desalinationBarPlotLabel = "Desalination Supplies by Contractor"
    desalinationBarPlotXAxisLabel = "Desalination (acre-feet/year)"
    desalinationColors = ['#F63366']

    displayPieAndBarPlots(desalinationVars, desalinationVarsForLabel, desalinationNumberOfVars, desalinationPlotInputData, desalinationBoxKey, desalinationPiePlotLabel, desalinationBarPlotLabel, desalinationBarPlotXAxisLabel, desalinationColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR RECYCLING
    #---------------------------------------------------------------#

    st.subheader("Recycling Scenarios")
    st.write(recyclingExplanationText)

    # Set up total demand variables for summary poster plots
    recyclingPlotInputData = st.session_state.recyclingdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    recyclingPlotInputData = pd.melt(recyclingPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    recyclingPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    recyclingVars = ['Recycle']

    recyclingVarsForLabel = [
        recyclingPlotInputData['Type'] == recyclingVars[0],
        ]
    recyclingNumberOfVars = [0]
    recyclingBoxKey = "Recycling Supplies Selectbox"
    recyclingPiePlotLabel = "Recycling Supplies by Study Region"
    recyclingBarPlotLabel = "Recycling Supplies by Contractor"
    recyclingBarPlotXAxisLabel = "Recycling (acre-feet/year)"
    recyclingColors = ['#F63366']

    displayPieAndBarPlots(recyclingVars, recyclingVarsForLabel, recyclingNumberOfVars, recyclingPlotInputData, recyclingBoxKey, recyclingPiePlotLabel, recyclingBarPlotLabel, recyclingBarPlotXAxisLabel, recyclingColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR POTABLE REUSE
    #---------------------------------------------------------------#

    st.subheader("Potable Reuse Scenarios")
    st.write(potableReuseExplanationText)

    # Set up total demand variables for summary poster plots
    potableReusePlotInputData = st.session_state.potableReusedf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    potableReusePlotInputData = pd.melt(potableReusePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    potableReusePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    potableReuseVars = ['Potable Reuse']

    potableReuseVarsForLabel = [
        potableReusePlotInputData['Type'] == potableReuseVars[0],
        ]
    potableReuseNumberOfVars = [0]
    potableReuseBoxKey = "Potable Reuse Supplies Selectbox"
    potableReusePiePlotLabel = "Potable Reuse Supplies by Study Region"
    potableReuseBarPlotLabel = "Potable Reuse Supplies by Contractor"
    potableReuseBarPlotXAxisLabel = "Potable Reuse (acre-feet/year)"
    potableReuseColors = ['#F63366']

    displayPieAndBarPlots(potableReuseVars, potableReuseVarsForLabel, potableReuseNumberOfVars, potableReusePlotInputData, potableReuseBoxKey, potableReusePiePlotLabel, potableReuseBarPlotLabel, potableReuseBarPlotXAxisLabel, potableReuseColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR CONTRACTUAL TRANSFERS
    #---------------------------------------------------------------#

    st.subheader("Contractual Transfers Scenarios")
    st.write(contractualTransfersExplanationText)

    # Set up total demand variables for summary poster plots
    contractualTransfersPlotInputData = st.session_state.contractualTransfersdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    contractualTransfersPlotInputData = pd.melt(contractualTransfersPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    contractualTransfersPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    contractualTransfersVars = ['Contractual Transfers']

    contractualTransfersVarsForLabel = [
        contractualTransfersPlotInputData['Type'] == contractualTransfersVars[0],
        ]
    contractualTransfersNumberOfVars = [0]
    contractualTransfersBoxKey = "Contractual Transfer Supplies Selectbox"
    contractualTransfersPiePlotLabel = "Contractual Transfer Supplies by Study Region"
    contractualTransfersBarPlotLabel = "Contractual Transfer Supplies by Contractor"
    contractualTransfersBarPlotXAxisLabel = "Contractual Transfers(acre-feet/year)"
    contractualTransfersColors = ['#F63366']

    displayPieAndBarPlots(contractualTransfersVars, contractualTransfersVarsForLabel, contractualTransfersNumberOfVars, contractualTransfersPlotInputData, contractualTransfersBoxKey, contractualTransfersPiePlotLabel, contractualTransfersBarPlotLabel, contractualTransfersBarPlotXAxisLabel, contractualTransfersColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR OTHER IMPORTED SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("Other Imported Supplies Scenarios")
    st.write(otherImportedSuppliesExplanationText)

    # Set up total demand variables for summary poster plots
    otherImportedSuppliesPlotInputData = st.session_state.otherImportedSuppliesdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    otherImportedSuppliesPlotInputData = pd.melt(otherImportedSuppliesPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    otherImportedSuppliesPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    otherImportedSuppliesVars = ['Other Imported']

    otherImportedSuppliesVarsForLabel = [
        otherImportedSuppliesPlotInputData['Type'] == otherImportedSuppliesVars[0],
        ]
    otherImportedSuppliesNumberOfVars = [0]
    otherImportedSuppliesBoxKey = "Other Imported Supplies Selectbox"
    otherImportedSuppliesPiePlotLabel = "Other Imported Supplies by Study Region"
    otherImportedSuppliesBarPlotLabel = "Other Imported Supplies by Contractor"
    otherImportedSuppliesBarPlotXAxisLabel = "Other Imported Supplies (acre-feet/year)"
    otherImportedSuppliesColors = ['#F63366']

    displayPieAndBarPlots(otherImportedSuppliesVars, otherImportedSuppliesVarsForLabel, otherImportedSuppliesNumberOfVars, otherImportedSuppliesPlotInputData, otherImportedSuppliesBoxKey, otherImportedSuppliesPiePlotLabel, otherImportedSuppliesBarPlotLabel, otherImportedSuppliesBarPlotXAxisLabel, otherImportedSuppliesColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SW CVP SUPPLIES
    #---------------------------------------------------------------#

    st.subheader("SWP CVP Supplies Scenarios")
    st.write(swpCVPExplanationText)

    # Set up total demand variables for summary poster plots
    swpCVPPlotInputData = st.session_state.swpCVPSuppliesdf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    swpCVPPlotInputData = pd.melt(swpCVPPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    swpCVPPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    swpCVPVars = ['SWP CVP']

    swpCVPVarsForLabel = [
        swpCVPPlotInputData['Type'] == swpCVPVars[0],
        ]
    swpCVPNumberOfVars = [0]
    swpCVPBoxKey = "SWP CVP Supplies Selectbox"
    swpCVPPiePlotLabel = "SWP CVP Supplies by Study Region"
    swpCVPBarPlotLabel = "SWP CVP Supplies by Contractor"
    swpCVPBarPlotXAxisLabel = "SWP CVP Supplies (acre-feet/year)"
    swpCVPColors = ['#F63366']

    displayPieAndBarPlots(swpCVPVars, swpCVPVarsForLabel, swpCVPNumberOfVars, swpCVPPlotInputData, swpCVPBoxKey, swpCVPPiePlotLabel, swpCVPBarPlotLabel, swpCVPBarPlotXAxisLabel, swpCVPColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR COST BY SUPPLY TYPE
    #---------------------------------------------------------------#

    st.subheader("Cost by Supply Type Scenarios")
    st.write(costBySupplyTypeExplanationText)

    # Set up total demand variables for summary poster plots
    costBySupplyTypePlotInputData = st.session_state.costBySupplyTypedf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    costBySupplyTypePlotInputData = pd.melt(costBySupplyTypePlotInputData, id_vars=['Variable','Contractor','Study Region'])
    costBySupplyTypePlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    costBySupplyTypeVars = ['Cost by Supply Type']

    costBySupplyTypeVarsForLabel = [
        costBySupplyTypePlotInputData['Type'] == costBySupplyTypeVars[0],
        ]
    costBySupplyTypeNumberOfVars = [0]
    costBySupplyTypeBoxKey = "Cost by Supply Type Selectbox"
    costBySupplyTypePiePlotLabel = "Cost by Supply Type by Study Region"
    costBySupplyTypeBarPlotLabel = "Cost by Supply Type by Contractor"
    costBySupplyTypeBarPlotXAxisLabel = "Cost by Supply Type ($/acre-feet-year)"
    costBySupplyTypeColors = ['#F63366']

    displayPieAndBarPlots(costBySupplyTypeVars, costBySupplyTypeVarsForLabel, costBySupplyTypeNumberOfVars, costBySupplyTypePlotInputData, costBySupplyTypeBoxKey, costBySupplyTypePiePlotLabel, costBySupplyTypeBarPlotLabel, costBySupplyTypeBarPlotXAxisLabel, costBySupplyTypeColors)
    
    #---------------------------------------------------------------#
    # SUMMARY POSTER FOR SUPPLY PRIORITY
    #---------------------------------------------------------------#

    # st.subheader("Supply Priority Scenarios")
    # st.write(supplyPriorityExplanationText)

    # # Set up total demand variables for summary poster plots
    # supplyPriorityPlotInputData = st.session_state.supplyPrioritydf[['Variable', 'Study Region','Contractor', str(st.session_state.futurePlanningYear)]]
    # supplyPriorityPlotInputData = pd.melt(supplyPriorityPlotInputData, id_vars=['Variable','Contractor','Study Region'])
    # supplyPriorityPlotInputData.rename(columns = {'variable': 'Year', 'Variable': 'Type', 'value': 'Value'}, inplace=True)
    # supplyPriorityVars = ['Supply Priority By Type']

    # supplyPriorityVarsForLabel = [
    #     supplyPriorityPlotInputData['Type'] == supplyPriorityVars[0],
    #     ]
    # supplyPriorityNumberOfVars = [0]
    # supplyPriorityBoxKey = "Supply Priority Selectbox"
    # supplyPriorityPiePlotLabel = "Supply Priority by Study Region"
    # supplyPriorityBarPlotLabel = "Supply Priority by Contractor"
    # supplyPriorityBarPlotXAxisLabel = "Supply Priority"
    # supplyPriorityColors = ['#F63366']

    # displayPieAndBarPlots(supplyPriorityVars, supplyPriorityVarsForLabel, supplyPriorityNumberOfVars, supplyPriorityPlotInputData, supplyPriorityBoxKey, supplyPriorityPiePlotLabel, supplyPriorityBarPlotLabel, supplyPriorityBarPlotXAxisLabel, supplyPriorityColors)
