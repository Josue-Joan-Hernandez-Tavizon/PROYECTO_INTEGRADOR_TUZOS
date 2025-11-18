import tkinter as tk
from tkinter import messagebox
from usuarios import usuario
from conexionBD import conexion, cursor
from modificaciones.modificaciones import menu_modificaciones
from registros.registro import (
    registrarJugador,
    agregarHorario,
    registrarPartido,
    registrarTorneo,
    vaciarRegistros
)

#Inicio de sesión
def mostrar_login():
    login_ventana = tk.Tk()
    login_ventana.title("Inicio de Sesión")

    tk.Label(login_ventana, text="Email:").pack(pady=5)
    email_entry = tk.Entry(login_ventana)
    email_entry.pack(pady=5)

    tk.Label(login_ventana, text="Contraseña:").pack(pady=5)
    contrasena_entry = tk.Entry(login_ventana, show="*")
    contrasena_entry.pack(pady=5)

    def iniciar_sesion():
        email = email_entry.get().lower().strip()
        contrasena = contrasena_entry.get().strip()
        datos = usuario.iniciar_sesion(email, contrasena)
        if datos:
            nombre, apellidos, email = datos[:3]
            messagebox.showinfo("Bienvenido", f"Hola {apellidos} ({email})")
            login_ventana.destroy()
            mostrar_menu_sistema()
        else:
            messagebox.showerror("Error", "Email o contraseña incorrectos.")

    tk.Button(login_ventana, text="Iniciar Sesión", command=iniciar_sesion).pack(pady=10)
    tk.Button(login_ventana, text="Salir", command=login_ventana.destroy).pack(pady=5)

    login_ventana.mainloop()

#Menú principal del sistema
def mostrar_menu_sistema():
    sistema = tk.Tk()
    sistema.title("Sistema Deportivo")

    opciones = [
        ("1 - Menú de Registro", lambda: [sistema.destroy(), menu_registro()]),
        ("2 - Volver al inicio de sesión", lambda: [sistema.destroy(), mostrar_login()]),
        ("3 - Salir", sistema.quit)
    ]

    for texto, accion in opciones:
        tk.Button(sistema, text=texto, width=40, command=accion).pack(pady=5)

    sistema.mainloop()

#Menú de registro con funciones gráficas
def menu_registro():
    ventana = tk.Tk()
    ventana.title("Menú de Registro")

    def ejecutar(opcion):
        ventana.destroy()
        if opcion == "1":
            registrarJugador()
        elif opcion == "2":
            agregarHorario()
        elif opcion == "3":
            registrarPartido()
        elif opcion == "4":
            registrarTorneo()
        elif opcion == "5":
            vaciarRegistros()
        elif opcion == "6":
            menu_modificaciones()
        elif opcion == "7":
            mostrar_menu_sistema()

    opciones = [
        ("1 - Inscribir jugador", "1"),
        ("2 - Registrar día de entrenamiento", "2"),
        ("3 - Registrar partido", "3"),
        ("4 - Registrar torneo", "4"),
        ("5 - Vaciar registros", "5"),
        ("6 - Editar o borrar registro", "6"),
        ("7 - Volver al menú principal", "7")
    ]

    for texto, valor in opciones:
        tk.Button(ventana, text=texto, width=40, command=lambda v=valor: ejecutar(v)).pack(pady=5)

    ventana.mainloop()

#Punto de entrada
if __name__ == "__main__":
    mostrar_login()