# Dash bootstrap cheatsheet: https://dashcheatsheet.pythonanywhere.com/

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # Setting local time format to spanish

load_figure_template('SUPERHERO')

df_clim_1 = pd.read_pickle('data/df_clim_1.pkl')
df_clim_2 = pd.read_pickle('data/df_clim_2.pkl')
df_clim = pd.concat([df_clim_1, df_clim_2], sort=False)

df_clim['amplitud_termica'] = df_clim['tmax']-df_clim['tmin']
df_estaciones = pd.read_pickle('data/df_estaciones_selection.pkl')

degree_sign = u'\N{DEGREE SIGN}'

# Creating map
# -----------------------------------------------------------------------------------------------
fig_map = px.scatter_mapbox(df_estaciones,
                            lat='latitud',
                            lon='longitud',
                            custom_data=['nombre', 'altitud'],
                            hover_name="nombre",
                            hover_data={'altitud': True, 'latitud': False, 'longitud': False},
                            color_discrete_sequence=['#521f14'],
                            zoom=4.2)
fig_map.update_layout(
    mapbox_style="open-street-map",
    margin={'b': 0, 'l': 0, 'r': 0, 't': 0})
fig_map.update_traces(hovertemplate='%{customdata[0]} <br>Altitud: %{customdata[1]} m')
# -----------------------------------------------------------------------------------------------

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE], prevent_initial_callbacks=True)
app.layout = html.Div([
    dbc.Row(dbc.Col(html.H1('Datos climatológicos España'),
                    width={'size':6, 'offset':0},
                    ), className="mt-3 m-2"
            ),
    dbc.Row(
        [
            dbc.Col(html.Div([html.P(['Estaciones de la ', html.A('AEMET', href="https://www.aemet.es/"), '. Selecciona una estación en el mapa']),
                              dcc.Graph(id='map',
                                        clickData={'points': [{'customdata': 'MADRID, RETIRO'}]},
                                        figure=fig_map)],
            className="shadow p-3 mb-5 bg-white rounded"),
            width=4),

            dbc.Col(html.Div([
                dbc.Row(html.H3('', id='nom_est', className="mt-3 m-2")),
                dbc.Row([
                    dbc.Col(html.Div([html.H4('Temperatura máxima'),
                                      dbc.Row([dbc.Col(html.Span('', id='date_max_1'), width=8), dbc.Col(html.Span('', id='max_1'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_max_2'), width=8), dbc.Col(html.Span('', id='max_2'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_max_3'), width=8), dbc.Col(html.Span('', id='max_3'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_max_4'), width=8), dbc.Col(html.Span('', id='max_4'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_max_5'), width=8), dbc.Col(html.Span('', id='max_5'))])
                                     ])),
                    dbc.Col(html.Div([html.H4('Temperatura mínima'),
                                      dbc.Row([dbc.Col(html.Span('', id='date_min_1'), width=8), dbc.Col(html.Span('', id='min_1'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_min_2'), width=8), dbc.Col(html.Span('', id='min_2'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_min_3'), width=8), dbc.Col(html.Span('', id='min_3'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_min_4'), width=8), dbc.Col(html.Span('', id='min_4'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_min_5'), width=8), dbc.Col(html.Span('', id='min_5'))])
                                     ])),
                    dbc.Col(html.Div([html.H4('Amplitud térmica'),
                                      dbc.Row([dbc.Col(html.Span('', id='date_amp_1'), width=8), dbc.Col(html.Span('', id='amp_1'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_amp_2'), width=8), dbc.Col(html.Span('', id='amp_2'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_amp_3'), width=8), dbc.Col(html.Span('', id='amp_3'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_amp_4'), width=8), dbc.Col(html.Span('', id='amp_4'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_amp_5'), width=8), dbc.Col(html.Span('', id='amp_5'))])
                                     ])),
                    dbc.Col(html.Div([html.H4('Precipitación'),
                                      dbc.Row([dbc.Col(html.Span('', id='date_prec_1'), width=8), dbc.Col(html.Span('', id='prec_1'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_prec_2'), width=8), dbc.Col(html.Span('', id='prec_2'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_prec_3'), width=8), dbc.Col(html.Span('', id='prec_3'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_prec_4'), width=8), dbc.Col(html.Span('', id='prec_4'))]),
                                      dbc.Row([dbc.Col(html.Span('', id='date_prec_5'), width=8), dbc.Col(html.Span('', id='prec_5'))])
                                     ]))
                            ],className="shadow p-3 mb-5 rounded")
                ]))
            ])
])

@app.callback(Output('nom_est', 'children'),
              Input('map', 'clickData'))
def update_name(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    return nombre

@app.callback(
    Output('date_max_1', 'children'),
    Output('max_1', 'children'),
    Output('date_max_2', 'children'),
    Output('max_2', 'children'),
    Output('date_max_3', 'children'),
    Output('max_3', 'children'),
    Output('date_max_4', 'children'),
    Output('max_4', 'children'),
    Output('date_max_5', 'children'),
    Output('max_5', 'children'),
    Input('map', 'clickData'))
def extract_tmax(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    df_aux = df_clim[df_clim['nombre'] == nombre].sort_values(by=['tmax', 'fecha'], ascending=[False, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.loc[i].fecha.strftime('%Y, %d %B')
        temperature = df_aux.loc[i].tmax
        result.append(fecha)
        result.append('{}'.format(temperature) + degree_sign + 'C')
    return tuple(result)

@app.callback(
    Output('date_min_1', 'children'),
    Output('min_1', 'children'),
    Output('date_min_2', 'children'),
    Output('min_2', 'children'),
    Output('date_min_3', 'children'),
    Output('min_3', 'children'),
    Output('date_min_4', 'children'),
    Output('min_4', 'children'),
    Output('date_min_5', 'children'),
    Output('min_5', 'children'),
    Input('map', 'clickData'))
def extract_tmin(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    df_aux = df_clim[df_clim['nombre'] == nombre].sort_values(by=['tmin', 'fecha'], ascending=[True, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.loc[i].fecha.strftime('%Y, %d %B')
        temperature = df_aux.loc[i].tmin
        result.append(fecha)
        result.append('{}'.format(temperature) + degree_sign + 'C')
    return tuple(result)

@app.callback(
    Output('date_amp_1', 'children'),
    Output('amp_1', 'children'),
    Output('date_amp_2', 'children'),
    Output('amp_2', 'children'),
    Output('date_amp_3', 'children'),
    Output('amp_3', 'children'),
    Output('date_amp_4', 'children'),
    Output('amp_4', 'children'),
    Output('date_amp_5', 'children'),
    Output('amp_5', 'children'),
    Input('map', 'clickData'))
def extract_amp(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    df_aux = df_clim[df_clim['nombre'] == nombre].sort_values(by=['amplitud_termica', 'fecha'], ascending=[False, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.loc[i].fecha.strftime('%Y, %d %B')
        temperature = df_aux.loc[i].amplitud_termica
        result.append(fecha)
        result.append('{:.1f}'.format(temperature) + degree_sign + 'C')
    return tuple(result)

@app.callback(
    Output('date_prec_1', 'children'),
    Output('prec_1', 'children'),
    Output('date_prec_2', 'children'),
    Output('prec_2', 'children'),
    Output('date_prec_3', 'children'),
    Output('prec_3', 'children'),
    Output('date_prec_4', 'children'),
    Output('prec_4', 'children'),
    Output('date_prec_5', 'children'),
    Output('prec_5', 'children'),
    Input('map', 'clickData'))
def extract_prec(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    df_aux = df_clim[df_clim['nombre'] == nombre].sort_values(by=['prec', 'fecha'], ascending=[False, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.loc[i].fecha.strftime('%Y, %d %B')
        prec = df_aux.loc[i].prec
        result.append(fecha)
        result.append('{}'.format(prec) + ' mm')
    return tuple(result)

# @app.callback(Output('tmed_graph', 'figure'), Input('dropdown_estacion', 'value'))
# def draw_tmed(estacion):
#     fig = px.line(df_grouped.reset_index().set_index('nombre').loc[estacion].reset_index(), x='fecha', y='tmed')
#     fig.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text']
#     )
#     return fig

# @app.callback(Output('tmed_graph', 'figure'), Input('map', 'clickData'))
# def draw_tmed(clickData):
#     nombre = clickData['points'][0]['customdata'][0]
#     fig = px.line(df_grouped.reset_index().set_index('nombre').loc[nombre].reset_index(), x='fecha', y='tmed')
#     # fig.update_layout(
#     #     plot_bgcolor=colors['background'],
#     #     paper_bgcolor=colors['background'],
#     #     font_color=colors['text']
#     # )
#     return fig


if __name__ == '__main__':
    app.run_server(debug=True)
