from funciones import *
from conexionBD import conexion, cursor

jugadores = []
entrenamientos = []
partidos = []
torneos = []

# 📝 Registro de jugador
def registrarJugador():
    borrarPantalla()
    print("\n📝 --- Registro de Jugador --- 📝\n")

    nombre     = input("👤 Nombre del jugador: ").strip().upper()
    apellidos  = input("👥 Apellidos del jugador: ").strip().upper()
    curp       = input("🆔 CURP del jugador: ").strip().upper()
    categoria  = input("📚 Categoría: ").strip().upper()
    numero     = input("🔢 Número de jugador: ").strip()
    pagado     = input("💰 ¿Inscripción pagada? (s/n): ").strip().lower()
    equipo     = input("🏷️ Equipo al que pertenece el jugador (nombre): ").strip().upper()

    if not nombre or not apellidos or not curp or not categoria or not numero or not equipo:
        print("\n❌ Datos incompletos. Intenta de nuevo.")
        esperarTecla()
        return

    pagado_bool = pagado == "s"

    try:
        # Buscar equipo por nombre; si no existe, crearlo (usamos la misma categoría)
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
        print("\n✅ Jugador registrado exitosamente.")
    except Exception as e:
        print(f"\n❌ Error al registrar jugador: {e}")

# 🗓️ Registro de horario de entrenamiento
def agregarHorario():
    borrarPantalla()
    print("\n🗓️ --- Registro de Día de Entrenamiento --- ⏰\n")

    dia       = input("📅 Día de entrenamiento: ").strip().upper()
    categoria = input("📚 Categoría que entrena: ").strip().upper()
    horario   = input("⏳ Horario (ej. 17:00-18:30): ").strip()

    if not dia or not categoria or not horario:
        print("\n❌ Datos incompletos. Intenta de nuevo.")
        esperarTecla()
        return

    try:
        sql = "INSERT INTO entrenamientos (dia, categoria, horario) VALUES (%s, %s, %s)"
        val = (dia, categoria, horario)
        cursor.execute(sql, val)
        conexion.commit()
        print("\n✅ Horario registrado exitosamente.")
    except Exception as e:
        if "Duplicate entry" in str(e):
            print("\n⚠️ Ya existe un horario registrado para esta categoría.")
        else:
            print(f"\n❌ Error al registrar horario: {e}")

# ⚽ Registro de partido
def registrarPartido():
    borrarPantalla()
    print("\n⚽ --- Registro de Partido --- 🏟️\n")

    local      = input("🏠 Equipo local (nombre): ").strip().upper()
    visitante  = input("🛫 Equipo visitante (nombre): ").strip().upper()
    categoria  = input("📚 Categoría del partido: ").strip().upper()
    dia        = input("📅 Día del partido: ").strip().upper()
    horario    = input("⏰ Horario del partido (HH:MM): ").strip()

    if not local or not visitante or not categoria or not dia or not horario:
        print("\n❌ Datos incompletos. Intenta de nuevo.")
        esperarTecla()
        return

    try:
        # Obtener/crear id del equipo local
        cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (local.lower(),))
        res = cursor.fetchone()
        if res:
            id_local = res[0]
        else:
            cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (local, categoria))
            id_local = cursor.lastrowid

        # Obtener/crear id del equipo visitante
        cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (visitante.lower(),))
        res = cursor.fetchone()
        if res:
            id_visitante = res[0]
        else:
            cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (visitante, categoria))
            id_visitante = cursor.lastrowid

        sql = """
            INSERT INTO partidos (id_equipo_local, id_equipo_visitante, categoria, dia, horario)
            VALUES (%s, %s, %s, %s, %s)
        """
        val = (id_local, id_visitante, categoria, dia, horario)
        cursor.execute(sql, val)
        conexion.commit()
        print("\n✅ Partido registrado exitosamente.")
    except Exception as e:
        print(f"\n❌ Error al registrar partido: {e}")

# 🏆 Registro de torneo
def registrarTorneo():
    borrarPantalla()
    print("\n🏆 --- Registro de Torneo --- 🏅\n")

    nombre    = input("🏷️ Nombre del torneo: ").strip().upper()
    categoria = input("📚 Categoría del torneo: ").strip().upper()

    try:
        cantidad = int(input("👥 Cantidad de equipos participantes: "))
        if cantidad <= 0:
            raise ValueError
    except ValueError:
        print("\n❌ Cantidad inválida.")
        esperarTecla()
        return

    equipos = []
    for i in range(cantidad):
        equipo = input(f"➡️ Nombre del equipo {i + 1}: ").strip().upper()
        equipos.append(equipo)

    try:
        sql = "INSERT INTO torneos (nombre, categoria) VALUES (%s, %s)"
        val = (nombre, categoria)
        cursor.execute(sql, val)
        id_torneo = cursor.lastrowid

        for equipo in equipos:
            # buscar equipo por nombre; si no existe, crearlo
            cursor.execute("SELECT id_equipo FROM equipos WHERE LOWER(nombre_equipo) = %s", (equipo.lower(),))
            fila = cursor.fetchone()
            if fila:
                id_equipo = fila[0]
            else:
                cursor.execute("INSERT INTO equipos (nombre_equipo, categoria) VALUES (%s, %s)", (equipo, categoria))
                id_equipo = cursor.lastrowid

            # ahora relacionar equipo <-> torneo
            cursor.execute("INSERT INTO equipos_torneo (id_torneo, id_equipo) VALUES (%s, %s)", (id_torneo, id_equipo))

        conexion.commit()
        print("\n✅ Torneo registrado exitosamente.")
    except Exception as e:
        print(f"\n❌ Error al registrar torneo: {e}")

# 🗑️ Vaciar todos los registros
def vaciarRegistros():
    borrarPantalla()
    print("\n🗑️ --- Vaciar todos los registros --- ⚠️\n")

    pwd = input("🔐 Ingresa la contraseña: ").strip()
    if pwd != "DRILLING":
        print("\n❌ Contraseña incorrecta. No se realizaron cambios.")
        esperarTecla()
        return

    confirm = input("⚠️ ¿Estás seguro que deseas borrar todos los registros? (s/n): ").strip().lower()
    if confirm != "s":
        print("\n🔄 Operación cancelada.")
        esperarTecla()
        return

    try:
        cursor.execute("DELETE FROM equipos_torneo")
        cursor.execute("DELETE FROM torneos")
        cursor.execute("DELETE FROM partidos")
        cursor.execute("DELETE FROM entrenamientos")
        cursor.execute("DELETE FROM jugadores")
        conexion.commit()
        print("\n✅ Todos los registros han sido eliminados de la base de datos.")
    except Exception as e:
        print(f"\n❌ Error al vaciar registros: {e}")
    esperarTecla()
