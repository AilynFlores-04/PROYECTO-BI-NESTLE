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

puestos = [
    "Gerente",
    "Supervisor",
    "Vendedor",
    "Analista",
    "Coordinador"
]

sucursales = [
    "Toluca",
    "Metepec",
    "Lerma",
    "Naucalpan",
    "Ecatepec"
]

for i in range(20):

    nombre = fake.name()
    puesto = random.choice(puestos)
    sucursal = random.choice(sucursales)

    sql = """
    INSERT INTO empleados
    (nombre, puesto, sucursal)
    VALUES (%s,%s,%s)
    """

    valores = (
        nombre,
        puesto,
        sucursal
    )

    cursor.execute(sql, valores)

conexion.commit()

print("20 empleados insertados correctamente")

cursor.close()
conexion.close()