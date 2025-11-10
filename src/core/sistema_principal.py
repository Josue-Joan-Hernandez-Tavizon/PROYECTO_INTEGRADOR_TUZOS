# sistema_principal.py
import tkinter as tk
from tkinter import messagebox
from src.views.registro_view import (
    RegistroApp_partido, 
    RegistroApp_horarios, 
    RegistroApp_entrenamiento, 
    RegistroApp_equipos
)

class SistemaPrincipal:
    def __init__(self, usuario):
        self.usuario = usuario
        self.root = None
        
    def mostrar_menu_principal(self):
        """Muestra el menú principal después del login"""
        self.root = tk.Tk()
        self.root.title("Sistema Deportivo Tuzos - Menú Principal")
        self.root.geometry("800x600")
        self.root.configure(bg="#212544")
        
        # Header
        frame_header = tk.Frame(self.root, bg="#212544", height=120)
        frame_header.pack(fill="x", pady=10)
        
        tk.Label(frame_header, text="SISTEMA DEPORTIVO TUZOS", 
                font=("Arial", 24, "bold"), 
                bg="#212544", fg="white").pack(pady=10)
        
        tk.Label(frame_header, text=f"Bienvenido: {self.usuario}", 
                font=("Arial", 16), 
                bg="#212544", fg="#FFB93B").pack()
        
        # Frame principal para botones
        frame_botones = tk.Frame(self.root, bg="#F5F5F5")
        frame_botones.pack(expand=True, fill="both", padx=50, pady=30)
        
        # Botones del menú principal
        opciones = [
            ("⚽ Registro de Partidos", self.mostrar_registro_partidos),
            ("📅 Registro de Horarios", self.mostrar_registro_horarios),
            ("🏃 Registro de Entrenamientos", self.mostrar_registro_entrenamientos),
            ("👥 Registro de Equipos", self.mostrar_registro_equipos),
            ("🚪 Cerrar Sesión", self.cerrar_sesion)
        ]
        
        for texto, comando in opciones:
            btn = tk.Button(frame_botones, text=texto, 
                          font=("Arial", 14), 
                          bg="#212544", fg="white",
                          width=30, height=2,
                          command=comando)
            btn.pack(pady=8)
        
        self.root.mainloop()
    
    def mostrar_registro_partidos(self):
        """Muestra la ventana de registro de partidos"""
        self.root.destroy()
        root = tk.Tk()
        RegistroApp_partido(root)
        root.mainloop()
    
    def mostrar_registro_horarios(self):
        """Muestra la ventana de registro de horarios"""
        self.root.destroy()
        root = tk.Tk()
        RegistroApp_horarios(root)
        root.mainloop()
    
    def mostrar_registro_entrenamientos(self):
        """Muestra la ventana de registro de entrenamientos"""
        self.root.destroy()
        root = tk.Tk()
        RegistroApp_entrenamiento(root)
        root.mainloop()
    
    def mostrar_registro_equipos(self):
        """Muestra la ventana de registro de equipos"""
        self.root.destroy()
        root = tk.Tk()
        RegistroApp_equipos(root)
        root.mainloop()
    
    def cerrar_sesion(self):
        """Cierra sesión y vuelve al login"""
        self.root.destroy()
        from src.views.login_view import iniciar_login
        iniciar_login()

def iniciar_sistema():
    """Función para iniciar el sistema completo"""
    def on_login_exitoso(usuario):
        sistema = SistemaPrincipal(usuario)
        sistema.mostrar_menu_principal()
    
    from src.views.login_view import iniciar_login
    iniciar_login(on_login_exitoso)

if __name__ == "__main__":
    iniciar_sistema()