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
    "Tlalnepantla",
    "Cuautitlan",
    "Atlacomulco"
]

segmentos = [
    "Minorista",
    "Mayorista",
    "Distribuidor",
    "Supermercado"
]

for i in range(200):

    nombre = fake.name()
    ciudad = random.choice(ciudades)
    segmento = random.choice(segmentos)

    sql = """
    INSERT INTO clientes
    (nombre, ciudad, segmento)
    VALUES (%s,%s,%s)
    """

    valores = (
        nombre,
        ciudad,
        segmento
    )

    cursor.execute(sql, valores)

conexion.commit()

print("200 clientes insertados correctamente")

cursor.close()
conexion.close()