import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load the CSV
df = pd.read_csv("pink_morsel_sales.csv")
df.columns = df.columns.str.strip().str.lower()
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Dash app
app = Dash(__name__)

app.layout = html.Div(
    style={'fontFamily': 'Arial, sans-serif', 'maxWidth': '1100px', 'margin': '0 auto', 'padding': '20px'},
    children=[
        html.H1(
            "Pink Morsel Sales Visualiser",
            style={'textAlign': 'center', 'color': '#c0392b', 'marginBottom': '5px'}
        ),
        html.P(
            "Soul Foods — Were sales higher before or after the price increase on 15 Jan 2021?",
            style={'textAlign': 'center', 'color': '#666', 'marginBottom': '20px'}
        ),

        # Region filter
        html.Div([
            html.Label("Filter by Region:", style={'fontWeight': 'bold', 'marginRight': '10px'}),
            dcc.RadioItems(
                id='region-filter',
                options=[{'label': 'All', 'value': 'all'}] +
                        [{'label': r.title(), 'value': r} for r in sorted(df['region'].unique())],
                value='all',
                inline=True,
                style={'display': 'inline-block'},
                inputStyle={'marginRight': '5px'},
                labelStyle={'marginRight': '20px'}
            )
        ], style={'marginBottom': '20px', 'padding': '10px', 'backgroundColor': '#f9f9f9', 'borderRadius': '8px'}),

        dcc.Graph(id='sales-chart')
    ]
)

@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_chart(region):
    filtered = df if region == 'all' else df[df['region'] == region]
    daily_sales = filtered.groupby('date')['sales'].sum().reset_index()
    max_sales = daily_sales['sales'].max()

    fig = px.line(
        daily_sales,
        x='date',
        y='sales',
        title=f'Daily Pink Morsel Sales{"" if region == "all" else f" — {region.title()} Region"}',
        labels={'date': 'Date', 'sales': 'Total Sales ($)'},
        color_discrete_sequence=['#e74c3c']
    )

    fig.update_traces(line=dict(width=2))

    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(showgrid=True, gridcolor='#eee', title='Date'),
        yaxis=dict(showgrid=True, gridcolor='#eee', title='Total Sales ($)'),
        hovermode='x unified',
        shapes=[
            dict(
                type='line',
                xref='x', yref='y',
                x0='2021-01-15', x1='2021-01-15',
                y0=0, y1=max_sales * 1.1,
                line=dict(color='#2c3e50', dash='dash', width=2),
            )
        ],
        annotations=[
            dict(
                x='2021-01-15',
                y=max_sales * 1.1,
                xref='x', yref='y',
                text='📈 Price Increase (15 Jan 2021)',
                showarrow=True,
                arrowhead=2,
                arrowcolor='#2c3e50',
                ax=80, ay=-30,
                font=dict(color='#2c3e50', size=12),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#2c3e50',
                borderwidth=1,
                borderpad=4
            )
        ]
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)