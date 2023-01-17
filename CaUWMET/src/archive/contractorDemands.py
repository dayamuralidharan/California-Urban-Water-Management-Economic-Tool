import pandas as pd
import os

# Get contractor demand and use by type from from data folder and create dataframes for each.
directoryOfThisFile = os.path.dirname(os.path.abspath(__file__))
dataDirectory = directoryOfThisFile.replace('src', 'data')
inputData = pd.read_csv(dataDirectory + "/contractorDemandsandUses.csv")


totalContractorDemand_NormOrBetterYear = inputData[
    inputData["Parameter"].str.match('Total wholesale and retail demand') & inputData["Year Type"].str.match('Normal or Better')
    ]

totalContractorDemand_SingleDryYear = inputData[
    inputData["Parameter"].str.match('Total wholesale and retail demand') & inputData["Year Type"].str.match('Single Dry Year')
    ]

totalContractorDemand_MultiDryYear = inputData[
    inputData["Parameter"].str.match('Total wholesale and retail demand') & inputData["Year Type"].str.match('Multi-Dry Year')
    ]

contractorUse_SingleFamilyResidential = inputData[
    inputData["Parameter"].str.match('Single Family Residential Use')]

contractorUse_MultiFamilyResidential = inputData[
    inputData["Parameter"].str.match('Multi-Family Residential Use')]

contractorUse_Industrial = inputData[
    inputData["Parameter"].str.match('Industrial Use')]

contractorUse_Commercial = inputData[
    inputData["Parameter"].str.match('Commercial Use')]

contractorUse_Agricultural = inputData[
    inputData["Parameter"].str.match('Agricultural Use')]