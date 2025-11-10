# consulta_view.py
from src.components.cont_r import ContR
from src.components.panel_r import PanelR
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
import customtkinter as ctk
from datetime import datetime
import csv
from src.models.database import Database
import os
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False

class ConsultaApp:
    def __init__(self, parent_frame, tabla):
        self.frame = parent_frame
        self.tabla = tabla
        self.db = Database()
        self.vista_detallada = False  # False = Vista Básica, True = Vista Detallada
        self.btn_toggle = None  # Referencia al botón toggle
        
        # Contenedor principal
        self.cont_m = ContR(self.frame, n_rad=20, h=550, w=325, color="#F8F9FA")
        self.cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.5)

        # Header con título e icono
        self.crear_header()

        # Contenedor de tabla
        cont_p = ContR(self.cont_m, n_rad=15, h=470, w=320, color="#FFFFFF")
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.56)

        # Barra de búsqueda
        self.crear_barra_busqueda(cont_p)

        # Tabla
        self.crear_tabla(cont_p)

        # Botones inferiores
        self.crear_botones(cont_p)

        # Cargar datos iniciales
        self.actualizar_datos()

    # HEADER
    def crear_header(self):
        header_frame = tk.Frame(self.cont_m, bg="#212544", height=40)
        header_frame.place(relx=0.5, rely=0.03, anchor=tk.CENTER, relwidth=1.0)
        header_frame.pack_propagate(False)

        iconos = {
            "JUGADORES": "⚽", "TORNEO": "🏆", "PARTIDOS": "🤝",
            "HORARIO": "⏰", "CATEGORIA": "📊", "ENTRENAMIENTO": "🏃",
            "PROFESORES": "👨‍🏫", "USUARIOS": "👥", "RESULTADOS": "🎯"
        }
        icono = iconos.get(self.tabla, "📋")

        titulo_frame = tk.Frame(header_frame, bg="#212544")
        titulo_frame.pack(expand=True)

        tk.Label(titulo_frame, text=icono, font=("Arial", 18),
                 bg="#212544", fg="#FFB93B").pack(side="left", padx=(0, 6))

        tk.Label(titulo_frame, text=f"CONSULTA DE {self.tabla}",
                 font=("Arial", 14, "bold"), fg="#FCFCFC",
                 bg="#212544").pack(side="left")

        self.contador_lb = tk.Label(header_frame, text="Cargando...",
                                    font=("Arial", 8),
                                    fg="#FFB93B", bg="#212544")
        self.contador_lb.pack(side="bottom", pady=(0, 2))

    # BARRA DE BÚSQUEDA
    def crear_barra_busqueda(self, parent):
        search_frame = tk.Frame(parent, bg="#FFFFFF")
        search_frame.place(relx=0.5, rely=0.12, anchor=tk.CENTER, relwidth=0.95)

        tk.Label(search_frame, text="🔍", font=("Arial", 10),
                 bg="#FFFFFF", fg="#666").pack(side="left")

        self.entry_busqueda = ctk.CTkEntry(
            search_frame,
            placeholder_text="Buscar...",
            corner_radius=10,
            border_width=2,
            border_color="#D9D9D9",
            fg_color="#FFFFFF",
            text_color="#000000",
            placeholder_text_color="#666",
            font=("Arial", 11),
            width=250
        )
        self.entry_busqueda.pack(side="left", fill="x", expand=True, padx=4)
        self.entry_busqueda.bind("<KeyRelease>", self.buscar_datos)

    # TABLA
    def crear_tabla(self, parent):
        # Contenedor principal para tabla
        contenedor_principal = tk.Frame(parent, bg="#FFFFFF")
        contenedor_principal.place(relx=0.5, rely=0.41, anchor=tk.CENTER,
                                   relwidth=0.98, relheight=0.48)
        
        # Frame para el header (sobresale arriba)
        self.header_frame = ctk.CTkFrame(
            contenedor_principal,
            corner_radius=20,
            fg_color="#212544",
            height=45
        )
        self.header_frame.pack(fill="x", padx=0, pady=(0, 0))
        self.header_frame.pack_propagate(False)
        
        # Frame para los datos con bordes redondeados
        ctk_frame = ctk.CTkFrame(
            contenedor_principal, 
            corner_radius=25,
            border_width=0,
            fg_color="#FFFFFF"
        )
        ctk_frame.pack(fill="both", expand=True, pady=(0, 0))

        # Frame interior para la tabla
        frame_tabla = tk.Frame(ctk_frame, bg="#FFFFFF")
        frame_tabla.pack(fill="both", expand=True, padx=8, pady=8)

        # Estilo mejorado de la tabla
        style = ttk.Style()
        style.theme_use("clam")
        
        # Estilo de filas con líneas - Aumentada altura        style = ttk.Style()
        style.configure("Treeview",
                       font=("Arial", 10),
                       rowheight=30,
                       background="#FFFFFF",
                       fieldbackground="#FFFFFF",
                       borderwidth=0)
        
        # CENTRAR TODO EL CONTENIDO DE LAS CELDAS
        style.configure("Treeview", anchor="center")
        style.configure("Treeview.Cell", anchor="center")
        
        style.configure("Treeview.Heading",
                       font=("Arial", 11, "bold"),
                       background="#212544",
                       foreground="white",
                       relief="flat")
        
        # Colores alternos para filas
        style.map("Treeview", background=[("selected", "#007bff")])
        self.tree = ttk.Treeview(frame_tabla, show='tree')
        self.tree.tag_configure("evenrow", background="#F8F9FA")
        self.tree.tag_configure("oddrow", background="#FFFFFF")

        # Scrollbars personalizados con CustomTkinter - Redondeados y modernos
        # Canvas personalizado para scrollbar vertical
        scrollbar_frame = ctk.CTkFrame(
            frame_tabla,
            fg_color="transparent",
            width=20
        )
        scrollbar_frame.pack(side="right", fill="y", padx=(5, 0))
        
        # Scrollbar vertical personalizado con CustomTkinter
        vs = ctk.CTkScrollbar(
            scrollbar_frame,
            orientation="vertical",
            command=self.tree.yview,
            width=20,
            fg_color="#E8ECEF",  # Fondo gris claro
            button_color="#212544",  # Color del thumb (azul del programa)
            button_hover_color="#1a1d38",  # Color al hacer hover
            corner_radius=10  # Bordes redondeados
        )
        vs.pack(fill="y", expand=True)
        
        # Empaquetar el Treeview (sin scrollbar horizontal)
        self.tree.pack(side="left", fill="both", expand=True)
        
        # Configurar solo el scrollbar vertical
        self.tree.configure(yscrollcommand=vs.set)

    def configurar_columnas_auto(self):
        """Configura el ancho de las columnas automáticamente y crea headers personalizados"""
        if not self.tree["columns"]:
            return
        
        # Limpiar headers anteriores
        for widget in self.header_frame.winfo_children():
            widget.destroy()
        
        num_columnas = len(self.tree["columns"])
        # Ancho aproximado disponible (en píxeles)
        ancho_total = 1250
        ancho_por_columna = ancho_total // num_columnas
        
        # Configurar columnas del Treeview sin stretch para evitar desbordamiento
        self.tree.column("#0", width=0, stretch=False)
        
        # Offset inicial por el padding del contenedor de la tabla (padx=8 en frame_tabla)
        offset_x = 8
        
        for idx, col in enumerate(self.tree["columns"]):
            # stretch=False evita que las columnas se expandan más allá del ancho definido
            self.tree.column(col, width=ancho_por_columna, minwidth=80, stretch=False, anchor='center')
            
            # Crear header personalizado con ancho fijo igual a la columna
            header_label = ctk.CTkLabel(
                self.header_frame,
                text=col.upper(),
                font=("Arial", 11, "bold"),
                text_color="#FFFFFF",
                fg_color="transparent",
                width=ancho_por_columna,  # Ancho explícito para centrado correcto
                anchor="center"
            )
            
            # Posición absoluta calculada desde la izquierda
            # Se coloca en el inicio de la columna correspondiente
            x_pos = offset_x + (idx * ancho_por_columna)
            
            # Anclar al lado oeste (izquierda) de la posición x_pos
            header_label.place(x=x_pos, rely=0.5, anchor="w")

    def insertar_con_estilo(self, datos):
        """Inserta filas con colores alternos"""
        for idx, row in enumerate(datos):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert("", "end", values=row, tags=(tag,))

    # BOTONES
    def crear_botones(self, parent):
        frame_botones = tk.Frame(parent, bg="#FFFFFF")
        frame_botones.place(relx=0.5, rely=0.67, anchor=tk.CENTER, relwidth=0.95)

        botones = [
            ("🔄 Actualizar", "#FF8C00", "#FF7F00", self.actualizar_datos),
        ]
        
        # Agregar botón de toggle solo para tabla de PARTIDOS y TORNEO
        # El botón empieza diciendo "Vista Detallada" para ir a esa vista
        if self.tabla == "PARTIDOS":
            botones.append(("🔍 Vista Detallada", "#4169E1", "#3654C7", self.toggle_vista_partidos))
        elif self.tabla == "TORNEO":
            botones.append(("🔍 Vista Detallada", "#4169E1", "#3654C7", self.toggle_vista_torneos))

        # Continuar con los otros botones
        botones.extend([
            ("📊 Exportar", "#28a745", "#218838", self.mostrar_opciones_exportacion),
            (" Copiar", "#17a2b8", "#138496", self.copiar_datos),
            ("🎯 Filtrar", "#6c757d", "#5a6268", self.filtrar_datos)
        ])

        for texto, color, hover_color, cmd in botones:
            btn = ctk.CTkButton(
                frame_botones,
                text=texto,
                fg_color=color,
                hover_color=hover_color,
                text_color="white",
                corner_radius=10,
                font=("Arial", 10, "bold"),
                command=cmd,
                width=120
            )
            btn.pack(side="left", padx=2)
            
            # Guardar referencia al botón toggle
            if (self.tabla == "PARTIDOS" or self.tabla == "TORNEO") and "Vista" in texto:
                self.btn_toggle = btn

    # OPCIONES DE EXPORTACIÓN
    def mostrar_opciones_exportacion(self):
        if not self.tree.get_children():
            messagebox.showwarning("Exportar", "No hay datos para exportar")
            return

        win = tk.Toplevel(self.frame)
        win.title("Exportar datos")
        win.geometry("300x150")
        win.config(bg="white")
        win.resizable(False, False)

        # Centrar ventana
        win.transient(self.frame)
        win.grab_set()

        tk.Label(win, text="Seleccione el formato de exportación:",
                 bg="white", font=("Arial", 10)).pack(pady=15)

        btn_frame = tk.Frame(win, bg="white")
        btn_frame.pack(pady=10)

        # Botón para CSV
        btn_csv = ctk.CTkButton(
            btn_frame, text="CSV",
            fg_color="#28a745",
            hover_color="#218838",
            text_color="white",
            corner_radius=10,
            font=("Arial", 10, "bold"),
            width=100,
            command=lambda: [self.exportar_csv(), win.destroy()]
        )
        btn_csv.pack(side="left", padx=5)

        # Botón para Excel
        if PANDAS_AVAILABLE:
            btn_excel = ctk.CTkButton(
                btn_frame, text="Excel",
                fg_color="#007bff",
                hover_color="#0056b3",
                text_color="white",
                corner_radius=10,
                font=("Arial", 10, "bold"),
                width=100,
                command=lambda: [self.exportar_excel(), win.destroy()]
            )
            btn_excel.pack(side="left", padx=5)

        # Botón para PDF
        if REPORTLAB_AVAILABLE:
            btn_pdf = ctk.CTkButton(
                btn_frame, text="PDF",
                fg_color="#dc3545",
                hover_color="#c82333",
                text_color="white",
                corner_radius=10,
                font=("Arial", 10, "bold"),
                width=100,
                command=lambda: [self.exportar_pdf(), win.destroy()]
            )
            btn_pdf.pack(side="left", padx=5)

        # Exportar directamente a CSV
        if not PANDAS_AVAILABLE and not REPORTLAB_AVAILABLE:
            win.destroy()
            self.exportar_csv()

    # EXPORTAR CSV
    def exportar_csv(self):
        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre = f"{self.tabla}_{fecha}.csv"

        ruta = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=nombre,
            filetypes=[("CSV", "*.csv")]
        )

        if not ruta:
            return

        columnas = self.tree["columns"]
        filas = [self.tree.item(i)["values"] for i in self.tree.get_children()]

        try:
            with open(ruta, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(columnas)
                writer.writerows(filas)

            messagebox.showinfo("Exportado", f"Archivo CSV guardado como:\n{ruta}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar CSV: {str(e)}")

    # EXPORTAR EXCEL
    def exportar_excel(self):
        if not PANDAS_AVAILABLE:
            messagebox.showerror("Error", 
                "Para exportar a Excel necesitas instalar pandas:\n"
                "pip install pandas openpyxl")
            return

        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre = f"{self.tabla}_{fecha}.xlsx"

        ruta = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            initialfile=nombre,
            filetypes=[("Excel", "*.xlsx")]
        )

        if not ruta:
            return

        try:
            # Obtener datos de la tabla
            columnas = self.tree["columns"]
            filas = [self.tree.item(i)["values"] for i in self.tree.get_children()]

            # Crear DataFrame
            df = pd.DataFrame(filas, columns=columnas)
            
            # Exportar a Excel
            with pd.ExcelWriter(ruta, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=self.tabla, index=False)
                
                # Autoajustar columnas
                worksheet = writer.sheets[self.tabla]
                for idx, col in enumerate(df.columns):
                    max_len = max(df[col].astype(str).str.len().max(), len(col)) + 2
                    worksheet.column_dimensions[chr(65 + idx)].width = max_len

            messagebox.showinfo("Exportado", f"Archivo Excel guardado como:\n{ruta}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar Excel: {str(e)}")

    # EXPORTAR PDF
    def exportar_pdf(self):
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Error", 
                "Para exportar a PDF necesitas instalar reportlab:\n"
                "pip install reportlab")
            return

        fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nombre = f"{self.tabla}_{fecha}.pdf"

        ruta = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            initialfile=nombre,
            filetypes=[("PDF", "*.pdf")]
        )

        if not ruta:
            return

        try:
            # Obtener datos
            columnas = self.tree["columns"]
            filas = [self.tree.item(i)["values"] for i in self.tree.get_children()]

            # Crear documento PDF
            doc = SimpleDocTemplate(ruta, pagesize=A4, topMargin=30)
            elements = []

            # Estilos
            styles = getSampleStyleSheet()
            
            # Título
            titulo = Paragraph(f"Reporte de {self.tabla}", styles['Title'])
            elements.append(titulo)
            
            # Información de exportación
            fecha_export = Paragraph(f"Exportado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                   styles['Normal'])
            elements.append(fecha_export)
            
            elementos_vacios = Paragraph("<br/><br/>", styles['Normal'])
            elements.append(elementos_vacios)

            # Preparar datos para la tabla
            datos_tabla = [columnas]  # Encabezados
            for fila in filas:
                datos_tabla.append([str(cell) for cell in fila])

            # Crear tabla
            tabla = Table(datos_tabla, repeatRows=1)
            
            # Estilo de la tabla
            estilo_tabla = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#212544")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ])
            
            # Aplicar estilo alternado a las filas
            for i in range(1, len(datos_tabla)):
                if i % 2 == 0:
                    estilo_tabla.add('BACKGROUND', (0, i), (-1, i), colors.HexColor("#f8f9fa"))

            tabla.setStyle(estilo_tabla)
            elements.append(tabla)

            # Generar PDF
            doc.build(elements)
            messagebox.showinfo("Exportado", f"Archivo PDF guardado como:\n{ruta}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")

    # BUSCAR EN TIEMPO REAL
    def buscar_datos(self, event):
        texto = self.entry_busqueda.get().lower()
        if not texto:  # Si está vacío, mostrar todo
            self.actualizar_datos()
            return

        self.actualizar_datos()  # Recarga todo

        for item in self.tree.get_children():
            valores = [str(self.tree.set(item, col)).lower()
                       for col in self.tree["columns"]]
            if texto not in " ".join(valores):
                self.tree.delete(item)

    # FILTRAR DATOS
    def filtrar_datos(self):
        if not self.tree.get_children():
            messagebox.showwarning("Filtrar", "No hay datos para filtrar")
            return

        win = tk.Toplevel(self.frame)
        win.title("Filtrar datos")
        win.geometry("300x200")
        win.config(bg="white")

        tk.Label(win, text="Columna:", bg="white").pack(pady=5)
        columnas = list(self.tree["columns"])
        cb_col = ttk.Combobox(win, values=columnas, state="readonly")
        cb_col.pack()

        tk.Label(win, text="Valor a buscar:", bg="white").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack()

        def aplicar():
            col = cb_col.get()
            val = entry.get().lower()

            self.actualizar_datos()

            for item in self.tree.get_children():
                texto = str(self.tree.set(item, col)).lower()
                if val not in texto:
                    self.tree.delete(item)

            win.destroy()

        ctk.CTkButton(
            win, text="Aplicar",
            fg_color="#212544",
            hover_color="#1a1d38",
            text_color="white",
            corner_radius=10,
            font=("Arial", 10, "bold"),
            command=aplicar
        ).pack(pady=10)

    # COPIAR DATOS
    def copiar_datos(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Copiar", "Selecciona un registro")
            return

        texto = ""
        for item in sel:
            fila = [str(x) for x in self.tree.item(item)["values"]]
            texto += "\t".join(fila) + "\n"

        self.frame.clipboard_clear()
        self.frame.clipboard_append(texto)
        messagebox.showinfo("Copiar", "Datos copiados al portapapeles")

    # ACTUALIZAR
    def actualizar_datos(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        funciones = {
            "JUGADORES": self.consultar_jugadores,
            "TORNEO": self.consultar_torneos,
            "PARTIDOS": self.consultar_partidos,
            "HORARIO": self.consultar_horarios,
            "CATEGORIA": self.consultar_categorias,
            "ENTRENAMIENTO": self.consultar_entrenamientos,
            "PROFESORES": self.consultar_profesores,
            "USUARIOS": self.consultar_usuarios,
            "RESULTADOS": self.consultar_resultados,
        }

        if self.tabla in funciones:
            datos = funciones[self.tabla]()
        else:
            datos = []

        self.contador_lb.config(text=f"Total de registros: {len(datos)}")

    # CONSULTAS
    def consultar_jugadores(self):
        query = """
        SELECT j.Nombre, j.Apellidos, j.CURP,
               c.Nombre as Categoria, j.Numero_jugador, j.Inscripcion
        FROM JUGADORES j
        LEFT JOIN CATEGORIA c ON j.Categoria = c.ID_Categoria
        ORDER BY j.Nombre, j.Apellidos
        """
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Nombre", "Apellidos", "CURP",
                                "Categoria", "Numero", "Inscripcion")

        self.tree.column("#0", width=0, stretch=tk.NO)
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()

        self.insertar_con_estilo(datos)

        return datos
    
    def toggle_vista_partidos(self):
        """Alterna entre vista básica y vista detallada de partidos"""
        # Cambiar estado
        self.vista_detallada = not self.vista_detallada
        
        # Actualizar texto del botón toggle directamente
        if self.btn_toggle:
            if self.vista_detallada:
                self.btn_toggle.configure(text="📊 Vista Básica")
            else:
                self.btn_toggle.configure(text="🔍 Vista Detallada")
        
        # Actualizar datos de la tabla
        self.actualizar_datos()
    
    def toggle_vista_torneos(self):
        """Alterna entre vista básica y vista detallada de torneos"""
        # Cambiar estado
        self.vista_detallada = not self.vista_detallada
        
        # Actualizar texto del botón toggle directamente
        if self.btn_toggle:
            if self.vista_detallada:
                self.btn_toggle.configure(text="📊 Vista Básica")
            else:
                self.btn_toggle.configure(text="🔍 Vista Detallada")
        
        # Actualizar datos de la tabla
        self.actualizar_datos()

    def consultar_torneos(self):
        query = """
        SELECT t.Nombre_torneo, c.Nombre as Categoria,
               t.Cantidad_Equipos, t.Duracion,
               t.Fecha_Inicial, t.Fecha_Termino, t.Estado
        FROM TORNEO t
        LEFT JOIN CATEGORIA c ON t.Categoria = c.ID_Categoria
        ORDER BY t.Fecha_Inicial DESC
        """
        datos = self.db.fetch_all(query)

        # Configurar columnas según la vista activa
        if self.vista_detallada:
            # Vista Detallada: todos los campos
            self.tree["columns"] = (
                "Nombre", "Categoria", "Equipos",
                "Duracion", "Fecha_Inicio", "Fecha_Fin"
            )
        else:
            # Vista Básica: nombre, duración y estado
            self.tree["columns"] = (
                "Nombre", "Duracion", "Estado"
            )
        
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()

        # Formatear datos según la vista
        datos_formateados = []
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        for row in datos:
            nombre, categoria, equipos, duracion, fecha_inicio, fecha_fin, estado = row
            
            if self.vista_detallada:
                # Vista Detallada: formatear fechas sin hora
                if fecha_inicio:
                    try:
                        if isinstance(fecha_inicio, str):
                            fecha_obj = datetime.strptime(fecha_inicio.split()[0], "%Y-%m-%d")
                        else:
                            fecha_obj = fecha_inicio
                        dia = fecha_obj.day
                        mes = meses[fecha_obj.month - 1]
                        fecha_inicio_fmt = f"{dia} de {mes}"
                    except:
                        fecha_inicio_fmt = str(fecha_inicio).split()[0] if isinstance(fecha_inicio, str) else str(fecha_inicio)
                else:
                    fecha_inicio_fmt = "-"
                
                if fecha_fin:
                    try:
                        if isinstance(fecha_fin, str):
                            fecha_obj = datetime.strptime(fecha_fin.split()[0], "%Y-%m-%d")
                        else:
                            fecha_obj = fecha_fin
                        dia = fecha_obj.day
                        mes = meses[fecha_obj.month - 1]
                        fecha_fin_fmt = f"{dia} de {mes}"
                    except:
                        fecha_fin_fmt = str(fecha_fin).split()[0] if isinstance(fecha_fin, str) else str(fecha_fin)
                else:
                    fecha_fin_fmt = "-"
                
                datos_formateados.append((nombre, categoria, equipos, duracion, fecha_inicio_fmt, fecha_fin_fmt))
            else:
                # Vista Básica: solo nombre, duración y estado
                estado_fmt = "✅ Activo" if estado == "Activo" else "❌ Inactivo"
                datos_formateados.append((nombre, duracion, estado_fmt))

        self.insertar_con_estilo(datos_formateados)

        return datos

    def consultar_partidos(self):
        query = """
        SELECT p.Fecha, p.Hora,
               p.Equipo_Local, p.Equipo_Visitante,
               COALESCE(r.Goles_Local, '-') AS Goles_Local,
               COALESCE(r.Goles_Visitante, '-') AS Goles_Visitante,
               COALESCE(r.Ganador, 'Sin resultado') AS Ganador,
               CONCAT(pr.Nombre, ' ', pr.Apellidos) AS Profesor,
               p.Lugar, c.Nombre AS Categoria, p.Tipo, p.Dia
        FROM PARTIDOS p
        LEFT JOIN PROFESORES pr ON p.Profesor = pr.Id_Profesores
        LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria
        LEFT JOIN RESULTADOS r ON p.Id_Partidos = r.ID_Partido
        ORDER BY p.Fecha DESC, p.Hora DESC
        """
        datos = self.db.fetch_all(query)

        # Configurar columnas según la vista activa
        if self.vista_detallada:
            # Vista Detallada: información secundaria
            self.tree["columns"] = (
                "Profesor", "Lugar", "Categoria", "Tipo"
            )
        else:
            # Vista Básica: información esencial del partido
            self.tree["columns"] = (
                "Fecha", "Local", "Visitante",
                "Goles_L", "Goles_V", "Ganador"
            )
        
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()

        # Formatear fechas a español completo
        datos_formateados = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        for row in datos:
            fecha, hora, *resto = row[:-1]  # Excluir el campo Dia al final
            dia_nombre = row[-1]  # Obtener el nombre del día desde el final
            
            # Debug: Verificar qué valores estamos recibiendo
            fecha_formateada = None
            
            # Prioridad 1: Intentar usar la fecha completa si existe
            if fecha and fecha != '' and str(fecha).strip().lower() not in ['none', 'null', '']:
                try:
                    # Si fecha es un objeto date o string de fecha completa
                    if isinstance(fecha, str):
                        if len(fecha) == 10:  # Formato YYYY-MM-DD
                            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                        else:
                            # Intentar parsear como datetime completo
                            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                    else:
                        # Fecha es un objeto date o datetime
                        fecha_obj = fecha
                    
                    # Procesar hora - IMPORTANTE: MySQL puede devolver timedelta
                    if hora:
                        # Si es timedelta (MySQL Time), convertir a time
                        if hasattr(hora, 'total_seconds'):
                            # Es timedelta, convertir a time
                            total_seconds = int(hora.total_seconds())
                            hours = total_seconds // 3600
                            minutes = (total_seconds % 3600) // 60
                            seconds = total_seconds % 60
                            from datetime import time
                            hora_obj = time(hours, minutes, seconds)
                        elif isinstance(hora, str):
                            # Es string
                            if ':' in hora:
                                hora_parts = hora.split(':')
                                hora_obj = datetime.strptime(f"{hora_parts[0]}:{hora_parts[1]}", "%H:%M").time()
                            else:
                                hora_obj = datetime.strptime(hora, "%H:%M:%S").time()
                        else:
                            # Ya es time object
                            hora_obj = hora
                        
                        # Combinar fecha y hora si es necesario
                        if hasattr(fecha_obj, 'hour'):
                            # Ya es datetime completo
                            fecha_completa_obj = fecha_obj
                        else:
                            # Es solo date, combinar con hora
                            fecha_completa_obj = datetime.combine(fecha_obj, hora_obj)
                        
                        dia_num = fecha_completa_obj.day
                        mes = meses[fecha_completa_obj.month - 1]
                        hora_fmt = fecha_completa_obj.strftime("%H:%M")
                        # Formato en múltiples líneas para que quepa en el campo
                        fecha_formateada = f"{dia_num} de {mes}\n{hora_fmt}"
                    else:
                        # Tenemos fecha pero no hora
                        if hasattr(fecha_obj, 'day'):
                            dia_num = fecha_obj.day
                            mes = meses[fecha_obj.month - 1]
                            # Formato en múltiples líneas
                            fecha_formateada = f"{dia_num} de {mes}"
                        
                except Exception as e:
                    # Si falla el formateo con fecha, intentar con día nombre
                    fecha_formateada = None
            
            # Prioridad 2: Si no se pudo formatear con fecha completa, usar día nombre
            if not fecha_formateada and dia_nombre and hora:
                try:
                    # Convertir hora a string
                    if hasattr(hora, 'total_seconds'):
                        # Es timedelta
                        total_seconds = int(hora.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        hora_fmt = f"{hours:02d}:{minutes:02d}"
                    elif isinstance(hora, str):
                        hora_fmt = hora.split(':')[0] + ':' + hora.split(':')[1] if ':' in str(hora) else str(hora)
                    else:
                        hora_fmt = hora.strftime("%H:%M") if hasattr(hora, 'strftime') else str(hora)
                    # Formato en múltiples líneas
                    fecha_formateada = f"{dia_nombre}\n{hora_fmt}\n(sin fecha)"
                except:
                    fecha_formateada = f"{dia_nombre} (sin fecha específica)"
            
            # Prioridad 3: Si todo falla, mostrar un mensaje
            if not fecha_formateada:
                fecha_formateada = "Fecha no especificada"
            
            # Extraer solo las columnas que necesitamos según la vista
            if self.vista_detallada:
                # Vista Detallada: Profesor, Lugar, Categoria, Tipo (indices 7, 8, 9, 10)
                datos_formateados.append((resto[5], resto[6], resto[7], resto[8]))
            else:
                # Vista Básica: Fecha, Local, Visitante, Goles_L, Goles_V, Ganador (indices 0, 1, 2, 3, 4, 5, 6)
                datos_formateados.append((fecha_formateada, *resto[:5]))
        
        self.insertar_con_estilo(datos_formateados)

        return datos

    def consultar_horarios(self):
        query = "SELECT Ocupacion, Hora, Disponibilidad, Dia FROM HORARIO"
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Ocupacion", "Dia_Hora", "Disponibilidad")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()

        # Formatear horarios
        datos_transformados = []
        
        for row in datos:
            ocupacion, hora, disponibilidad, dia_nombre = row
            
            # Formatear día y hora
            if dia_nombre and hora:
                if isinstance(hora, str):
                    hora_fmt = hora.split(':')[0] + ':' + hora.split(':')[1] if ':' in str(hora) else str(hora)
                else:
                    # Manejar timedelta de MySQL
                    if hasattr(hora, 'total_seconds'):
                        total_seconds = int(hora.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        hora_fmt = f"{hours:02d}:{minutes:02d}"
                    else:
                        hora_fmt = hora.strftime("%H:%M") if hasattr(hora, 'strftime') else str(hora)
                fecha_formateada = f"{dia_nombre} a las {hora_fmt}"
            else:
                fecha_formateada = "-"
            
            disponibilidad_fmt = "✔ Disponible" if disponibilidad == 1 else "✘ Ocupado"
            datos_transformados.append((ocupacion, fecha_formateada, disponibilidad_fmt))
        
        self.insertar_con_estilo(datos_transformados)

        return datos

    def consultar_categorias(self):
        query = "SELECT Nombre FROM CATEGORIA ORDER BY Nombre"
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Nombre",)
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()
        for row in datos:
            self.tree.insert("", "end", values=row)

        return datos

    def consultar_entrenamientos(self):
        query = """
        SELECT e.Hora, e.Dia,
               CONCAT(p.Nombre, ' ', p.Apellidos) AS Profesor,
               c.Nombre AS Categoria
        FROM ENTRENAMIENTO e
        LEFT JOIN PROFESORES p ON e.Profesor = p.Id_Profesores
        LEFT JOIN CATEGORIA c ON e.Categoria = c.ID_Categoria
        ORDER BY e.Dia, e.Hora
        """
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Dia_Hora", "Profesor", "Categoria")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()
        
        # Formatear horarios
        datos_formateados = []
        
        for row in datos:
            hora, dia_nombre, profesor, categoria = row
            
            # Formatear día y hora
            if dia_nombre and hora:
                if isinstance(hora, str):
                    hora_fmt = hora.split(':')[0] + ':' + hora.split(':')[1] if ':' in str(hora) else str(hora)
                else:
                    # Manejar timedelta de MySQL
                    if hasattr(hora, 'total_seconds'):
                        total_seconds = int(hora.total_seconds())
                        hours = total_seconds // 3600
                        minutes = (total_seconds % 3600) // 60
                        hora_fmt = f"{hours:02d}:{minutes:02d}"
                    else:
                        hora_fmt = hora.strftime("%H:%M") if hasattr(hora, 'strftime') else str(hora)
                fecha_formateada = f"{dia_nombre} a las {hora_fmt}"
            else:
                fecha_formateada = "-"
            
            datos_formateados.append((fecha_formateada, profesor, categoria))
        
        self.insertar_con_estilo(datos_formateados)

        return datos

    def consultar_profesores(self):
        query = """
        SELECT p.Nombre, p.Apellidos,
               c.Nombre AS Categoria
        FROM PROFESORES p
        LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria
        ORDER BY p.Nombre, p.Apellidos
        """
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Nombre", "Apellidos", "Categoria")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()
        for row in datos:
            self.tree.insert("", "end", values=row)

        return datos

    def consultar_usuarios(self):
        query = """
        SELECT usuario, email
        FROM USUARIOS ORDER BY usuario
        """
        datos = self.db.fetch_all(query)

        self.tree["columns"] = ("Usuario", "Email")
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()
        for row in datos:
            self.tree.insert("", "end", values=row)

        return datos


    def consultar_resultados(self):
        query = """
        SELECT p.Fecha, p.Hora,
               p.Equipo_Local, r.Goles_Local,
               p.Equipo_Visitante, r.Goles_Visitante,
               r.Ganador, r.Perdedor,
               p.Lugar, c.Nombre AS Categoria, p.Dia
        FROM RESULTADOS r
        LEFT JOIN PARTIDOS p ON r.ID_Partido = p.Id_Partidos
        LEFT JOIN CATEGORIA c ON p.Categoria = c.ID_Categoria
        ORDER BY p.Fecha DESC, p.Hora DESC
        """
        datos = self.db.fetch_all(query)

        self.tree["columns"] = (
            "Fecha_Hora", "Local", "Goles_L",
            "Visitante", "Goles_V", "Ganador", "Perdedor",
            "Lugar", "Categoria"
        )
        self.tree.column("#0", width=0, stretch=tk.NO)

        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.upper())
        
        self.configurar_columnas_auto()
        
        # Formatear fechas a español completo
        datos_formateados = []
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
        meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
                 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
        
        for row in datos:
            fecha, hora, *resto = row[:-1]
            dia_nombre = row[-1]
            
            # Formatear fecha
            if fecha and hora:
                try:
                    if isinstance(fecha, str):
                        if len(fecha) == 10:
                            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d")
                        else:
                            fecha_obj = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S")
                    else:
                        fecha_obj = fecha
                    
                    if isinstance(hora, str):
                        if ':' in hora:
                            hora_parts = hora.split(':')
                            hora_obj = datetime.strptime(f"{hora_parts[0]}:{hora_parts[1]}", "%H:%M").time()
                        else:
                            hora_obj = datetime.strptime(hora, "%H:%M:%S").time()
                    else:
                        hora_obj = hora
                    
                    if hasattr(fecha_obj, 'hour'):
                        fecha_completa_obj = fecha_obj
                    else:
                        fecha_completa_obj = datetime.combine(fecha_obj, hora_obj)
                    
                    dia_num = fecha_completa_obj.day
                    mes = meses[fecha_completa_obj.month - 1]
                    hora_fmt = fecha_completa_obj.strftime("%H:%M")
                    fecha_formateada = f"{dia_num} de {mes} a las {hora_fmt}"
                except:
                    if isinstance(hora, str):
                        hora_fmt = hora.split(':')[0] + ':' + hora.split(':')[1] if ':' in str(hora) else str(hora)
                    else:
                        hora_fmt = hora.strftime("%H:%M") if hasattr(hora, 'strftime') else str(hora)
                    fecha_formateada = f"{dia_nombre} a las {hora_fmt}"
            elif dia_nombre and hora:
                if isinstance(hora, str):
                    hora_fmt = hora.split(':')[0] + ':' + hora.split(':')[1] if ':' in str(hora) else str(hora)
                else:
                    hora_fmt = hora.strftime("%H:%M") if hasattr(hora, 'strftime') else str(hora)
                fecha_formateada = f"{dia_nombre} a las {hora_fmt}"
            else:
                fecha_formateada = "-"
            
            datos_formateados.append((fecha_formateada, *resto))
        
        self.insertar_con_estilo(datos_formateados)

        return datos