import tkinter as tk
from tkinter import messagebox, simpledialog
from conexionBD import conexion, cursor

def menu_modificaciones():
    ventana = tk.Tk()
    ventana.title("Modificar o Borrar Registros")

    opciones = [
        ("1 - Jugador", modificar_jugador),
        ("2 - Día de entrenamiento", modificar_entrenamiento),
        ("3 - Partido", modificar_partido),
        ("4 - Torneo", modificar_torneo),
        ("5 - Volver", ventana.destroy)
    ]

    for texto, accion in opciones:
        tk.Button(ventana, text=texto, width=40, command=accion).pack(pady=5)

    ventana.mainloop()

# MOD jugadores
def modificar_jugador():
    ventana = tk.Tk()
    ventana.title("Modificar/Borrar Jugador")

    tk.Label(ventana, text="CURP del jugador:").pack()
    curp_entry = tk.Entry(ventana)
    curp_entry.pack()

    def buscar():
        curp = curp_entry.get().strip()
        cursor.execute("SELECT * FROM jugadores WHERE curp = %s", (curp,))
        jugador = cursor.fetchone()

        if not jugador:
            messagebox.showerror("Error", "Jugador no encontrado.")
            ventana.destroy()
            return

        accion = simpledialog.askstring("Acción", "¿Editar (e) o Borrar (b)?").strip().lower()
        if accion == "e":
            nombre = simpledialog.askstring("Nuevo nombre", "Dejar vacío para mantener actual:")
            apellido = simpledialog.askstring("Nuevos apellidos", "Dejar vacío para mantener actual:")
            nueva_curp = simpledialog.askstring("Nueva CURP", "Dejar vacío para mantener actual:")
            categoria = simpledialog.askstring("Nueva categoría", "Dejar vacío para mantener actual:")
            numero = simpledialog.askstring("Nuevo número", "Dejar vacío para mantener actual:")
            pagado = simpledialog.askstring("¿Inscripción pagada? (s/n)", "s/n")

            pagado_bool = pagado == "s"

            try:
                cursor.execute("""
                    UPDATE jugadores
                    SET nombre = %s, apellido = %s, curp = %s, categoria = %s, numero = %s, pagado = %s
                    WHERE curp = %s
                """, (
                    nombre or jugador[1],
                    apellido or jugador[2],
                    nueva_curp or jugador[3],
                    categoria or jugador[4],
                    numero or jugador[5],
                    pagado_bool,
                    curp
                ))
                conexion.commit()
                messagebox.showinfo("Éxito", "Jugador actualizado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {e}")

        elif accion == "b":
            cursor.execute("DELETE FROM jugadores WHERE curp = %s", (curp,))
            conexion.commit()
            messagebox.showinfo("Eliminado", "Jugador eliminado.")

        ventana.destroy()

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)
    ventana.mainloop()

# ------------------ ENTRENAMIENTOS ------------------
def modificar_entrenamiento():
    ventana = tk.Tk()
    ventana.title("Modificar/Borrar Entrenamiento")

    tk.Label(ventana, text="Día del entrenamiento:").pack()
    dia_entry = tk.Entry(ventana)
    dia_entry.pack()

    def buscar():
        dia = dia_entry.get().strip()
        cursor.execute("SELECT * FROM entrenamientos WHERE dia = %s", (dia,))
        entrenamiento = cursor.fetchone()

        if not entrenamiento:
            messagebox.showerror("Error", "Entrenamiento no encontrado.")
            ventana.destroy()
            return

        accion = simpledialog.askstring("Acción", "¿Editar (e) o Borrar (b)?").strip().lower()
        if accion == "e":
            nueva_cat = simpledialog.askstring("Nueva categoría", "Dejar vacío para mantener actual:")
            nuevo_horario = simpledialog.askstring("Nuevo horario", "Dejar vacío para mantener actual:")
            try:
                cursor.execute("""
                    UPDATE entrenamientos
                    SET categoria = %s, horario = %s
                    WHERE dia = %s
                """, (
                    nueva_cat or entrenamiento[1],
                    nuevo_horario or entrenamiento[2],
                    dia
                ))
                conexion.commit()
                messagebox.showinfo("Éxito", "Entrenamiento actualizado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar: {e}")
        elif accion == "b":
            cursor.execute("DELETE FROM entrenamientos WHERE dia = %s", (dia,))
            conexion.commit()
            messagebox.showinfo("Eliminado", "Entrenamiento eliminado.")

        ventana.destroy()

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)
    ventana.mainloop()

