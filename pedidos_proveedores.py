import mysql.connector
import random
from datetime import datetime, timedelta

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SI2026",
    database="nestle_transaccional"
)

cursor = conexion.cursor()

# Obtener IDs reales de proveedores
cursor.execute("""
SELECT id_proveedor
FROM proveedores
""")

proveedores = [fila[0] for fila in cursor.fetchall()]

fecha_inicio = datetime(2025, 1, 1)
fecha_fin = datetime(2025, 6, 30)

for i in range(500):

    dias = (fecha_fin - fecha_inicio).days

    fecha_pedido = fecha_inicio + timedelta(
        days=random.randint(0, dias)
    )

    id_proveedor = random.choice(proveedores)

    monto = round(
        random.uniform(5000, 100000),
        2
    )

    sql = """
    INSERT INTO pedidos_proveedores
    (id_proveedor, fecha_pedido, monto)
    VALUES (%s, %s, %s)
    """

    valores = (
        id_proveedor,
        fecha_pedido.date(),
        monto
    )

    cursor.execute(sql, valores)

conexion.commit()

print("500 pedidos generados correctamente")

cursor.close()
conexion.close()