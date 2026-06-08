from faker import Faker
import mysql.connector
import random

fake = Faker("es_MX")

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SI2026",
    database="nestle_transaccional"
)

cursor = conexion.cursor()

ciudades = [
    "Toluca",
    "Metepec",
    "Lerma",
    "Naucalpan",
    "Ecatepec",
    "Puebla",
    "Queretaro",
    "Guadalajara"
]

for i in range(15):

    nombre = f"Proveedor {i+1}"
    ciudad = random.choice(ciudades)

    sql = """
    INSERT INTO proveedores
    (nombre_proveedor, ciudad)
    VALUES (%s,%s)
    """

    valores = (
        nombre,
        ciudad
    )

    cursor.execute(sql, valores)

conexion.commit()

print("15 proveedores insertados correctamente")

cursor.close()
conexion.close()