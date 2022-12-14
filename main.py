from layouts.layout import layout
from layouts.callbacks import register_callbacks
from dash import Dash
import dash_bootstrap_components as dbc
from data.postgresql.update_db import new_data, update_db

# Automatic database update
data=new_data()
if data is not None:
    update_db(data)

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)