import streamlit as st
import pandas as pd
from src.globalUtilities import selectSpecifiedRows


def mapColorsByStudyRegion(contractorInfo):
    # Get contractor dataframe
    contractors_df = contractorInfo.copy()
    contractors_df = selectSpecifiedRows(contractors_df, 'Include in model', 'Yes')[['Contractor', 'Study Region']]
    # Get list of study regions to assign unique color to each
    unique_regions = contractors_df['Study Region'].unique()

    # Use color-blind friendly colors. Note this will only work for up to 10 unique study regions.
    colors_data = {'Color': ["#D55E00", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#999999", "#CC79A7"]}
    
    # Map Study Regions to colors using the colors_data dictionary
    colors_mapping = dict(zip(unique_regions, colors_data['Color']))
    contractors_df['Color'] = contractors_df['Study Region'].map(colors_mapping)
    contractorsSorted = contractors_df.sort_values(by='Contractor')

    # Display the merged DataFrame
    # test = contractors_df[['Contractor', 'Study Region', 'Color']]
    # print(test)

    colors = contractorsSorted['Color']
    
    return colors