import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.express as px

gdp_data = pd.read_csv('gdp_cleaned.csv')
fiscal_data = pd.read_csv('fiscal_cleaned.csv')
data = pd.read_csv('data/Stringency data.csv')
df = pd.DataFrame(data)

countries_to_include = ['China', 'France', 'Germany', 'Italy', 'Japan', 'United Kingdom', 'United States', 'South Korea', 'Spain']

gdp_data = gdp_data[gdp_data['country'].isin(countries_to_include)]
fiscal_data = fiscal_data[fiscal_data['country'].isin(countries_to_include)]

def update_scatter_plot(relayoutData):
    # Merge the two datasets if necessary
    merged_data = pd.merge(gdp_data, fiscal_data, on='country')

    # Create the scatter plot using Plotly Express
    fig = px.scatter(merged_data, x='GDP per capita, PPP (constant 2017 international $)', y='total_fiscal', color='country', title="GDP vs Fiscal Data")

    # Set a dark theme template
    fig.update_layout(template='plotly_dark')

    return fig

def update_graph(selected_countries):
    fig = px.line(df, x='Date', y=selected_countries)
    fig.update_traces(mode='lines+markers')
    fig.update_layout(
        title='COVID-19 Stringency Index by Country',
        xaxis_title='Date',
        yaxis_title='Stringency Index',
        template='plotly_dark' 
    )
    return fig

layout = html.Div([
    html.H1("Impact Page", style={'textAlign': 'center'}),
    
    html.Div([html.H3("Graph1: Scatter Plot of GDP vs Fiscal Data", style={'color': 'white'}),
    dcc.Graph(id='scatter-plot', figure=update_scatter_plot(), config={'displayModeBar': False}),
]),
    html.Div([html.H3("Graph 2: Add your second graph here"),
    dcc.Dropdown(
        id='country-dropdown',
        options=[{'label': country, 'value': country} for country in df.columns[1:]],
        value=['Canada'],  # Default selected country
        multi=True
    ),
    dcc.Graph(id='line-plot', figure=update_graph())
        ]),

])
