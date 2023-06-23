import pandas as pd
import numpy as np
import plotly.graph_objs as go
import plotly.express as px
from layouts.constants import month_list, degree_sign
from data.postgresql.data_fetch import data_fetch
from data.postgresql.queries import query_records, query_records_month, query_year_prec, query_year_anom, query_tmed, query_prec_month,query_prec_year

def extract_data(column, estacion, tab, month=None):
    order = tab[-3:]

    if month:
        df = pd.DataFrame(data_fetch(query_records_month(column, estacion, order, month)), columns=['fecha', column])
    else:
        df = pd.DataFrame(data_fetch(query_records(column, estacion, order)), columns=['fecha', column])

    result = []
    for i in range(5):
        fecha = df.iloc[i].fecha
        result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month - 1]))
        temperature = df.iloc[i][column]
        if column == 'prec':
            result.append('{:.1f} mm'.format(temperature))
        else:
            result.append('{:.1f}{}'.format(temperature, degree_sign + 'C'))
    return tuple(result)
#######################################################################################################
#######################################################################################################
def extract_prec_month(estacion):
    query = query_prec_month(estacion)
    results = data_fetch(query)

    dates = ['{} {}'.format(month_list[result[0] - 1], result[1]) for result in results]
    precipitations = ['{:.1f} mm'.format(result[2]) for result in results]
    return (
        dates[0], precipitations[0],
        dates[1], precipitations[1],
        dates[2], precipitations[2],
        dates[3], precipitations[3],
        dates[4], precipitations[4]
    )
#######################################################################################################
def extract_prec_year(estacion):
    query = query_prec_year(estacion)
    results = data_fetch(query)
    
    # Ordenar los resultados en orden ascendente
    results_asc = sorted(results, key=lambda x: x[1])

    # Obtener los valores máximos y mínimos
    results_max = results_asc[-5:][::-1]  # Los 5 valores máximos en orden descendente
    results_min = results_asc[:5]  # Los 5 valores mínimos en orden ascendente

    # Crear las listas de fechas y valores para máximos y mínimos
    dates_max = ['{}'.format(result[0]) for result in results_max]
    values_max = ['{:.1f} mm'.format(result[1]) for result in results_max]
    dates_min = ['{}'.format(result[0]) for result in results_min]
    values_min = ['{:.1f} mm'.format(result[1]) for result in results_min]
    # Retornar los valores como una tupla
    return (
        dates_max[0], values_max[0],
        dates_max[1], values_max[1],
        dates_max[2], values_max[2],
        dates_max[3], values_max[3],
        dates_max[4], values_max[4],
        dates_min[0], values_min[0],
        dates_min[1], values_min[1],
        dates_min[2], values_min[2],
        dates_min[3], values_min[3],
        dates_min[4], values_min[4]
    )



#######################################################################################################
## G R Á F I C O   P R E C I P I T A C I Ó N 
#######################################################################################################
def get_prec(estacion, year):

    df_aux = pd.DataFrame(data_fetch(query_year_prec(estacion, year)), columns=['month', 'day','prec'])
    df_prec = pd.pivot_table(df_aux, values='prec', index='month', columns='day')
    #print(df_prec)
    heat_prec = np.empty((12,31))*np.nan
    
    heat_prec = df_prec.to_numpy()
    return heat_prec

def fig_prec(estacion, year):
    heat_prec = get_prec(estacion, year)

    customdata=[]
    customdata.append(heat_prec)

    fig = px.imshow(heat_prec, color_continuous_scale='BuPu',
                    zmin=0, zmax=20, text_auto='.1f', aspect='auto')
    values_df = pd.DataFrame(heat_prec).apply(lambda x: np.round(x,1), axis=1).fillna('x').astype('str')
    fig.update_traces(text=values_df,
                        texttemplate='%{text}')
    fig.update_traces(hoverongaps=False, textfont=dict(size=11))
    fig.update_yaxes(range=[0, 11])
    fig.update(data=[{'customdata': np.dstack((customdata[0])),
                    'hovertemplate':'%{x} de %{y}<br>Precipitacion: %{z:.2f}mm.'}])

    fig.update_layout(
        margin={'b': 10, 'l': 0, 'r': 40, 't': 40},
        paper_bgcolor='#32383e',
        plot_bgcolor= '#32383e',
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
                tickfont=dict(color='white', size=11),
                title=dict(text='Precipitación (mm)', font=dict(color='white', size=11)),
                # ticklabelposition = 'inside'
            )
        )
    )
    fig.update_xaxes(tickfont_color='white', tickfont_size=11)
    fig.update_yaxes(tickfont_color='white', tickfont_size=11)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(range=[11.5,-0.5], autorange=False, showgrid=False, zeroline=False)
    return fig
