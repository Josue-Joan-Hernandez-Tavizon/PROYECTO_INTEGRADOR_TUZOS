import os

def borrarPantalla():
    os.system("cls")

def esperarTecla():
    input("\n\t\t... ⚠️ Oprima cualquier tecla para continuar ⚠️ ...")

def menu_usurios():
    print("\n\t👤 ..:: MENÚ DE USUARIO ::.. 👤\n")
    print("\t1️⃣\t Registrar Usuario")
    print("\t2️⃣\t Iniciar Sesión")
    print("\t3️⃣\t Mostrar Partidos")
    print("\t4️⃣\t Mostrar Jugadores")
    print("\t5️⃣\t 🚪 Salir\n")

    opcion = input("👉 Elige una opción: ").strip()
    return opcion
