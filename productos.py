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

categorias = [
    "Chocolate",
    "Cafe",
    "Cereal",
    "Lacteo",
    "Agua",
    "Galletas"
]

productos = [
    "Chocolate Premium",
    "Chocolate Blanco",
    "Cafe Clasico",
    "Cafe Descafeinado",
    "Cereal Integral",
    "Cereal Infantil",
    "Leche Entera",
    "Leche Deslactosada",
    "Yogurt Natural",
    "Yogurt Fresa",
    "Agua Natural",
    "Agua Mineral",
    "Galletas Vainilla",
    "Galletas Chocolate"
]

for i in range(50):
    nombre = random.choice(productos)
    categoria = random.choice(categorias)
    precio = round(random.uniform(15, 250), 2)
    stock = random.randint(50, 1000)

    sql = """
    INSERT INTO productos
    (nombre_producto, categoria, precio, stock)
    VALUES (%s,%s,%s,%s)
    """

    valores = (nombre, categoria, precio, stock)

    cursor.execute(sql, valores)

conexion.commit()

print("50 productos insertados correctamente")

cursor.close()
conexion.close()