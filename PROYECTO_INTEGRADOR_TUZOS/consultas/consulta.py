from registros import registro
from conexionBD import conexion, cursor
from funciones import *


def menu_consulta():
    while True:
        borrarPantalla()
        print("\n\t🔍..::: MENÚ DE CONSULTA :::..🔍\n")
        print("1️⃣\t Consultar jugador")
        print("2️⃣\t Consultar días de entrenamiento")
        print("3️⃣\t Consultar partidos por día")
        print("4️⃣\t Consultar torneos")
        print("5️⃣\t 🔙Volver al menú principal🔙\n")

        opcion = input("👉\t Elige una opción: ").strip()

        match opcion:
            case "1":
                consultarJugador()
            case "2":
                consultarDiasEntrenamiento()
            case "3":
                consultarPartidosPorDia()
            case "4":
                consultarTorneo()
            case "5":
                break
            case _:
                input("❌\t Opción inválida. Intenta de nuevo...")

def consultarJugador():
    borrarPantalla()
    print("🔍 --- Consulta de Jugador --- 🔍\n")
    nombre = input("👤 Ingresa el nombre del jugador: ").strip().lower()
    apellido = input("👤 Ingresa el apellido del jugador: ").strip().lower()

    try:
        sql = """
            SELECT nombre, apellido, curp, categoria, numero, pagado
            FROM jugadores
            WHERE LOWER(nombre) = %s AND LOWER(apellido) = %s
        """
        cursor.execute(sql, (nombre, apellido))
        resultados = cursor.fetchall()

        if resultados:
            print(f"\n✅ Se encontraron {len(resultados)} resultado(s):\n")
            for idx, jugador in enumerate(resultados, start=1):
                inscripcion = "✅ Sí" if jugador[5] else "❌ No"
                print(f"🎽 Jugador {idx}")
                print(f"👤 Nombre: {jugador[0]} {jugador[1]}")
                print(f"🆔 CURP: {jugador[2]}")
                print(f"📚 Categoría: {jugador[3]}")
                print(f"🔢 Número: {jugador[4]}")
                print(f"💰 Inscripción pagada: {inscripcion}")
                print("-" * 40)
        else:
            print("⚠️ No se encontró ningún jugador con ese nombre y apellido.")
    except Exception as e:
        print(f"❌ Error al consultar jugador: {e}")

def consultarDiasEntrenamiento():
    borrarPantalla()
    print("📅 --- Consulta de Entrenamientos --- 📅\n")
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    try:
        for dia in dias_semana:
            print(f"\n📆 Día: {dia}")
            sql = "SELECT categoria, horario FROM entrenamientos WHERE LOWER(dia) = %s"
            cursor.execute(sql, (dia.lower(),))
            resultados = cursor.fetchall()

            if resultados:
                for cat, hora in resultados:
                    print(f"  📚 Categoría: {cat} - ⏰ Horario: {hora}")
            else:
                print("  ❌ Día sin actividades.")
    except Exception as e:
        print(f"❌ Error al consultar entrenamientos: {e}")

    esperarTecla()

def consultarPartidosPorDia():
    borrarPantalla()
    print("⚽ --- Consulta de Partidos por Día --- ⚽\n")
    dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]

    try:
        for dia in dias_semana:
            print(f"\n📆 Día: {dia}")
            sql = """
                SELECT el.nombre_equipo AS local, ev.nombre_equipo AS visitante, p.categoria, p.horario
                FROM partidos p
                JOIN equipos el ON p.id_equipo_local = el.id_equipo
                JOIN equipos ev ON p.id_equipo_visitante = ev.id_equipo
                WHERE LOWER(p.dia) = %s
            """
            cursor.execute(sql, (dia.lower(),))
            resultados = cursor.fetchall()

            if resultados:
                for local, visitante, cat, hora in resultados:
                    print(f"  🏠 {local} vs 🛫 {visitante} - 📚 Categoría: {cat} - ⏰ Horario: {hora}")
            else:
                print("  ❌ Día sin actividades.")
    except Exception as e:
        print(f"❌ Error al consultar partidos: {e}")
    esperarTecla()


