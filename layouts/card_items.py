from layouts.figures import fig_map
from dash import dcc, html
import dash_bootstrap_components as dbc

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