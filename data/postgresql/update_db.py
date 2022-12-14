import requests
import json
import pandas as pd
from datetime import date, timedelta
from data.postgresql.data_fetch import data_fetch
from data.postgresql.queries import query_estaciones, query_last
from sqlalchemy import create_engine
import os

df_estaciones = pd.DataFrame(data_fetch(query_estaciones()), columns=['latitud', 'provincia', 'altitud', 'indicativo', 'nombre', 'indsinop', 'longitud'])

def new_data():
    aemet_api_key = os.getenv('AEMET_API_KEY')
    querystring = {
        "api_key": aemet_api_key}

    headers = {
        'Accept': "application/json"
    }

    # query parameters
    fechaIni = data_fetch(query_last('SANTIAGO DE COMPOSTELA AEROPUERTO'))[0][0] + timedelta(1)
    fechaFin = pd.to_datetime(date.today())
    idema = ','.join(df_estaciones['indicativo'].to_list())

    df_clim_update = pd.DataFrame()  # Empty dataframe to fill

    url_format = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}"
    date_format = '{}T00:00:00UTC'  # query str format

    fechaIniStr = date_format.format(str(fechaIni)[:10])
    fechaFinStr = date_format.format(str(fechaFin)[:10])

    url = url_format.format(fechaIniStr, fechaFinStr, idema)
    r = requests.get(url, headers=headers, params=querystring)
    # If there is no new data, return None
    if json.loads(r.text)['estado'] == 404:
        return
    url_datos = r.json()['datos']
    r_datos = requests.get(url_datos, headers=headers, params=querystring)
    datos = json.loads(r_datos.text)

    df = pd.DataFrame(datos)

    df_clim_update = pd.concat([df_clim_update, df])

    df_clim_update['fecha'] = pd.to_datetime(df_clim_update['fecha'])

    df_clim_update['altitud'].astype('int16', copy=False)

    df_clim_update['tmed'] = df_clim_update['tmed'].str.replace(',', '.')
    df_clim_update['tmed'] = df_clim_update['tmed'].str.extract('(-*\d+.\d+)').astype(float)

    df_clim_update['prec'] = df_clim_update['prec'].str.replace(',', '.')
    df_clim_update['prec'] = df_clim_update['prec'].str.extract('(\d+.\d+)').astype(float)

    df_clim_update['tmin'] = df_clim_update['tmin'].str.replace(',', '.')
    df_clim_update['tmin'] = df_clim_update['tmin'].str.extract('(-*\d+.\d+)').astype(float)

    df_clim_update['tmax'] = df_clim_update['tmax'].str.replace(',', '.')
    df_clim_update['tmax'] = df_clim_update['tmax'].str.extract('(-*\d+.\d+)').astype(float)

    df_clim_update = df_clim_update[['fecha', 'indicativo', 'nombre', 'provincia', 'altitud', 'tmed', 'prec', 'tmin', 'tmax']]

    df_clim_update = df_clim_update.dropna(subset=['tmed', 'prec', 'tmin', 'tmax'], how='all')

    return df_clim_update

def update_db(df):
    postgresql_url = os.getenv('POSTGRESQL_URL')
    db = create_engine(postgresql_url)
    conn = db.connect()
    
    for item in df['nombre'].unique():
        df[df['nombre']==item].to_sql(item, con=conn, if_exists='append', index=False)
    
    conn.close()