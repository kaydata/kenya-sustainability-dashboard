import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Load the prepared data
data = pd.read_csv('combined_data.csv')

# Extract the year from the 'Year' column
data['Year'] = pd.to_datetime(data['Year']).dt.year

# Create the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create the layout of the app
app.layout = dbc.Container(
    [
        dbc.Row([dbc.Col(html.H1("Environment and Sustainability in Kenya", className="text-center mb-4"))]),
        dbc.Row([
            dbc.Col(
                dcc.RangeSlider(
                    id='year-slider',
                    min=data['Year'].min(),
                    max=data['Year'].max(),
                    value=[data['Year'].min(), data['Year'].max()],
                    marks={str(year): str(year) for year in data['Year'].unique()},
                    step=None,
                ), width=12
            )
        ], className="mb-4"),
        dbc.Row([
            dbc.Col(
                dcc.Dropdown(
                    id='metric-dropdown',
                    options=[{'label': col, 'value': col} for col in data.columns[1:]],
                    value=[data.columns[1]],
                    multi=True
                ), width=12
            )
        ], className="mb-4"),
        dbc.Row(
            id='graphs-row',
            className="mb-4"
        )
    ],
    fluid=True,
    style={"backgroundColor": "#f8f9fa"}
)

# Callback to update graphs based on selected years and metrics
@app.callback(
    Output('graphs-row', 'children'),
    [Input('year-slider', 'value'),
     Input('metric-dropdown', 'value')]
)
def update_graphs(year_range, selected_metrics):
    filtered_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

    if not isinstance(selected_metrics, list):
        selected_metrics = [selected_metrics]

    graphs = []
    for metric in selected_metrics:
        fig = px.line(filtered_data, x='Year', y=metric, title=metric)
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor="LightSteelBlue",
        )
        graphs.append(dbc.Col(dcc.Graph(figure=fig), width=6))

    return graphs

if __name__ == '__main__':
    app.run_server(debug=True)
