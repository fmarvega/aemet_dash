from layouts.layout import layout
from layouts.callbacks import register_callbacks
from dash import Dash
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc
from data.postgresql.update_db import new_data, update_db

load_figure_template('SUPERHERO')

# Automatic database update
data=new_data()
if data is not None:
    update_db(data)

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout = layout
register_callbacks(app)

app.run_server(debug=True)
