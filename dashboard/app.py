import streamlit as st
import pandas as pd
from datetime import date, timedelta

# Configuración básica de la página
st.set_page_config(
    page_title="Inventario semántico sostenible",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    # Lee el CSV desde la carpeta data
    df = pd.read_csv("data/inventario_ejemplo.csv", parse_dates=["caducidad"])
    # Limpieza sencilla
    df["categoria"] = df["categoria"].fillna("Sin categoría")
    df["proveedor"] = df["proveedor"].fillna("Sin proveedor")
    df["envase"] = df["envase"].fillna("Sin envase")
    df["certificacion"] = df["certificacion"].fillna("Sin certificación")
    return df

df = cargar_datos()

st.title("Inventario semántico sostenible")

st.write(
    "Este panel muestra información básica del inventario a partir de un fichero CSV. "
    "En siguientes iteraciones se conectará con los datos RDF del triple store (Fuseki)."
)

# --- SIDEBAR: filtros ---
st.sidebar.header("Filtros")

st.sidebar.subheader("Carga de CSV")

archivo_csv = st.sidebar.file_uploader(
    "Sube un archivo CSV de inventario",
    type=["csv"]
)

if archivo_csv:
    df = pd.read_csv(archivo_csv, encoding="utf-8")
    df["caducidad"] = pd.to_datetime(df["caducidad"], errors="coerce")
else:
    df = cargar_datos()


# Filtro por categoría
categorias = sorted(df["categoria"].unique())
cat_sel = st.sidebar.multiselect(
    "Categorías",
    options=categorias,
    default=categorias
)

# Filtro por proveedor
proveedores = sorted(df["proveedor"].unique())
prov_sel = st.sidebar.multiselect(
    "Proveedores",
    options=proveedores,
    default=proveedores
)

# Filtro por fecha de caducidad máxima
hoy = date.today()
default_max = hoy + timedelta(days=90)
fecha_max = st.sidebar.date_input(
    "Mostrar productos que caducan antes de...",
    value=default_max
)

# Aplicar filtros
df_filtrado = df[
    (df["categoria"].isin(cat_sel)) &
    (df["proveedor"].isin(prov_sel)) &
    (df["caducidad"] <= pd.to_datetime(fecha_max))
]

# --- MÉTRICAS PRINCIPALES ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Nº de productos (filtrados)", len(df_filtrado))

with col2:
    st.metric("Stock total (filtrado)", int(df_filtrado["stock"].sum()))

with col3:
    proximos_30 = df[df["caducidad"] <= pd.to_datetime(hoy + timedelta(days=30))]
    st.metric("Caduquen en ≤ 30 días", len(proximos_30))

st.markdown("---")

# --- TABLA PRINCIPAL ---
st.subheader("Listado de productos filtrados")

st.dataframe(
    df_filtrado.sort_values("caducidad"),
    use_container_width=True
)

