# eliminar_view.py
from src.components.cont_r import ContR
from src.components.panel_r import PanelR
from tkinter import ttk, messagebox
import tkinter as tk
import customtkinter as ctk
from src.models.database import Database

class EliminarApp:
    def __init__(self, parent_frame, tabla):
        self.frame = parent_frame
        self.tabla = tabla
        self.db = Database()
        self.registro_actual = None
        
        # Frame principal
        self.cont_m = ContR(self.frame, n_rad=20, h=500, w=200, color="#F8F9FA", command=None)
        self.cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.5)
        
        # Header
        header_frame = tk.Frame(self.cont_m, bg="#212544", height=40)
        header_frame.place(relx=0.5, rely=0.04, anchor=tk.CENTER, relwidth=1.0)
        header_frame.pack_propagate(False)
        
        # Título con icono
        titulo_frame = tk.Frame(header_frame, bg="#212544")
        titulo_frame.pack(expand=True)
        
        iconos = {
            "JUGADORES": "⚽", "TORNEO": "🏆", "PARTIDOS": "🤝", 
            "HORARIO": "⏰", "CATEGORIA": "📊", "ENTRENAMIENTO": "🏃",
            "PROFESORES": "👨‍🏫", "USUARIOS": "👥"
        }
        icono = iconos.get(tabla, "🗑️")
        
        tk.Label(titulo_frame, text=icono, font=("Arial", 18),
                bg="#212544", fg="#FFB93B").pack(side="left", padx=(0, 6))
        
        titulo_lb = tk.Label(titulo_frame, text=f"ELIMINAR {tabla}",
                           font=("Arial", 14, "bold"), fg="#FCFCFC", bg="#212544")
        titulo_lb.pack(side="left")
        
        # Frame para contenido
        cont_p = ContR(self.cont_m, n_rad=15, h=420, w=180, color="#FFFFFF", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.55)
        
        # Crear interfaz según la tabla
        if tabla == "JUGADORES":
            self.crear_interfaz_jugadores(cont_p)
        elif tabla == "TORNEO":
            self.crear_interfaz_torneos(cont_p)
        elif tabla == "PARTIDOS":
            self.crear_interfaz_partidos(cont_p)
        elif tabla == "HORARIO":
            self.crear_interfaz_horarios(cont_p)
        elif tabla == "CATEGORIA":
            self.crear_interfaz_categorias(cont_p)
        elif tabla == "ENTRENAMIENTO":
            self.crear_interfaz_entrenamientos(cont_p)
        elif tabla == "PROFESORES":
            self.crear_interfaz_profesores(cont_p)
        elif tabla == "USUARIOS":
            self.crear_interfaz_usuarios(cont_p)
        
        # Cargar datos iniciales
        self.cargar_registros()
    
    def crear_interfaz_jugadores(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Jugador:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_jugadores = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10,
            border_width=2,
            border_color="#D9D9D9",
            button_color="#212544",
            button_hover_color="#FFB93B",
            fg_color="#FFFFFF",
            text_color="#000000",
            font=("Arial", 11),
            width=300
        )
        self.combo_jugadores.pack(side="left", fill="x", expand=True)
        self.combo_jugadores.configure(command=self.mostrar_datos_jugador)
        
        # Frame para mostrar datos
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        # Etiquetas para mostrar datos
        self.labels = {}
        campos = [
            ("Nombre:", "label_nombre", 0.1),
            ("Apellidos:", "label_apellidos", 0.2),
            ("CURP:", "label_curp", 0.3),
            ("Categoría:", "label_categoria", 0.4),
            ("Número:", "label_numero", 0.5),
            ("Inscripción:", "label_inscripcion", 0.6)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        # Botones
        self.crear_botones_accion(parent, self.eliminar_jugador, 0.8)
    
    def crear_interfaz_torneos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Torneo:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_torneos = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_torneos.pack(side="left", fill="x", expand=True)
        self.combo_torneos.configure(command=self.mostrar_datos_torneo)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        self.labels = {}
        campos = [
            ("Nombre Torneo:", "label_nombre", 0.1),
            ("Categoría:", "label_categoria", 0.2),
            ("Cantidad Equipos:", "label_equipos", 0.3),
            ("Duración:", "label_duracion", 0.4),
            ("Fecha Inicio:", "label_inicio", 0.5),
            ("Fecha Fin:", "label_fin", 0.6)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_torneo, 0.8)
    
    def crear_interfaz_partidos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Partido:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_partidos = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_partidos.pack(side="left", fill="x", expand=True)
        self.combo_partidos.configure(command=self.mostrar_datos_partido)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        self.labels = {}
        campos = [
            ("Día:", "label_dia", 0.1),
            ("Hora:", "label_hora", 0.2),
            ("Equipo Local:", "label_local", 0.3),
            ("Equipo Visitante:", "label_visitante", 0.4),
            ("Profesor:", "label_profesor", 0.5),
            ("Lugar:", "label_lugar", 0.6),
            ("Categoría:", "label_categoria", 0.7),
            ("Tipo:", "label_tipo", 0.8)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_partido, 0.70)
    
    def crear_interfaz_horarios(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Horario:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_horarios = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_horarios.pack(side="left", fill="x", expand=True)
        self.combo_horarios.configure(command=self.mostrar_datos_horario)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        self.labels = {}
        campos = [
            ("Ocupación:", "label_ocupacion", 0.2),
            ("Hora:", "label_hora", 0.3),
            ("Día:", "label_dia", 0.4),
            ("Disponibilidad:", "label_disponibilidad", 0.5)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_horario, 0.75)
    
    def crear_interfaz_categorias(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Categoría:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_categorias = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_categorias.pack(side="left", fill="x", expand=True)
        self.combo_categorias.configure(command=self.mostrar_datos_categoria)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.2)
        
        self.labels = {}
        lbl_titulo = tk.Label(frame_datos, text="Nombre Categoría:", font=("Arial", 9, "bold"),
                            bg="#FFFFFF", fg="#333", anchor="w")
        lbl_titulo.place(relx=0.05, rely=0.3, relwidth=0.4)
        
        self.labels["label_nombre"] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                             bg="#FFFFFF", fg="#000", anchor="w")
        self.labels["label_nombre"].place(relx=0.45, rely=0.3, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_categoria, 0.65)
    
    def crear_interfaz_entrenamientos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Entrenamiento:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_entrenamientos = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_entrenamientos.pack(side="left", fill="x", expand=True)
        self.combo_entrenamientos.configure(command=self.mostrar_datos_entrenamiento)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        self.labels = {}
        campos = [
            ("Día:", "label_dia", 0.2),
            ("Hora:", "label_hora", 0.3),
            ("Profesor:", "label_profesor", 0.4),
            ("Categoría:", "label_categoria", 0.5)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_entrenamiento, 0.75)
    
    def crear_interfaz_profesores(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Profesor:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_profesores = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_profesores.pack(side="left", fill="x", expand=True)
        self.combo_profesores.configure(command=self.mostrar_datos_profesor)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.3)
        
        self.labels = {}
        campos = [
            ("Nombre:", "label_nombre", 0.2),
            ("Apellidos:", "label_apellidos", 0.4),
            ("Categoría:", "label_categoria", 0.6)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_profesor, 0.7)
    
    def crear_interfaz_usuarios(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Seleccionar Usuario:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_usuarios = ctk.CTkComboBox(
            frame_buscar, state="readonly",
            corner_radius=10, border_width=2, border_color="#D9D9D9",
            button_color="#212544", button_hover_color="#FFB93B",
            fg_color="#FFFFFF", text_color="#000000",
            font=("Arial", 11), width=300
        )
        self.combo_usuarios.pack(side="left", fill="x", expand=True)
        self.combo_usuarios.configure(command=self.mostrar_datos_usuario)
        
        frame_datos = tk.Frame(parent, bg="#FFFFFF")
        frame_datos.place(relx=0.5, rely=0.35, anchor=tk.CENTER, relwidth=0.9, relheight=0.3)
        
        self.labels = {}
        campos = [
            ("Usuario:", "label_usuario", 0.2),
            ("Email:", "label_email", 0.4),
            ("Password:", "label_password", 0.6)
        ]
        
        for texto, nombre, rely in campos:
            lbl_titulo = tk.Label(frame_datos, text=texto, font=("Arial", 9, "bold"),
                                bg="#FFFFFF", fg="#333", anchor="w")
            lbl_titulo.place(relx=0.05, rely=rely, relwidth=0.4)
            
            self.labels[nombre] = tk.Label(frame_datos, text="", font=("Arial", 9),
                                         bg="#FFFFFF", fg="#000", anchor="w")
            self.labels[nombre].place(relx=0.45, rely=rely, relwidth=0.5)
        
        self.crear_botones_accion(parent, self.eliminar_usuario, 0.7)
    
    def crear_botones_accion(self, parent, comando_eliminar, rely):
        """Crea los botones de Eliminar y Limpiar con CustomTkinter"""
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=rely, anchor=tk.CENTER, relwidth=0.9)
        
        btn_eliminar = ctk.CTkButton(
            frame_botones, text="🗑️ Eliminar",
            fg_color="#dc3545",
            hover_color="#c82333",
            text_color="white",
            corner_radius=10,
            font=("Arial", 10, "bold"),
            command=comando_eliminar
        )
        btn_eliminar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(
            frame_botones, text="🔄 Limpiar",
            fg_color="#6c757d",
            hover_color="#5a6268",
            text_color="white",
            corner_radius=10,
            font=("Arial", 10, "bold"),
            command=self.limpiar_datos
        )
        btn_limpiar.pack(side="left", padx=5)
    
    def cargar_registros(self):
        try:
            if self.tabla == "JUGADORES":
                query = """
                SELECT j.ID_jugador, j.Nombre, j.Apellidos, c.Nombre, j.Numero_jugador
                FROM JUGADORES j
                LEFT JOIN CATEGORIA c ON j.Categoria = c.ID_Categoria
                ORDER BY j.Nombre
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_jugadores'):
                    self.combo_jugadores.configure(values=[f"{row[0]} | {row[1]} | {row[2]} | {row[3] or 'Sin categoría'} | #{row[4]}" for row in datos])
            
            elif self.tabla == "TORNEO":
                query = """
                SELECT t.Id_Torneo, t.Nombre_torneo, c.Nombre, t.Cantidad_Equipos, t.Duracion
                FROM TORNEO t
                LEFT JOIN CATEGORIA c ON t.Categoria = c.ID_Categoria
                ORDER BY t.Nombre_torneo
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_torneos'):
                    self.combo_torneos.configure(values=[f"{row[0]} | {row[1]} | {row[2] or 'Sin categoría'} | {row[3]} equipos | {row[4]}" for row in datos])
            
            elif self.tabla == "PARTIDOS":
                query = """
                SELECT p.Id_Partidos, p.Equipo_Local, p.Equipo_Visitante, p.Dia, p.Hora, c.Nombre
                FROM PARTIDOS p
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria
                ORDER BY p.Dia, p.Hora
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_partidos'):
                    self.combo_partidos.configure(values=[f"{row[0]} | {row[1]} vs {row[2]} | {row[3]} {str(row[4])[:5]} | {row[5] or 'Sin categoría'}" for row in datos])
            
            elif self.tabla == "HORARIO":
                query = """
                SELECT ID_Horario, Dia, Hora, Ocupacion, Disponibilidad
                FROM HORARIO
                ORDER BY FIELD(Dia, 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'), Hora
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_horarios'):
                    disponibilidad_text = lambda d: "Disponible" if d == 1 else "Ocupado"
                    self.combo_horarios.configure(values=[f"{row[0]} | {row[1]} | {str(row[2])[:5]} | {row[3]} | {disponibilidad_text(row[4])}" for row in datos])
            
            elif self.tabla == "CATEGORIA":
                query = "SELECT ID_Categoria, Nombre FROM CATEGORIA ORDER BY Nombre"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_categorias'):
                    self.combo_categorias.configure(values=[f"{row[0]} | {row[1]}" for row in datos])
            
            elif self.tabla == "ENTRENAMIENTO":
                query = """
                SELECT e.Id_Entrenamiento, e.Dia, e.Hora, CONCAT(p.Nombre, ' ', p.Apellidos), c.Nombre
                FROM ENTRENAMIENTO e
                LEFT JOIN PROFESORES p ON e.Profesor = p.Id_Profesores
                LEFT JOIN CATEGORIA c ON e.Categoria = c.ID_Categoria
                ORDER BY FIELD(e.Dia, 'Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo'), e.Hora
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_entrenamientos'):
                    self.combo_entrenamientos.configure(values=[f"{row[0]} | {row[1]} | {str(row[2])[:5]} | {row[3] or 'Sin profesor'} | {row[4] or 'Sin categoría'}" for row in datos])
            
            elif self.tabla == "PROFESORES":
                query = """
                SELECT p.Id_Profesores, p.Nombre, p.Apellidos, c.Nombre
                FROM PROFESORES p
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria
                ORDER BY p.Nombre
                """
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_profesores'):
                    self.combo_profesores.configure(values=[f"{row[0]} | {row[1]} | {row[2]} | {row[3] or 'Sin categoría'}" for row in datos])
            
            elif self.tabla == "USUARIOS":
                query = "SELECT id, usuario, email FROM USUARIOS ORDER BY usuario"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_usuarios'):
                    self.combo_usuarios.configure(values=[f"{row[0]} | {row[1]} | {row[2]}" for row in datos])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    def mostrar_datos_jugador(self, event):
        try:
            seleccion = self.combo_jugadores.get()
            if seleccion:
                id_jugador = seleccion.split(" | ")[0]
                query = """
                SELECT j.ID_jugador, j.Nombre, j.Apellidos, j.CURP, c.Nombre, 
                       j.Numero_jugador, j.Inscripcion 
                FROM JUGADORES j 
                LEFT JOIN CATEGORIA c ON j.Categoria = c.ID_Categoria 
                WHERE j.ID_jugador = %s
                """
                datos = self.db.fetch_all(query, (id_jugador,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_nombre'].config(text=datos[0][1])
                    self.labels['label_apellidos'].config(text=datos[0][2])
                    self.labels['label_curp'].config(text=datos[0][3])
                    self.labels['label_categoria'].config(text=datos[0][4])
                    self.labels['label_numero'].config(text=str(datos[0][5]))
                    self.labels['label_inscripcion'].config(text=str(datos[0][6]))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_torneo(self, event):
        try:
            seleccion = self.combo_torneos.get()
            if seleccion:
                id_torneo = seleccion.split(" | ")[0]
                query = """
                SELECT t.Id_Torneo, t.Nombre_torneo, c.Nombre, 
                       t.Cantidad_Equipos, t.Duracion, t.Fecha_Inicial, t.Fecha_Termino 
                FROM TORNEO t 
                LEFT JOIN CATEGORIA c ON t.Categoria = c.ID_Categoria 
                WHERE t.Id_Torneo = %s
                """
                datos = self.db.fetch_all(query, (id_torneo,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_nombre'].config(text=datos[0][1])
                    self.labels['label_categoria'].config(text=datos[0][2])
                    self.labels['label_equipos'].config(text=str(datos[0][3]))
                    self.labels['label_duracion'].config(text=datos[0][4])
                    self.labels['label_inicio'].config(text=str(datos[0][5]))
                    self.labels['label_fin'].config(text=str(datos[0][6]))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_partido(self, event):
        try:
            seleccion = self.combo_partidos.get()
            if seleccion:
                id_partido = seleccion.split(" | ")[0]
                query = """
                SELECT p.Id_Partidos, p.Dia, p.Hora, p.Equipo_Local, p.Equipo_Visitante, 
                       CONCAT(pr.Nombre, ' ', pr.Apellidos), p.Lugar, c.Nombre, p.Tipo 
                FROM PARTIDOS p 
                LEFT JOIN PROFESORES pr ON p.Profesor = pr.Id_Profesores 
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria 
                WHERE p.Id_Partidos = %s
                """
                datos = self.db.fetch_all(query, (id_partido,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_dia'].config(text=datos[0][1])
                    self.labels['label_hora'].config(text=datos[0][2])
                    self.labels['label_local'].config(text=datos[0][3])
                    self.labels['label_visitante'].config(text=datos[0][4])
                    self.labels['label_profesor'].config(text=datos[0][5])
                    self.labels['label_lugar'].config(text=datos[0][6])
                    self.labels['label_categoria'].config(text=datos[0][7])
                    self.labels['label_tipo'].config(text=datos[0][8])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_horario(self, event):
        try:
            seleccion = self.combo_horarios.get()
            if seleccion:
                id_horario = seleccion.split(" | ")[0]
                query = "SELECT ID_Horario, Ocupacion, Hora, Dia, Disponibilidad FROM HORARIO WHERE ID_Horario = %s"
                datos = self.db.fetch_all(query, (id_horario,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_ocupacion'].config(text=datos[0][1])
                    self.labels['label_hora'].config(text=datos[0][2])
                    self.labels['label_dia'].config(text=datos[0][3])
                    disponibilidad = "✅ Disponible" if datos[0][4] == 1 else "❌ Ocupado"
                    self.labels['label_disponibilidad'].config(text=disponibilidad)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_categoria(self, event):
        try:
            seleccion = self.combo_categorias.get()
            if seleccion:
                id_categoria = seleccion.split(" | ")[0]
                query = "SELECT ID_Categoria, Nombre FROM CATEGORIA WHERE ID_Categoria = %s"
                datos = self.db.fetch_all(query, (id_categoria,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_nombre'].config(text=datos[0][1])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_entrenamiento(self, event):
        try:
            seleccion = self.combo_entrenamientos.get()
            if seleccion:
                id_entrenamiento = seleccion.split(" | ")[0]
                query = """
                SELECT e.Id_Entrenamiento, e.Dia, e.Hora, 
                       CONCAT(p.Nombre, ' ', p.Apellidos), c.Nombre 
                FROM ENTRENAMIENTO e 
                LEFT JOIN PROFESORES p ON e.Profesor = p.Id_Profesores 
                LEFT JOIN CATEGORIA c ON e.Categoria = c.ID_Categoria 
                WHERE e.Id_Entrenamiento = %s
                """
                datos = self.db.fetch_all(query, (id_entrenamiento,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_dia'].config(text=datos[0][1])
                    self.labels['label_hora'].config(text=datos[0][2])
                    self.labels['label_profesor'].config(text=datos[0][3])
                    self.labels['label_categoria'].config(text=datos[0][4])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_profesor(self, event):
        try:
            seleccion = self.combo_profesores.get()
            if seleccion:
                id_profesor = seleccion.split(" | ")[0]
                query = """
                SELECT p.Id_Profesores, p.Nombre, p.Apellidos, c.Nombre 
                FROM PROFESORES p 
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria 
                WHERE p.Id_Profesores = %s
                """
                datos = self.db.fetch_all(query, (id_profesor,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_nombre'].config(text=datos[0][1])
                    self.labels['label_apellidos'].config(text=datos[0][2])
                    self.labels['label_categoria'].config(text=datos[0][3])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def mostrar_datos_usuario(self, event):
        try:
            seleccion = self.combo_usuarios.get()
            if seleccion:
                id_usuario = seleccion.split(" | ")[0]
                query = "SELECT id, usuario, email, password FROM USUARIOS WHERE id = %s"
                datos = self.db.fetch_all(query, (id_usuario,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.labels['label_usuario'].config(text=datos[0][1])
                    self.labels['label_email'].config(text=datos[0][2])
                    self.labels['label_password'].config(text="*" * len(datos[0][3]))
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def eliminar_jugador(self):
        self._eliminar_registro("JUGADORES", "ID_jugador", "jugador")
    
    def eliminar_torneo(self):
        self._eliminar_registro("TORNEO", "Id_Torneo", "torneo")
    
    def eliminar_partido(self):
        self._eliminar_registro("PARTIDOS", "Id_Partidos", "partido")
    
    def eliminar_horario(self):
        self._eliminar_registro("HORARIO", "ID_Horario", "horario")
    
    def eliminar_categoria(self):
        self._eliminar_registro("CATEGORIA", "ID_Categoria", "categoría")
    
    def eliminar_entrenamiento(self):
        self._eliminar_registro("ENTRENAMIENTO", "Id_Entrenamiento", "entrenamiento")
    
    def eliminar_profesor(self):
        self._eliminar_registro("PROFESORES", "Id_Profesores", "profesor")
    
    def eliminar_usuario(self):
        self._eliminar_registro("USUARIOS", "id", "usuario")
    
    def _eliminar_registro(self, tabla, campo_id, nombre_entidad):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", f"Selecciona un {nombre_entidad} para eliminar")
                return
            
            # Confirmación de eliminación
            respuesta = messagebox.askyesno(
                "Confirmar Eliminación",
                f"¿Estás seguro de que deseas eliminar este {nombre_entidad}?\n\n"
                f"Esta acción no se puede deshacer.",
                icon='warning'
            )
            
            if respuesta:
                query = f"DELETE FROM {tabla} WHERE {campo_id} = %s"
                if self.db.execute_query(query, (self.registro_actual[0],)):
                    messagebox.showinfo("Éxito", f"{nombre_entidad.capitalize()} eliminado correctamente")
                    self.cargar_registros()
                    self.limpiar_datos()
                else:
                    messagebox.showerror("Error", f"Error al eliminar el {nombre_entidad}")
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar {nombre_entidad}: {str(e)}")
    
    def limpiar_datos(self):
        self.registro_actual = None
        for label in self.labels.values():
            label.config(text="")
        
        # Limpiar combos de búsqueda
        if hasattr(self, 'combo_jugadores'):
            self.combo_jugadores.set('')
        if hasattr(self, 'combo_torneos'):
            self.combo_torneos.set('')
        if hasattr(self, 'combo_partidos'):
            self.combo_partidos.set('')
        if hasattr(self, 'combo_horarios'):
            self.combo_horarios.set('')
        if hasattr(self, 'combo_categorias'):
            self.combo_categorias.set('')
        if hasattr(self, 'combo_entrenamientos'):
            self.combo_entrenamientos.set('')
        if hasattr(self, 'combo_profesores'):
            self.combo_profesores.set('')
        if hasattr(self, 'combo_usuarios'):
            self.combo_usuarios.set('')