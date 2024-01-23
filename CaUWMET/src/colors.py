from src.globalUtilities import selectSpecifiedRows

#Another color blind friendly palot for reference
# {'Color': ["#D55E00", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#999999", "#CC79A7"]}

def mapColorsByStudyRegion(contractorInfo):
    # Get contractor dataframe
    contractors_df = contractorInfo.copy()
    contractors_df = selectSpecifiedRows(contractors_df, 'Include in model', 'Yes')[['Contractor', 'Study Region']]
    # Get list of study regions to assign unique color to each
    unique_regions = contractors_df['Study Region'].unique()

    # Use color-blind friendly colors. Note this will only work for up to 10 unique study regions.
    colors_data = {'Color': ["#00CC96", "#AE62E5", "#EF553B", "#636EFA", "#FFA15A", "#19D3F3", "#999999", "#FF6692"]}
    
    # Map Study Regions to colors using the colors_data dictionary
    colors_mapping = dict(zip(unique_regions, colors_data['Color']))
    contractors_df['Color'] = contractors_df['Study Region'].map(colors_mapping)

    #The plot sorts the contractors before displaying, so need colors to be sorted as well to correspond to the correct contractor
    contractorsSorted = contractors_df.sort_values(by='Contractor')
    colors = contractorsSorted['Color']
    
    return colors, colors_mapping