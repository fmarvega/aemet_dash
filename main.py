# Dash bootstrap cheatsheet: https://dashcheatsheet.pythonanywhere.com/
from layouts.layout import layout
from layouts.callbacks import register_callbacks
from dash import Dash
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

load_figure_template('SUPERHERO')

app = Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
server = app.server
app.layout = layout
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)