'''
https://dash.plot.ly/getting-started-part-2
'''
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['dashServer1.css']
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id='my-id', value='initial value 1', type='text'),
    dcc.Input(id='my-id2', value='initial value 1', type='text'),
    html.Div(id='my-div'), html.Div(id='my-div2')
])


@app.callback(
    [Output(component_id='my-div', component_property='children'), Output(component_id='my-div2', component_property='children')],
    [   Input(component_id='my-id', component_property='value'), Input(component_id='my-id2', component_property='value')]
)

def update_output_div(input_value, input_value2):
    print("input_value:", input_value)
    print("input_value2:", input_value2)
    return ('value =  "{}"'.format(input_value), 'value =  "{}"'.format(input_value2))


if __name__ == '__main__':
    app.run_server(debug=False)
