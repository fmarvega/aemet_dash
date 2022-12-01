import pandas as pd
import numpy as np
import plotly.express as px
from dash import Input, Output
from layouts.constants import month_list, degree_sign
from layouts.functions import update_df
from layouts.aux_functions import extract_data

df_clim_1 = pd.read_csv('data/df_clim_1.csv')
df_clim_2 = pd.read_csv('data/df_clim_2.csv')
df_estaciones = pd.read_csv('data/df_estaciones.csv')

df_clim = pd.concat([df_clim_1, df_clim_2], sort=False)
df_clim['fecha'] = pd.to_datetime(df_clim['fecha'])
df_clim = update_df(df_clim, df_estaciones)

df_clim['amplitud_termica'] = df_clim['tmax']-df_clim['tmin']

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
        df_aux = df_clim[df_clim['nombre'] == nombre]
        year_max = df_aux[['tmax','fecha']].dropna(subset=['tmax']).sort_values(by='fecha', ascending=True).iloc[0].fecha.year
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
        return extract_data(df_clim, 'tmax', nombre, tab, month)

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
        return extract_data(df_clim, 'tmin', nombre, tab, month)

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
        return extract_data(df_clim, 'amplitud_termica', nombre, tab, month)

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
        return extract_data(df_clim, 'prec', nombre, 'max', month)

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