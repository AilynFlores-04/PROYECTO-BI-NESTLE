import pandas as pd
from sqlalchemy import create_engine
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# =====================================
# CONEXION
# =====================================

engine = create_engine(
    "mysql+pymysql://root:SI2026@localhost/nestle_dw"
)

# =====================================
# ANALISIS 1
# TOP 10 PRODUCTOS MAS RENTABLES
# =====================================

print("\n=====================================")
print("TOP 10 PRODUCTOS MAS RENTABLES")
print("=====================================\n")

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

productos = pd.read_sql(query_productos, engine)

print(productos)

productos.to_csv(
    "top_10_productos.csv",
    index=False
)

plt.figure(figsize=(10,6))

plt.bar(
    productos["nombre_producto"],
    productos["ventas"]
)

plt.title("Top 10 Productos Más Rentables")
plt.xlabel("Producto")
plt.ylabel("Ventas")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# =====================================
# ANALISIS 2
# VENTAS POR MES
# =====================================

print("\n=====================================")
print("VENTAS POR MES")
print("=====================================\n")

query_meses = """
SELECT
    df.nombre_mes,
    SUM(fv.subtotal) AS ventas
FROM fact_ventas fv
INNER JOIN dim_fecha df
    ON fv.fecha_key = df.fecha_key
GROUP BY df.nombre_mes
"""

ventas_mes = pd.read_sql(query_meses, engine)

print(ventas_mes)

ventas_mes.to_csv(
    "ventas_por_mes.csv",
    index=False
)

plt.figure(figsize=(10,6))

plt.plot(
    ventas_mes["nombre_mes"],
    ventas_mes["ventas"],
    marker="o"
)

plt.title("Ventas por Mes")
plt.xlabel("Mes")
plt.ylabel("Ventas")

plt.grid(True)

plt.tight_layout()

plt.show()

# =====================================
# ANALISIS 3
# VENTAS POR EMPLEADO
# =====================================

print("\n=====================================")
print("VENTAS POR EMPLEADO")
print("=====================================\n")

query_empleados = """
SELECT
    de.nombre,
    SUM(fv.subtotal) AS ventas
FROM fact_ventas fv
INNER JOIN dim_empleado de
    ON fv.empleado_key = de.empleado_key
GROUP BY de.nombre
ORDER BY ventas DESC
"""

ventas_empleado = pd.read_sql(
    query_empleados,
    engine
)

print(ventas_empleado)

ventas_empleado.to_csv(
    "ventas_por_empleado.csv",
    index=False
)

plt.figure(figsize=(10,6))

plt.bar(
    ventas_empleado["nombre"],
    ventas_empleado["ventas"]
)

plt.title("Ventas por Empleado")
plt.xlabel("Empleado")
plt.ylabel("Ventas")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()

# =====================================
# MINERIA DE DATOS
# K-MEANS
# =====================================

print("\n=====================================")
print("SEGMENTACION DE CLIENTES")
print("=====================================\n")

query_clientes = """
SELECT
    dc.cliente_key,
    dc.nombre,
    COUNT(fv.venta_key) AS total_compras,
    SUM(fv.subtotal) AS gasto_total
FROM dim_cliente dc
INNER JOIN fact_ventas fv
    ON dc.cliente_key = fv.cliente_key
GROUP BY
    dc.cliente_key,
    dc.nombre
"""

clientes = pd.read_sql(
    query_clientes,
    engine
)

X = clientes[
    [
        "total_compras",
        "gasto_total"
    ]
]

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

clientes["cluster"] = kmeans.fit_predict(X)

promedios = clientes.groupby(
    "cluster"
)["gasto_total"].mean()

orden = (
    promedios
    .sort_values()
    .index
    .tolist()
)

etiquetas = {
    orden[0]: "Ocasional",
    orden[1]: "Frecuente",
    orden[2]: "Premium"
}

clientes["segmento"] = (
    clientes["cluster"]
    .map(etiquetas)
)

print(
    clientes[
        [
            "cliente_key",
            "nombre",
            "total_compras",
            "gasto_total",
            "segmento"
        ]
    ].head(20)
)

clientes.to_csv(
    "clientes_segmentados.csv",
    index=False
)

plt.figure(figsize=(10,6))

for segmento in clientes["segmento"].unique():

    datos = clientes[
        clientes["segmento"] == segmento
    ]

    plt.scatter(
        datos["total_compras"],
        datos["gasto_total"],
        label=segmento
    )

plt.title(
    "Segmentacion de Clientes con K-Means"
)

plt.xlabel("Total Compras")
plt.ylabel("Gasto Total")

plt.legend()

plt.tight_layout()

plt.show()

# =====================================
# FIN
# =====================================

print("\n=====================================")
print("ANALISIS COMPLETADO")
print("=====================================\n")

print("Archivos generados:")
print("- top_10_productos.csv")
print("- ventas_por_mes.csv")
print("- ventas_por_empleado.csv")
print("- clientes_segmentados.csv")