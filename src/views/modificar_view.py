from src.components.cont_r import ContR
from src.components.panel_r import PanelR
from tkinter import messagebox
import tkinter as tk
import customtkinter as ctk
from src.models.database import Database
from tkcalendar import DateEntry

class ModificarApp:
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
        icono = iconos.get(tabla, "✏️")
        
        tk.Label(titulo_frame, text=icono, font=("Arial", 18),
                bg="#212544", fg="#FFB93B").pack(side="left", padx=(0, 6))
        
        titulo_lb = tk.Label(titulo_frame, text=f"MODIFICAR {tabla}",
                           font=("Arial", 14, "bold"), fg="#FCFCFC", bg="#212544")
        titulo_lb.pack(side="left")
        
        # Frame para contenido
        cont_p = ContR(self.cont_m, n_rad=15, h=420, w=180, color="#FFFFFF", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.55)
        
        # Crear interfaz según la tabla
        if tabla == "JUGADORES":
            self.crear_formulario_jugadores(cont_p)
        elif tabla == "TORNEO":
            self.crear_formulario_torneos(cont_p)
        elif tabla == "PARTIDOS":
            self.crear_formulario_partidos(cont_p)
        elif tabla == "HORARIO":
            self.crear_formulario_horarios(cont_p)
        elif tabla == "CATEGORIA":
            self.crear_formulario_categorias(cont_p)
        elif tabla == "ENTRENAMIENTO":
            self.crear_formulario_entrenamientos(cont_p)
        elif tabla == "PROFESORES":
            self.crear_formulario_profesores(cont_p)
        elif tabla == "USUARIOS":
            self.crear_formulario_usuarios(cont_p)
        
        # Cargar datos iniciales
        self.cargar_registros()
    
    def crear_formulario_horarios(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Horario:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_horarios = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_horarios.pack(side="left", fill="x", expand=True)
        self.combo_horarios.set("Elige horario")
        self.combo_horarios.configure(command=lambda choice: self.cargar_datos_horario(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.5)
        
        campos = [
            ("Ocupación:", "combo_ocupacion", 0.1),
            ("Hora:", "combo_hora", 0.3),
            ("Día:", "combo_dia", 0.5),
            ("Disponibilidad:", "combo_disponibilidad", 0.7)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            if nombre == "combo_ocupacion":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["Entrenamiento", "Partido", "Torneo", "Reunion"])
            elif nombre == "combo_hora":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=[f"{h:02d}:00" for h in range(7, 22)])
            elif nombre == "combo_dia":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
            elif nombre == "combo_disponibilidad":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["Disponible", "Ocupado"])
            else:
                widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_horario)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)

    def crear_formulario_entrenamientos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Entrenamiento:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_entrenamientos = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_entrenamientos.pack(side="left", fill="x", expand=True)
        self.combo_entrenamientos.set("Elige entrenamiento")
        self.combo_entrenamientos.configure(command=lambda choice: self.cargar_datos_entrenamiento(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.5)
        
        campos = [
            ("Día:", "combo_dia", 0.1),
            ("Hora:", "combo_hora", 0.3),
            ("Profesor:", "combo_profesor", 0.5),
            ("Categoría:", "combo_categoria", 0.7)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            if nombre == "combo_dia":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
            elif nombre == "combo_hora":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=[f"{h:02d}:00" for h in range(7, 22)])
            elif nombre == "combo_profesor":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
            elif nombre == "combo_categoria":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
            else:
                widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        
        # Cargar datos en comboboxes
        self.cargar_profesores()
        self.cargar_categorias()
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_entrenamiento)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_jugadores(self, parent):
        # Frame para buscar
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Jugador:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_jugadores = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_jugadores.pack(side="left", fill="x", expand=True)
        self.combo_jugadores.set("Elige jugador")
        self.combo_jugadores.configure(command=lambda choice: self.cargar_datos_jugador(None))
        
        # Frame para formulario
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.4, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        # Campos del formulario
        campos = [
            ("Nombre:", "entry_nombre", 0.1),
            ("Apellidos:", "entry_apellidos", 0.2),
            ("CURP:", "entry_curp", 0.3),
            ("Categoría:", "combo_categoria", 0.4),
            ("Número:", "spin_numero", 0.5),
            ("Inscripción:", "date_inscripcion", 0.6)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            if nombre == "combo_categoria":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
            elif nombre == "spin_numero":
                widget = ctk.CTkEntry(frame_form, width=18*8, corner_radius=8, border_width=2, height=35, placeholder_text="1-99")
            elif nombre == "date_inscripcion":
                widget = DateEntry(frame_form, width=18, selectmode='day', locale='es_ES', date_pattern='dd/mm/yyyy', showweeknumbers=False, state='normal')
            else:
                widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        
        # Cargar datos en comboboxes
        self.cargar_categorias()
        # Botones
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_jugador)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_torneos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Torneo:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_torneos = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_torneos.pack(side="left", fill="x", expand=True)
        self.combo_torneos.set("Elige torneo")
        self.combo_torneos.configure(command=lambda choice: self.cargar_datos_torneo(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.6)
        
        campos = [
            ("Nombre Torneo:", "entry_nombre", 0.1),
            ("Categoría:", "combo_categoria", 0.17),
            ("Cantidad Equipos:", "spin_equipos", 0.24),
            ("Duración:", "combo_duracion", 0.31),
            ("Fecha Inicio:", "date_inicio", 0.38),
            ("Fecha Fin:", "date_fin", 0.45),
            ("Estado:", "combo_estado", 0.52),
            ("Equipo Ganador:", "entry_ganador", 0.59)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            if nombre == "combo_categoria":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
            elif nombre == "spin_equipos":
                widget = ctk.CTkEntry(frame_form, width=18*8, corner_radius=8, border_width=2, height=35, placeholder_text="1-20")
            elif nombre == "combo_duracion":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["1 semana", "2 semanas", "1 mes", "2 meses", "3 meses"])
            elif nombre == "combo_estado":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500", values=["Activo", "Inactivo"])
            elif "date" in nombre:
                widget = DateEntry(frame_form, width=18, selectmode='day', locale='es_ES', date_pattern='dd/mm/yyyy', showweeknumbers=False, state='normal')
            else:
                widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        
        # Cargar datos en comboboxes
        self.cargar_categorias()
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_torneo)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_partidos(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Partido:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_partidos = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_partidos.pack(side="left", fill="x", expand=True)
        self.combo_partidos.set("Elige partido")
        self.combo_partidos.configure(command=lambda choice: self.cargar_datos_partido(None))
        
        # Frame scrollable para el formulario - ajustado para no sobreponerse con botones
        scrollable_frame = ctk.CTkScrollableFrame(parent, fg_color="#FFFFFF", corner_radius=10)
        scrollable_frame.place(relx=0.5, rely=0.42, anchor=tk.CENTER, relwidth=0.9, relheight=0.48)
        
        campos = [
            ("Día:", "combo_dia"),
            ("Hora:", "combo_hora"),
            ("Equipo Local:", "entry_local"),
            ("Equipo Visitante:", "entry_visitante"),
            ("Goles Local:", "entry_goles_local"),
            ("Goles Visitante:", "entry_goles_visitante"),
            ("Profesor:", "combo_profesor"),
            ("Lugar:", "entry_lugar"),
            ("Categoría:", "combo_categoria"),
            ("Tipo:", "combo_tipo"),
            ("Torneo:", "combo_torneo"),
            ("Ganador:", "combo_ganador")
        ]
        
        self.campos = {}
        for idx, (texto, nombre) in enumerate(campos):
            # Label
            lbl = tk.Label(scrollable_frame, text=texto, font=("Arial", 10, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.grid(row=idx, column=0, sticky="w", padx=(10, 5), pady=8)
            
            # Widget
            if "combo" in nombre:
                if nombre == "combo_dia":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500", 
                                            values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"])
                elif nombre == "combo_hora":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500", 
                                            values=[f"{h:02d}:00" for h in range(7, 22)])
                elif nombre == "combo_profesor":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500")
                elif nombre == "combo_categoria":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500")
                elif nombre == "combo_tipo":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500", 
                                            values=["Amistoso", "Torneo", "Liga", "Eliminatorio"],
                                            command=self.toggle_campo_torneo)
                elif nombre == "combo_torneo":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500")
                elif nombre == "combo_ganador":
                    widget = ctk.CTkComboBox(scrollable_frame, width=300, corner_radius=8, border_width=2, 
                                            button_color="#FFB93B", button_hover_color="#FFA500", 
                                            values=["Sin resultado", "Empate"])
            else:
                # Campos de entrada - placeholder especial para goles
                if "goles" in nombre:
                    widget = ctk.CTkEntry(scrollable_frame, width=300, corner_radius=8, border_width=2, height=35,
                                        placeholder_text="0-99")
                else:
                    widget = ctk.CTkEntry(scrollable_frame, width=300, corner_radius=8, border_width=2, height=35)
            
            widget.grid(row=idx, column=1, sticky="ew", padx=(5, 10), pady=8)
            self.campos[nombre] = widget
        
        # Configurar grid
        scrollable_frame.grid_columnconfigure(1, weight=1)
        
        
        # Cargar datos en comboboxes
        self.cargar_profesores()
        self.cargar_categorias()
        self.cargar_torneos()
        
        # Function to update ganador options
        def actualizar_opciones_ganador(*args):
            local = self.campos['entry_local'].get()
            visitante = self.campos['entry_visitante'].get()
            opciones = ["Sin resultado", "Empate"]
            if local:
                opciones.append(local)
            if visitante:
                opciones.append(visitante)
            self.campos['combo_ganador'].configure(values=opciones)
        
        # Bind to team fields
        self.campos['entry_local'].bind('<KeyRelease>', actualizar_opciones_ganador)
        self.campos['entry_visitante'].bind('<KeyRelease>', actualizar_opciones_ganador)
        
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_partido)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_categorias(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Categoría:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_categorias = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_categorias.pack(side="left", fill="x", expand=True)
        self.combo_categorias.set("Elige categoría")
        self.combo_categorias.configure(command=lambda choice: self.cargar_datos_categoria(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.3)
        
        lbl = tk.Label(frame_form, text="Nombre Categoría:", font=("Arial", 9, "bold"),
                      bg="#FFFFFF", fg="#333", anchor="w")
        lbl.place(relx=0.05, rely=0.3, relwidth=0.4)
        
        self.campos = {}
        self.campos["entry_nombre"] = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
        self.campos["entry_nombre"].place(relx=0.45, rely=0.3, relwidth=0.5)
        
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_categoria)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_profesores(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Profesor:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_profesores = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_profesores.pack(side="left", fill="x", expand=True)
        self.combo_profesores.set("Elige profesor")
        self.combo_profesores.configure(command=lambda choice: self.cargar_datos_profesor(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        campos = [
            ("Nombre:", "entry_nombre", 0.2),
            ("Apellidos:", "entry_apellidos", 0.4),
            ("Categoría:", "combo_categoria", 0.6)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            if nombre == "combo_categoria":
                widget = ctk.CTkComboBox(frame_form, width=20*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
            else:
                widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        
        # Cargar datos en comboboxes
        self.cargar_categorias()
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_profesor)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def crear_formulario_usuarios(self, parent):
        frame_buscar = tk.Frame(parent, bg="#FFFFFF")
        frame_buscar.place(relx=0.5, rely=0.08, anchor=tk.CENTER, relwidth=0.9)
        
        tk.Label(frame_buscar, text="🔍 Buscar Usuario:", font=("Arial", 10, "bold"),
                bg="#FFFFFF", fg="#333").pack(side="left", padx=(0, 8))
        
        self.combo_usuarios = ctk.CTkComboBox(frame_buscar, width=25*8, corner_radius=8, border_width=2, button_color="#FFB93B", button_hover_color="#FFA500")
        self.combo_usuarios.pack(side="left", fill="x", expand=True)
        self.combo_usuarios.set("Elige usuario")
        self.combo_usuarios.configure(command=lambda choice: self.cargar_datos_usuario(None))
        
        frame_form = tk.Frame(parent, bg="#FFFFFF")
        frame_form.place(relx=0.5, rely=0.45, anchor=tk.CENTER, relwidth=0.9, relheight=0.4)
        
        campos = [
            ("Usuario:", "entry_usuario", 0.2),
            ("Email:", "entry_email", 0.4),
            ("Password:", "entry_password", 0.6)
        ]
        
        self.campos = {}
        for texto, nombre, rely in campos:
            lbl = tk.Label(frame_form, text=texto, font=("Arial", 9, "bold"),
                          bg="#FFFFFF", fg="#333", anchor="w")
            lbl.place(relx=0.05, rely=rely, relwidth=0.4)
            
            widget = ctk.CTkEntry(frame_form, width=22*8, corner_radius=8, border_width=2, height=35)
            if nombre == "entry_password":
                widget.configure(show="*")
            
            widget.place(relx=0.45, rely=rely, relwidth=0.5)
            self.campos[nombre] = widget
        
        
        # Cargar datos en comboboxes
        self.cargar_categorias()
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.70, anchor=tk.CENTER, relwidth=0.9)
        
        btn_actualizar = ctk.CTkButton(frame_botones, text="💾 Actualizar", font=("Arial", 10, "bold"), fg_color="#28a745", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.actualizar_usuario)
        btn_actualizar.pack(side="left", padx=5)
        
        btn_limpiar = ctk.CTkButton(frame_botones, text="🔄 Limpiar", font=("Arial", 10, "bold"), fg_color="#6c757d", text_color="white", corner_radius=8, height=35, cursor="hand2", command=self.limpiar_formulario)
        btn_limpiar.pack(side="left", padx=5)
    
    def cargar_registros(self):
        try:
            if self.tabla == "JUGADORES":
                query = "SELECT ID_jugador, CONCAT(Nombre, ' ', Apellidos) FROM JUGADORES ORDER BY Nombre"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_jugadores'):
                    self.combo_jugadores.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "TORNEO":
                query = "SELECT Id_Torneo, Nombre_torneo FROM TORNEO ORDER BY Nombre_torneo"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_torneos'):
                    self.combo_torneos.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "PARTIDOS":
                query = "SELECT Id_Partidos, CONCAT(Equipo_Local, ' vs ', Equipo_Visitante) FROM PARTIDOS ORDER BY Dia"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_partidos'):
                    self.combo_partidos.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "HORARIO":
                query = "SELECT ID_Horario, CONCAT(Dia, ' ', Hora, ' - ', Ocupacion) FROM HORARIO ORDER BY Dia, Hora"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_horarios'):
                    self.combo_horarios.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "CATEGORIA":
                query = "SELECT ID_Categoria, Nombre FROM CATEGORIA ORDER BY Nombre"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_categorias'):
                    self.combo_categorias.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "ENTRENAMIENTO":
                query = "SELECT Id_Entrenamiento, CONCAT(Dia, ' ', Hora) FROM ENTRENAMIENTO ORDER BY Dia, Hora"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_entrenamientos'):
                    self.combo_entrenamientos.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "PROFESORES":
                query = "SELECT Id_Profesores, CONCAT(Nombre, ' ', Apellidos) FROM PROFESORES ORDER BY Nombre"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_profesores'):
                    self.combo_profesores.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
            
            elif self.tabla == "USUARIOS":
                query = "SELECT id, usuario FROM USUARIOS ORDER BY usuario"
                datos = self.db.fetch_all(query)
                if hasattr(self, 'combo_usuarios'):
                    self.combo_usuarios.configure(values=[f"{row[0]} - {row[1]}" for row in datos])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar registros: {str(e)}")
    
    def cargar_categorias(self):
        try:
            query = "SELECT ID_Categoria, Nombre FROM CATEGORIA"
            datos = self.db.fetch_all(query)
            if datos:
                self.categorias_dict = {nombre: id for id, nombre in datos}
                for combo in [self.campos.get('combo_categoria')]:
                    if combo:
                        combo.configure(values=list(self.categorias_dict.keys()))
        except Exception as e:
            print(f"Error al cargar categorías: {e}")
    
    def cargar_torneos(self):
        try:
            query = "SELECT Id_Torneo, Nombre_torneo FROM TORNEO"
            datos = self.db.fetch_all(query)
            if datos:
                self.torneos_dict = {nombre: id for id, nombre in datos}
                if self.campos.get('combo_torneo'):
                    self.campos['combo_torneo'].configure(values=list(self.torneos_dict.keys()))
        except Exception as e:
            print(f"Error al cargar torneos: {e}")
    
    def toggle_campo_torneo(self, choice=None):
        """Muestra u oculta la fila del campo de torneo según el tipo de partido"""
        if not hasattr(self, 'campos') or 'combo_tipo' not in self.campos:
            return
            
        # Buscar la fila del campo de torneo en el grid
        for widget in self.campos.get('combo_torneo').master.winfo_children():
            # Obtener info del grid
            info = widget.grid_info()
            if info and 'row' in info:
                # Encontrar label y combo de torneo (deben estar en la misma fila que combo_torneo)
                if widget == self.campos.get('combo_torneo') or (hasattr(widget, 'cget') and 'Torneo:' in str(widget.cget('text') if 'text' in widget.keys() else '')):
                    if self.campos['combo_tipo'].get() == "Torneo":
                        widget.grid()  # Mostrar
                    else:
                        widget.grid_remove()  # Ocultar pero mantener espacio
    
    def cargar_profesores(self):
        try:
            profesores = self.db.fetch_all("SELECT Id_Profesores, CONCAT(Nombre, ' ', Apellidos) FROM PROFESORES ORDER BY Nombre")
            if profesores and hasattr(self, 'campos') and 'combo_profesor' in self.campos:
                self.profesores_dict = {nombre: id for id, nombre in profesores}
                self.campos['combo_profesor'].configure(values=list(self.profesores_dict.keys()))
        except Exception as e:
            print(f"Error al cargar profesores: {e}")
    
    def cargar_datos_jugador(self, event):
        try:
            seleccion = self.combo_jugadores.get()
            if seleccion:
                id_jugador = seleccion.split(" - ")[0]
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
                    self.campos['entry_nombre'].delete(0, "end")
                    self.campos['entry_nombre'].insert(0, datos[0][1])
                    self.campos['entry_apellidos'].delete(0, "end")
                    self.campos['entry_apellidos'].insert(0, datos[0][2])
                    self.campos['entry_curp'].delete(0, "end")
                    self.campos['entry_curp'].insert(0, datos[0][3])
                    self.campos['combo_categoria'].set(datos[0][4])
                    self.campos['spin_numero'].delete(0, "end")
                    self.campos['spin_numero'].insert(0, str(datos[0][5]))
                    
                    # Cargar fecha y forzar el estado a normal después
                    self.campos['date_inscripcion'].set_date(datos[0][6])
                    self.campos['date_inscripcion'].configure(state='normal')
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_torneo(self, event):
        try:
            seleccion = self.combo_torneos.get()
            if seleccion:
                id_torneo = seleccion.split(" - ")[0]
                query = """
                SELECT t.Id_Torneo, t.Nombre_torneo, c.Nombre, 
                       t.Cantidad_Equipos, t.Duracion, t.Fecha_Inicial, t.Fecha_Termino, t.Estado, t.Equipo_Ganador 
                FROM TORNEO t 
                LEFT JOIN CATEGORIA c ON t.Categoria = c.ID_Categoria 
                WHERE t.Id_Torneo = %s
                """
                datos = self.db.fetch_all(query, (id_torneo,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['entry_nombre'].delete(0, "end")
                    self.campos['entry_nombre'].insert(0, datos[0][1])
                    self.campos['combo_categoria'].set(datos[0][2])
                    self.campos['spin_equipos'].delete(0, "end")
                    self.campos['spin_equipos'].insert(0, str(datos[0][3]))
                    self.campos['combo_duracion'].set(datos[0][4])
                    
                    # Cargar fechas y forzar el estado a normal después
                    self.campos['date_inicio'].set_date(datos[0][5])
                    self.campos['date_inicio'].configure(state='normal')
                    
                    self.campos['date_fin'].set_date(datos[0][6])
                    self.campos['date_fin'].configure(state='normal')
                    
                    self.campos['combo_estado'].set(datos[0][7] if datos[0][7] else "Activo")
                    
                    # Cargar equipo ganador
                    self.campos['entry_ganador'].delete(0, "end")
                    if datos[0][8]:  # Si hay un ganador registrado
                        self.campos['entry_ganador'].insert(0, datos[0][8])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_partido(self, event):
        try:
            seleccion = self.combo_partidos.get()
            if seleccion:
                id_partido = seleccion.split(" - ")[0]
                query = """
                SELECT p.Id_Partidos, p.Dia, p.Hora, p.Equipo_Local, p.Equipo_Visitante, 
                       pr.Id_Profesores, p.Lugar, c.ID_Categoria, p.Tipo,
                       r.Ganador, r.Goles_Local, r.Goles_Visitante,
                       p.ID_Torneo, t.Nombre_torneo
                FROM PARTIDOS p 
                LEFT JOIN PROFESORES pr ON p.Profesor = pr.Id_Profesores 
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria 
                LEFT JOIN RESULTADOS r ON p.Id_Partidos = r.ID_Partido
                LEFT JOIN TORNEO t ON p.ID_Torneo = t.Id_Torneo
                WHERE p.Id_Partidos = %s
                """
                datos = self.db.fetch_all(query, (id_partido,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['combo_dia'].set(datos[0][1])
                    self.campos['combo_hora'].set(datos[0][2])
                    self.campos['entry_local'].delete(0, "end")
                    self.campos['entry_local'].insert(0, datos[0][3])
                    self.campos['entry_visitante'].delete(0, "end")
                    self.campos['entry_visitante'].insert(0, datos[0][4])
                    
                    # Cargar goles si existen
                    if datos[0][10] is not None:  # Goles_Local
                        self.campos['entry_goles_local'].delete(0, "end")
                        self.campos['entry_goles_local'].insert(0, str(datos[0][10]))
                    else:
                        self.campos['entry_goles_local'].delete(0, "end")
                    
                    if datos[0][11] is not None:  # Goles_Visitante
                        self.campos['entry_goles_visitante'].delete(0, "end")
                        self.campos['entry_goles_visitante'].insert(0, str(datos[0][11]))
                    else:
                        self.campos['entry_goles_visitante'].delete(0, "end")
                    
                    # Actualizar opciones de ganador con los equipos del partido
                    local = datos[0][3]
                    visitante = datos[0][4]
                    opciones_ganador = ["Sin resultado", "Empate"]
                    if local:
                        opciones_ganador.append(local)
                    if visitante:
                        opciones_ganador.append(visitante)
                    self.campos['combo_ganador'].configure(values=opciones_ganador)
                    
                    # Cargar el ganador si existe
                    if datos[0][9]:  # Ganador
                        self.campos['combo_ganador'].set(datos[0][9])
                    else:
                        self.campos['combo_ganador'].set("Sin resultado")
                    
                    # Cargar el torneo si existe
                    if datos[0][13]:  # Nombre_torneo
                        self.campos['combo_torneo'].set(datos[0][13])
                    else:
                        self.campos['combo_torneo'].set("")
                    
                    # Cargar profesor y categoría por ID
                    self.cargar_profesor_por_id(datos[0][5])
                    self.cargar_categoria_por_id(datos[0][7])
                    self.campos['entry_lugar'].delete(0, "end")
                    self.campos['entry_lugar'].insert(0, datos[0][6])
                    self.campos['combo_tipo'].set(datos[0][8])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_horario(self, event):
        try:
            seleccion = self.combo_horarios.get()
            if seleccion:
                id_horario = seleccion.split(" - ")[0]
                query = "SELECT ID_Horario, Ocupacion, Hora, Dia, Disponibilidad FROM HORARIO WHERE ID_Horario = %s"
                datos = self.db.fetch_all(query, (id_horario,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['combo_ocupacion'].set(datos[0][1])
                    self.campos['combo_hora'].set(datos[0][2])
                    self.campos['combo_dia'].set(datos[0][3])
                    disponibilidad = "Disponible" if datos[0][4] == 1 else "Ocupado"
                    self.campos['combo_disponibilidad'].set(disponibilidad)
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_categoria(self, event):
        try:
            seleccion = self.combo_categorias.get()
            if seleccion:
                id_categoria = seleccion.split(" - ")[0]
                query = "SELECT ID_Categoria, Nombre FROM CATEGORIA WHERE ID_Categoria = %s"
                datos = self.db.fetch_all(query, (id_categoria,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['entry_nombre'].delete(0, "end")
                    self.campos['entry_nombre'].insert(0, datos[0][1])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_entrenamiento(self, event):
        try:
            seleccion = self.combo_entrenamientos.get()
            if seleccion:
                id_entrenamiento = seleccion.split(" - ")[0]
                query = """
                SELECT e.Id_Entrenamiento, e.Dia, e.Hora, 
                       pr.Id_Profesores, c.ID_Categoria 
                FROM ENTRENAMIENTO e 
                LEFT JOIN PROFESORES pr ON e.Profesor = pr.Id_Profesores 
                LEFT JOIN CATEGORIA c ON e.Categoria = c.ID_Categoria 
                WHERE e.Id_Entrenamiento = %s
                """
                datos = self.db.fetch_all(query, (id_entrenamiento,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['combo_dia'].set(datos[0][1])
                    self.campos['combo_hora'].set(datos[0][2])
                    # Cargar profesor y categoría por ID
                    self.cargar_profesor_por_id(datos[0][3])
                    self.cargar_categoria_por_id(datos[0][4])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_profesor(self, event):
        try:
            seleccion = self.combo_profesores.get()
            if seleccion:
                id_profesor = seleccion.split(" - ")[0]
                query = """
                SELECT p.Id_Profesores, p.Nombre, p.Apellidos, c.ID_Categoria 
                FROM PROFESORES p 
                LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria 
                WHERE p.Id_Profesores = %s
                """
                datos = self.db.fetch_all(query, (id_profesor,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['entry_nombre'].delete(0, "end")
                    self.campos['entry_nombre'].insert(0, datos[0][1])
                    self.campos['entry_apellidos'].delete(0, "end")
                    self.campos['entry_apellidos'].insert(0, datos[0][2])
                    self.cargar_categoria_por_id(datos[0][3])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_datos_usuario(self, event):
        try:
            seleccion = self.combo_usuarios.get()
            if seleccion:
                id_usuario = seleccion.split(" - ")[0]
                query = "SELECT id, usuario, email, password FROM USUARIOS WHERE id = %s"
                datos = self.db.fetch_all(query, (id_usuario,))
                
                if datos:
                    self.registro_actual = datos[0]
                    self.campos['entry_usuario'].delete(0, "end")
                    self.campos['entry_usuario'].insert(0, datos[0][1])
                    self.campos['entry_email'].delete(0, "end")
                    self.campos['entry_email'].insert(0, datos[0][2])
                    self.campos['entry_password'].delete(0, "end")
                    self.campos['entry_password'].insert(0, datos[0][3])
                    
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def cargar_profesor_por_id(self, id_profesor):
        try:
            if id_profesor:
                query = "SELECT CONCAT(Nombre, ' ', Apellidos) FROM PROFESORES WHERE Id_Profesores = %s"
                datos = self.db.fetch_all(query, (id_profesor,))
                if datos and hasattr(self, 'campos') and 'combo_profesor' in self.campos:
                    self.campos['combo_profesor'].set(datos[0][0])
        except Exception as e:
            print(f"Error al cargar profesor por ID: {e}")
    
    def cargar_categoria_por_id(self, id_categoria):
        try:
            if id_categoria:
                query = "SELECT Nombre FROM CATEGORIA WHERE ID_Categoria = %s"
                datos = self.db.fetch_all(query, (id_categoria,))
                if datos and hasattr(self, 'campos') and 'combo_categoria' in self.campos:
                    self.campos['combo_categoria'].set(datos[0][0])
        except Exception as e:
            print(f"Error al cargar categoría por ID: {e}")
    
    def actualizar_jugador(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un jugador para modificar")
                return
            
            # Validar campos
            if (not self.campos['entry_nombre'].get() or not self.campos['entry_apellidos'].get() or
                not self.campos['entry_curp'].get() or self.campos['combo_categoria'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            query = """
            UPDATE JUGADORES 
            SET Nombre = %s, Apellidos = %s, CURP = %s, Categoria = %s, 
                Numero_jugador = %s, Inscripcion = %s 
            WHERE ID_jugador = %s
            """
            params = (
                self.campos['entry_nombre'].get(),
                self.campos['entry_apellidos'].get(),
                self.campos['entry_curp'].get(),
                self.categorias_dict[self.campos['combo_categoria'].get()],
                int(self.campos['spin_numero'].get()),
                self.campos['date_inscripcion'].get_date(),
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Jugador actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el jugador")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar jugador: {str(e)}")
    
    def actualizar_torneo(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un torneo para modificar")
                return
            
            if (not self.campos['entry_nombre'].get() or self.campos['combo_categoria'].get() == "" or
                self.campos['combo_duracion'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            query = """
            UPDATE TORNEO 
            SET Nombre_torneo = %s, Categoria = %s, Cantidad_Equipos = %s, 
                Duracion = %s, Fecha_Inicial = %s, Fecha_Termino = %s, Estado = %s, Equipo_Ganador = %s 
            WHERE Id_Torneo = %s
            """
            params = (
                self.campos['entry_nombre'].get(),
                self.categorias_dict[self.campos['combo_categoria'].get()],
                int(self.campos['spin_equipos'].get()),
                self.campos['combo_duracion'].get(),
                self.campos['date_inicio'].get_date(),
                self.campos['date_fin'].get_date(),
                self.campos['combo_estado'].get(),
                self.campos['entry_ganador'].get() if self.campos['entry_ganador'].get() else None,
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Torneo actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el torneo")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar torneo: {str(e)}")
    
    def actualizar_partido(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un partido para modificar")
                return
            
            if (self.campos['combo_dia'].get() == "" or self.campos['combo_hora'].get() == "" or
                not self.campos['entry_local'].get() or not self.campos['entry_visitante'].get() or
                self.campos['combo_profesor'].get() == "" or self.campos['combo_categoria'].get() == "" or
                self.campos['combo_tipo'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            # Actualizar partido  
            # Obtener ID del torneo si se seleccionó
            id_torneo = None
            torneo_seleccionado = self.campos['combo_torneo'].get()
            if torneo_seleccionado and torneo_seleccionado in self.torneos_dict:
                id_torneo = self.torneos_dict[torneo_seleccionado]
            
            query = """
            UPDATE PARTIDOS 
            SET Dia = %s, Hora = %s, Equipo_Local = %s, Equipo_Visitante = %s, 
                Profesor = %s, Lugar = %s, Categoria = %s, Tipo = %s, ID_Torneo = %s
            WHERE Id_Partidos = %s
            """
            params = (
                self.campos['combo_dia'].get(),
                self.campos['combo_hora'].get(),
                self.campos['entry_local'].get(),
                self.campos['entry_visitante'].get(),
                self.profesores_dict[self.campos['combo_profesor'].get()],
                self.campos['entry_lugar'].get(),
                self.categorias_dict[self.campos['combo_categoria'].get()],
                self.campos['combo_tipo'].get(),
                id_torneo,
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                # Actualizar RESULTADOS si se seleccionó un ganador o si hay goles
                ganador = self.campos['combo_ganador'].get()
                goles_local_str = self.campos['entry_goles_local'].get()
                goles_visitante_str = self.campos['entry_goles_visitante'].get()
                
                # Convertir goles a enteros, default a 0 si está vacío
                try:
                    goles_local = int(goles_local_str) if goles_local_str else 0
                except ValueError:
                    goles_local = 0
                
                try:
                    goles_visitante = int(goles_visitante_str) if goles_visitante_str else 0
                except ValueError:
                    goles_visitante = 0
                
                if ganador and ganador != "Sin resultado":
                    # Calcular perdedor
                    local = self.campos['entry_local'].get()
                    visitante = self.campos['entry_visitante'].get()
                    
                    if ganador == "Empate":
                        perdedor = None
                    elif ganador == local:
                        perdedor = visitante
                    else:
                        perdedor = local
                    
                    # Verificar si ya existe un resultado
                    check_query = "SELECT ID_Resultado FROM RESULTADOS WHERE ID_Partido = %s"
                    resultado_existente = self.db.fetch_all(check_query, (self.registro_actual[0],))
                    
                    if resultado_existente:
                        # Actualizar resultado existente
                        update_result_query = """
                        UPDATE RESULTADOS 
                        SET Goles_Local = %s, Goles_Visitante = %s, Ganador = %s, Perdedor = %s
                        WHERE ID_Partido = %s
                        """
                        self.db.execute_query(update_result_query, (goles_local, goles_visitante, ganador, perdedor, self.registro_actual[0]))
                    else:
                        # Crear nuevo resultado
                        insert_result_query = """
                        INSERT INTO RESULTADOS (ID_Partido, Goles_Local, Goles_Visitante, Ganador, Perdedor)
                        VALUES (%s, %s, %s, %s, %s)
                        """
                        self.db.execute_query(insert_result_query, (self.registro_actual[0], goles_local, goles_visitante, ganador, perdedor))
                
                messagebox.showinfo("Éxito", "Partido actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el partido")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar partido: {str(e)}")
    
    def actualizar_horario(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un horario para modificar")
                return
            
            if (self.campos['combo_ocupacion'].get() == "" or self.campos['combo_hora'].get() == "" or
                self.campos['combo_dia'].get() == "" or self.campos['combo_disponibilidad'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            disponibilidad = 1 if self.campos['combo_disponibilidad'].get() == "Disponible" else 0
            
            query = """
            UPDATE HORARIO 
            SET Ocupacion = %s, Hora = %s, Dia = %s, Disponibilidad = %s 
            WHERE ID_Horario = %s
            """
            params = (
                self.campos['combo_ocupacion'].get(),
                self.campos['combo_hora'].get(),
                self.campos['combo_dia'].get(),
                disponibilidad,
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Horario actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el horario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar horario: {str(e)}")
    
    def actualizar_categoria(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona una categoría para modificar")
                return
            
            if not self.campos['entry_nombre'].get():
                messagebox.showerror("Error", "Por favor ingrese el nombre de la categoría")
                return
            
            query = "UPDATE CATEGORIA SET Nombre = %s WHERE ID_Categoria = %s"
            params = (self.campos['entry_nombre'].get(), self.registro_actual[0])
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Categoría actualizada correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar la categoría")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar categoría: {str(e)}")
    
    def actualizar_entrenamiento(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un entrenamiento para modificar")
                return
            
            if (self.campos['combo_dia'].get() == "" or self.campos['combo_hora'].get() == "" or
                self.campos['combo_profesor'].get() == "" or self.campos['combo_categoria'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            query = """
            UPDATE ENTRENAMIENTO 
            SET Dia = %s, Hora = %s, Profesor = %s, Categoria = %s 
            WHERE Id_Entrenamiento = %s
            """
            params = (
                self.campos['combo_dia'].get(),
                self.campos['combo_hora'].get(),
                self.profesores_dict[self.campos['combo_profesor'].get()],
                self.categorias_dict[self.campos['combo_categoria'].get()],
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Entrenamiento actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el entrenamiento")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar entrenamiento: {str(e)}")
    
    def actualizar_profesor(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un profesor para modificar")
                return
            
            if (not self.campos['entry_nombre'].get() or not self.campos['entry_apellidos'].get() or
                self.campos['combo_categoria'].get() == ""):
                messagebox.showerror("Error", "Por favor complete todos los campos obligatorios")
                return
            
            query = """
            UPDATE PROFESORES 
            SET Nombre = %s, Apellidos = %s, Categoria = %s 
            WHERE Id_Profesores = %s
            """
            params = (
                self.campos['entry_nombre'].get(),
                self.campos['entry_apellidos'].get(),
                self.categorias_dict[self.campos['combo_categoria'].get()],
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Profesor actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el profesor")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar profesor: {str(e)}")
    
    def actualizar_usuario(self):
        try:
            if not self.registro_actual:
                messagebox.showwarning("Advertencia", "Selecciona un usuario para modificar")
                return
            
            if (not self.campos['entry_usuario'].get() or not self.campos['entry_email'].get() or
                not self.campos['entry_password'].get()):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            query = "UPDATE USUARIOS SET usuario = %s, email = %s, password = %s WHERE id = %s"
            params = (
                self.campos['entry_usuario'].get(),
                self.campos['entry_email'].get(),
                self.campos['entry_password'].get(),
                self.registro_actual[0]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Éxito", "Usuario actualizado correctamente")
                self.cargar_registros()
                self.limpiar_formulario()
            else:
                messagebox.showerror("Error", "Error al actualizar el usuario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar usuario: {str(e)}")
    
    def limpiar_formulario(self):
        self.registro_actual = None
        for nombre, widget in self.campos.items():
            if isinstance(widget, ctk.CTkEntry):
                widget.delete(0, "end")
                if "numero" in nombre:
                    widget.insert(0, "1")
                elif "equipos" in nombre:
                    widget.insert(0, "2")
            elif isinstance(widget, ctk.CTkComboBox):
                widget.set('')
            elif isinstance(widget, DateEntry):
                widget.set_date(None)
        
        # Limpiar combos de búsqueda
        if hasattr(self, 'combo_jugadores'):
            self.combo_jugadores.set('Elige jugador')
        if hasattr(self, 'combo_torneos'):
            self.combo_torneos.set('Elige torneo')
        if hasattr(self, 'combo_partidos'):
            self.combo_partidos.set('Elige partido')
        if hasattr(self, 'combo_horarios'):
            self.combo_horarios.set('Elige horario')
        if hasattr(self, 'combo_categorias'):
            self.combo_categorias.set('Elige categoría')
        if hasattr(self, 'combo_entrenamientos'):
            self.combo_entrenamientos.set('Elige entrenamiento')
        if hasattr(self, 'combo_profesores'):
            self.combo_profesores.set('Elige profesor')
        if hasattr(self, 'combo_usuarios'):
            self.combo_usuarios.set('Elige usuario')