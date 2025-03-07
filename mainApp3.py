import dash
import dash_html_components as html
from dash.dependencies import Input, Output
import subprocess
import time
import psutil

# Function to check if a port is in use
def is_port_in_use(port):
    for conn in psutil.net_connections():
        if conn.laddr.port == port:
            return True
    return False

# Start external Dash apps if they are not running
def start_dash_app(script_name, port):
    if not is_port_in_use(port):
        return subprocess.Popen(["python", script_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return None

# Start the Classification and Clustering apps
classification_process = start_dash_app("dashApp.py", 8051)
clustering_process = start_dash_app("clusterApp.py", 8052)

app = dash.Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    html.Div([
        html.Button("Classification", id="classification-btn", n_clicks=0),
        html.Button("Clustering", id="clustering-btn", n_clicks=0),
    ]),
    html.Div(id='page-content')  # Dynamically updates the content
])

@app.callback(
    Output('page-content', 'children'),
    [Input('classification-btn', 'n_clicks'),
     Input('clustering-btn', 'n_clicks')]
)
def display_page(classification_clicks, clustering_clicks):
    if classification_clicks > 0:
        return html.Iframe(src="http://127.0.0.1:8051", width="100%", height="800px")
    elif clustering_clicks > 0:
        return html.Iframe(src="http://127.0.0.1:8052", width="100%", height="800px")

    return html.H3("Welcome! Click a button to load an app.")

if __name__ == '__main__':
    time.sleep(2)  # Give subprocesses time to start
    app.run_server(debug=True, port=8050)
