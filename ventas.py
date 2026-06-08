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

fecha_inicio = datetime(2025, 1, 1)
fecha_fin = datetime(2025, 6, 30)

for i in range(3000):

    dias = (fecha_fin - fecha_inicio).days

    fecha_venta = fecha_inicio + timedelta(
        days=random.randint(0, dias)
    )

    id_cliente = random.randint(1, 200)

    id_empleado = random.randint(1, 20)

    total = round(random.uniform(100, 5000), 2)

    sql = """
    INSERT INTO ventas
    (fecha_venta, id_cliente, id_empleado, total)
    VALUES (%s, %s, %s, %s)
    """

    valores = (
        fecha_venta.date(),
        id_cliente,
        id_empleado,
        total
    )

    cursor.execute(sql, valores)

conexion.commit()

print("3000 ventas insertadas correctamente")

cursor.close()
conexion.close()