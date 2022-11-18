# Dash bootstrap cheatsheet: https://dashcheatsheet.pythonanywhere.com/

import pandas as pd
import numpy as np
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
# import locale
from functions import update_df

# locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8') # Setting local time format to spanish

load_figure_template('SUPERHERO')

df_clim_1 = pd.read_csv('data/df_clim_1.csv')
df_clim_2 = pd.read_csv('data/df_clim_2.csv')
df_estaciones = pd.read_csv('data/df_estaciones.csv')

df_clim = pd.concat([df_clim_1, df_clim_2], sort=False)
df_clim['fecha'] = pd.to_datetime(df_clim['fecha'])
df_clim = update_df(df_clim, df_estaciones)

df_clim['amplitud_termica'] = df_clim['tmax']-df_clim['tmin']

degree_sign = u'\N{DEGREE SIGN}'
month_list = ['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']

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
# -----------------------------------------------------------------------------------------------
# Creating cards
# -------------------------------
card_map = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.P(['Selecciona una estación de la ',
                                      html.A('AEMET', href="https://www.aemet.es/", target='blank'),
                                      ' sobre el mapa']),
                              dcc.Graph(id='map',
                                        clickData={'points': [{'customdata': 'MADRID, RETIRO'}]},
                                        figure=fig_map,
                                        style={'height':'74vh'})]
                             )
                ]
            )
        )
# -------------------------------
card_max = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Temperatura máxima'),
                              html.Span('Datos desde '), html.Span('', id='desde_max'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_max_max"),
                                      dbc.Tab(label="Min", tab_id="tab_max_min")
                                  ],
                                  id='tabs_max',
                                  active_tab = 'tab_max_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_max_1'), width=9),
                                       dbc.Col(html.Span('', id='max_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_max_2'), width=9),
                                       dbc.Col(html.Span('', id='max_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_max_3'), width=9),
                                       dbc.Col(html.Span('', id='max_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_max_4'), width=9),
                                       dbc.Col(html.Span('', id='max_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_max_5'), width=9),
                                       dbc.Col(html.Span('', id='max_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_min = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Temperatura mínima'),
                              html.Span('Datos desde '), html.Span('', id='desde_min'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_min_max"),
                                      dbc.Tab(label="Min", tab_id="tab_min_min")
                                  ],
                                  id='tabs_min',
                                  active_tab = 'tab_min_min'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_min_1'), width=9),
                                       dbc.Col(html.Span('', id='min_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_min_2'), width=9),
                                       dbc.Col(html.Span('', id='min_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_min_3'), width=9),
                                       dbc.Col(html.Span('', id='min_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_min_4'), width=9),
                                       dbc.Col(html.Span('', id='min_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_min_5'), width=9),
                                       dbc.Col(html.Span('', id='min_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_amp = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Amplitud térmica'),
                              html.Span('Datos desde '), html.Span('', id='desde_amp'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_amp_max"),
                                      dbc.Tab(label="Min", tab_id="tab_amp_min")
                                  ],
                                  id='tabs_amp',
                                  active_tab = 'tab_amp_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_amp_1'), width=9),
                                       dbc.Col(html.Span('', id='amp_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_amp_2'), width=9),
                                       dbc.Col(html.Span('', id='amp_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_amp_3'), width=9),
                                       dbc.Col(html.Span('', id='amp_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_amp_4'), width=9),
                                       dbc.Col(html.Span('', id='amp_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_amp_5'), width=9),
                                       dbc.Col(html.Span('', id='amp_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_prec = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Precipitación'),
                              html.Span('Datos desde '), html.Span('', id='desde_prec'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_prec_max")
                                  ],
                                  id='tabs_prec',
                                  active_tab = 'tab_prec_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_prec_1'), width=8),
                                       dbc.Col(html.Span('', id='prec_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_prec_2'), width=8),
                                       dbc.Col(html.Span('', id='prec_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_prec_3'), width=8),
                                       dbc.Col(html.Span('', id='prec_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_prec_4'), width=8),
                                       dbc.Col(html.Span('', id='prec_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_prec_5'), width=8),
                                       dbc.Col(html.Span('', id='prec_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_graph = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([
                              dbc.Row(
                                  [
                                      dbc.Col(html.H4('Anomalía térmica diaria'), width=3),
                                      dbc.Col(html.P('Año', style={"text-align":'right'}), align='center', width={'size':1,'offset':6}),
                                      dbc.Col(
                                          dbc.Input(type='number', value=2022, max=2022, step=1, id='year_input', size='sm')
                                      )
                                  ]
                              ),
                              dcc.Graph(id='graph_anom')
                              ])
                ]
            )
        )
# -------------------------------
cards = dbc.CardGroup(
    [
        card_max, card_min, card_amp, card_prec
    ]
)
# -------------------------------


# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE]) #, prevent_initial_callbacks=True)
server = app.server