def consultarTorneo():
    borrarPantalla()
    print("🏆 --- Consulta de Torneos --- 🏅\n")

    try:
        sql_torneos = "SELECT id_torneo, nombre, categoria FROM torneos"
        cursor.execute(sql_torneos)
        torneos = cursor.fetchall()

        if not torneos:
            print("⚠️ No hay torneos registrados.")
        else:
            for torneo in torneos:
                id_torneo, nombre, categoria = torneo
                print(f"\n🏷️ Torneo: {nombre}")
                print(f"📚 Categoría: {categoria}")
                print("👥 Equipos:")

                sql_equipos = """
                    SELECT e.nombre_equipo
                    FROM equipos_torneo et
                    JOIN equipos e ON et.id_equipo = e.id_equipo
                    WHERE et.id_torneo = %s
                """
                cursor.execute(sql_equipos, (id_torneo,))
                equipos = cursor.fetchall()

                if not equipos:
                    print("  ❌ No hay equipos asignados a este torneo.")
                else:
                    for eq in equipos:
                        print(f"  - {eq[0]}")
    except Exception as e:
        print(f"❌ Error al consultar torneos: {e}")
    esperarTecla()


def mostrarJugadores():
    borrarPantalla()
    print("📋 --- Lista de Jugadores --- 📋\n")

    try:
        sql = "SELECT id_jugador, nombre, apellido, curp, categoria, numero, pagado FROM jugadores"
        cursor.execute(sql)
        registros = cursor.fetchall()

        if not registros:
            print("⚠️ No hay jugadores registrados.")
        else:
            for reg in registros:
                inscripcion = "✅ Sí" if reg[6] else "❌ No"
                print(f"ID: {reg[0]} | {reg[1]} {reg[2]} | CURP: {reg[3]} | "
                      f"Categoría: {reg[4]} | Número: {reg[5]} | Pagado: {inscripcion}")
    except Exception as e:
        print(f"❌ Error al mostrar jugadores: {e}")
    esperarTecla()

def mostrarPartidosConJugadores():
    borrarPantalla()
    print("🏟️ --- Lista de Partidos y Jugadores --- 🏟️\n")

    try:
        sql_partidos = """
            SELECT p.id_partido, p.id_equipo_local, p.id_equipo_visitante, p.categoria, p.dia, p.horario
            FROM partidos p
            ORDER BY p.dia, p.horario
        """
        cursor.execute(sql_partidos)
        partidos = cursor.fetchall()

        if not partidos:
            print("⚠️ No hay partidos registrados.")
            esperarTecla()
            return

        for partido in partidos:
            id_partido, id_local, id_visitante, categoria, dia, horario = partido

            # obtener nombres de equipos
            cursor.execute("SELECT nombre_equipo FROM equipos WHERE id_equipo = %s", (id_local,))
            local_row = cursor.fetchone()
            local_name = local_row[0] if local_row else "Equipo desconocido"

            cursor.execute("SELECT nombre_equipo FROM equipos WHERE id_equipo = %s", (id_visitante,))
            visit_row = cursor.fetchone()
            visitante_name = visit_row[0] if visit_row else "Equipo desconocido"

            print(f"\n🏷️ Partido ID: {id_partido} — {local_name} vs {visitante_name} — {categoria} — {dia} {horario}")

            # jugadores locales
            sql_jug_local = """
                SELECT nombre, apellido 
                FROM jugadores 
                WHERE id_equipo = %s
            """
            cursor.execute(sql_jug_local, (id_local,))
            jugadores_local = cursor.fetchall()
            print("  🔵 Jugadores Locales:")
            if jugadores_local:
                for jug in jugadores_local:
                    print(f"     - {jug[0]} {jug[1]}")
            else:
                print("     ❌ Sin jugadores registrados.")

            # jugadores visitantes
            cursor.execute(sql_jug_local, (id_visitante,))
            jugadores_visitante = cursor.fetchall()
            print("  🔴 Jugadores Visitantes:")
            if jugadores_visitante:
                for jug in jugadores_visitante:
                    print(f"     - {jug[0]} {jug[1]}")
            else:
                print("     ❌ Sin jugadores registrados.")

            print("-" * 50)

    except Exception as e:
        print(f"❌ Error al mostrar partidos: {e}")

    esperarTecla()

