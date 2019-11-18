# dash Demo

Demonstration project using the plotly dash framework

## Installation


```bash
pip install dash==1.6.1  
pip install dash-daq==0.3.1  
```

## development notes

Follows the working examples from here
https://dash.plot.ly/getting-started

had to turn off debug mode, related git issue
https://github.com/pallets/flask/issues/3133
https://flask.palletsprojects.com/en/1.0.x/cli/
```
#app.run_server(debug=True) # this causes errors - OSError: [Errno 8] Exec format error:
app.run_server(debug=False)
```




## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
