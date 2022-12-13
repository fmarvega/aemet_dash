def query_records(column, estacion, max):
    if max=='max':
        order = 'DESC'
    else:
        order = ''

    query = '''
        SELECT fecha, {} 
        FROM "{}" 
        WHERE {} IS NOT NULL 
        ORDER BY {} {}, fecha DESC LIMIT 5
    '''.format(column, estacion, column, column, order)
    return query

def query_records_month(column, estacion, max, month):
    if max=='max':
        order = 'DESC'
    else:
        order = ''

    query = '''
        SELECT fecha, {} 
        FROM "{}" 
        WHERE ({} IS NOT NULL) AND ((EXTRACT(MONTH FROM "fecha")) = {}) 
        ORDER BY {} {}, fecha DESC LIMIT 5
    '''.format(column, estacion, column, month, column, order)
    return query

def query_year(estacion, year):

    query = '''
        SELECT EXTRACT(MONTH FROM fecha),EXTRACT (DAY FROM fecha), tmed, tmax, tmin 
        FROM "{}" 
        WHERE fecha >= '{}-01-01' AND fecha <= '{}-12-31'
    '''.format(estacion, year, year)
    return query

def query_tmed(estacion):

    query = '''
        SELECT EXTRACT(MONTH FROM fecha),EXTRACT (DAY FROM fecha), AVG(tmed)
        FROM "{}"
        GROUP BY EXTRACT(MONTH FROM fecha), EXTRACT (DAY FROM fecha)
        ORDER BY EXTRACT(MONTH FROM fecha), EXTRACT(DAY FROM fecha)
    '''.format(estacion)
    return query

def query_estaciones():

    query = '''
        SELECT *
        FROM estaciones
    '''
    return query

def query_from(estacion, column):

    query = '''
        SELECT fecha
        FROM "{}"
        WHERE "{}" IS NOT NULL 
        ORDER BY fecha LIMIT 1
    '''.format(estacion, column)
    return query

def query_last(estacion):

    query = '''
        SELECT fecha
        FROM "{}"
        ORDER BY fecha DESC LIMIT 1
    '''.format(estacion)
    return query