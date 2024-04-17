# Importar paquetes
import streamlit as st
import pandas as pd
import plotly.express as px
import pycountry

# Leer datos
@st.cache(allow_output_mutation=True)
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
    return df

df = load_data()

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

# Interfaz de usuario
st.title("Explorador de Datos de Gapminder - Ejemplo")

selected_country = st.selectbox("Selecciona un país", paises_unicos, index=0)

size = st.slider("Selecciona el tamaño de los puntos:", min_value=1, max_value=10, value=5)

color = st.selectbox("Selecciona el color de los puntos:", ['continent', 'country', 'lifeExp', 'gdpPercap'], index=0)

# Gráfico de dispersión
st.plotly_chart(px.scatter(
    df[df['country'] == selected_country],
    x='gdpPercap', 
    y='lifeExp', 
    size='pop', 
    color=color, 
    hover_name='country', 
    log_x=True,
    title=f'Indicadores para {selected_country}'
).update_traces(marker=dict(size=size)))

# Gráfico de barras de distribución de población por continente
continent_population = df.groupby('continent')['pop'].sum().reset_index()
st.plotly_chart(px.bar(
    continent_population,
    x='continent',
    y='pop',
    color='continent',
    title='Distribución de la población por continente'
))

# Mapa según el país seleccionado
filtered_df = df[df['country'] == selected_country]
fig = px.scatter_geo(
    filtered_df,
    locations="iso_alpha",
    hover_name="country",
    projection="natural earth",
    title=f'Mapa para {selected_country}'
)

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
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig)

# Estadísticas resumidas
filtered_df = df[df['country'] == selected_country]
stats = filtered_df.describe()
st.table(stats)
