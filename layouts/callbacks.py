import pandas as pd
from dash import Input, Output
from layouts.aux_functions import extract_data, extract_prec_month,extract_prec_year,fig_anom,fig_prec,get_anom_month,generate_bar_chart
from data.postgresql.data_fetch import data_fetch
from data.postgresql.queries import query_estaciones, query_from
import dash
import plotly.graph_objs as go

df_estaciones = pd.DataFrame(data_fetch(query_estaciones()), columns=['latitud', 'provincia', 'altitud', 'indicativo', 'nombre', 'indsinop', 'longitud'])

def register_callbacks(app):
    
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
                Output('desde_med', 'children'),
                Output('desde_amp', 'children'),
                Output('desde_prec', 'children'),
                Output('desde_prec_month', 'children'),
                Output('desde_prec_year', 'children'),
                Output('desde_anom_month', 'children'),
                Output('year_input', 'min'),
                Input('nom_est', 'children'))
    def update_year(nombre):
        year_max = data_fetch(query_from(nombre, 'tmax'))[0][0].year
        year_prec = data_fetch(query_from(nombre, 'prec'))[0][0].year
        print('YEARMAX',year_max)
        print('YEARPREC',year_prec)
        return (str(year_max), str(year_max), str(year_max), str(year_max),str(year_max),str(year_max),str(year_max),str(year_max), year_max)

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
        return extract_data('tmax', nombre, tab, month)

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
        return extract_data('tmin', nombre, tab, month)

    @app.callback(
        Output('date_med_1', 'children'),
        Output('med_1', 'children'),
        Output('date_med_2', 'children'),
        Output('med_2', 'children'),
        Output('date_med_3', 'children'),
        Output('med_3', 'children'),
        Output('date_med_4', 'children'),
        Output('med_4', 'children'),
        Output('date_med_5', 'children'),
        Output('med_5', 'children'),
        Input('nom_est', 'children'),
        Input('tabs_med', 'active_tab'),
        Input('month_radio', 'value'))
    def extract_tmed(nombre, tab, month):
        return extract_data('tmed', nombre, tab, month)

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
        return extract_data('tmax-tmin', nombre, tab, month)
    #-------------------------------------------------------
    # PRECIPITACIÓN DIARIA
    #-------------------------------------------------------
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
        return extract_data('prec', nombre, 'max', month)
    
    #-------------------------------------------------------
    # PRECIPITACIÓN MENSUAL
    #-------------------------------------------------------
    @app.callback(
        Output('date_preci_month_1', 'children'),
        Output('preci_month_1', 'children'),
        Output('date_preci_month_2', 'children'),
        Output('preci_month_2', 'children'),
        Output('date_preci_month_3', 'children'),
        Output('preci_month_3', 'children'),
        Output('date_preci_month_4', 'children'),
        Output('preci_month_4', 'children'),
        Output('date_preci_month_5', 'children'),
        Output('preci_month_5', 'children'),
        Input('nom_est', 'children')
    )
    def extract_prec(nombre):
        result = extract_prec_month(nombre)
        return (
            result[0], result[1],
            result[2], result[3],
            result[4], result[5],
            result[6], result[7],
            result[8], result[9]
        )
    #-------------------------------------------------------
    # PRECIPITACIÓN ANUAL
    #-------------------------------------------------------
    @app.callback(
        Output('date_preci_year_1', 'children'),
        Output('preci_year_1', 'children'),
        Output('date_preci_year_2', 'children'),
        Output('preci_year_2', 'children'),
        Output('date_preci_year_3', 'children'),
        Output('preci_year_3', 'children'),
        Output('date_preci_year_4', 'children'),
        Output('preci_year_4', 'children'),
        Output('date_preci_year_5', 'children'),
        Output('preci_year_5', 'children'),
        Input('nom_est', 'children'),
        Input('tabs_prec_year', 'active_tab')
    )
    def extract_prec(nombre,current_tab):
        results = extract_prec_year(nombre)
        
        dates_max = results[0:10:2]  # Fechas de los máximos valores de precipitación
        values_max = results[1:10:2]  # Valores de los máximos valores de precipitación
        dates_min = results[10:20:2]  # Fechas de los mínimos valores de precipitación
        values_min = results[11:20:2]  # Valores de los mínimos valores de precipitación
        if current_tab == 'tab_preci_year_max':
            return (
                dates_max[0], values_max[0],
                dates_max[1], values_max[1],
                dates_max[2], values_max[2],
                dates_max[3], values_max[3],
                dates_max[4], values_max[4]
            )
        elif current_tab == 'tab_preci_year_min':
            return (
                dates_min[0], values_min[0],
                dates_min[1], values_min[1],
                dates_min[2], values_min[2],
                dates_min[3], values_min[3],
                dates_min[4], values_min[4]
            )


    #-------------------------------------------------------
    # TOP5 ANOMALIAS MENSUALES
    #-------------------------------------------------------
    @app.callback(
        Output('date_month_anom_1', 'children'),
        Output('month_anom_1', 'children'),
        Output('date_month_anom_2', 'children'),
        Output('month_anom_2', 'children'),
        Output('date_month_anom_3', 'children'),
        Output('month_anom_3', 'children'),
        Output('date_month_anom_4', 'children'),
        Output('month_anom_4', 'children'),
        Output('date_month_anom_5', 'children'),
        Output('month_anom_5', 'children'),
        Input('nom_est', 'children'),
        Input('year_input_anom', 'value'),
        Input('tabs_anom', 'active_tab')
    )
    def extract_top5_anom(nombre, year, current_tab):
        result = get_anom_month(nombre, year)
        top_dates = result[:10][::2]  # Fechas de las anomalías máximas
        top_anomalies = result[:10][1::2]  # Valores de las anomalías máximas
        down_dates = result[10:][::2]  # Fechas de las anomalías mínimas
        down_anomalies = result[10:][1::2]  # Valores de las anomalías mínimas    

        if current_tab == 'tabs_anom_max':
            return (
                top_dates[0], top_anomalies[0],
                top_dates[1], top_anomalies[1],
                top_dates[2], top_anomalies[2],
                top_dates[3], top_anomalies[3],
                top_dates[4], top_anomalies[4]
            )
        elif current_tab == 'tabs_anom_min':
            return (
                down_dates[0], down_anomalies[0],
                down_dates[1], down_anomalies[1],
                down_dates[2], down_anomalies[2],
                down_dates[3], down_anomalies[3],
                down_dates[4], down_anomalies[4]
            )



    #-------------------------------------------------------
    # HEATMAP PRECIPITACIÓN 
    #-------------------------------------------------------
    @app.callback(
        Output('graph_prec', 'figure'),
        Output('year_input_prec', 'max'),
        Input('nom_est', 'children'),
        Input('year_input_prec', 'value'),
        Input('graph_select', 'value')
    )
    def plot_prec(nombre, year, graph_select):
        if graph_select == 'prec':  
            return fig_prec(nombre, year), pd.Timestamp.today().year
        else:

            pass

    #-------------------------------------------------------
    # HEATMAP ANOMALÍA
    #-------------------------------------------------------
    @app.callback(
        Output('graph_anom', 'figure'),
        Output('year_input_anom', 'max'),
        Input('nom_est', 'children'),
        Input('year_input_anom', 'value'),
        Input('graph_select', 'value') 
    )
    def plot_anom(nombre, year, graph_select):
        if graph_select == 'anom': 
            return fig_anom(nombre, year), pd.Timestamp.today().year
        else:

            pass
        
    @app.callback(
    Output('card_graph_prec', 'style'),
    Output('card_graph_anom', 'style'),
    Input('graph_select', 'value')
    )
    def update_graph_select(value):
        if value == 'prec':
            return {'display': 'block'}, {'display': 'none'}
        elif value == 'anom':
            return {'display': 'none'}, {'display': 'block'}
        else:
            return dash.no_update, dash.no_update
    #-------------------------------------------------------
    # GRAFICO DE BARRAS
    #-------------------------------------------------------
    @app.callback(
        Output('bar_chart', 'figure'),
        Input('year_input_prec', 'value'), 
        Input('nom_est', 'children')
    )
    def update_bar_chart(year, estacion):
        if year is None:
           
            return go.Figure()

        return generate_bar_chart(year, estacion)