# ------------------ PARTIDOS ------------------
def modificar_partido():
    ventana = tk.Tk()
    ventana.title("Modificar/Borrar Partido")

    tk.Label(ventana, text="Día del partido:").pack()
    dia_entry = tk.Entry(ventana)
    dia_entry.pack()

    def buscar():
        dia = dia_entry.get().strip()
        cursor.execute("SELECT * FROM partidos WHERE dia = %s", (dia,))
        partido = cursor.fetchone()

        if not partido:
            messagebox.showerror("Error", "Partido no encontrado.")
            ventana.destroy()
            return

        accion = simpledialog.askstring("Acción", "¿Editar (e) o Borrar (b)?").strip().lower()
        if accion == "e":
            local = simpledialog.askstring("Nuevo equipo local", "Dejar vacío para mantener actual:").upper()
            visitante = simpledialog.askstring("Nuevo equipo visitante", "Dejar vacío para mantener actual:").upper()
            categoria = simpledialog.askstring("Nueva categoría", "Dejar vacío para mantener actual:").upper()
            nuevo_dia = simpledialog.askstring("Nuevo día", "Dejar vacío para mantener actual:")
            horario = simpledialog.askstring("Nuevo horario", "Dejar vacío para mantener actual:")

            try:
                # Local
                if local:
                    cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (local.lower(),))
                    r = cursor.fetchone()
                    id_local = r[0] if r else cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (local, categoria or partido[3])) or cursor.lastrowid
                else:
                    id_local = partido[1]

                # Visitante
                if visitante:
                    cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (visitante.lower(),))
                    r = cursor.fetchone()
                    id_visitante = r[0] if r else cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (visitante, categoria or partido[3])) or cursor.lastrowid
                else:
                    id_visitante = partido[2]

                cursor.execute("""
                    UPDATE partidos
                    SET id_equipo_local = %s, id_equipo_visitante = %s, categoria = %s, dia = %s, horario = %s
                    WHERE id_partido = %s
                """, (
                    id_local,
                    id_visitante,
                    categoria or partido[3],
                    nuevo_dia or partido[4],
                    horario or partido[5],
                    partido[0]
                ))
                conexion.commit()
                messagebox.showinfo("Éxito", "Partido actualizado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar partido: {e}")
        elif accion == "b":
            cursor.execute("DELETE FROM partidos WHERE id_partido = %s", (partido[0],))
            conexion.commit()
            messagebox.showinfo("Eliminado", "Partido eliminado.")

        ventana.destroy()

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)
    ventana.mainloop()

# ------------------ TORNEOS ------------------
def modificar_torneo():
    ventana = tk.Tk()
    ventana.title("Modificar/Borrar Torneo")

    tk.Label(ventana, text="Nombre del torneo:").pack()
    nombre_entry = tk.Entry(ventana)
    nombre_entry.pack()

    def buscar():
        nombre = nombre_entry.get().strip().upper()
        cursor.execute("SELECT * FROM torneos WHERE nombre = %s", (nombre,))
        torneo = cursor.fetchone()

        if not torneo:
            messagebox.showerror("Error", "Torneo no encontrado.")
            ventana.destroy()
            return

        accion = simpledialog.askstring("Acción", "¿Editar (e) o Borrar (b)?").strip().lower()
        if accion == "e":
            nuevo_nombre = simpledialog.askstring("Nuevo nombre", "Dejar vacío para mantener actual:").upper()
            nueva_cat = simpledialog.askstring("Nueva categoría", "Dejar vacío para mantener actual:").upper()

            try:
                cursor.execute("""
                    UPDATE torneos
                    SET nombre = %s, categoria = %s
                    WHERE id_torneo = %s
                """, (
                    nuevo_nombre or torneo[1],
                                        nueva_cat or torneo[2],
                    torneo[0]
                ))
                conexion.commit()

                actualizar = simpledialog.askstring("Actualizar equipos", "¿Deseas actualizar los equipos del torneo? (s/n):")
                if actualizar and actualizar.lower() == "s":
                    cursor.execute("DELETE FROM equipos_torneo WHERE id_torneo = %s", (torneo[0],))
                    cantidad = simpledialog.askinteger("Cantidad", "Nueva cantidad de equipos:")
                    for i in range(cantidad):
                        nombre_equipo = simpledialog.askstring("Equipo", f"Nombre del equipo {i+1}:").strip().upper()
                        cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (nombre_equipo.lower(),))
                        fila = cursor.fetchone()
                        if fila:
                            id_equipo = fila[0]
                        else:
                            cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (nombre_equipo, nueva_cat or torneo[2]))
                            id_equipo = cursor.lastrowid
                        cursor.execute("INSERT INTO equipos_torneo (id_torneo, id_equipo) VALUES (%s, %s)", (torneo[0], id_equipo))
                    conexion.commit()

                messagebox.showinfo("Éxito", "Torneo actualizado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al actualizar torneo: {e}")

        elif accion == "b":
            try:
                cursor.execute("DELETE FROM equipos_torneo WHERE id_torneo = %s", (torneo[0],))
                cursor.execute("DELETE FROM torneos WHERE id_torneo = %s", (torneo[0],))
                conexion.commit()
                messagebox.showinfo("Eliminado", "Torneo eliminado.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar torneo: {e}")

        ventana.destroy()

    tk.Button(ventana, text="Buscar", command=buscar).pack(pady=10)
    ventana.mainloop()