import pandas as pd
import plotly.express as px
from dash import Input, Output
from layouts.constants import month_list, degree_sign
from layouts.functions import update_df
from layouts.aux_functions import extract_data, fig_anom
from data.postgresql.data_fetch import data_fetch
from data.postgresql.queries import query_estaciones, query_from

# df_clim_1 = pd.read_csv('data/df_clim_1.csv')
# df_clim_2 = pd.read_csv('data/df_clim_2.csv')
# df_estaciones = pd.read_csv('data/df_estaciones.csv')
df_estaciones = pd.DataFrame(data_fetch(query_estaciones()), columns=['latitud', 'provincia', 'altitud', 'indicativo', 'nombre', 'indsinop', 'longitud'])

# df_clim = pd.concat([df_clim_1, df_clim_2], sort=False)
# df_clim['fecha'] = pd.to_datetime(df_clim['fecha'])
# df_clim = update_df(df_clim, df_estaciones)

# df_clim['amplitud_termica'] = df_clim['tmax']-df_clim['tmin']

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
                Output('desde_amp', 'children'),
                Output('desde_prec', 'children'),
                Output('year_input', 'min'),
                Input('nom_est', 'children'))
    def update_year(nombre):
        # df_aux = df_clim[df_clim['nombre'] == nombre]
        year_max = data_fetch(query_from(nombre, 'tmax'))[0][0].year
        year_prec = data_fetch(query_from(nombre, 'prec'))[0][0].year
        # year_max = df_aux[['tmax','fecha']].dropna(subset=['tmax']).sort_values(by='fecha', ascending=True).iloc[0].fecha.year
        # year_prec = df_aux[['prec','fecha']].dropna(subset=['prec']).sort_values(by='fecha', ascending=True).iloc[0].fecha.year
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

    @app.callback(
        Output('graph_anom', 'figure'),
        Input('nom_est', 'children'),
        Input('year_input', 'value'))
    def plot_anom(nombre, year):
        return fig_anom(nombre, year)