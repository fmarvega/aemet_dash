def update_df(df_clim, df_estaciones):
    import requests
    import json
    import pandas as pd
    from datetime import date, timedelta
    import time

    querystring = {
        "api_key": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJmbWFydmVnYUBnbWFpbC5jb20iLCJqdGkiOiI5NmZhNTM1ZC0yYzY1LTRjNDktYWUxYS00YWU4M2UzNjhmNzIiLCJpc3MiOiJBRU1FVCIsImlhdCI6MTYyNjg3MDE1NSwidXNlcklkIjoiOTZmYTUzNWQtMmM2NS00YzQ5LWFlMWEtNGFlODNlMzY4ZjcyIiwicm9sZSI6IiJ9.PC6TWrEaDskCo6G8dJCXlO6CvDqNYKESGj5WGVh5sYI"}

    headers = {
        'Accept': "application/json"
    }

    # query parameters
    fechaIni = df_clim.sort_values('fecha', ascending=False).iloc[0]['fecha'] + timedelta(1)
    fechaFin = pd.to_datetime(date.today())
    idema = ','.join(df_estaciones['indicativo'].to_list())

    df_clim_update = pd.DataFrame()  # Empty dataframe to fill

    url_format = "https://opendata.aemet.es/opendata/api/valores/climatologicos/diarios/datos/fechaini/{}/fechafin/{}/estacion/{}"
    date_format = '{}T00:00:00UTC'  # query str format

    date_range = fechaFin - fechaIni
    fechaIniAux = fechaIni

    # Splitting long querys
    while date_range > timedelta(1800):
        fechaFinAux = fechaIniAux + timedelta(1800)
        # Query data
        fechaIniAuxStr = date_format.format(str(fechaIniAux)[:10])
        fechaFinAuxStr = date_format.format(str(fechaFinAux)[:10])

        url = url_format.format(fechaIniAuxStr, fechaFinAuxStr, idema)
        r = requests.get(url, headers=headers, params=querystring)
        if json.loads(r.text)['estado'] == 404:
            return df_clim
        url_datos = r.json()['datos']
        r_datos = requests.get(url_datos, headers=headers, params=querystring)
        datos = json.loads(r_datos.text)

        df = pd.DataFrame(datos)

        # Concat dataframe
        df_clim_update = pd.concat([df_clim_update, df])

        # Recalculate dates
        fechaIniAux = fechaFinAux + timedelta(1)
        date_range = fechaFin - fechaIniAux

    # Query data in datarange < 1800
    fechaIniAuxStr = date_format.format(str(fechaIniAux)[:10])
    fechaFinStr = date_format.format(str(fechaFin)[:10])

    url = url_format.format(fechaIniAuxStr, fechaFinStr, idema)
    r = requests.get(url, headers=headers, params=querystring)
    # If there is no new data, return the original df
    if json.loads(r.text)['estado'] == 404:
        return df_clim
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

    df_clim_update = df_clim_update[list(df_clim.columns)]

    df_clim_update = df_clim_update.dropna(subset=['tmed', 'prec', 'tmin', 'tmax'], how='all')

    return pd.concat([df_clim, df_clim_update], sort=False)