#######################################################################################################
## G R Á F I C O   A N O M A L I A S
#######################################################################################################
def get_anom(estacion, year):
    df_med = pd.DataFrame(data_fetch(query_tmed(estacion)), columns=['month','day','tmed'])
    df_med = pd.pivot_table(df_med, values='tmed', index='month', columns='day')
    #print(df_med)
    df_aux = pd.DataFrame(data_fetch(query_year_anom(estacion, year)), columns=['month', 'day', 'tmed', 'tmax', 'tmin'])
    df_heat = pd.pivot_table(df_aux, values='tmed', index='month', columns='day')
    df_max = pd.pivot_table(df_aux, values='tmax', index='month', columns='day')
    df_min = pd.pivot_table(df_aux, values='tmin', index='month', columns='day')

    heat_anom = np.empty((12,31))*np.nan
    heat_max = np.empty((12,31))*np.nan
    heat_min = np.empty((12,31))*np.nan
    
    shape_mat = df_heat.to_numpy().shape
    months = (df_heat.index.astype(int).to_numpy()-1).tolist()

    if len(months) == 1:
        heat_anom[:shape_mat[0],:shape_mat[1]] = df_heat.to_numpy()-df_med.to_numpy()[months,range(len(df_heat.to_numpy()))]
    else:
        heat_anom[:shape_mat[0],:shape_mat[1]] = df_heat.to_numpy()-df_med.to_numpy()[months,:]

    heat_med = heat_anom + df_med.to_numpy()
    heat_max[:shape_mat[0], :shape_mat[1]] = df_max.to_numpy()
    heat_min[:shape_mat[0], :shape_mat[1]] = df_min.to_numpy()
    return heat_anom, heat_med, heat_max, heat_min

    
def fig_anom(estacion, year):
    heat_anom, heat_med, heat_max, heat_min = get_anom(estacion, year)

    customdata=[]
    customdata.append(heat_med)
    customdata.append(heat_max)
    customdata.append(heat_min)

    fig = px.imshow(heat_anom, color_continuous_scale='RdBu_r',
                    zmin=-15, zmax=15, text_auto='.1f', aspect='auto')
    values_df = pd.DataFrame(heat_anom).apply(lambda x: np.round(x,1), axis=1).fillna('x').astype('str')
    fig.update_traces(text=values_df,
                        texttemplate='%{text}')
    fig.update_traces(hoverongaps=False, textfont=dict(size=11))
    fig.update_yaxes(range=[0, 11])
    fig.update(data=[{'customdata': np.dstack((customdata[0],customdata[1],customdata[2])),
                    'hovertemplate':'%{x} de %{y}<br>Anomalía: %{z:.2f}\u00b0C<br>Temperatura media: %{customdata[0]:.1f}\u00b0C<br>Temperatura máxima: %{customdata[1]:.1f}\u00b0C<br>Temperatura mínima: %{customdata[2]:.1f}\u00b0C'}])

    fig.update_layout(
        margin={'b': 10, 'l': 0, 'r': 40, 't': 40},
        paper_bgcolor='#32383e',
        plot_bgcolor= '#32383e',
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
                tickfont=dict(color='white', size=11),
                title=dict(text='Anomalía térmica (' + degree_sign + 'C)', font=dict(color='white', size=11)),
                # ticklabelposition = 'inside'
            )
        )
    )
    fig.update_xaxes(tickfont_color='white', tickfont_size=11)
    fig.update_yaxes(tickfont_color='white', tickfont_size=11)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(range=[11.5,-0.5], autorange=False, showgrid=False, zeroline=False)
    return fig
