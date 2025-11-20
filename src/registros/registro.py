import tkinter as tk
from tkinter import messagebox, simpledialog
from ..conexionBD import conexion, cursor

# 📝 Registro de jugador
def registrarJugador():
    ventana = tk.Tk()
    ventana.title("Registro de Jugador")

    campos = {
        "Nombre": tk.Entry(ventana),
        "Apellidos": tk.Entry(ventana),
        "CURP": tk.Entry(ventana),
        "Categoría": tk.Entry(ventana),
        "Número": tk.Entry(ventana),
        "¿Inscripción pagada? (s/n)": tk.Entry(ventana),
        "Equipo": tk.Entry(ventana)
    }

    for etiqueta, entrada in campos.items():
        tk.Label(ventana, text=etiqueta).pack()
        entrada.pack()

    def registrar():
        nombre = campos["Nombre"].get().strip().upper()
        apellidos = campos["Apellidos"].get().strip().upper()
        curp = campos["CURP"].get().strip().upper()
        categoria = campos["Categoría"].get().strip().upper()
        numero = campos["Número"].get().strip()
        pagado = campos["¿Inscripción pagada? (s/n)"].get().strip().lower()
        equipo = campos["Equipo"].get().strip().upper()

        if not all([nombre, apellidos, curp, categoria, numero, equipo]):
            messagebox.showerror("Error", "Datos incompletos.")
            return

        pagado_bool = pagado == "s"

        try:
            cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (equipo.lower(),))
            fila = cursor.fetchone()
            if fila:
                id_equipo = fila[0]
            else:
                cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (equipo, categoria))
                id_equipo = cursor.lastrowid

            sql = """
                INSERT INTO jugadores (nombre, apellido, curp, categoria, numero, pagado, id_equipo)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            val = (nombre, apellidos, curp, categoria, numero, pagado_bool, id_equipo)
            cursor.execute(sql, val)
            conexion.commit()
            messagebox.showinfo("Éxito", "Jugador registrado exitosamente.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar jugador: {e}")

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
    ventana.mainloop()

# 🗓️ Registro de horario de entrenamiento
def agregarHorario():
    ventana = tk.Tk()
    ventana.title("Registro de Entrenamiento")

    dia_entry = tk.Entry(ventana)
    cat_entry = tk.Entry(ventana)
    hora_entry = tk.Entry(ventana)

    tk.Label(ventana, text="Día").pack()
    dia_entry.pack()
    tk.Label(ventana, text="Categoría").pack()
    cat_entry.pack()
    tk.Label(ventana, text="Horario").pack()
    hora_entry.pack()

    def registrar():
        dia = dia_entry.get().strip().upper()
        categoria = cat_entry.get().strip().upper()
        horario = hora_entry.get().strip()

        if not dia or not categoria or not horario:
            messagebox.showerror("Error", "Datos incompletos.")
            return

        try:
            cursor.execute("INSERT INTO entrenamientos (dia, categoria, horario) VALUES (%s, %s, %s)", (dia, categoria, horario))
            conexion.commit()
            messagebox.showinfo("Éxito", "Horario registrado.")
            ventana.destroy()
        except Exception as e:
            if "Duplicate entry" in str(e):
                messagebox.showwarning("Duplicado", "Ya existe un horario para esta categoría.")
            else:
                messagebox.showerror("Error", f"Error al registrar: {e}")

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
    ventana.mainloop()

# ⚽ Registro de partido
def registrarPartido():
    ventana = tk.Tk()
    ventana.title("Registro de Partido")

    campos = {
        "Equipo local": tk.Entry(ventana),
        "Equipo visitante": tk.Entry(ventana),
        "Categoría": tk.Entry(ventana),
        "Día": tk.Entry(ventana),
        "Horario": tk.Entry(ventana)
    }

    for etiqueta, entrada in campos.items():
        tk.Label(ventana, text=etiqueta).pack()
        entrada.pack()

    def registrar():
        local = campos["Equipo local"].get().strip().upper()
        visitante = campos["Equipo visitante"].get().strip().upper()
        categoria = campos["Categoría"].get().strip().upper()
        dia = campos["Día"].get().strip().upper()
        horario = campos["Horario"].get().strip()

        if not all([local, visitante, categoria, dia, horario]):
            messagebox.showerror("Error", "Datos incompletos.")
            return

        try:
            cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (local.lower(),))
            r = cursor.fetchone()
            id_local = r[0] if r else cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (local, categoria)) or cursor.lastrowid

            cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (visitante.lower(),))
            r = cursor.fetchone()
            id_visitante = r[0] if r else cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (visitante, categoria)) or cursor.lastrowid

            cursor.execute("""
                INSERT INTO partidos (id_equipo_local, id_equipo_visitante, categoria, dia, horario)
                VALUES (%s, %s, %s, %s, %s)
            """, (id_local, id_visitante, categoria, dia, horario))
            conexion.commit()
            messagebox.showinfo("Éxito", "Partido registrado.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar partido: {e}")

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
    ventana.mainloop()

# 🏆 Registro de torneo
def registrarTorneo():
    ventana = tk.Tk()
    ventana.title("Registro de Torneo")

    nombre_entry = tk.Entry(ventana)
    cat_entry = tk.Entry(ventana)
    cantidad_entry = tk.Entry(ventana)

    tk.Label(ventana, text="Nombre del torneo").pack()
    nombre_entry.pack()
    tk.Label(ventana, text="Categoría").pack()
    cat_entry.pack()
    tk.Label(ventana, text="Cantidad de equipos").pack()
    cantidad_entry.pack()

    def registrar():
        nombre = nombre_entry.get().strip().upper()
        categoria = cat_entry.get().strip().upper()
        try:
            cantidad = int(cantidad_entry.get().strip())
            if cantidad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Cantidad inválida.")
            return

        equipos = []
        for i in range(cantidad):
            eq = simpledialog.askstring("Equipo", f"Nombre del equipo {i+1}:")
            if eq:
                equipos.append(eq.strip().upper())

        try:
            cursor.execute("INSERT INTO torneos (nombre, categoria) VALUES (%s, %s)", (nombre, categoria))
            id_torneo = cursor.lastrowid

            for equipo in equipos:
                cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (equipo.lower(),))
                fila = cursor.fetchone()
                id_equipo = fila[0] if fila else cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (equipo, categoria)) or cursor.lastrowid
                cursor.execute("INSERT INTO equipos_torneo (id_torneo, id_equipo) VALUES (%s, %s)", (id_torneo, id_equipo))

            conexion.commit()
            messagebox.showinfo("Éxito", "Torneo registrado.")
            ventana.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar torneo: {e}")

    tk.Button(ventana, text="Registrar", command=registrar).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
    ventana.mainloop()

def vaciarRegistros():
    ventana = tk.Tk()
    ventana.title("Vaciar todos los registros")

    tk.Label(ventana, text="Ingresa la contraseña para continuar:").pack(pady=5)
    pwd_entry = tk.Entry(ventana, show="*")
    pwd_entry.pack(pady=5)

    def confirmar_vaciado():
        pwd = pwd_entry.get().strip()
        if pwd != "DRILLING":
            messagebox.showerror("Error", "Contraseña incorrecta. No se realizaron cambios.")
            ventana.destroy()
            return

        confirm = messagebox.askyesno("Confirmar", "¿Estás seguro que deseas borrar todos los registros?")
        if not confirm:
            messagebox.showinfo("Cancelado", "Operación cancelada.")
            ventana.destroy()
            return

        try:
            cursor.execute("DELETE FROM equipos_torneo")
            cursor.execute("DELETE FROM torneos")
            cursor.execute("DELETE FROM partidos")
            cursor.execute("DELETE FROM entrenamientos")
            cursor.execute("DELETE FROM jugadores")
            conexion.commit()
            messagebox.showinfo("Éxito", "Todos los registros han sido eliminados.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al vaciar registros: {e}")
        ventana.destroy()

    tk.Button(ventana, text="Vaciar registros", command=confirmar_vaciado).pack(pady=10)
    tk.Button(ventana, text="Cancelar", command=ventana.destroy).pack()
    ventana.mainloop()
