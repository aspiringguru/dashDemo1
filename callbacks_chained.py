'''
https://dash.plot.ly/getting-started-part-2
'''

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

all_options = {
    'America': ['New York City', 'San Francisco', 'Cincinnati'],
    'Canada': [u'Montréal', 'Toronto', 'Ottawa']
}

for k in all_options.keys():
    print("k:", k)

app.layout = html.Div([
    dcc.RadioItems(
        id='countries-dropdown',
        options=[{'label': k, 'value': k} for k in all_options.keys()],
        value='America'
    ),
    html.Hr(),
    dcc.RadioItems(id='cities-dropdown'),
    html.Hr(),
    html.Div(id='display-selected-values'),
    html.Hr(),
    html.Div(id='display-selected-city')
])


@app.callback(
    Output('cities-dropdown', 'options'),
    [Input('countries-dropdown', 'value')])
def set_cities_options(selected_country):
    print("start set_cities_options.")
    return [{'label': i, 'value': i} for i in all_options[selected_country]]


@app.callback(
    Output('cities-dropdown', 'value'),
    [Input('cities-dropdown', 'options')])
def set_cities_value(available_options):
    print("start set_cities_value.")
    return available_options[0]['value']


@app.callback(
    [Output('display-selected-values', 'children'),
     Output('display-selected-city', 'children')],
    [Input('countries-dropdown', 'value'),
     Input('cities-dropdown', 'value')])
def set_display_children(selected_country, selected_city):
    print("start set_display_children.")
    result1 = u'{} is a city in {}'.format(selected_city, selected_country,)
    return result1, selected_city


if __name__ == '__main__':
    app.run_server(debug=False)
