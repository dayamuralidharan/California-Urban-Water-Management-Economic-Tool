import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import streamlit as st
from src.colors import mapColorsByStudyRegion
from src.globalUtilities import roundValues

def formatLongTermWMOResults(df):
    #Format dataframe for display
    for i in range (df.shape[1]):
        df.iloc[:,i] = df.iloc[:,i].apply(roundValues)
        old_column_name = df.columns[i]
        new_column_name = df.iloc[0, i]
        df.rename(columns={old_column_name: new_column_name}, inplace=True)
        
    old_column_name = df.columns[0]
    df.rename(columns={old_column_name: 'Contractor'}, inplace=True)
    df = df.drop(0)
    #df = pd.melt(df, id_vars='Contractor')

    # Define a color blind friendly color palette
    colors = ["#D55E00", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#999999", "#CC79A7"]
    
    # Creating a bar plot using Plotly's graph_objs
    fig = go.Figure()

    # Adding traces for each column
    for i, column in enumerate(df.columns[1:]):
        fig.add_trace(go.Bar(
            x=df['Contractor'],
            y=df[column],
            name=column,
            marker_color = colors[i]
        ))

    # Updating layout
    fig.update_layout(
        title='Optimized Long-term Water Management Option by Contractor',
        xaxis=dict(title='Contractor'),
        yaxis=dict(title='Volume (acre-feet/year)'),
        barmode='stack',  # Change to 'group' if you want grouped bars instead of stacked
        height=700
    )

    # Show the plot
    st.plotly_chart(fig)
    st.table(df)




