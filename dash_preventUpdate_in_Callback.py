'''
https://dash.plot.ly/state
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

external_stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Button('Click here to see the content', id='button'),
    html.Div(id='body-div'),
    html.Div(id='click_count')
])

@app.callback(
    [Output(component_id='body-div', component_property='children'),
     Output(component_id='click_count', component_property='children')],
    [Input(component_id='button', component_property='n_clicks')]
)
def update_output(n_clicks):
    print("update_output : n_clicks=", n_clicks)
    if n_clicks is None:
        raise PreventUpdate
    else:
        return "Elephants are the only animal that can't jump", '''The button has been pressed {} times.'''.format(n_clicks)

if __name__ == '__main__':
    app.run_server(debug=False)
