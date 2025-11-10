from PIL import ImageTk, Image
import tkinter as tk
import pywinstyles

class plantilla_f:
    def __init__(self, root):   
        # Ventana
        self.root = root
        root.title("Inicio de sesión")
        root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")
        root.resizable(True, True)
        root.update()
        
        # Cache para la imagen de fondo (optimización de rendimiento)
        self.fondo_original_cached = None
        self.resize_job = None  # Para debounce de resize
        
        # Header
        frame_mb = tk.Frame(root, bg="#212544", width=self.root.winfo_width())
        frame_mb.place(relx=0, rely=0, relwidth=1, relheight=0.19)
        tk.Label(frame_mb, bg="#EF7D1A").place(relx=0.157, rely=0.1, relwidth=0.56, relheight=0.2)
        tk.Label(frame_mb, bg="#FFB93B").place(relx=0.68, rely=0.46, relwidth=0.32, relheight=0.23)
        
        # Logo principal con manejo de errores
        iconct_lb = None
        icon_lb = None
        try:
            img_phi = ImageTk.PhotoImage(Image.open("assets\\imagenes\\log_prin_2.png").resize((116, 116), Image.LANCZOS))
            iconct_lb = tk.Label(frame_mb, bg="#212544")
            iconct_lb.place(relx=0.076, rely=0.44, anchor='center')
            icon_lb = tk.Label(iconct_lb, bg="#212544", image=img_phi, cursor="hand2")
            icon_lb.image = img_phi 
            icon_lb.pack(side="top", fill="both", expand=True)
            try:
                pywinstyles.set_opacity(icon_lb, color="#212544")
            except:
                pass
        except Exception as e:
            print(f"Error cargando logo: {e}")
            iconct_lb = tk.Label(frame_mb, bg="#212544", text="LOGO", cursor="hand2")
            iconct_lb.place(relx=0.076, rely=0.44, anchor='center')
        
        # Texto de bienvenida
        bs_lb = tk.Label(frame_mb, text="Bienvenido al sistema", font=("Arial", 44, "bold"),
                        bg="#212544", fg="#FCFCFC")
        bs_lb.place(relx=0.168, rely=0.30)
        
        # Decoración
        frame_dec = tk.Frame(root, bg="#F28305")
        frame_dec.place(rely=0.17, anchor='center', relheight=0.02, relwidth=2)
        frame_dec.config(cursor="circle")
        
        # Fondo - MODIFICADO PARA EXPANSIÓN HORIZONTAL
        frame_prin = tk.Frame(root, width=self.root.winfo_width())
        frame_prin.place(rely=0.19, relwidth=1, relheight=0.81)    

        fondo_lb = None
        try:
            # Cargar y cachear la imagen original (solo una vez)
            self.fondo_original_cached = Image.open("assets\\imagenes\\fondo_alt.jpeg")
            
            # Redimensionar la imagen para que ocupe todo el ancho manteniendo la relación de aspecto
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight() * 0.81  # 81% de la altura para el área de fondo
            
            # Calcular nuevas dimensiones manteniendo relación de aspecto
            img_width, img_height = self.fondo_original_cached.size
            aspect_ratio = img_width / img_height
            
            # Ajustar al ancho disponible
            new_width = int(screen_width)
            new_height = int(new_width / aspect_ratio)
            
            # Si la altura es menor que la disponible, ajustar por altura
            if new_height < screen_height:
                new_height = int(screen_height)
                new_width = int(new_height * aspect_ratio)
            
            # Redimensionar la imagen usando la caché
            fondo_redim = self.fondo_original_cached.resize((new_width, new_height), Image.LANCZOS)
            fondo = ImageTk.PhotoImage(fondo_redim)
            
            fondo_lb = tk.Label(frame_prin, image=fondo, bg="#F5F5F5")
            fondo_lb.image = fondo
            fondo_lb.place(relx=0.5, anchor='n', relwidth=1, height=new_height)
            
            # Centrar verticalmente si es necesario
            if new_height < frame_prin.winfo_height():
                fondo_lb.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, height=new_height)
            
        except Exception as e:
            print(f"Error cargando fondo: {e}")
            fondo_lb = tk.Label(frame_prin, bg="#F5F5F5")
            fondo_lb.place(relwidth=1, relheight=1)

        # Atributos
        self.frame_mb = frame_mb
        self.frame_prin = frame_prin
        self.frame_dec = frame_dec
        self.iconct_lb = iconct_lb
        self.icon_lb = icon_lb
        self.fondo_lb = fondo_lb 
        self.bs_lb = bs_lb
        
        # Vincular evento de redimensionamiento
        self.root.bind('<Configure>', self.on_resize)
    
    def on_resize(self, event):
        """Maneja el redimensionamiento de la ventana con debounce"""
        # Cancelar el trabajo de resize anterior si existe (debounce)
        if self.resize_job:
            self.root.after_cancel(self.resize_job)
        
        # Programar el resize para después de 100ms de inactividad
        self.resize_job = self.root.after(100, self._do_resize)
    
    def _do_resize(self):
        """Realiza el redimensionamiento real de la imagen"""
        if self.fondo_lb and hasattr(self.fondo_lb, 'image') and self.fondo_original_cached:
            try:
                # Obtener dimensiones actuales
                screen_width = self.root.winfo_width()
                screen_height = int(self.root.winfo_height() * 0.81)
                
                # Calcular nuevas dimensiones manteniendo relación de aspecto
                img_width, img_height = self.fondo_original_cached.size
                aspect_ratio = img_width / img_height
                
                # Ajustar al ancho disponible
                new_width = max(screen_width, 1)  # Evitar width 0
                new_height = int(new_width / aspect_ratio)
                
                # Si la altura es menor que la disponible, ajustar por altura
                if new_height < screen_height:
                    new_height = max(screen_height, 1)
                    new_width = int(new_height * aspect_ratio)
                
                # Redimensionar la imagen usando la caché en memoria
                fondo_redim = self.fondo_original_cached.resize((new_width, new_height), Image.LANCZOS)
                fondo = ImageTk.PhotoImage(fondo_redim)
                
                # Actualizar la imagen del label
                self.fondo_lb.config(image=fondo)
                self.fondo_lb.image = fondo
                
                # Actualizar la posición
                self.fondo_lb.place(relx=0.5, anchor='n', relwidth=1, height=new_height)
                
                # Centrar verticalmente si es necesario
                if new_height < self.frame_prin.winfo_height():
                    self.fondo_lb.place(relx=0.5, rely=0.5, anchor='center', relwidth=1, height=new_height)
                    
            except Exception as e:
                print(f"Error redimensionando fondo: {e}")

    def header_v2(self, PanelR, Cont_Cr, ContR, search_callback=None, home_callback=None):
        """Header versión 2 con controles adicionales"""
        # Eliminar el texto de bienvenida original
        try:
            self.bs_lb.destroy()
        except:
            pass
        
        # Configurar callback del logo para regresar al menú principal
        if home_callback and self.icon_lb:
            # Eliminar binding anterior si existe
            try:
                self.icon_lb.unbind("<Button-1>")
            except:
                pass
            # Agregar nuevo binding
            self.icon_lb.bind("<Button-1>", lambda e: home_callback())
        elif home_callback and self.iconct_lb:
            # Si no hay icon_lb, usar iconct_lb
            try:
                self.iconct_lb.unbind("<Button-1>")
            except:
                pass
            self.iconct_lb.bind("<Button-1>", lambda e: home_callback())
        
        # Contenedor circular para usuario
        try:
            cont_sn = Cont_Cr(self.frame_mb, 30, "#212544", "#212544")  # Radio más grande y azul
            cont_sn.place(relx=0.534, rely=0.395)
            img_mn = ImageTk.PhotoImage(Image.open("assets\\imagenes\\log_us2.png").resize((35, 35), Image.LANCZOS))
            uss_lb = tk.Label(self.frame_mb, image=img_mn, bg="#212544", cursor="hand2")  # Fondo azul
            uss_lb.place(relx=0.538, rely=0.45)
            uss_lb.image = img_mn
            
            # Tooltip para mostrar hora y usuario
            self.tooltip = None
            self.tooltip_update_job = None  # Para guardar el job de actualización
            
            def mostrar_tooltip(event):
                if self.tooltip:
                    return
                
                from datetime import datetime
                usuario_actual = getattr(self, 'usuario_actual', 'Usuario')
                
                # Crear tooltip
                self.tooltip = tk.Toplevel(self.root)
                self.tooltip.wm_overrideredirect(True)
                self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
                
                # Crear label que se actualizará
                tooltip_label = tk.Label(self.tooltip, text="",
                                justify=tk.LEFT, background="#212544", foreground="white",
                                relief=tk.SOLID, borderwidth=1, font=("Arial", 10, "bold"),
                                padx=10, pady=5)
                tooltip_label.pack()
                
                # Función para actualizar el reloj
                def actualizar_reloj():
                    if self.tooltip:
                        hora_actual = datetime.now().strftime("%H:%M:%S")
                        tooltip_label.config(text=f"👤 {usuario_actual}\n🕒 {hora_actual}")
                        # Programar próxima actualización en 1 segundo
                        self.tooltip_update_job = self.root.after(1000, actualizar_reloj)
                
                # Iniciar actualización del reloj
                actualizar_reloj()
            
            def ocultar_tooltip(event):
                # Cancelar actualización del reloj
                if self.tooltip_update_job:
                    self.root.after_cancel(self.tooltip_update_job)
                    self.tooltip_update_job = None
                
                if self.tooltip:
                    self.tooltip.destroy()
                    self.tooltip = None
            
            uss_lb.bind("<Enter>", mostrar_tooltip)
            uss_lb.bind("<Leave>", ocultar_tooltip)
            
        except Exception as e:
            print(f"Error en contenedor usuario: {e}")
        
        # Barra de búsqueda - CONSOLIDADA (sin ContR duplicado)
        try:
            # Frame contenedor para la barra de búsqueda
            search_frame = tk.Frame(self.frame_mb, bg="#EDEDED", highlightthickness=0)
            search_frame.place(relx=0.174, rely=0.45, relwidth=0.35, relheight=0.24)
            
            # Ícono de búsqueda
            img_mn = ImageTk.PhotoImage(Image.open("assets\\imagenes\\icon_buscar.png").resize((24, 24), Image.LANCZOS))
            busq_lb = tk.Label(search_frame, image=img_mn, bg="#EDEDED")
            busq_lb.pack(side="left", padx=(10, 5))
            busq_lb.image = img_mn
            
            # Campo de entrada
            self.entry_bq = tk.Entry(search_frame, bg="#EDEDED", relief="flat",
                                     font=('arial', 13), fg="#666666")
            self.entry_bq.pack(side="left", fill="both", expand=True, padx=(0, 10))
            self.entry_bq.insert(0, "Buscar función...")
            
            # Guardar callback de búsqueda
            self.search_callback = search_callback
            
            # Frame para sugerencias (inicialmente oculto)
            self.suggestions_frame = None
            
            # Sugerencias populares organizadas por categoría - MEJORADAS
            self.suggestions = [
                ("⭐ Búsquedas Rápidas", [
                    "consultar partidos",
                    "registrar jugadores",
                    "consultar horarios",
                    "registrar partidos"
                ]),
                ("📝 Registrar", [
                    "registrar jugadores",
                    "registrar partidos",
                    "registrar torneos",
                    "registrar horarios",
                    "registrar entrenamientos",
                    "registrar profesores",
                    "registrar categorias",
                    "registrar usuarios"
                ]),
                ("🔍 Consultar", [
                    "consultar jugadores",
                    "consultar partidos",
                    "consultar torneos",
                    "consultar horarios",
                    "consultar entrenamientos",
                    "consultar profesores",
                    "consultar categorias"
                ]),
                ("✏️ Modificar", [
                    "modificar jugadores",
                    "modificar partidos",
                    "modificar torneos",
                    "modificar horarios",
                    "modificar entrenamientos",
                    "modificar profesores",
                    "modificar categorias"
                ]),
                ("🗑️ Eliminar", [
                    "eliminar jugadores",
                    "eliminar partidos",
                    "eliminar torneos",
                    "eliminar horarios",
                    "eliminar entrenamientos",
                    "eliminar profesores",
                    "eliminar categorias"
                ])
            ]
            
            # Eventos para placeholder
            def on_focus_in(event):
                if self.entry_bq.get() == "Buscar función...":
                    self.entry_bq.delete(0, tk.END)
                    self.entry_bq.config(fg="black")
                # Mostrar sugerencias
                self.show_suggestions()
            
            def on_focus_out(event):
                # Restaurar placeholder si el campo está vacío
                if self.entry_bq.get() == "":
                    self.entry_bq.insert(0, "Buscar función...")
                    self.entry_bq.config(fg="#666666")
                # Pequeño delay para permitir clicks en sugerencias antes de ocultarlas
                self.root.after(200, lambda: self.hide_suggestions_if_needed(event))
            
            def on_enter(event):
                texto = self.entry_bq.get()
                if texto and texto != "Buscar función..." and self.search_callback:
                    self.search_callback(texto)
                    self.hide_suggestions()
            
            def on_key_release(event):
                # Ocultar sugerencias si el usuario está escribiendo
                if event.keysym not in ['Up', 'Down', 'Return', 'Escape']:
                    if len(self.entry_bq.get()) > 0 and self.entry_bq.get() != "Buscar función...":
                        self.hide_suggestions()
            
            self.entry_bq.bind("<FocusIn>", on_focus_in)
            self.entry_bq.bind("<FocusOut>", on_focus_out)
            self.entry_bq.bind("<Return>", on_enter)
            self.entry_bq.bind("<KeyRelease>", on_key_release)
            self.entry_bq.bind("<Escape>", lambda e: self.hide_suggestions())
            
        except Exception as e:
            print(f"Error en barra búsqueda: {e}")
    
    def show_suggestions(self):
        """Muestra el panel de sugerencias"""
        if self.suggestions_frame:
            self.suggestions_frame.destroy()
        
        # Crear frame de sugerencias
        self.suggestions_frame = tk.Frame(self.root, bg="white", relief="solid", bd=1)
        self.suggestions_frame.place(relx=0.174, rely=0.13, relwidth=0.35)
        
        # Título
        title = tk.Label(self.suggestions_frame, text="Sugerencias de búsqueda",
                        font=('arial', 10, 'bold'), bg="white", fg="#212544",
                        anchor='w', padx=10, pady=5)
        title.pack(fill='x')
        
        # Separador
        sep = tk.Frame(self.suggestions_frame, bg="#CCCCCC", height=1)
        sep.pack(fill='x')
        
        # Scroll frame para sugerencias
        canvas = tk.Canvas(self.suggestions_frame, bg="white", highlightthickness=0, height=200)
        scrollbar = tk.Scrollbar(self.suggestions_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="white")
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Agregar sugerencias por categoría
        for category, items in self.suggestions:
            # Categoría
            cat_label = tk.Label(scrollable_frame, text=category,
                                font=('arial', 9, 'bold'), bg="white", fg="#666666",
                                anchor='w', padx=15, pady=3)
            cat_label.pack(fill='x')
            
            # Items de la categoría
            for item in items:
                item_frame = tk.Frame(scrollable_frame, bg="white")
                item_frame.pack(fill='x')
                
                item_label = tk.Label(item_frame, text=f"  • {item}",
                                     font=('arial', 9), bg="white", fg="#212544",
                                     anchor='w', padx=20, pady=2, cursor="hand2")
                item_label.pack(fill='x')
                
                # Hover effect
                def on_enter_item(e, lbl=item_label):
                    lbl.config(bg="#F0F0F0")
                
                def on_leave_item(e, lbl=item_label):
                    lbl.config(bg="white")
                
                def on_click_item(e, text=item):
                    self.entry_bq.delete(0, tk.END)
                    self.entry_bq.insert(0, text)
                    self.entry_bq.config(fg="black")
                    if self.search_callback:
                        self.search_callback(text)
                    self.hide_suggestions()
                
                item_label.bind("<Enter>", on_enter_item)
                item_label.bind("<Leave>", on_leave_item)
                item_label.bind("<Button-1>", on_click_item)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Hacer que el frame de sugerencias esté por encima
        self.suggestions_frame.lift()
        
        # Bind para detectar clics fuera del panel de sugerencias
        def check_click_outside(event):
            """Verifica si el clic fue fuera del panel de sugerencias"""
            if self.suggestions_frame:
                # Obtener coordenadas del panel de sugerencias
                x = self.suggestions_frame.winfo_rootx()
                y = self.suggestions_frame.winfo_rooty()
                width = self.suggestions_frame.winfo_width()
                height = self.suggestions_frame.winfo_height()
                
                # Verificar si el clic fue fuera del panel
                if not (x <= event.x_root <= x + width and y <= event.y_root <= y + height):
                    # También verificar que no sea en el campo de búsqueda
                    entry_x = self.entry_bq.winfo_rootx()
                    entry_y = self.entry_bq.winfo_rooty()
                    entry_width = self.entry_bq.winfo_width()
                    entry_height = self.entry_bq.winfo_height()
                    
                    if not (entry_x <= event.x_root <= entry_x + entry_width and 
                            entry_y <= event.y_root <= entry_y + entry_height):
                        # Restaurar placeholder si el campo está vacío
                        if self.entry_bq.get() == "" or self.entry_bq.get() == "Buscar función...":
                            self.entry_bq.delete(0, tk.END)
                            self.entry_bq.insert(0, "Buscar función...")
                            self.entry_bq.config(fg="#666666")
                        
                        # Quitar el foco del campo de búsqueda
                        self.root.focus()
                        
                        # Ocultar sugerencias
                        self.hide_suggestions()
        
        # Vincular evento de clic al root
        self.root.bind("<Button-1>", check_click_outside, add="+")
        
        # Guardar referencia para poder eliminarla después
        self.click_outside_handler = check_click_outside
    
    def hide_suggestions(self):
        """Oculta el panel de sugerencias"""
        if self.suggestions_frame:
            # Desvincular el evento de clic si existe
            if hasattr(self, 'click_outside_handler'):
                try:
                    self.root.unbind("<Button-1>", self.click_outside_handler)
                except:
                    pass
            
            self.suggestions_frame.destroy()
            self.suggestions_frame = None
    
    def hide_suggestions_if_needed(self, event):
        """Oculta sugerencias solo si el foco no está en el entry"""
        # Ya no necesitamos restaurar el placeholder aquí porque on_focus_out lo hace
        self.hide_suggestions()