from layouts.card_items import card_map, cards1,cards2, card_graph_prec,card_graph_anom,card_graph_bar
from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Row(
        [
            dbc.Col(html.Div(
                [
                    dbc.Row(html.H1('Datos climatológicos AEMET', className="my-4", style={'text-align':'center'})),
                ]
            ), width=4
            ),

            dbc.Col(html.Div([
                dbc.Row([dbc.Col(html.H3('OVIEDO', id='nom_est', className="mt-3")),
                         dbc.Row([dbc.Col(html.H6('Provincia: ASTURIAS', id='provincia_est'), width=3),
                         dbc.Col(html.H6('Altitud: 336 m', id='altitud_est'))])
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
                    card_map,
                    card_graph_bar
                ], className="mx-3"
            ), width=4
            ),

            dbc.Col(html.Div([
                dbc.Row(dbc.Col([cards1])),
                dbc.Row(dbc.Col([cards2])),
                dbc.RadioItems(
                options=[
                    {'label':' Precipitación diaria ', 'value': 'prec'},
                    {'label':' Anomalía térmica diaria ', 'value': 'anom'},
                    #{'label': ' Anomalía de horas de sol', 'value': 'anom_sol'}
            ],
                value='prec', inline=True,  id='graph_select',
                className="me-3", 
                style={'margin-right': '35px', 'text-align': 'left'}
           ),
                dbc.Row(dbc.Col(card_graph_prec, id='card_graph_prec')),
                dbc.Row(dbc.Col(card_graph_anom, id='card_graph_anom'))
                ], className="me-3"), width=8)
            ], className='g-0', style={'height':'80vh'})
])