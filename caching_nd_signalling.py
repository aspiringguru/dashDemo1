'''
http://dash-docs.herokuapp.com/sharing-data-between-callbacks

https://flask-caching.readthedocs.io/en/latest/
pip install Flask-Caching
https://pypi.org/project/Flask-Caching/

File "caching_nd_signalling.py", line 56, in <module>
cache.init_app(app.server, config=CACHE_CONFIG)

ValueError: Redis URL must specify one of the followingschemes (redis://, rediss://, unix

https://redislabs.com/blog/redis-on-windows-10/
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install redis-server
redis-cli -v
sudo service redis-server restart

#Execute a simple Redis command to verify your Redis server is running and available
redis-cli
127.0.0.1:6379> set user:1 "Jane"
127.0.0.1:6379> get user:1
# 127.0.0.1:6379>"Jane"
exit # to return to bash



sudo service redis-server stop


This example:

Uses Redis via Flask-Cache for storing “global variables”. This data is accessed through a function, the output of which is cached and keyed by its input arguments.
Uses the hidden div solution to send a signal to the other callbacks when the expensive computation is complete.
Note that instead of Redis, you could also save this to the file system. See https://flask-caching.readthedocs.io/en/latest/ for more details.
This “signaling” is cool because it allows the expensive computation to only take up one process. Without this type of signaling, each callback could end up computing the expensive computation in parallel, locking four processes instead of one.
This approach is also advantageous in that future sessions can use the pre-computed value. This will work well for apps that have a small number of inputs.

Here’s what this example looks like. Some things to note:

I’ve simulated an expensive process by using a time.sleep(5).
When the app loads, it takes five seconds to render all four graphs.
The initial computation only blocks one process.
Once the computation is complete, the signal is sent and four callbacks are executed in parallel to render the graphs. Each of these callbacks retrieves the data from the “global store”: the Redis or filesystem cache.
I’ve set processes=6 in app.run_server so that multiple callbacks can be executed in parallel. In production, this is done with something like $ gunicorn --workers 6 --threads 2 app:server
Selecting a value in the dropdown will take less than five seconds if it has already been selected in the past. This is because the value is being pulled from the cache.
Similarly, reloading the page or opening the app in a new window is also fast because the initial state and the initial expensive computation has already been computed.

still getting this error after installing redis on ubuntu app under windows
ValueError: Redis URL must specify one of the followingschemes (redis://, rediss://, unix://)
'''
print ("starting, importing libraries")
import os
import copy
import time
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.dependencies import Input, Output
from flask_caching import Cache


external_stylesheets = [
    # Dash CSS
    'bWLwgP.css'
    #'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Loading screen CSS
    'brPBPO.css'
    #'https://codepen.io/chriddyp/pen/brPBPO.css'
    ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
CACHE_CONFIG = {
    # try 'filesystem' if you don't want to setup redis
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.environ.get('REDIS_URL', 'localhost:6379')
}
cache = Cache()
cache.init_app(app.server, config=CACHE_CONFIG)

N = 100

df = pd.DataFrame({
    'category': (
        (['apples'] * 5 * N) +
        (['oranges'] * 10 * N) +
        (['figs'] * 20 * N) +
        (['pineapples'] * 15 * N)
    )
})
df['x'] = np.random.randn(len(df['category']))
df['y'] = np.random.randn(len(df['category']))

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in df['category'].unique()],
        value='apples'
    ),
    html.Div([
        html.Div(dcc.Graph(id='graph-1'), className="six columns"),
        html.Div(dcc.Graph(id='graph-2'), className="six columns"),
    ], className="row"),
    html.Div([
        html.Div(dcc.Graph(id='graph-3'), className="six columns"),
        html.Div(dcc.Graph(id='graph-4'), className="six columns"),
    ], className="row"),

    # hidden signal value
    html.Div(id='signal', style={'display': 'none'})
])


# perform expensive computations in this "global store"
# these computations are cached in a globally available
# redis memory store which is available across processes
# and for all time.
@cache.memoize()
def global_store(value):
    # simulate expensive query
    print('Computing value with {}'.format(value))
    time.sleep(5)
    return df[df['category'] == value]


def generate_figure(value, figure):
    fig = copy.deepcopy(figure)
    filtered_dataframe = global_store(value)
    fig['data'][0]['x'] = filtered_dataframe['x']
    fig['data'][0]['y'] = filtered_dataframe['y']
    fig['layout'] = {'margin': {'l': 20, 'r': 10, 'b': 20, 't': 10}}
    return fig


@app.callback(Output('signal', 'children'), [Input('dropdown', 'value')])
def compute_value(value):
    # compute value and send a signal when done
    global_store(value)
    return value


@app.callback(Output('graph-1', 'figure'), [Input('signal', 'children')])
def update_graph_1(value):
    # generate_figure gets data from `global_store`.
    # the data in `global_store` has already been computed
    # by the `compute_value` callback and the result is stored
    # in the global redis cached
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'markers',
            'marker': {
                'opacity': 0.5,
                'size': 14,
                'line': {'border': 'thin darkgrey solid'}
            }
        }]
    })


@app.callback(Output('graph-2', 'figure'), [Input('signal', 'children')])
def update_graph_2(value):
    return generate_figure(value, {
        'data': [{
            'type': 'scatter',
            'mode': 'lines',
            'line': {'shape': 'spline', 'width': 0.5},
        }]
    })


@app.callback(Output('graph-3', 'figure'), [Input('signal', 'children')])
def update_graph_3(value):
    return generate_figure(value, {
        'data': [{
            'type': 'histogram2d',
        }]
    })


@app.callback(Output('graph-4', 'figure'), [Input('signal', 'children')])
def update_graph_4(value):
    return generate_figure(value, {
        'data': [{
            'type': 'histogram2dcontour',
        }]
    })


if __name__ == '__main__':
    app.run_server(debug=False, processes=6)
