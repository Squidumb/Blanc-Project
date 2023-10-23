import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
from sklearn.impute import SimpleImputer

df = pd.read_excel('data/data.xlsx')
imputer = SimpleImputer(strategy='median')
numeric_columns = df.select_dtypes(include=['float64'])
imputer.fit(numeric_columns)
df_filled = df.copy()
df_filled[numeric_columns.columns] = imputer.transform(numeric_columns)
df_filled

european_countries = ["Germany", "France", "Italy", "Spain", "United Kingdom", "Greece", "Portugal", "Netherlands", "Belgium", "Austria", "Sweden", "Norway", "Denmark", "Switzerland", "Ireland", "Finland", "Poland", "Czech Republic", "Hungary", "Slovakia", "Romania", "Bulgaria", "Croatia", "Slovenia", "Estonia", "Latvia", "Lithuania", "Luxembourg", "Cyprus", "Malta", "Iceland", "Liechtenstein", "Andorra", "Monaco", "San Marino", "Vatican City", "Albania", "North Macedonia", "Montenegro", "Serbia", "Bosnia and Herzegovina", "Kosovo", "Moldova", "Ukraine", "Belarus", "Russia", "Turkey"]
european_df = df_filled[df_filled['country'].isin(european_countries)]
european_df['date'] = pd.to_datetime(european_df['date'])
monthly_data = european_df.groupby(european_df['date'].dt.to_period('M')).sum()


app = dash.Dash(__name__)

app.layout = layout = html.Div([
    html.H1("Landing Page", style={'textAlign': 'center'}),
        # Dropdowns for COVID-19 data
    html.Div([
        dcc.Dropdown(
            id='country-dropdown',
            options=[{'label': country, 'value': country} for country in european_df['country'].unique()],
            value='Albania',
            style={'width': '50%'}
        ),
        dcc.Dropdown(
            id='feature-dropdown',
            options=[
                {'label': 'Total Cases', 'value': 'total_cases'},
                {'label': 'Total Deaths', 'value': 'total_deaths'},
                {'label': 'Stringency Index', 'value': 'stringency_index'},
            ],
            value='total_cases',
            style={'width': '50%'}
        ),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # Line and Bar plots for COVID-19 data
    html.Div([
        dcc.Graph(id='line-plot', style={'width': '50%'}),
        dcc.Graph(id='bar-plot', style={'width': '50%'}),
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    # World map for GDP data
    dcc.Graph(id='world-map'),

    # Slider for selecting date or month
    dcc.Slider(
        id='time-slider',
        min=0,
        max=len(monthly_data) - 1,
        value=0,
        marks={i: {'label': date.strftime('%b %Y')} for i, date in enumerate(monthly_data.index)}
    ),

    # Interpretation text
    html.Div([
        html.H3("Interpretation :"),
        html.P("The total number of COVID-19 cases was significantly high during the COVID-19 pandemic. Similarly, the total number of deaths in that year was substantial, which may have contributed to the elevated unemployment rate that had a significant impact on the global economy. The stringency index was notably high for all EU countries, indicating that governments took this issue seriously. Additionally, the GDP of most countries remained relatively low in the year 2020.")
    ])
])

@app.callback(
    Output('line-plot', 'figure'),
    [Input('country-dropdown', 'value'), Input('feature-dropdown', 'value')]
)
def update_line_plot(selected_country, selected_feature):
    filtered_df = european_df[european_df['country'] == selected_country]
    fig = px.line(filtered_df, x='date', y=selected_feature, title=f'{selected_feature} in {selected_country}')
    return fig

@app.callback(
    Output('bar-plot', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_bar_plot(selected_feature):
    fig = px.bar(european_df, x='country', y=selected_feature, title=f'{selected_feature} by Country')
    return fig

@app.callback(
    Output('world-map', 'figure'),
    [Input('time-slider', 'value')]
)
def update_world_map(selected_month):
    selected_date = monthly_data.index[selected_month].to_timestamp()
    filtered_df = european_df[european_df['date'].dt.to_period('M') == monthly_data.index[selected_month]]
    fig = px.choropleth(filtered_df, locations='country_code', color='gdp_per_capita', hover_name='country',
                        title=f'World GDP in {selected_date.strftime("%b %Y")}')
    return fig

