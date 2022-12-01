import plotly.express as px
from layouts.callbacks import df_estaciones

mapbox_access_token = "pk.eyJ1IjoicGFuY2lxdWUiLCJhIjoiY2w5ZTNnbWQyMGF1aTN2cGI4ZHIxcTZ0dCJ9.PwSiTH8rn9eRYk0FbVLi8w"
mapbox_style = "mapbox://styles/pancique/clacuhyf5003514nsklotaxcl"
# Creating map
# -----------------------------------------------------------------------------------------------
fig_map = px.scatter_mapbox(df_estaciones,
                            lat='latitud',
                            lon='longitud',
                            custom_data=['nombre', 'altitud', 'provincia'],
                            hover_name="nombre",
                            hover_data={'altitud': True, 'latitud': False, 'longitud': False},
                            # color_discrete_sequence=['#521f14'],
                            zoom=4.1,
                            center={'lat':37,'lon':-7}
                            )
fig_map.update_traces(
    marker=dict(size=12,
                symbol='circle',
                color='#EC9374')
)
fig_map.layout.mapbox.accesstoken = mapbox_access_token
fig_map.update_layout(
    mapbox_style=mapbox_style,
    margin={'b': 0, 'l': 0, 'r': 0, 't': 0},
    paper_bgcolor='rgba(0,0,0,0)',
    autosize=True)
fig_map.update_traces(hovertemplate='%{customdata[0]} <br>Altitud: %{customdata[1]} m')