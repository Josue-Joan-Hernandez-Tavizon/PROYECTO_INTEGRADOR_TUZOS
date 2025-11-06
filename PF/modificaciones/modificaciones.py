# modificaciones.py
from funciones import *
from conexionBD import conexion, cursor

def menu_modificaciones():
    while True:
        borrarPantalla()
        print("\n🔧 --- MODIFICAR O BORRAR REGISTROS --- 🔧")
        print("1. 🧑‍🤝‍🧑 Jugador")
        print("2. 🗓️ Día de entrenamiento")
        print("3. ⚽ Partido")
        print("4. 🏆 Torneo")
        print("5. 🔙 Volver\n")
        opcion = input("Selecciona una opción: ").strip()

        if opcion == "1":
            modificar_jugador()
        elif opcion == "2":
            modificar_entrenamiento()
        elif opcion == "3":
            modificar_partido()
        elif opcion == "4":
            modificar_torneo()
        elif opcion == "5":
            break
        else:
            input("❌ Opción inválida. Presiona Enter para continuar...")

# ------------------ JUGADORES ------------------

def modificar_jugador():
    curp = input("🆔 CURP del jugador a modificar/eliminar: ").strip()

    cursor.execute("SELECT * FROM jugadores WHERE curp = %s", (curp,))
    jugador = cursor.fetchone()

    if not jugador:
        print("⚠️ Jugador no encontrado.")
        esperarTecla()
        return

    print(f"\n🔎 [ENCONTRADO] {jugador}")
    accion = input("✏️ ¿Deseas editar (e) o borrar (b) este jugador?: ").strip().lower()

    if accion == "e":
        nombre     = input("👤 Nuevo nombre: ").strip()
        apellido   = input("👥 Nuevos apellidos: ").strip()
        nueva_curp = input("🆔 Nueva CURP: ").strip()
        categoria  = input("📚 Nueva categoría: ").strip()
        numero     = input("🔢 Nuevo número: ").strip()
        pagado     = input("💰 ¿Inscripción pagada? (s/n): ").strip().lower()

        pagado_bool = pagado == "s"

        try:
            cursor.execute("""
                UPDATE jugadores
                SET nombre = %s,
                    apellido = %s,
                    curp = %s,
                    categoria = %s,
                    numero = %s,
                    pagado = %s
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
            print("✅ Jugador actualizado.")
        except Exception as e:
            print(f"❌ Error al actualizar jugador: {e}")

    elif accion == "b":
        cursor.execute("DELETE FROM jugadores WHERE curp = %s", (curp,))
        conexion.commit()
        print("🗑️ Jugador eliminado.")

    esperarTecla()


# ------------------ ENTRENAMIENTOS ------------------

def modificar_entrenamiento():
    dia = input("📅 Día del entrenamiento a modificar/eliminar: ").strip()

    cursor.execute("SELECT * FROM entrenamientos WHERE dia = %s", (dia,))
    entrenamiento = cursor.fetchone()

    if not entrenamiento:
        print("⚠️ Entrenamiento no encontrado.")
        esperarTecla()
        return

    print(f"\n🔎 [ENCONTRADO] {entrenamiento}")
    accion = input("✏️ ¿Deseas editar (e) o borrar (b) este entrenamiento?: ").strip().lower()

    if accion == "e":
        nueva_cat = input("📚 Nueva categoría: ").strip()
        nuevo_horario = input("⏰ Nuevo horario: ").strip()

        try:
            cursor.execute("""
                UPDATE entrenamientos
                SET categoria = %s, horario = %s
                WHERE dia = %s
            """, (nueva_cat or entrenamiento[1], nuevo_horario or entrenamiento[2], dia))
            conexion.commit()
            print("✅ Entrenamiento actualizado.")
        except Exception as e:
            print(f"❌ Error al actualizar: {e}")

    elif accion == "b":
        cursor.execute("DELETE FROM entrenamientos WHERE dia = %s", (dia,))
        conexion.commit()
        print("🗑️ Entrenamiento eliminado.")

    esperarTecla()

# ------------------ PARTIDOS ------------------

def modificar_partido():
    dia = input("📅 Día del partido a modificar/eliminar: ").strip()

    cursor.execute("SELECT * FROM partidos WHERE dia = %s", (dia,))
    partido = cursor.fetchone()

    if not partido:
        print("⚠️ Partido no encontrado.")
        esperarTecla()
        return

    print(f"\n🔎 [ENCONTRADO] {partido}")
    accion = input("✏️ ¿Deseas editar (e) o borrar (b) este partido?: ").strip().lower()

    if accion == "e":
        local = input("🏠 Nuevo equipo local (nombre, deja vacío para mantener): ").strip().upper()
        visitante = input("🛫 Nuevo equipo visitante (nombre, deja vacío para mantener): ").strip().upper()
        categoria = input("📚 Nueva categoría (deja vacío para mantener): ").strip().upper()
        nuevo_dia = input("📅 Nuevo día: ").strip()
        horario = input("⏰ Nuevo horario: ").strip()

        try:
            # partido structure: (id_partido, id_equipo_local, id_equipo_visitante, categoria, dia, horario)
            # Local
            if local:
                cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (local.lower(),))
                r = cursor.fetchone()
                if r:
                    id_local = r[0]
                else:
                    # crear equipo si no existe (asignamos categoria actual si no se puso nueva)
                    cat_to_use = categoria if categoria else partido[3]
                    cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (local, cat_to_use))
                    id_local = cursor.lastrowid
            else:
                id_local = partido[1]

            # Visitante
            if visitante:
                cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (visitante.lower(),))
                r = cursor.fetchone()
                if r:
                    id_visitante = r[0]
                else:
                    cat_to_use = categoria if categoria else partido[3]
                    cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (visitante, cat_to_use))
                    id_visitante = cursor.lastrowid
            else:
                id_visitante = partido[2]

            sql = """
                UPDATE partidos
                SET id_equipo_local = %s, id_equipo_visitante = %s, categoria = %s, dia = %s, horario = %s
                WHERE id_partido = %s
            """
            valores = (
                id_local,
                id_visitante,
                categoria or partido[3],
                nuevo_dia or partido[4],
                horario or partido[5],
                partido[0]
            )
            cursor.execute(sql, valores)
            conexion.commit()
            print("✅ Partido actualizado.")
        except Exception as e:
            print(f"❌ Error al actualizar partido: {e}")

    elif accion == "b":
        try:
            cursor.execute("DELETE FROM partidos WHERE id_partido = %s", (partido[0],))
            conexion.commit()
            print("🗑️ Partido eliminado.")
        except Exception as e:
            print(f"❌ Error al eliminar partido: {e}")

    esperarTecla()


# ------------------ TORNEOS ------------------

def modificar_torneo():
    nombre = input("🏷️ Nombre del torneo a modificar/eliminar: ").strip().upper()
    cursor.execute("SELECT * FROM torneos WHERE nombre = %s", (nombre,))
    torneo = cursor.fetchone()

    if not torneo:
        print("⚠️ Torneo no encontrado.")
        esperarTecla()
        return

    print(f"\n🔎 [ENCONTRADO] {torneo}")
    accion = input("✏️ ¿Deseas editar (e) o borrar (b) este torneo?: ").strip().lower()

    if accion == "e":
        nuevo_nombre = input("🏷️ Nuevo nombre: ").strip().upper()
        nueva_cat = input("📚 Nueva categoría: ").strip().upper()

        try:
            cursor.execute("""
                UPDATE torneos
                SET nombre = %s, categoria = %s
                WHERE id_torneo = %s
            """, (nuevo_nombre or torneo[1], nueva_cat or torneo[2], torneo[0]))
            conexion.commit()

            actualizar = input("🔁 ¿Deseas actualizar los equipos del torneo? (s/n): ").strip().lower()
            if actualizar == "s":
                cursor.execute("DELETE FROM equipos_torneo WHERE id_torneo = %s", (torneo[0],))
                cantidad = int(input("👥 Nueva cantidad de equipos: "))
                for i in range(cantidad):
                    nombre_equipo = input(f"➡️ Equipo {i+1}: ").strip().upper()
                    # obtener/crear id_equipo
                    cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (nombre_equipo.lower(),))
                    fila = cursor.fetchone()
                    if fila:
                        id_equipo = fila[0]
                    else:
                        cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (nombre_equipo, nueva_cat or torneo[2]))
                        id_equipo = cursor.lastrowid
                    cursor.execute("INSERT INTO equipos_torneo (id_torneo, id_equipo) VALUES (%s, %s)", (torneo[0], id_equipo))
                conexion.commit()

            print("✅ Torneo actualizado.")
        except Exception as e:
            print(f"❌ Error al actualizar torneo: {e}")

    elif accion == "b":
        try:
            cursor.execute("DELETE FROM equipos_torneo WHERE id_torneo = %s", (torneo[0],))
            cursor.execute("DELETE FROM torneos WHERE id_torneo = %s", (torneo[0],))
            conexion.commit()
            print("🗑️ Torneo eliminado.")
        except Exception as e:
            print(f"❌ Error al eliminar torneo: {e}")

    esperarTecla()
