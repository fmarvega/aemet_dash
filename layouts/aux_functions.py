import pandas as pd
import numpy as np
import plotly.express as px
from layouts.constants import month_list, degree_sign
from data.postgresql.data_fetch import data_fetch
from data.postgresql.queries import query_records, query_records_month, query_tmed, query_year

def extract_data(column, estacion, tab, month):

        order = tab[-3:]

        if month:
            df = pd.DataFrame(data_fetch(query_records_month(column, estacion, order, month)), columns=['fecha',column])
        else:
            df = pd.DataFrame(data_fetch(query_records(column, estacion, order)), columns=['fecha',column])

        result = []
        for i in range(5):
            fecha = df.iloc[i].fecha
            result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month-1]))
            temperature = df.iloc[i][column]
            if column == 'prec':
                result.append('{:.1f}'.format(temperature) + ' mm')
            else:
                result.append('{:.1f}'.format(temperature) + degree_sign + 'C')
        return tuple(result)

def get_anom(estacion, year):
    df_med = pd.DataFrame(data_fetch(query_tmed(estacion)), columns=['month','day','tmed'])
    df_med = pd.pivot_table(df_med, values='tmed', index='month', columns='day')

    # print(df_med)

    df_aux = pd.DataFrame(data_fetch(query_year(estacion, year)), columns=['month', 'day', 'tmed', 'tmax', 'tmin'])
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