#########################################################################################################################
def get_top_anom(estacion, year):
    df_med = pd.DataFrame(data_fetch(query_tmed(estacion)), columns=['month','day','tmed'])
    df_med = pd.pivot_table(df_med, values='tmed', index='month', columns='day')

    df_aux = pd.DataFrame(data_fetch(query_year_anom(estacion, year)), columns=['month', 'day', 'tmed', 'tmax', 'tmin'])
    df_heat = pd.pivot_table(df_aux, values='tmed', index='month', columns='day')

    heat_anom = np.empty((12,31))*np.nan
    
    shape_mat = df_heat.to_numpy().shape
    months = (df_heat.index.astype(int).to_numpy()-1).tolist()

    if len(months) == 1:
        heat_anom[:shape_mat[0],:shape_mat[1]] = df_heat.to_numpy()-df_med.to_numpy()[months,range(len(df_heat.to_numpy()))]
    else:
        heat_anom[:shape_mat[0],:shape_mat[1]] = df_heat.to_numpy()-df_med.to_numpy()[months,:]

    return heat_anom

def get_anom_month(estacion, year):
    heat_anom = get_top_anom(estacion, year)
    
    anom_month_avg = [(i, np.nanmean(heat_anom[i])) for i in range(len(heat_anom))]
    anom_month_avg = sorted(anom_month_avg, key=lambda x: x[1], reverse=True)
    anom_month_avg_2 = sorted(anom_month_avg, key=lambda x: x[1], reverse=False)
    top5_months = anom_month_avg[:5]
    down5_months = anom_month_avg_2[:5]
    results = [(month, year, anomaly) for (month, anomaly) in top5_months]
    results2 = [(month, year, anomaly) for (month, anomaly) in down5_months]
    print('TOP5 anomalies', results)
    dates = ['{} {}'.format(month_list[result[0]], result[1]) for result in results]
    dates2 = ['{} {}'.format(month_list[result[0]], result[1]) for result in results2]

    anomalies = ['{:.1f} {}'.format(result[2], degree_sign + 'C') for result in results]
    anomalies2 = ['{:.1f} {}'.format(result[2], degree_sign + 'C') for result in results2]
    #print('anomalies',anomalies,anomalies2)
    return (
        dates[0], anomalies[0],
        dates[1], anomalies[1],
        dates[2], anomalies[2],
        dates[3], anomalies[3],
        dates[4], anomalies[4],
        dates2[0], anomalies2[0],
        dates2[1], anomalies2[1],
        dates2[2], anomalies2[2],
        dates2[3], anomalies2[3],
        dates2[4], anomalies2[4],
        
    )
#######################################################################################################
## G R Á F I C O   B A R R A S
#######################################################################################################
def generate_bar_chart(year, estacion):
    query = query_prec_month(estacion)
    results = data_fetch(query)
    df_filtered = sorted(results, key=lambda x: (x[0], x[1]))

    df = pd.DataFrame(df_filtered, columns=['month', 'year', 'prec'])
    df_filtered = df[df['year'] == year].astype(int)

    month_names = [month_list[int(result[1]['month']) - 1] + ' ' + str(result[1]['year']) for result in df_filtered.iterrows()]

    # Crear la figura de barras
    fig = go.Figure()
    fig.add_trace(go.Bar(x=month_names, y=df_filtered['prec']))
    fig.update_layout(
        title='Precipitación para el año {} (Total: {} mm)'.format(year, df_filtered['prec'].sum().round(1)),
        paper_bgcolor='#32383e',
        plot_bgcolor= '#32383e',
        xaxis_title='Mes',
        yaxis_title='Lluvia mm',
        font=dict(size=12,color= '#999'),
    ),
    fig.update_xaxes(tickfont_color='white', tickfont_size=11)
    fig.update_yaxes(tickfont_color='white',tickfont_size=11)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(showgrid=True,gridcolor='LightBlue',gridwidth=1,)
    #fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=1)
    return fig
