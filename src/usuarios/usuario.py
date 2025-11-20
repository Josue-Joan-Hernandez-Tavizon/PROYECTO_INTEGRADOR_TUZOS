from conexionBD import conexion, cursor
import datetime
import hashlib

def hash_password(contrasena):
    return hashlib.sha256(contrasena.encode()).hexdigest()

def registrar(nombre, apellidos, email, contrasena, id_equipo):
    try:
        # normalizar id_equipo: si viene vacío -> None
        if id_equipo is not None and str(id_equipo).strip() == "":
            id_equipo = None
        # Hash de la contraseña
        contrasena_hashed = hash_password(contrasena)

        sql = "INSERT INTO usuarios (nombre, apellidos, email, contrasena, id_equipo) VALUES (%s, %s, %s, %s, %s)"
        val = (nombre, apellidos, email, contrasena_hashed, id_equipo)
        cursor.execute(sql, val)
        conexion.commit()
        return True
    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        return False

def iniciar_sesion(email, contrasena):
    try:
        contrasena_hashed = hash_password(contrasena)
        sql = "SELECT * FROM usuarios WHERE email = %s AND contrasena = %s"
        val = (email, contrasena_hashed)
        cursor.execute(sql, val)
        registro = cursor.fetchone()
        if registro:
            return registro
        else:
            return None
    except Exception as e:
        print(f"❌ Error al iniciar sesión: {e}")
        return None
