'''
https://dash.plot.ly/getting-started-part-2
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(
        id='num',
        type='number',
        value=5
    ),
    dcc.Input(
        id='num2',
        type='number',
        value=3
    ),
    html.Table([
        html.Tr([html.Td(['x', html.Sup(2)]), html.Td(id='square')]),
        html.Tr([html.Td(['x', html.Sup(3)]), html.Td(id='cube')]),
        html.Tr([html.Td([2, html.Sup('x')]), html.Td(id='twos')]),
        html.Tr([html.Td([3, html.Sup('x')]), html.Td(id='threes')]),
        html.Tr([html.Td(['x', html.Sup('x')]), html.Td(id='x^x')]),
        html.Tr([html.Td(['y']), html.Td(id='y')]),
    ]),
])


@app.callback(
    [Output('square', 'children'),
     Output('cube', 'children'),
     Output('twos', 'children'),
     Output('threes', 'children'),
     Output('x^x', 'children'),
     Output('y', 'children')],
    [Input('num', 'value'),
     Input('num2', 'value')])
def callback_a(x, x2):
    print("x=", x)
    print("x2=", x2)
    return x**2, x**3, 2**x, 3**x, x**x, x2


if __name__ == '__main__':
    app.run_server(debug=False)
