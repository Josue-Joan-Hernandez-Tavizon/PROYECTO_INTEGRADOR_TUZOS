from src.models.database import Database
# import bcrypt  # DESHABILITADO TEMPORALMENTE

def validar_credenciales(usuario, password):
    """
    Valida las credenciales del usuario en la base de datos
    USANDO TEXTO PLANO (bcrypt deshabilitado temporalmente)
    """
    try:
        db = Database()
        
        # Obtener el password desde la base de datos
        query = "SELECT password FROM USUARIOS WHERE usuario = %s"
        result = db.fetch_all(query, (usuario,))
        
        db.close()
        
        # Si no existe el usuario, retornar False
        if not result or len(result) == 0:
            return False
        
        password_bd = result[0][0]
        
        # Comparación directa de texto plano
        return password == password_bd
        
    except Exception as e:
        print(f"Error al validar credenciales: {e}")
        return False