# Importar paquetes
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
import pycountry

# Leer datos
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Obtener lista de países únicos
paises_unicos = df['country'].unique()

# Función para obtener el código ISO de un país
def get_iso_alpha(country_name):
    try:
        country = pycountry.countries.lookup(country_name)
        return country.alpha_3
    except LookupError:
        return None

# Agregar una columna 'iso_alpha' al DataFrame
df['iso_alpha'] = df['country'].apply(get_iso_alpha)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Explorador de Datos de Gapminder - Ejemplo ", style={'textAlign': 'center'}),
    
    html.Div([
        dcc.Dropdown(
            id='dropdown-country',
            options=[{'label': country, 'value': country} for country in paises_unicos],
            value='United States'
        ),
        
        dcc.Graph(id='scatter-plot'),
        
        html.Label('Selecciona el tamaño de los puntos:'),
        dcc.Slider(
            id='size-slider',
            min=1,
            max=10,
            value=5,
            marks={i: str(i) for i in range(1, 11)},
        ),
        
        html.Label('Selecciona el color de los puntos:'),
        dcc.Dropdown(
            id='color-dropdown',
            options=[
                {'label': 'Continente', 'value': 'continent'},
                {'label': 'País', 'value': 'country'},
                {'label': 'Esperanza de vida', 'value': 'lifeExp'},
                {'label': 'PIB per cápita', 'value': 'gdpPercap'}
            ],
            value='continent'
        ),
        
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='bar-chart'),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div([
        dcc.Graph(id='map-plot'),
    ], style={'width': '100%', 'display': 'inline-block'}),
    
    html.Div([
        html.Div(id='summary-stats')
    ]),
])

# Callback para actualizar el gráfico de dispersión según los parámetros seleccionados
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('dropdown-country', 'value'),
     Input('size-slider', 'value'),
     Input('color-dropdown', 'value')]
)
def update_scatter_plot(selected_country, size, color):
    filtered_df = df[df['country'] == selected_country]
    fig = px.scatter(filtered_df, x='gdpPercap', y='lifeExp', size='pop', color=color, hover_name='country', log_x=True, title=f'Indicadores para {selected_country}')
    fig.update_traces(marker=dict(size=size))
    return fig

# Callback para actualizar el gráfico de barras de distribución de población por continente
@app.callback(
    Output('bar-chart', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_bar_chart(selected_country):
    continent_population = df.groupby('continent')['pop'].sum().reset_index()
    fig = px.bar(continent_population, x='continent', y='pop', color='continent', title='Distribución de la población por continente')
    return fig

# Callback para actualizar el mapa según el país seleccionado
@app.callback(
    Output('map-plot', 'figure'),
    [Input('dropdown-country', 'value')]
)
def update_map_plot(selected_country):
    filtered_df = df[df['country'] == selected_country]
    fig = px.scatter_geo(filtered_df, locations="iso_alpha", hover_name="country", projection="natural earth", title=f'Mapa para {selected_country}')
    
    # Establecer estilo del mapa
    fig.update_geos(
        showcoastlines=True, coastlinecolor="RebeccaPurple",
        showland=True, landcolor="LightGreen",
        showocean=True, oceancolor="LightBlue",
        showlakes=True, lakecolor="Blue",
        showrivers=True, rivercolor="Blue"
    )
    
    # Ajustar el tamaño de los marcadores
    fig.update_traces(marker=dict(size=12))
    
    # Añadir título y cambiar el color de fondo del gráfico
    fig.update_layout(title=f'Mapa para {selected_country}', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    
    return fig

# Callback para calcular y mostrar estadísticas resumidas
@app.callback(
    Output('summary-stats', 'children'),
    [Input('dropdown-country', 'value'),
     Input('size-slider', 'value'),
     Input('color-dropdown', 'value')]
)
def update_summary_stats(selected_country, size, color):
    filtered_df = df[df['country'] == selected_country]
    stats = filtered_df.describe()
    return html.Table([
        html.Tr([html.Th(col) for col in stats.columns]),
        html.Tr([html.Td(stats.loc['mean', col]) for col in stats.columns]),
        html.Tr([html.Td(stats.loc['50%', col]) for col in stats.columns]),
        html.Tr([html.Td(stats.loc['std', col]) for col in stats.columns])
    ])

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)

