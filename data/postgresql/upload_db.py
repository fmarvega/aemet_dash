from sqlalchemy import create_engine
import pandas as pd
from layouts.tokens import postgresql_url

df_clim_1 = pd.read_csv('data/df_clim_1.csv')
df_clim_2 = pd.read_csv('data/df_clim_2.csv')
df_estaciones = pd.read_csv('data/df_estaciones.csv')

df_clim = pd.concat([df_clim_1, df_clim_2], sort=False)
df_clim['fecha'] = pd.to_datetime(df_clim['fecha'])

def initial_update_db():

    """ Connect to the PostgreSQL database server """
    db = create_engine(postgresql_url)
    conn = db.connect()
    print('Database connection established')

    df_estaciones.to_sql('estaciones', con=conn, if_exists='replace', index=False)
    for item in df_estaciones['nombre']:
        df_clim[df_clim['nombre']==item].to_sql(item, con=conn, if_exists='replace', index=False)
    
    print('Data uploaded to database')

    conn.close()
    print('Database connection closed')


if __name__ == '__main__':
    initial_update_db()