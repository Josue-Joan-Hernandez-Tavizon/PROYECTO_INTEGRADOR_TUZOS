import pandas as pd
from fpdf import FPDF
import mysql.connector
import importlib.util
import subprocess
import funciones
import sys

# 📌 Verificar si openpyxl está instalado (necesario para exportar a Excel)
if importlib.util.find_spec("openpyxl") is None:
    print("📦 Instalando 'openpyxl'...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])

def _get_connection():
    """Conecta directamente a la BD bd_futbol"""
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="bd_futbol"
    )

def exportar_jugadores_excel():
    funciones.borrarPantalla()
    try:
        conexion = _get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT CONCAT(nombre, ' ', apellido) AS nombre_completo,
                   categoria,
                   numero,
                   CASE 
                       WHEN pagado = 1 THEN 'Pagado'
                       ELSE 'Pendiente'
                   END AS estado_pago
            FROM jugadores
        """)
        datos = cursor.fetchall()
        conexion.close()

        if not datos:
            print("⚠ No hay jugadores registrados para exportar.")
            return

        print(f"📋 {len(datos)} jugadores encontrados. Exportando a Excel...")
        df = pd.DataFrame(datos, columns=["Nombre Completo", "Categoría", "Número", "Estado de Pago"])
        df.to_excel("jugadores.xlsx", index=False, engine="openpyxl")
        print("✅ Archivo 'jugadores.xlsx' creado correctamente.")
        funciones.esperarTecla()
        

    except Exception as e:
        print(f"❌ Error al exportar a Excel: {e}")
        funciones.esperarTecla()

def exportar_jugadores_pdf():
    funciones.borrarPantalla()
    try:
        conexion = _get_connection()
        cursor = conexion.cursor()
        cursor.execute("""
            SELECT CONCAT(nombre, ' ', apellido) AS nombre_completo,
                   categoria,
                   numero,
                   CASE 
                       WHEN pagado = 1 THEN 'Pagado'
                       ELSE 'Pendiente'
                   END AS estado_pago
            FROM jugadores
        """)
        datos = cursor.fetchall()
        conexion.close()

        if not datos:
            print("⚠ No hay jugadores registrados para exportar.")
            funciones.esperarTecla()
            return

        print(f"📋 {len(datos)} jugadores encontrados. Exportando a PDF...")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=14)
        pdf.cell(200, 10, "Listado de Jugadores", ln=True, align="C")
        pdf.ln(10)

        # Encabezados
        pdf.set_font("Arial", "B", 12)
        pdf.cell(60, 10, "Nombre Completo", border=1)
        pdf.cell(40, 10, "Categoría", border=1)
        pdf.cell(25, 10, "Número", border=1)
        pdf.cell(50, 10, "Estado de Pago", border=1)
        pdf.ln()

        # Datos
        pdf.set_font("Arial", size=12)
        for jugador in datos:
            pdf.cell(60, 10, str(jugador[0]), border=1)
            pdf.cell(40, 10, str(jugador[1]), border=1)
            pdf.cell(25, 10, str(jugador[2]), border=1, align="C")
            pdf.cell(50, 10, str(jugador[3]), border=1)
            pdf.ln()

        pdf.output("jugadores.pdf")
        print("✅ Archivo 'jugadores.pdf' creado correctamente.")
        funciones.esperarTecla()

    except Exception as e:
        print(f"❌ Error al exportar a PDF: {e}")

# 📌 Ejecutar funciones
exportar_jugadores_excel()
exportar_jugadores_pdf()