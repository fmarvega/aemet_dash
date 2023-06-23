from layouts.map_figure import fig_map
from dash import dcc, html
import dash_bootstrap_components as dbc

# -----------------------------------------------------------------------------------------------
# Creating cards
# -----------------------------------------------------------------------------------------------
card_map = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.P(['Selecciona una estación de la ',
                                      html.A('AEMET', href="https://www.aemet.es/", target='blank'),
                                      ' sobre el mapa']),
                              dcc.Graph(id='map',
                                        clickData={'points': [{'customdata': 'OVIEDO'}]},
                                        figure=fig_map,
                                        style={'height':'43vh'})]
                             )
                ]
            )
        )
# -------------------------------
card_graph_bar = dbc.Card(
                dbc.CardBody(

                [
                    dbc.Col(
                        dcc.Graph(id='bar_chart'), md=12,
                    )
                ]
            )
        )
# -------------------------------
card_max = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Temperatura máxima'),
                              html.Span('Datos desde '), html.Span('', id='year_input'), html.Span('', id='desde_max'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_max_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tab_max_min",active_label_style={"color": "#41C5FA"})
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
                                      dbc.Tab(label="Max", tab_id="tab_min_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tab_min_min",active_label_style={"color": "#41C5FA"})
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
card_med = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Temperatura media'),
                              html.Span('Datos desde '), html.Span('', id='desde_med'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_med_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tab_med_min",active_label_style={"color": "#41C5FA"})
                                  ],
                                  id='tabs_med',
                                  active_tab = 'tab_med_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_med_1'), width=9),
                                       dbc.Col(html.Span('', id='med_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_med_2'), width=9),
                                       dbc.Col(html.Span('', id='med_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_med_3'), width=9),
                                       dbc.Col(html.Span('', id='med_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_med_4'), width=9),
                                       dbc.Col(html.Span('', id='med_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_med_5'), width=9),
                                       dbc.Col(html.Span('', id='med_5'))])
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
                                      dbc.Tab(label="Max", tab_id="tab_amp_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tab_amp_min",active_label_style={"color": "#41C5FA"})
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
                                      dbc.Tab(label="Max", tab_id="tab_prec_max",active_label_style={"color": "#41C5FA"})
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
card_prec_month = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Precipitación Mensual'),
                              html.Span('Datos desde '), html.Span('', id='desde_prec_month'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_preci_month_max",active_label_style={"color": "#41C5FA"})
                                  ],
                                  id='tabs_prec_month',
                                  active_tab = 'tab_preci_month_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_month_1'), width=8),
                                       dbc.Col(html.Span('', id='preci_month_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_month_2'), width=8),
                                       dbc.Col(html.Span('', id='preci_month_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_month_3'), width=8),
                                       dbc.Col(html.Span('', id='preci_month_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_month_4'), width=8),
                                       dbc.Col(html.Span('', id='preci_month_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_month_5'), width=8),
                                       dbc.Col(html.Span('', id='preci_month_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_prec_year = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Precipitación Anual'),
                              html.Span('Datos desde '), html.Span('', id='desde_prec_year'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tab_preci_year_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tab_preci_year_min",active_label_style={"color": "#41C5FA"})
                                  ],
                                  id='tabs_prec_year',
                                  active_tab = 'tab_preci_year_max'
                              ),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_year_1'), width=8),
                                       dbc.Col(html.Span('', id='preci_year_1'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_year_2'), width=8),
                                       dbc.Col(html.Span('', id='preci_year_2'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_year_3'), width=8),
                                       dbc.Col(html.Span('', id='preci_year_3'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_year_4'), width=8),
                                       dbc.Col(html.Span('', id='preci_year_4'))]),
                              dbc.Row([dbc.Col(html.Span('', id='date_preci_year_5'), width=8),
                                       dbc.Col(html.Span('', id='preci_year_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_anom_month = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.H4('Anomalías Mensuales'),
                              html.Span('Datos desde '), html.Span('', id='desde_anom_month'),
                              dbc.Tabs(
                                  [
                                      dbc.Tab(label="Max", tab_id="tabs_anom_max",active_label_style={"color": "#FA4141"}),
                                      dbc.Tab(label="Min", tab_id="tabs_anom_min",active_label_style={"color": "#41C5FA"})
                                  ],
                                  id='tabs_anom',
                                  active_tab = 'tabs_anom_max'
                              ),
                            dbc.Row([dbc.Col(html.Span('', id='date_month_anom_1'), width=8),
                                     dbc.Col(html.Span('', id='month_anom_1'))]),
                            dbc.Row([dbc.Col(html.Span('', id='date_month_anom_2'), width=8),
                                     dbc.Col(html.Span('', id='month_anom_2'))]),
                            dbc.Row([dbc.Col(html.Span('', id='date_month_anom_3'), width=8),
                                     dbc.Col(html.Span('', id='month_anom_3'))]),
                            dbc.Row([dbc.Col(html.Span('', id='date_month_anom_4'), width=8),
                                     dbc.Col(html.Span('', id='month_anom_4'))]),
                            dbc.Row([dbc.Col(html.Span('', id='date_month_anom_5'), width=8),
                                     dbc.Col(html.Span('', id='month_anom_5'))])
                              ])
                ]
            )
        )
# -------------------------------
card_graph_prec = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.Br(),
                              dbc.Row(
                                  [
                                      dbc.Col(html.H4('Precipitación diaria'), width=3),
                                      dbc.Col(html.P('Año', style={"text-align":'right'}), align='center', width={'size':1,'offset':6}),
                                      dbc.Col(
                                          dbc.Input(type='number', value=2022, max=2022, step=1, id='year_input_prec', size='sm')
                                      )
                                  ]
                              ),
                              dcc.Graph(id='graph_prec')
                              ])
                ]
            )
        )

# -------------------------------
card_graph_anom = dbc.Card(
            dbc.CardBody(
                [
                    html.Div([html.Br(),
                              dbc.Row(
                                  [
                                      dbc.Col(html.H4('Anomalía térmica diaria'), width=3),
                                      dbc.Col(html.P('Año', style={"text-align":'right'}), align='center', width={'size':1,'offset':6}),
                                      dbc.Col(
                                          dbc.Input(type='number', value=2022, max=2022, step=1, id='year_input_anom', size='sm')
                                      )
                                  ]
                              ),
                              dcc.Graph(id='graph_anom')
                              ])
                ]
            )
        )
# -------------------------------

cards1 = dbc.CardGroup(
    [
        card_max, card_min, card_med, card_amp
    ]
)
cards2 = dbc.CardGroup(
    [
        card_prec, card_prec_month, card_prec_year, card_anom_month
    ]
)
# -------------------------------