import streamlit as st
import json
#import geopandas as gpd
#import geoviews as gv
import pyproj
import plotly.graph_objs as go
import traceback

def app():
    class opt_echo:
        def __init__(self):
            self.checkbox = st.sidebar.checkbox("Show source code", key = "1")

            self.orig_extract_stack = traceback.extract_stack

            if self.checkbox:
                traceback.extract_stack = lambda: self.orig_extract_stack()[:-2]
                self.echo = st.echo()

        def __enter__(self):
            if self.checkbox:
                return self.echo.__enter__()

        def __exit__(self, type, value, traceback):
            if self.checkbox:
                self.echo.__exit__(type, value, traceback)

            # For some reason I need to import this again.
            import traceback

            traceback.extract_stack = self.orig_extract_stack

    with opt_echo():
        st.title('Model Overview')
        st.markdown('To add: Overview of model logic, map of contractors with summary information on their supplies.')

        # reading in the polygon shapefile
        #polygon = gpd.read_file("inputData/geospatial/ModelContractorsPolygon.shp")

        # project geopandas dataframe
        #map_df = polygon
        #map_df.to_crs(pyproj.CRS.from_epsg(3857), inplace=True)

        #reading in the points shapefile
        #points = gpd.read_file("inputData/geospatial/ModelContractorsPoints.shp")

        #project geopandas dataframe
        #points.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

        # define lat, long for points
        #Lat = points['Lat']
        #Long = points['Long']

        # leases to geojson
        #path = "reference/geojson.json"

        # map_df.to_file(path, driver = "GeoJSON")
        # with open(path) as geofile:
        #     j_file = json.load(geofile)

        #index geojson
        # i=1
        # for feature in j_file["features"]:
        #     feature ['id'] = str(i).zfill(2)
        #     i += 1
        
        # mapbox token
        #token = "pk.eyJ1IjoibmlyYS0xOCIsImEiOiJja21remVtbXExNjg2Mm9xbXF2MDhxbHFhIn0.E9OSgsFY-ziqkJkayUpZ8w"

        # define layers and plot map
        # choro = go.Choroplethmapbox(z=map_df['STFIPS'], locations = map_df.index, colorscale = 'magma', geojson = j_file, text = map_df['AGENCYNAME'], marker_line_width=0.1)
            # Your choropleth data here
        #choro = go.Polygons(map_df['STFIPS'], map_df.index, colorscale = 'magma', geojson = j_file, text = map_df['AGENCYNAME'], marker_line_width=0.1)

        #scatt = go.Scattermapbox(lat=Lat, lon=Long, text= map_df['AGENCYNAME'], mode='markers+text',below='False', marker=dict( size=12, color ='rgb(56, 44, 100)'))
            # Your scatter data here

        #layout = go.Layout(title_x =0.5, width=950, height=700,mapbox = dict(center= dict(lat=37, lon=-95),accesstoken= 'token', zoom=4,style="stamen-terrain"))
        

        # streamlit multiselect widget
        # layer1 = st.multiselect('Layer Selection', [choro, scatt], format_func=lambda x: 'Polygon' if x==choro else 'Points')
        # layer1 = st.selectbox('Layer Selection', [scatt], format_func=lambda x: 'Points')

        #st.write('Layer 1:', layer1)
        # fig = go.Figure(data=layer1, layout=layout)


        # display streamlit
        # st.plotly_chart(fig)