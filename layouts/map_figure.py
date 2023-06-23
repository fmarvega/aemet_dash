import plotly.express as px
from layouts.callbacks import df_estaciones
# -----------------------------------------------------------------------------------------------
fig_map = px.scatter_mapbox(df_estaciones,
                            lat='latitud',
                            lon='longitud',
                            custom_data=['nombre', 'altitud', 'provincia'],
                            hover_name="nombre",
                            hover_data={'altitud': True, 'latitud': False, 'longitud': False},
                            # color_discrete_sequence=['#521f14'],
                            #zoom=7.1,
                            center={'lat':40,'lon':-4}
                            )
fig_map.update_traces(
    marker=dict(size=12,
                symbol='circle',
                color='#EC9374')
)
fig_map.update_layout(
    mapbox_style="mapbox://styles/mapbox/dark-v10",
    mapbox_accesstoken="MAPBOX_TOKEN", 
    mapbox_zoom=4.05,
    mapbox_center=dict(lat=36.5, lon=-6),
    margin={'b': 0, 'l': 0, 'r': 0, 't': 0},
)
fig_map.update_traces(hovertemplate='%{customdata[0]} <br>Altitud: %{customdata[1]} m')
#fig_map.show()