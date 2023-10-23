import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

# Callback to handle page navigation
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/impact':
        # Import the impact page module
        from pages import impact
        return impact.layout
    else:
        # Default to the landing page
        from pages import landing
        return landing.layout

if __name__ == '__main__':
    app.run_server(debug=True)
