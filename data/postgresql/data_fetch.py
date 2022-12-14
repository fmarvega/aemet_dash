from sqlalchemy import create_engine
import os

def data_fetch(query):
    conn = None
    postgresql_url = os.getenv('POSTGRESQL_URL')       
    db = create_engine(postgresql_url)
    conn = db.connect()
    data = conn.execute(query)

    if conn is not None:
        conn.close()
    
    return data.all()