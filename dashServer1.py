# -*- coding: utf-8 -*-
'''
https://dash.plot.ly/getting-started
pip install dash==1.6.1
pip install dash-daq==0.3.1

'''

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['dashServer1.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}


app.layout = html.Div(children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),


    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 6], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

print("__name__ = ", __name__)
if __name__ == '__main__':
    print("start server")
    #app.run_server(debug=True) # this causes errors - OSError: [Errno 8] Exec format error:
    #app.run_server(dev_tools_hot_reload=False)
    #https://dash.plot.ly/devtools
    app.run_server(debug=False)
