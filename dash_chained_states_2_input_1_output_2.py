'''
https://dash.plot.ly/state

as dash_chained_states_2_input_1_output.py but with the dcc.Input as dash.dependencies.State and a button as dash.dependencies.Input.
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

external_stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='input-1-state', type='text', value='Montréal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Button(id='submit-button2', n_clicks=0, children='Submit'),
    html.Div(id='output-state')
])


@app.callback(Output('output-state', 'children'),
              [Input('submit-button', 'n_clicks'),
               Input('submit-button2', 'n_clicks')],
              [State('input-1-state', 'value'),
               State('input-2-state', 'value')])
def update_output(n_clicks, n_clicks2, input1, input2):
    print("update_output : n_clicks=", n_clicks)
    print("update_output : n_clicks2=", n_clicks2)
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}", second button pressed {} times."
    '''.format(n_clicks, input1, input2, n_clicks2)


if __name__ == '__main__':
    app.run_server(debug=False)
