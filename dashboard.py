import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

# =====================================
# CONFIGURACION
# =====================================

st.set_page_config(
    page_title="Dashboard BI Nestlé",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard BI Nestlé")
st.write("Proyecto de Business Intelligence")

# =====================================
# CONEXION MYSQL
# =====================================

engine = create_engine(
    "mysql+pymysql://root:SI2026@localhost/nestle_dw"
)

# =====================================
# KPIs
# =====================================

ventas = pd.read_sql("""
SELECT SUM(subtotal) AS total
FROM fact_ventas
""", engine)

productos = pd.read_sql("""
SELECT SUM(cantidad) AS total_productos
FROM fact_ventas
""", engine)

clientes = pd.read_sql("""
SELECT COUNT(*) AS total_clientes
FROM dim_cliente
""", engine)

ventas_count = pd.read_sql("""
SELECT COUNT(*) AS total_ventas
FROM fact_ventas
""", engine)

ventas_totales = float(ventas.iloc[0]["total"])
productos_vendidos = int(productos.iloc[0]["total_productos"])
total_clientes = int(clientes.iloc[0]["total_clientes"])
total_ventas = int(ventas_count.iloc[0]["total_ventas"])

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Ventas Totales",
        f"${ventas_totales:,.2f}"
    )

with col2:
    st.metric(
        "Productos Vendidos",
        f"{productos_vendidos:,}"
    )

with col3:
    st.metric(
        "Clientes",
        f"{total_clientes:,}"
    )

with col4:
    st.metric(
        "Número de Ventas",
        f"{total_ventas:,}"
    )

# =====================================
# VENTAS POR CATEGORIA
# =====================================

query_categoria = """
SELECT
    dp.categoria,
    SUM(fv.subtotal) AS ventas
FROM fact_ventas fv
INNER JOIN dim_producto dp
    ON fv.producto_key = dp.producto_key
GROUP BY dp.categoria
ORDER BY ventas DESC
"""

df_categoria = pd.read_sql(query_categoria, engine)

fig_categoria = px.bar(
    df_categoria,
    x="categoria",
    y="ventas",
    title="Ventas por Categoría"
)

st.plotly_chart(
    fig_categoria,
    use_container_width=True
)

# =====================================
# VENTAS POR MES
# =====================================

query_mes = """
SELECT
    nombre_mes,
    SUM(fv.subtotal) AS ventas
FROM fact_ventas fv
INNER JOIN dim_fecha df
    ON fv.fecha_key = df.fecha_key
GROUP BY nombre_mes
"""

df_mes = pd.read_sql(query_mes, engine)

meses_es = {
    "January": "Enero",
    "February": "Febrero",
    "March": "Marzo",
    "April": "Abril",
    "May": "Mayo",
    "June": "Junio",
    "July": "Julio",
    "August": "Agosto",
    "September": "Septiembre",
    "October": "Octubre",
    "November": "Noviembre",
    "December": "Diciembre"
}

df_mes["nombre_mes"] = df_mes["nombre_mes"].replace(meses_es)

orden_meses = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
]

df_mes["nombre_mes"] = pd.Categorical(
    df_mes["nombre_mes"],
    categories=orden_meses,
    ordered=True
)

df_mes = df_mes.sort_values("nombre_mes")

fig_mes = px.pie(
    df_mes,
    names="nombre_mes",
    values="ventas",
    title="Participación de Ventas por Mes"
)

st.plotly_chart(
    fig_mes,
    use_container_width=True
)

# =====================================
# FILTRO DE CATEGORIA
# =====================================

st.subheader("Filtrar Top 10 Productos")

categorias = pd.read_sql("""
SELECT
    dp.categoria,
    SUM(fv.subtotal) AS ventas
FROM fact_ventas fv
INNER JOIN dim_producto dp
    ON fv.producto_key = dp.producto_key
GROUP BY dp.categoria
ORDER BY ventas DESC
LIMIT 5
""", engine)

lista_categorias = ["Todas"] + categorias["categoria"].tolist()

categoria_seleccionada = st.selectbox(
    "Selecciona una categoría",
    lista_categorias
)

# =====================================
# TOP 10 PRODUCTOS
# =====================================

if categoria_seleccionada == "Todas":

    query_productos = """
    SELECT
        dp.nombre_producto,
        SUM(fv.subtotal) AS ventas
    FROM fact_ventas fv
    INNER JOIN dim_producto dp
        ON fv.producto_key = dp.producto_key
    GROUP BY dp.nombre_producto
    ORDER BY ventas DESC
    LIMIT 10
    """

else:

    query_productos = f"""
    SELECT
        dp.nombre_producto,
        SUM(fv.subtotal) AS ventas
    FROM fact_ventas fv
    INNER JOIN dim_producto dp
        ON fv.producto_key = dp.producto_key
    WHERE dp.categoria = '{categoria_seleccionada}'
    GROUP BY dp.nombre_producto
    ORDER BY ventas DESC
    LIMIT 10
    """

df_productos = pd.read_sql(
    query_productos,
    engine
)

fig_productos = px.bar(
    df_productos,
    x="nombre_producto",
    y="ventas",
    title=f"Top 10 Productos - {categoria_seleccionada}"
)

st.plotly_chart(
    fig_productos,
    use_container_width=True
)

# =====================================
# FIN
# =====================================

st.success("Dashboard cargado correctamente")