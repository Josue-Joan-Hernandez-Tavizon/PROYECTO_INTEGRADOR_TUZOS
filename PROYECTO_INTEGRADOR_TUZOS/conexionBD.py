import mysql.connector
from mysql.connector import Error

try:
    conexion = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="",
        database="bd_futbol"
    )
    cursor = conexion.cursor(buffered=True)
except Error as e:
    print(f"En este momento no es posible comunicarse con el sistema: {e}")
    conexion = None
    cursor = None
