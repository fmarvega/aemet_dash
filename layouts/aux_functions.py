from layouts.constants import month_list, degree_sign

def extract_data(df, column, nombre, tab, month):
        df_aux = df[df['nombre'] == nombre]
        if month:
            df_aux = df_aux[df_aux['fecha'].dt.month == month]
        if tab[-3:] == 'max':
            df_aux = df_aux.sort_values(by=[column, 'fecha'], ascending=[False, False]).head(5).reset_index()
        else:
            df_aux = df_aux.sort_values(by=[column, 'fecha'], ascending=[True, False]).head(5).reset_index()
        result = []
        for i in range(5):
            fecha = df_aux.iloc[i].fecha
            result.append('{}, {} {}'.format(fecha.year, fecha.day, month_list[fecha.month-1]))
            temperature = df_aux.iloc[i][column]
            if column == 'prec':
                result.append('{:.1f}'.format(temperature) + ' mm')
            else:
                result.append('{:.1f}'.format(temperature) + degree_sign + 'C')
        return tuple(result)