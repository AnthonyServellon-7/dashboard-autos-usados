import streamlit as st
import pandas as pd
import plotly.express as px

# Configuracion base
st.set_page_config(page_title="Dashboard Car Details", layout="wide")

# Carga de dataset
@st.cache_data
def load_data():
    df = pd.read_csv('Car_details_v3_clean.csv')
    return df

df = load_data()

# Filtros laterales cruzados
st.sidebar.header("Filtros de Búsqueda")

fuel_options = st.sidebar.multiselect(
    "Tipo de Combustible", 
    options=df['fuel'].unique(), 
    default=df['fuel'].unique()
)

transmission_options = st.sidebar.multiselect(
    "Transmisión", 
    options=df['transmission'].unique(), 
    default=df['transmission'].unique()
)

seller_options = st.sidebar.multiselect(
    "Tipo de Vendedor", 
    options=df['seller_type'].unique(), 
    default=df['seller_type'].unique()
)

owner_options = st.sidebar.multiselect(
    "Propietario", 
    options=df['owner'].unique(), 
    default=df['owner'].unique()
)

# Aplicacion de filtros
df_filtered = df[
    (df['fuel'].isin(fuel_options)) & 
    (df['transmission'].isin(transmission_options)) &
    (df['seller_type'].isin(seller_options)) &
    (df['owner'].isin(owner_options))
]

# Layout principal
st.title("Dashboard Analítico: Mercado de Vehículos Usados")
st.markdown("Exploración interactiva de precios, kilometraje y características de vehículos.")

# KPIs
st.subheader("Métricas Generales")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de Autos", f"{len(df_filtered):,}")
col2.metric("Precio Promedio", f"₹ {df_filtered['selling_price'].mean():,.2f}")
col3.metric("Kilometraje Promedio", f"{df_filtered['km_driven'].mean():,.0f} km")

if 'edad' in df_filtered.columns:
    col4.metric("Edad Promedio", f"{df_filtered['edad'].mean():,.1f} años")
else:
    col4.metric("Año Promedio", f"{df_filtered['year'].mean():,.0f}")

st.write("---")

# Graficos
st.subheader("Análisis Visual del Mercado")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    fig1 = px.scatter(df_filtered, x='km_driven', y='selling_price', color='fuel',
                      title="Relación: Precio vs. Kilometraje",
                      labels={'km_driven': 'Kilometraje', 'selling_price': 'Precio (₹)'},
                      template='plotly_white')
    st.plotly_chart(fig1, use_container_width=True)

with col_graf2:
    fig2 = px.box(df_filtered, x='transmission', y='selling_price', color='transmission',
                  title="Distribución de Precios por Transmisión",
                  labels={'transmission': 'Transmisión', 'selling_price': 'Precio (₹)'},
                  template='plotly_white')
    st.plotly_chart(fig2, use_container_width=True)

st.write("---")
st.subheader("Vista de Datos")
st.dataframe(df_filtered.head(15))