app.layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.Div(
                [
                    dbc.Row(html.H1('Datos climatológicos AEMET', className="my-4", style={'text-align':'center'})),
                ]
            ), width=4
            ),

            dbc.Col(html.Div([
                dbc.Row([dbc.Col(html.H3('MADRID, RETIRO', id='nom_est', className="mt-3")),
                         dbc.Row([dbc.Col(html.H6('Provincia: MADRID', id='provincia_est'), width=3),
                         dbc.Col(html.H6('Altitud: 667 m', id='altitud_est'))])
                         ]),
                dbc.RadioItems(options=[
                    {'label':'Enero', 'value':1},
                    {'label':'Febrero', 'value':2},
                    {'label':'Marzo', 'value':3},
                    {'label':'Abril', 'value':4},
                    {'label':'Mayo', 'value':5},
                    {'label':'Junio', 'value':6},
                    {'label':'Julio', 'value':7},
                    {'label':'Agosto', 'value':8},
                    {'label':'Septiembre', 'value':9},
                    {'label':'Octubre', 'value':10},
                    {'label':'Noviembre', 'value':11},
                    {'label':'Diciembre', 'value':12},
                    {'label':'Todos', 'value':0},
                    ],
                    value=0, inline=True, id='month_radio')
                ], className="me-3"), width=8)
            ]),
    dbc.Row(
        [
            dbc.Col(html.Div(
                [
                    card_map
                ], className="mx-3"
            ), width=4
            ),

            dbc.Col(html.Div([
                dbc.Row(dbc.Col([cards])),
                dbc.Row(dbc.Col(card_graph))
                ], className="me-3"), width=8)
            ], className='g-0', style={'height':'80vh'})
])

@app.callback(Output('nom_est', 'children'),
              Output('provincia_est', 'children'),
              Output('altitud_est', 'children'),
              Input('map', 'clickData'),
              prevent_initial_call=True)
def update_name(clickData):
    nombre = clickData['points'][0]['customdata'][0]
    altitud = 'Altitud: {} m'.format(clickData['points'][0]['customdata'][1])
    provincia = 'Provincia: {}'.format(clickData['points'][0]['customdata'][2])
    return (nombre, provincia, altitud)

@app.callback(Output('desde_max', 'children'),
              Output('desde_min', 'children'),
              Output('desde_amp', 'children'),
              Output('desde_prec', 'children'),
              Output('year_input', 'min'),
              Input('nom_est', 'children'))
def update_year(nombre):
    df_aux = df_clim[df_clim['nombre'] == nombre]

    year_max = df_aux[['tmax','fecha']].dropna(subset=['tmax']).sort_values(by='fecha', ascending=True).iloc[0].fecha.year
    # year_min = df_aux[['tmin','fecha']].dropna().sort_values(by='fecha', ascending=True).iloc[0].fecha.dt.year
    # year_amp = df_aux[['amplitud_termica','fecha']].dropna().sort_values(by='fecha', ascending=True).iloc[0].fecha.dt.year
    year_prec = df_aux[['prec','fecha']].dropna(subset=['prec']).sort_values(by='fecha', ascending=True).iloc[0].fecha.year

    return (str(year_max), str(year_max), str(year_max), str(year_prec), year_max)

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
    Input('nom_est', 'children'),
    Input('tabs_max', 'active_tab'),
    Input('month_radio', 'value'))
def extract_tmax(nombre, tab, month):
    df_aux = df_clim[df_clim['nombre'] == nombre]
    if month:
        df_aux = df_aux[df_aux['fecha'].dt.month == month]
    if tab == 'tab_max_max':
        df_aux = df_aux.sort_values(by=['tmax', 'fecha'], ascending=[False, False]).head(5).reset_index()
    else:
        df_aux = df_aux.sort_values(by=['tmax', 'fecha'], ascending=[True, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.iloc[i].fecha
        result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month-1]))
        temperature = df_aux.iloc[i].tmax
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
    Input('nom_est', 'children'),
    Input('tabs_min', 'active_tab'),
    Input('month_radio', 'value'))
def extract_tmin(nombre, tab, month):
    df_aux = df_clim[df_clim['nombre'] == nombre]
    if month:
        df_aux = df_aux[df_aux['fecha'].dt.month == month]
    if tab == 'tab_min_min':
        df_aux = df_aux.sort_values(by=['tmin', 'fecha'], ascending=[True, False]).head(5).reset_index()
    else:
        df_aux = df_aux.sort_values(by=['tmin', 'fecha'], ascending=[False, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.iloc[i].fecha
        result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month - 1]))
        temperature = df_aux.iloc[i].tmin
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
    Input('nom_est', 'children'),
    Input('tabs_amp', 'active_tab'),
    Input('month_radio', 'value'))
def extract_amp(nombre, tab, month):
    df_aux = df_clim[df_clim['nombre'] == nombre]
    if month:
        df_aux = df_aux[df_aux['fecha'].dt.month == month]
    if tab == 'tab_amp_max':
        df_aux = df_aux.sort_values(by=['amplitud_termica', 'fecha'], ascending=[False, False]).head(5).reset_index()
    else:
        df_aux = df_aux.sort_values(by=['amplitud_termica', 'fecha'], ascending=[True, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.iloc[i].fecha
        result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month - 1]))
        temperature = df_aux.iloc[i].amplitud_termica
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
    Input('nom_est', 'children'),
    Input('month_radio', 'value'))
