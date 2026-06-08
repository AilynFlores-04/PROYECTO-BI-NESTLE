import mysql.connector

# =====================================
# CONEXIONES
# =====================================

transaccional = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SI2026",
    database="nestle_transaccional"
)

dw = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SI2026",
    database="nestle_dw"
)

cursor_trans = transaccional.cursor()
cursor_dw = dw.cursor()

# =====================================
# FACT_VENTAS
# =====================================

cursor_trans.execute("""
SELECT
    dv.id_producto,
    v.id_cliente,
    v.id_empleado,
    v.fecha_venta,
    dv.cantidad,
    dv.subtotal
FROM detalle_ventas dv
INNER JOIN ventas v
    ON dv.id_venta = v.id_venta
""")

ventas_dw = cursor_trans.fetchall()

for venta in ventas_dw:

    id_producto = venta[0]
    id_cliente = venta[1]
    id_empleado = venta[2]
    fecha_venta = venta[3]
    cantidad = venta[4]
    subtotal = venta[5]

    # Buscar producto_key
    cursor_dw.execute("""
    SELECT producto_key
    FROM dim_producto
    WHERE id_producto = %s
    """, (id_producto,))
    producto_key = cursor_dw.fetchone()[0]

    # Buscar cliente_key
    cursor_dw.execute("""
    SELECT cliente_key
    FROM dim_cliente
    WHERE id_cliente = %s
    """, (id_cliente,))
    cliente_key = cursor_dw.fetchone()[0]

    # Buscar empleado_key
    cursor_dw.execute("""
    SELECT empleado_key
    FROM dim_empleado
    WHERE id_empleado = %s
    """, (id_empleado,))
    empleado_key = cursor_dw.fetchone()[0]

    # Buscar fecha_key
    cursor_dw.execute("""
    SELECT fecha_key
    FROM dim_fecha
    WHERE fecha = %s
    """, (fecha_venta,))
    fecha_key = cursor_dw.fetchone()[0]

    # Insertar en fact_ventas
    cursor_dw.execute("""
    INSERT INTO fact_ventas
    (
        producto_key,
        cliente_key,
        empleado_key,
        fecha_key,
        cantidad,
        subtotal
    )
    VALUES (%s,%s,%s,%s,%s,%s)
    """,
    (
        producto_key,
        cliente_key,
        empleado_key,
        fecha_key,
        cantidad,
        subtotal
    ))

dw.commit()

print("Tabla fact_ventas cargada correctamente")

# =====================================
# CIERRE DE CONEXIONES
# =====================================

cursor_trans.close()
cursor_dw.close()

transaccional.close()
dw.close()

print("ETL finalizado correctamente")