import psycopg2
from data.postgresql.config import config
import pandas as pd

def data_fetch(query):
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
		
        # create a cursor
        cur = conn.cursor()
        
	# execute a statement
        cur.execute(query)

        # display the PostgreSQL database server version
        data = cur.fetchall()
       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    
    return data