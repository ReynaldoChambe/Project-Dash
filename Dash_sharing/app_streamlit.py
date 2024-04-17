# Importar paquetes
import streamlit as st
import pandas as pd
import plotly.express as px

# Incorporar datos
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Diseño de la aplicación
st.title('Mi primera aplicación con datos y gráficos')

# Agregar controles para la interacción
col_chosen = st.radio('Selecciona una columna', ['pop', 'lifeExp', 'gdpPercap'])
fig = px.histogram(df, x='continent', y=col_chosen, histfunc='avg')
st.plotly_chart(fig)

# Mostrar datos en tabla
st.write('Datos:')
st.write(df)
