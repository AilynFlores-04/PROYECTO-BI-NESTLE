import mysql.connector

try:
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="SI2026",
        database="nestle_transaccional"
    )

    if conexion.is_connected():
        print("Conexion exitosa a MySQL")

except Exception as error:
    print("Error:", error)

finally:
    if 'conexion' in locals() and conexion.is_connected():
        conexion.close()
        print("Conexion cerrada")