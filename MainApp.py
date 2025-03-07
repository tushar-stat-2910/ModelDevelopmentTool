import os
import subprocess
import dash
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Button("Classification", id="classification-btn", n_clicks=0),
    html.Button("Clustering", id="clustering-btn", n_clicks=0),
    html.Div(id='page-content')
])

# Track process instances
processes = {}

@app.callback(
    Output('page-content', 'children'),
    [Input('classification-btn', 'n_clicks'),
     Input('clustering-btn', 'n_clicks')]
)
def launch_app(classification_clicks, clustering_clicks):
    global processes
    ctx = dash.callback_context
    if not ctx.triggered:
        return html.H3("Welcome! Click a button to load an app.")

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    # Start classification app
    if button_id == "classification-btn":
        if "classification" not in processes:
            processes["classification"] = subprocess.Popen(["python", "dashApp.py"])
        return html.Iframe(src="http://127.0.0.1:8051", width="100%", height="600px")

    # Start clustering app
    elif button_id == "clustering-btn":
        if "clustering" not in processes:
            processes["clustering"] = subprocess.Popen(["python", "clusterApp.py"])
        return html.Iframe(src="http://127.0.0.1:8052", width="100%", height="600px")

    return html.H3("Welcome! Click a button to load an app.")

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
