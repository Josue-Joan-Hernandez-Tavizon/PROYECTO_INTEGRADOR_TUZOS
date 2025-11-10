import tkinter as tk
import customtkinter as ctk
from src.views.login_view import LoginApp
from src.components.plantilla import plantilla_f
from src.views.registro_view import (
    RegistroApp_partido,
    RegistroApp_horarios,
    RegistroApp_entrenamiento,
    RegistroApp_equipos,
    RegistroApp_jugador,
    RegistroApp_torneo,
    RegistroApp_profesor,
    RegistroApp_usuario
)
from src.views.consulta_view import ConsultaApp
from src.views.modificar_view import ModificarApp
from src.views.eliminar_view import EliminarApp
from src.components.cont_r import ContR, Cont_Cr
from src.components.panel_r import PanelR

class SistemaCompleto:
    def __init__(self):
        self.root = None
        self.usuario_actual = None
        self.plantilla = None
        self.historial_navegacion = []  # Para el historial de navegación
        self.navegando_atras = False  # Flag para evitar agregar al historial al retroceder
    
    def iniciar(self):
        """Inicia el sistema"""
        self.mostrar_login()
    
    def mostrar_login(self):
        """Muestra la ventana de login"""
        if self.root:
            self.root.destroy()
        
        self.root = tk.Tk()
        LoginApp(self.root, on_login_success=self._login_exitoso)
        
        self.root.mainloop()
    
    def _login_exitoso(self, usuario):
        """Se ejecuta cuando el login es exitoso"""
        self.usuario_actual = usuario
        self.root.destroy()
        self.mostrar_menu_principal()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal con header de plantilla"""
        self.root = tk.Tk()
        self.root.title(f"Sistema Deportivo - {self.usuario_actual}")
        
        # Actualizar la ventana para asegurar que se inicialice correctamente
        self.root.update_idletasks()
        
        # Obtener el área de trabajo disponible usando la API de Windows
        # Esto excluye automáticamente la barra de tareas
        try:
            import ctypes
            user32 = ctypes.windll.user32
            # SM_CXSCREEN = 0 (ancho de pantalla completa)
            # SM_CYSCREEN = 1 (alto de pantalla completa)
            # SM_CXFULLSCREEN = 16 (ancho del área de trabajo)
            # SM_CYFULLSCREEN = 17 (alto del área de trabajo sin barra de tareas)
            work_width = user32.GetSystemMetrics(0)  # Ancho completo
            work_height = user32.GetSystemMetrics(17)  # Alto sin barra de tareas
            
            # Establecer geometría en la posición (0,0)
            self.root.geometry(f"{work_width}x{work_height}+0+0")
        except:
            # Fallback: usar tamaño fijo si falla la API de Windows
            self.root.geometry("1200x700")
        
        # Actualizar nuevamente después de establecer geometría
        self.root.update_idletasks()
        self.root.resizable(True, True)
        
        # Usar plantilla_f para el header con callback de búsqueda y de home
        self.plantilla = plantilla_f(self.root)
        self.plantilla.usuario_actual = self.usuario_actual  # Pasar el usuario a la plantilla
        self.plantilla.header_v2(PanelR, Cont_Cr, ContR, 
                                 search_callback=self._buscar_funcion,
                                 home_callback=self._mostrar_menu_crud)
        
        # Frame contenido
        self.frame_contenido = tk.Frame(self.plantilla.frame_prin, bg="white")
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Mostrar menú inicial
        self._mostrar_menu_crud()
        
        # Agregar info usuario
        self._agregar_info_usuario()
        
        # Configurar atajos de teclado (keyboard shortcuts)
        self.root.bind('<Control-r>', lambda e: self.mostrar_menu_registrar())
        self.root.bind('<Control-R>', lambda e: self.mostrar_menu_registrar())
        self.root.bind('<Control-m>', lambda e: self.mostrar_menu_modificar())
        self.root.bind('<Control-M>', lambda e: self.mostrar_menu_modificar())
        self.root.bind('<Control-q>', lambda e: self.mostrar_menu_consultar())
        self.root.bind('<Control-Q>', lambda e: self.mostrar_menu_consultar())
        self.root.bind('<Control-e>', lambda e: self.mostrar_menu_eliminar())
        self.root.bind('<Control-E>', lambda e: self.mostrar_menu_eliminar())
        self.root.bind('<Control-BackSpace>', lambda e: self._retroceder_navegacion())
        
        self.root.mainloop()
    
    def _buscar_funcion(self, texto_busqueda):
        """Busca y navega a una función del menú"""
        texto = texto_busqueda.lower().strip()
        
        # Diccionario de funciones buscables
        funciones = {
            # Registrar
            "registrar jugadores": self.mostrar_registro_jugador,
            "registrar torneos": self.mostrar_registro_torneo,
            "registrar partidos": self.mostrar_registro_partidos,
            "registrar horarios": self.mostrar_registro_horarios,
            "registrar categorias": self.mostrar_registro_equipos,
            "registrar entrenamientos": self.mostrar_registro_entrenamientos,
            "registrar profesores": self.mostrar_registro_profesor,
            "registrar usuarios": self.mostrar_registro_usuario,
            # Consultar
            "consultar jugadores": lambda: self.mostrar_consulta("JUGADORES"),
            "consultar torneos": lambda: self.mostrar_consulta("TORNEO"),
            "consultar partidos": lambda: self.mostrar_consulta("PARTIDOS"),
            "consultar horarios": lambda: self.mostrar_consulta("HORARIO"),
            "consultar categorias": lambda: self.mostrar_consulta("CATEGORIA"),
            "consultar entrenamientos": lambda: self.mostrar_consulta("ENTRENAMIENTO"),
            "consultar profesores": lambda: self.mostrar_consulta("PROFESORES"),
            "consultar usuarios": lambda: self.mostrar_consulta("USUARIOS"),
            "consultar resultados": lambda: self.mostrar_consulta("RESULTADOS"),
            # Modificar
            "modificar jugadores": lambda: self.mostrar_modificar("JUGADORES"),
            "modificar torneos": lambda: self.mostrar_modificar("TORNEO"),
            "modificar partidos": lambda: self.mostrar_modificar("PARTIDOS"),
            "modificar horarios": lambda: self.mostrar_modificar("HORARIO"),
            "modificar categorias": lambda: self.mostrar_modificar("CATEGORIA"),
            "modificar entrenamientos": lambda: self.mostrar_modificar("ENTRENAMIENTO"),
            "modificar profesores": lambda: self.mostrar_modificar("PROFESORES"),
            "modificar usuarios": lambda: self.mostrar_modificar("USUARIOS"),
            # Eliminar
            "eliminar jugadores": lambda: self.mostrar_eliminar("JUGADORES"),
            "eliminar torneos": lambda: self.mostrar_eliminar("TORNEO"),
            "eliminar partidos": lambda: self.mostrar_eliminar("PARTIDOS"),
            "eliminar horarios": lambda: self.mostrar_eliminar("HORARIO"),
            "eliminar categorias": lambda: self.mostrar_eliminar("CATEGORIA"),
            "eliminar entrenamientos": lambda: self.mostrar_eliminar("ENTRENAMIENTO"),
            "eliminar profesores": lambda: self.mostrar_eliminar("PROFESORES"),
            "eliminar usuarios": lambda: self.mostrar_eliminar("USUARIOS"),
            # Menús principales
            "registrar": self.mostrar_menu_registrar,
            "consultar": self.mostrar_menu_consultar,
            "modificar": self.mostrar_menu_modificar,
            "eliminar": self.mostrar_menu_eliminar,
        }
        
        # Buscar coincidencia exacta
        if texto in funciones:
            funciones[texto]()
            return
        
        # Buscar coincidencia parcial
        coincidencias = [key for key in funciones.keys() if texto in key]
        
        if len(coincidencias) == 1:
            # Una sola coincidencia, navegar directamente
            funciones[coincidencias[0]]()
        elif len(coincidencias) > 1:
            # Múltiples coincidencias, mostrar mensaje
            self._mostrar_resultados_busqueda(coincidencias, funciones)
        else:
            # Sin coincidencias
            self._mostrar_mensaje_sin_resultados(texto)
    
    def _mostrar_resultados_busqueda(self, coincidencias, funciones):
        """Muestra los resultados de búsqueda cuando hay múltiples coincidencias"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        # Título
        titulo = tk.Label(self.frame_contenido, text="Resultados de búsqueda",
                         font=("Arial", 18, "bold"),
                         bg="white", fg="#212544")
        titulo.pack(pady=20)
        
        # Contenedor de resultados
        contenedor = ctk.CTkFrame(self.frame_contenido, fg_color="#CCCBCB", corner_radius=15)
        contenedor.pack(fill="none", padx=230, pady=10)
        
        subtitulo = tk.Label(contenedor, text="Selecciona una opción:",
                            font=("Arial", 14, "bold"),
                            bg="#CCCBCB", fg="#212544")
        subtitulo.pack(pady=15)
        
        # Botones para cada coincidencia
        for coincidencia in coincidencias:
            btn = ctk.CTkButton(contenedor, text=coincidencia.title(),
                               font=("Arial", 12, "bold"),
                               fg_color="#212544",
                               hover_color="#1a1d38",
                               text_color="white",
                               width=400, height=50,
                               corner_radius=12,
                               command=funciones[coincidencia])
            btn.pack(pady=5, padx=20)
        
        # Botón volver
        btn_volver = ctk.CTkButton(contenedor, text="🔙 Volver",
                                   font=("Arial", 12, "bold"),
                                   fg_color="#212544",
                                   hover_color="#1a1d38",
                                   text_color="white",
                                   width=400, height=50,
                                   corner_radius=12,
                                   command=self._mostrar_menu_crud)
        btn_volver.pack(pady=15, padx=20)
    
    def _mostrar_mensaje_sin_resultados(self, texto):
        """Muestra mensaje cuando no hay resultados de búsqueda"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        msg = tk.Label(self.frame_contenido, 
                      text=f"No se encontraron resultados para: '{texto}'",
                      font=("Arial", 16),
                      bg="white", fg="#212544")
        msg.pack(pady=50)
        
        sugerencia = tk.Label(self.frame_contenido,
                             text="Intenta buscar: 'registrar jugadores', 'consultar partidos', etc.",
                             font=("Arial", 12),
                             bg="white", fg="#666666")
        sugerencia.pack(pady=10)
        
        btn_volver = ctk.CTkButton(self.frame_contenido, text="🔙 Volver",
                                   font=("Arial", 12, "bold"),
                                   fg_color="#212544",
                                   hover_color="#1a1d38",
                                   text_color="white",
                                   width=200, height=40,
                                   corner_radius=10,
                                   command=self._mostrar_menu_crud)
        btn_volver.pack(pady=20)
    
    def _agregar_info_usuario(self):
        """Agrega información del usuario en el header"""
        info_usuario = tk.Label(self.plantilla.frame_mb, text=f"👤 {self.usuario_actual}",
                               font=("Arial", 12, "bold"),
                               bg="#212544", fg="#FFB93B")
        info_usuario.place(relx=0.85, rely=0.7)
    
    def _agregar_al_historial(self, funcion):
        """Agrega una función al historial de navegación"""
        if not self.navegando_atras:
            # Solo agregar si no estamos navegando hacia atrás
            self.historial_navegacion.append(funcion)
            # Limitar el historial a 20 elementos
            if len(self.historial_navegacion) > 20:
                self.historial_navegacion.pop(0)
    
    def _retroceder_navegacion(self):
        """Retrocede a la vista anterior en el historial"""
        if len(self.historial_navegacion) > 1:
            # Quitar la vista actual
            self.historial_navegacion.pop()
            # Obtener la vista anterior
            vista_anterior = self.historial_navegacion.pop()
            # Marcar que estamos navegando atrás
            self.navegando_atras = True
            # Llamar a la vista anterior
            vista_anterior()
            # Desmarcar navegación atrás
            self.navegando_atras = False
        elif len(self.historial_navegacion) == 1:
            # Si solo hay una vista, volver al menú principal
            self.historial_navegacion.clear()
            self.navegando_atras = True
            self._mostrar_menu_crud()
            self.navegando_atras = False

    def _mostrar_menu_crud(self):
        """Muestra el menú CRUD principal"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        # Contenedor azul exterior con bordes redondeados
        contenedor_amarillo = ctk.CTkFrame(self.frame_contenido, fg_color="#212544", corner_radius=20)
        contenedor_amarillo.pack(pady=10, padx=230, fill="none")
        
        # Frame interior para el contenedor gris y botón cerrar
        contenedor_interior = ctk.CTkFrame(contenedor_amarillo, fg_color="#212544", corner_radius=0)
        contenedor_interior.pack(fill="both", padx=100, pady=30)
        
        # Mensaje de bienvenida den del contenedor azul - centrado verticalmente
        bienvenida = tk.Label(contenedor_interior, text=f"¡Bienvenido {self.usuario_actual}!",
                         font=("Arial", 18, "bold"),
                         bg="#212544", fg="#FCFCFC")
        bienvenida.pack(pady=15, expand=True)
        
        # Contenedor gris para las opciones con bordes redondeados
        contenedor_opciones = ctk.CTkFrame(contenedor_interior, fg_color="#CCCBCB", corner_radius=15)
        contenedor_opciones.pack(fill="none", padx=2, pady=(1, 15))
        
        # Título dentro del contenedor gris
        titulo = tk.Label(contenedor_opciones, text="MENÚ PRINCIPAL",
                         font=("Arial", 20, "bold"),
                         bg="#CCCBCB", fg="#212544")
        titulo.pack(pady=(10, 10))
        
        # Frame para two columns
        frame_opciones = ctk.CTkFrame(contenedor_opciones, fg_color="transparent")
        frame_opciones.pack(fill="none", padx=15, pady=6)
        
        # Columna izquierda
        frame_izq = ctk.CTkFrame(frame_opciones, fg_color="transparent")
        frame_izq.pack(side="left", padx=5, pady=20)
        
        # Espacio entre columnas
        frame_espacio = ctk.CTkFrame(frame_opciones, fg_color="transparent", width=120)
        frame_espacio.pack(side="left", padx=0)
        
        # Columna derecha
        frame_der = ctk.CTkFrame(frame_opciones, fg_color="transparent")
        frame_der.pack(side="right", padx=5, pady=20)
        
        opciones_izq = [
            ("REGISTRAR", self.mostrar_menu_registrar),
            ("CONSULTAR", self.mostrar_menu_consultar)
        ]
        
        opciones_der = [
            ("MODIFICAR", self.mostrar_menu_modificar),
            ("ELIMINAR", self.mostrar_menu_eliminar)
        ]
        
        # Crear botones columna izquierda
        for texto, comando in opciones_izq:
            btn = ctk.CTkButton(frame_izq, text=texto,
                           font=("Arial", 14, "bold"),
                           fg_color="#FFB93B",
                           hover_color="#E5A635",
                           text_color="black",
                           width=250, height=60,
                           corner_radius=15,
                           command=comando)
            btn.pack(pady=35)
        
        # Crear botones columna derecha
        for texto, comando in opciones_der:
            btn = ctk.CTkButton(frame_der, text=texto,
                           font=("Arial", 14, "bold"),
                           fg_color="#FFB93B",
                           hover_color="#E5A635",
                           text_color="black",
                           width=250, height=60,
                           corner_radius=15,
                           command=comando)
            btn.pack(pady=35)
        
        # Frame para el botón de cerrar sesión (centrado abajo)
        frame_cierre = ctk.CTkFrame(contenedor_opciones, fg_color="transparent")
        frame_cierre.pack(fill="x", padx=10, pady=10)
        
        btn_cerrar = ctk.CTkButton(frame_cierre, text="Cerrar Sesión",
                              font=("Arial", 14, "bold"),
                              fg_color="#FF6B6B",
                              hover_color="#E55555",
                              text_color="white",
                              width=550, height=60,
                              corner_radius=15,
                              command=self.cerrar_sesion)
        btn_cerrar.pack()
    
    def mostrar_menu_registrar(self):
        """Submenú Registrar - Coincide con las tablas de la BD"""
        self._agregar_al_historial(self.mostrar_menu_registrar)
        self._mostrar_submenu("REGISTRAR", [
            ("Jugadores", self.mostrar_registro_jugador),
            ("Torneos", self.mostrar_registro_torneo),
            ("Partidos", self.mostrar_registro_partidos),
            ("Horarios", self.mostrar_registro_horarios),
            ("Categorias", self.mostrar_registro_equipos),
            ("Entrenamientos", self.mostrar_registro_entrenamientos),
            ("Profesores", self.mostrar_registro_profesor),
            ("Usuarios", self.mostrar_registro_usuario)
        ])
    
    def mostrar_menu_consultar(self):
        """Submenú Consultar - Coincide con las tablas de la BD"""
        self._agregar_al_historial(self.mostrar_menu_consultar)
        self._mostrar_submenu("CONSULTAR", [
            ("Dashboard", self.mostrar_resumen_general),
            ("Jugadores", lambda: self.mostrar_consulta("JUGADORES")),
            ("Torneos", lambda: self.mostrar_consulta("TORNEO")),
            ("Partidos", lambda: self.mostrar_consulta("PARTIDOS")),
            ("Horarios", lambda: self.mostrar_consulta("HORARIO")),
            ("Categorias", lambda: self.mostrar_consulta("CATEGORIA")),
            ("Entrenamientos", lambda: self.mostrar_consulta("ENTRENAMIENTO")),
            ("Profesores", lambda: self.mostrar_consulta("PROFESORES")),
            ("Usuarios", lambda: self.mostrar_consulta("USUARIOS")),
            ("Resultados", lambda: self.mostrar_consulta("RESULTADOS"))
        ])
    
    def mostrar_menu_modificar(self):
        """Submenú Modificar - Coincide con las tablas de la BD"""
        self._agregar_al_historial(self.mostrar_menu_modificar)
        self._mostrar_submenu("MODIFICAR", [
            ("Jugadores", lambda: self.mostrar_modificar("JUGADORES")),
            ("Torneos", lambda: self.mostrar_modificar("TORNEO")),
            ("Partidos", lambda: self.mostrar_modificar("PARTIDOS")),
            ("Horarios", lambda: self.mostrar_modificar("HORARIO")),
            ("Categorias", lambda: self.mostrar_modificar("CATEGORIA")),
            ("Entrenamientos", lambda: self.mostrar_modificar("ENTRENAMIENTO")),
            ("Profesores", lambda: self.mostrar_modificar("PROFESORES")),
            ("Usuarios", lambda: self.mostrar_modificar("USUARIOS"))
        ])
    
    def mostrar_menu_eliminar(self):
        """Submenú Eliminar - Coincide con las tablas de la BD"""
        self._agregar_al_historial(self.mostrar_menu_eliminar)
        self._mostrar_submenu("ELIMINAR", [
            ("Jugadores", lambda: self.mostrar_eliminar("JUGADORES")),
            ("Torneos", lambda: self.mostrar_eliminar("TORNEO")),
            ("Partidos", lambda: self.mostrar_eliminar("PARTIDOS")),
            ("Horarios", lambda: self.mostrar_eliminar("HORARIO")),
            ("Categorias", lambda: self.mostrar_eliminar("CATEGORIA")),
            ("Entrenamientos", lambda: self.mostrar_eliminar("ENTRENAMIENTO")),
            ("Profesores", lambda: self.mostrar_eliminar("PROFESORES")),
            ("Usuarios", lambda: self.mostrar_eliminar("USUARIOS"))
        ])
    
    def _mostrar_submenu(self, titulo, opciones):
        """Muestra un submenú genérico con botones azules"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        # Título principal
        titulo_label = tk.Label(self.frame_contenido, text=titulo,
                               font=("Arial", 18, "bold"),
                               bg="white", fg="#212544")
        titulo_label.pack(pady=20)
        
        # Contenedor gris para las opciones con bordes redondeados
        contenedor_opciones = ctk.CTkFrame(self.frame_contenido, fg_color="#CCCBCB", corner_radius=15)
        contenedor_opciones.pack(fill="none", padx=230, pady=10)
        
        # Título dentro del contenedor
        titulo_contenedor = tk.Label(contenedor_opciones, text=f"¿Qué deseas {titulo.lower()}?",
                                     font=("Arial", 16, "bold"),
                                     bg="#CCCBCB", fg="#212544")
        titulo_contenedor.pack(pady=(10, 15))
        
        # Frame para two columns
        frame_opciones = ctk.CTkFrame(contenedor_opciones, fg_color="transparent")
        frame_opciones.pack(fill="none", padx=15, pady=10)
        
        # Columna izquierda
        frame_izq = ctk.CTkFrame(frame_opciones, fg_color="transparent")
        frame_izq.pack(side="left", padx=5, pady=15)
        
        # Espacio entre columnas
        frame_espacio = ctk.CTkFrame(frame_opciones, fg_color="transparent", width=120)
        frame_espacio.pack(side="left", padx=0)
        
        # Columna derecha
        frame_der = ctk.CTkFrame(frame_opciones, fg_color="transparent")
        frame_der.pack(side="right", padx=5, pady=15)
        
        # Dividir opciones en two columns
        mitad = len(opciones) // 2
        opciones_izq = opciones[:mitad]
        opciones_der = opciones[mitad:]
        
        # Botones columna izquierda
        for texto, comando in opciones_izq:
            btn = ctk.CTkButton(frame_izq, text=texto,
                           font=("Arial", 12, "bold"),
                           fg_color="#212544",
                           hover_color="#1a1d38",
                           text_color="white",
                           width=250, height=50,
                           corner_radius=12,
                           command=comando)
            btn.pack(pady=10)
        
        # Botones columna derecha
        for texto, comando in opciones_der:
            btn = ctk.CTkButton(frame_der, text=texto,
                           font=("Arial", 12, "bold"),
                           fg_color="#212544",
                           hover_color="#1a1d38",
                           text_color="white",
                           width=250, height=50,
                           corner_radius=12,
                           command=comando)
            btn.pack(pady=10)
        
        # Frame para el botón volver (centrado abajo)
        frame_volver = ctk.CTkFrame(contenedor_opciones, fg_color="transparent")
        frame_volver.pack(fill="x", padx=10, pady=10)
        
        btn_volver = ctk.CTkButton(frame_volver, text="🔙 Volver",
                              font=("Arial", 12, "bold"),
                              fg_color="#212544",
                              hover_color="#1a1d38",
                              text_color="white",
                              width=550, height=50,
                              corner_radius=12,
                              command=self._mostrar_menu_crud)
        btn_volver.pack()
    
    def _mostrar_mensaje(self, texto):
        """Muestra un mensaje de función en desarrollo"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        msg = tk.Label(self.frame_contenido, text=f"{texto}\n\nFunción en desarrollo",
                      font=("Arial", 16),
                      bg="white")
        msg.pack(pady=50)
        
        btn_volver = ctk.CTkButton(self.frame_contenido, text="🔙 Volver",
                              font=("Arial", 12, "bold"),
                              fg_color="#212544",
                              hover_color="#1a1d38",
                              text_color="white",
                              width=200, height=40,
                              corner_radius=10,
                              command=self._mostrar_menu_crud)
        btn_volver.pack(pady=20)
    
    
    def mostrar_resumen_general(self):
        """Dashboard con estadísticas y calendario de partidos próximos"""
        from src.models.database import Database
        from datetime import datetime
        
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        
        # Título principal
        titulo = tk.Label(self.frame_contenido, text="DASHBOARD",
                         font=("Arial", 24, "bold"),
                         bg="white", fg="#212544")
        titulo.pack(pady=(20, 30))
        
        # Contenedor principal horizontal
        contenedor_principal = tk.Frame(self.frame_contenido, bg="white")
        contenedor_principal.pack(fill="both", expand=True, padx=40, pady=(0, 20))
        
        # === LADO IZQUIERDO: 3 tarjetas azules (cuadradas en fila horizontal) ===
        lado_izquierdo = tk.Frame(contenedor_principal, bg="white")
        lado_izquierdo.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        db = Database()
        color_azul = "#212544"
        
        # Configuración de las 3 tarjetas
        tarjetas_config = [
            ("🏟️", "PARTIDOS", "SELECT COUNT(*) FROM PARTIDOS"),
            ("⚽", "JUGADORES", "SELECT COUNT(*) FROM JUGADORES"),
            ("📊", "CATEGORÍAS", "SELECT COUNT(*) FROM CATEGORIA"),
        ]
        
        # Frame horizontal para los cuadrados
        frame_cuadrados = tk.Frame(lado_izquierdo, bg="white")
        frame_cuadrados.pack(expand=True)
        
        for icono, nombre, query in tarjetas_config:
            # Obtener el contador
            try:
                resultado = db.fetch_all(query)
                total = resultado[0][0] if resultado else 0
            except Exception as e:
                print(f"Error al obtener datos de {nombre}: {e}")
                total = 0
            
            # Crear tarjeta cuadrada azul
            tarjeta = ctk.CTkFrame(frame_cuadrados, fg_color=color_azul, corner_radius=15,
                                  width=180, height=180)
            tarjeta.pack(side="left", padx=10)  # Horizontal con side="left"
            tarjeta.pack_propagate(False)  # Mantener dimensiones fijas
            
            # Contenedor interno centrado
            contenido = tk.Frame(tarjeta, bg=color_azul)
            contenido.place(relx=0.5, rely=0.5, anchor="center")
            
            # Icono
            lbl_icono = tk.Label(contenido, text=icono, font=("Arial", 40),
                               bg=color_azul, fg="white")
            lbl_icono.pack()
            
            # Número
            lbl_numero = tk.Label(contenido, text=str(total), 
                                font=("Arial", 36, "bold"),
                                bg=color_azul, fg="#FFB93B")
            lbl_numero.pack(pady=(5, 0))
            
            # Nombre
            lbl_nombre = tk.Label(contenido, text=nombre, 
                                font=("Arial", 12, "bold"),
                                bg=color_azul, fg="white")
            lbl_nombre.pack(pady=(5, 0))
        
        # === LADO DERECHO: Calendario mensual (gris) ===
        lado_derecho = ctk.CTkFrame(contenedor_principal, fg_color="#E8E8E8", corner_radius=15)
        lado_derecho.pack(side="right", fill="both", expand=True)
        
        # Título del calendario
        from datetime import datetime
        import calendar
        
        mes_actual = datetime.now().month
        año_actual = datetime.now().year
        nombre_mes = calendar.month_name[mes_actual]
        
        titulo_calendario = tk.Label(lado_derecho, text=f"📅 {nombre_mes.upper()} {año_actual}",
                                     font=("Arial", 16, "bold"),
                                     bg="#E8E8E8", fg="#212544")
        titulo_calendario.pack(pady=(20, 15))
        
        # Contenedor del calendario
        contenedor_calendario = tk.Frame(lado_derecho, bg="#E8E8E8")
        contenedor_calendario.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Días de la semana (encabezados)
        dias_semana = ["LUN", "MAR", "MIÉ", "JUE", "VIE", "SÁB", "DOM"]
        frame_headers = tk.Frame(contenedor_calendario, bg="#E8E8E8")
        frame_headers.pack(fill="x", pady=(0, 5))
        
        for dia in dias_semana:
            lbl_dia = tk.Label(frame_headers, text=dia, font=("Arial", 9, "bold"),
                             bg="#E8E8E8", fg="#666666", width=5)
            lbl_dia.pack(side="left", expand=True)
        
        # Obtener días con partidos del mes actual
        dias_con_partidos = set()
        try:
            query_dias = """
                SELECT DISTINCT DAY(Fecha) 
                FROM PARTIDOS 
                WHERE MONTH(Fecha) = %s 
                AND YEAR(Fecha) = %s 
                AND Fecha IS NOT NULL
            """
            result = db.fetch_all(query_dias, (mes_actual, año_actual))
            if result:
                dias_con_partidos = {row[0] for row in result if row[0]}
        except Exception as e:
            print(f"Error al obtener días con partidos: {e}")
        
        # Obtener torneos activos del mes actual (fechas inicio y fin)
        torneos_info = {}  # {dia: [lista de nombres de torneos]}
        try:
            query_torneos = """
                SELECT DAY(Fecha_Inicial) as dia_inicio, DAY(Fecha_Termino) as dia_fin, 
                       Nombre_torneo, Fecha_Inicial, Fecha_Termino
                FROM TORNEO
                WHERE Estado = 'Activo'
                AND ((MONTH(Fecha_Inicial) = %s AND YEAR(Fecha_Inicial) = %s)
                     OR (MONTH(Fecha_Termino) = %s AND YEAR(Fecha_Termino) = %s)
                     OR (Fecha_Inicial \u003c %s AND Fecha_Termino \u003e %s))
            """
            from datetime import date
            primer_dia = date(año_actual, mes_actual, 1)
            import calendar as cal_mod
            ultimo_dia = date(año_actual, mes_actual, cal_mod.monthrange(año_actual, mes_actual)[1])
            
            result_torneos = db.fetch_all(query_torneos, (mes_actual, año_actual, mes_actual, año_actual, ultimo_dia, primer_dia))
            
            if result_torneos:
                for dia_inicio, dia_fin, nombre_torneo, fecha_inicio, fecha_fin in result_torneos:
                    # Marcar día de inicio si es en este mes
                    if fecha_inicio.month == mes_actual and fecha_inicio.year == año_actual:
                        if dia_inicio not in torneos_info:
                            torneos_info[dia_inicio] = []
                        torneos_info[dia_inicio].append(f"Inicio: {nombre_torneo}")
                    
                    # Marcar día de fin si es en este mes
                    if fecha_fin.month == mes_actual and fecha_fin.year == año_actual:
                        if dia_fin not in torneos_info:
                            torneos_info[dia_fin] = []
                        torneos_info[dia_fin].append(f"Fin: {nombre_torneo}")
        except Exception as e:
            print(f"Error al obtener torneos activos: {e}")
        
        # Generar el calendario del mes
        cal = calendar.monthcalendar(año_actual, mes_actual)
        dia_hoy = datetime.now().day
        
        for semana in cal:
            frame_semana = tk.Frame(contenedor_calendario, bg="#E8E8E8")
            frame_semana.pack(fill="x", pady=2)
            
            for dia in semana:
                if dia == 0:
                    # Día vacío (del mes anterior/siguiente)
                    lbl_dia = tk.Label(frame_semana, text="", 
                                     bg="#E8E8E8", width=5, height=2)
                    lbl_dia.pack(side="left", expand=True, padx=1)
                else:
                    # Determinar color del día
                    tiene_torneo = dia in torneos_info
                    tiene_partido = dia in dias_con_partidos
                    
                    if dia == dia_hoy:
                        # Día actual - amarillo
                        bg_color = "#FFB93B"
                        fg_color = "white"
                        fuente = ("Arial", 11, "bold")
                    elif tiene_partido:
                        # Día con partido real - azul
                        bg_color = "#212544"
                        fg_color = "white"
                        fuente = ("Arial", 10, "bold")
                    else:
                        # Día normal
                        bg_color = "white"
                        fg_color = "#212544"
                        fuente = ("Arial", 10)
                    
                    # Frame del día con borde redondeado
                    # Si tiene torneo, agregar borde verde
                    if tiene_torneo:
                        frame_dia = ctk.CTkFrame(frame_semana, fg_color=bg_color, 
                                                corner_radius=8, width=40, height=40,
                                                border_width=3, border_color="#28a745")
                    else:
                        frame_dia = ctk.CTkFrame(frame_semana, fg_color=bg_color, 
                                                corner_radius=8, width=40, height=40)
                    
                    frame_dia.pack(side="left", expand=True, padx=2, pady=2)
                    frame_dia.pack_propagate(False)
                    
                    lbl_numero = tk.Label(frame_dia, text=str(dia), 
                                        font=fuente, bg=bg_color, fg=fg_color)
                    lbl_numero.place(relx=0.5, rely=0.5, anchor="center")
                    
                    # Agregar tooltip si tiene torneo
                    if tiene_torneo:
                        tooltip_text = "\n".join(torneos_info[dia])
                        # Crear tooltip simple con bind
                        def crear_tooltip(widget, texto):
                            def mostrar_tooltip(event):
                                tooltip = tk.Toplevel()
                                tooltip.wm_overrideredirect(True)
                                tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                                label = tk.Label(tooltip, text=texto, background="#FFFACD", 
                                               relief="solid", borderwidth=1, font=("Arial", 9),
                                               padx=5, pady=3)
                                label.pack()
                                widget.tooltip = tooltip
                            
                            def ocultar_tooltip(event):
                                if hasattr(widget, 'tooltip'):
                                    widget.tooltip.destroy()
                                    del widget.tooltip
                            
                            widget.bind('\u003cEnter\u003e', mostrar_tooltip)
                            widget.bind('\u003cLeave\u003e', ocultar_tooltip)
                        
                        crear_tooltip(frame_dia, tooltip_text)
                        crear_tooltip(lbl_numero, tooltip_text)
        
        # Leyenda
        frame_leyenda = tk.Frame(contenedor_calendario, bg="#E8E8E8")
        frame_leyenda.pack(pady=(10, 0))
        
        # Partido programado
        leyenda1 = tk.Frame(frame_leyenda, bg="#E8E8E8")
        leyenda1.pack(side="left", padx=10)
        cuadro1 = ctk.CTkFrame(leyenda1, fg_color="#212544", width=15, height=15, corner_radius=3)
        cuadro1.pack(side="left", padx=(0, 5))
        cuadro1.pack_propagate(False)
        tk.Label(leyenda1, text="Partido", font=("Arial", 8), bg="#E8E8E8", fg="#666666").pack(side="left")
        
        # Hoy
        leyenda2 = tk.Frame(frame_leyenda, bg="#E8E8E8")
        leyenda2.pack(side="left", padx=10)
        cuadro2 = ctk.CTkFrame(leyenda2, fg_color="#FFB93B", width=15, height=15, corner_radius=3)
        cuadro2.pack(side="left", padx=(0, 5))
        cuadro2.pack_propagate(False)
        tk.Label(leyenda2, text="Hoy", font=("Arial", 8), bg="#E8E8E8", fg="#666666").pack(side="left")
        
        # Torneo activo (borde verde)
        leyenda3 = tk.Frame(frame_leyenda, bg="#E8E8E8")
        leyenda3.pack(side="left", padx=10)
        cuadro3 = ctk.CTkFrame(leyenda3, fg_color="white", width=15, height=15, corner_radius=3,
                              border_width=2, border_color="#28a745")
        cuadro3.pack(side="left", padx=(0, 5))
        cuadro3.pack_propagate(False)
        tk.Label(leyenda3, text="Torneo", font=("Arial", 8), bg="#E8E8E8", fg="#666666").pack(side="left")
        
        # Botón volver
        self._agregar_boton_volver(self.mostrar_menu_consultar)
    
    def mostrar_consulta(self, tabla):
        """Muestra la consulta de una tabla específica"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        ConsultaApp(self.frame_contenido, tabla)
        self._agregar_boton_volver(self.mostrar_menu_consultar)
    
    def mostrar_modificar(self, tabla):
        """Muestra la pantalla de modificar para una tabla específica"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        ModificarApp(self.frame_contenido, tabla)
        self._agregar_boton_volver(self.mostrar_menu_modificar)
    
    def mostrar_eliminar(self, tabla):
        """Muestra la pantalla de eliminar para una tabla específica"""
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        EliminarApp(self.frame_contenido, tabla)
        self._agregar_boton_volver(self.mostrar_menu_eliminar)
    
    def mostrar_registro_partidos(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_partido(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_horarios(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_horarios(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_entrenamientos(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_entrenamiento(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_equipos(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_equipos(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_jugador(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_jugador(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_torneo(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_torneo(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_profesor(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_profesor(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def mostrar_registro_usuario(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
        RegistroApp_usuario(self.frame_contenido, on_success=self.mostrar_menu_registrar)
        self._agregar_boton_volver(self.mostrar_menu_registrar)
    
    def _agregar_boton_volver(self, volver_callback=None):
        """Agrega botón volver al menú"""
        if volver_callback is None:
            volver_callback = self._mostrar_menu_crud
        
        frame_btn = tk.Frame(self.frame_contenido, bg="white")
        frame_btn.pack(side="bottom", pady=20)
        
        btn = ctk.CTkButton(frame_btn, text="🔙 Volver",
                       font=("Arial", 12, "bold"),
                       fg_color="#212544",
                       hover_color="#1a1d38",
                       text_color="white",
                       width=200, height=50,
                       corner_radius=12,
                       command=volver_callback)
        btn.pack()
    
    def cerrar_sesion(self):
        """Cierra sesión y regresa al login"""
        self.usuario_actual = None
        self.plantilla = None
        self.root.quit()
        self.mostrar_login()

def main():
    sistema = SistemaCompleto()
    sistema.iniciar()

if __name__ == "__main__":
    main()