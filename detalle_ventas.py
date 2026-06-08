import mysql.connector
import random

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SI2026",
    database="nestle_transaccional"
)

cursor = conexion.cursor()

for venta in range(1, 3001):

    cantidad_productos = random.randint(1, 3)

    for i in range(cantidad_productos):

        id_producto = random.randint(1, 50)

        cantidad = random.randint(1, 10)

        cursor.execute("""
            SELECT precio
            FROM productos
            WHERE id_producto = %s
        """, (id_producto,))

        precio = cursor.fetchone()[0]

        subtotal = round(precio * cantidad, 2)

        sql = """
        INSERT INTO detalle_ventas
        (id_venta, id_producto, cantidad, subtotal)
        VALUES (%s, %s, %s, %s)
        """

        valores = (
            venta,
            id_producto,
            cantidad,
            subtotal
        )

        cursor.execute(sql, valores)

conexion.commit()

print("Detalle de ventas generado correctamente")

cursor.close()
conexion.close()