def extract_prec(nombre, month):
    df_aux = df_clim[df_clim['nombre'] == nombre]
    if month:
        df_aux = df_aux[df_aux['fecha'].dt.month == month]
    df_aux = df_aux.sort_values(by=['prec', 'fecha'], ascending=[False, False]).head(5).reset_index()
    result = []
    for i in range(5):
        fecha = df_aux.iloc[i].fecha
        result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month - 1]))
        prec = df_aux.iloc[i].prec
        result.append('{}'.format(prec) + ' mm')
    return tuple(result)

@app.callback(
    Output('graph_anom', 'figure'),
    Input('nom_est', 'children'),
    Input('year_input', 'value'))
def plot_anom(nombre, year):
    df_aux = df_clim[df_clim['nombre'] == nombre]

    heat_anom = np.empty((12, 31))
    heat_anom[:] = np.nan

    heat_max = np.empty((12, 31))
    heat_max[:] = np.nan

    heat_min = np.empty((12, 31))
    heat_min[:] = np.nan

    df_med = df_aux.groupby('fecha').agg({'tmed': np.mean})
    df_med = pd.pivot_table(df_med, values='tmed', index=df_med.index.month, columns=df_med.index.day)

    df_aux = df_aux[df_aux['fecha'].dt.year.isin([year])]
    df_aux['month'] = df_aux['fecha'].dt.month
    df_aux['day'] = df_aux['fecha'].dt.day
    df_aux = df_aux[['month', 'day', 'tmed', 'tmax', 'tmin']]
    df_heat = pd.pivot_table(df_aux, values='tmed', index='month', columns='day')

    shape_mat = df_heat.to_numpy().shape
    months = (df_heat.index.to_numpy() - 1).tolist()
    heat_anom[:shape_mat[0],:shape_mat[1]] = df_heat.to_numpy()-df_med.to_numpy()[months,:]

    df_max = pd.pivot_table(df_aux, values='tmax', index='month', columns='day')
    df_min = pd.pivot_table(df_aux, values='tmin', index='month', columns='day')

    heat_max[:shape_mat[0], :shape_mat[1]] = df_max.to_numpy()
    heat_min[:shape_mat[0], :shape_mat[1]] = df_min.to_numpy()

    customdata=[]
    customdata.append(heat_anom + df_med.to_numpy())
    customdata.append(heat_max)
    customdata.append(heat_min)

    fig = px.imshow(heat_anom, color_continuous_scale='RdBu_r',
                    zmin=-15, zmax=15, text_auto='.1f', aspect='auto')
    values_df = pd.DataFrame(heat_anom).apply(lambda x: np.round(x,1), axis=1).fillna('x').astype('str')
    fig.update_traces(text=values_df,
                      texttemplate='%{text}')
    fig.update_traces(hoverongaps=False)
    fig.update_yaxes(range=[0, 11])
    fig.update(data=[{'customdata': np.dstack((customdata[0],customdata[1],customdata[2])),
                      'hovertemplate':'%{x} de %{y}<br>Anomalía: %{z:.2f}\u00b0C<br>Temperatura media: %{customdata[0]:.1f}\u00b0C<br>Temperatura máxima: %{customdata[1]:.1f}\u00b0C<br>Temperatura mínima: %{customdata[2]:.1f}\u00b0C'}])
    # fig.update_traces(customdata=customdata,
    #                   hoverinfo='all',
    #                   hovertemplate='%{x} de %{y}<br>Anomalía: %{z:.2f}ºC<br>Temperatura media: %{customdata[0]}')
    fig.update_layout(
        margin={'b': 10, 'l': 0, 'r': 40, 't': 40},
        paper_bgcolor='rgba(0,0,0,0)',
        # plot_bgcolor=None,
        yaxis=dict(
            tickmode='array',
            ticklen=0,
            tickvals=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            ticktext=['Enero ', 'Febrero ', 'Marzo ', 'Abril ', 'Mayo ', 'Junio ', 'Julio ', 'Agosto ', 'Septiembre ',
                      'Octubre ', 'Noviembre ', 'Diciembre ']
        ),
        xaxis=dict(
            tickmode='array',
            ticklen=0,
            tickvals=[n for n in range(31)],
            ticktext=[str(n + 1) for n in range(31)],
            side='top'
        ),
        coloraxis=dict(
            colorbar=dict(
                orientation='h',
                x=0.2,
                y=-0.2,
                thickness=20,
                len=0.4,
                title='Anomalía térmica (' + degree_sign + 'C)',
                # ticklabelposition = 'inside'
            )
        )
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(range=[11.5,-0.5], autorange=False, showgrid=False, zeroline=False)
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
