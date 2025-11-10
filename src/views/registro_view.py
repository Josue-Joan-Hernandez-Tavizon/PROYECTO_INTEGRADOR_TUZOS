from src.components.cont_r import Cont_Cr, ContR
from tkcalendar import Calendar, DateEntry
from PIL import ImageTk, Image
from src.components.panel_r import PanelR
from tkinter import ttk, messagebox
import tkinter as tk
import customtkinter as ctk
from src.models.database import Database
import datetime
import re
# import bcrypt  # DESHABILITADO TEMPORALMENTE

class RegistroApp_partido:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Partidos", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        # Primero crear todos los widgets
        tk.Label(cont_p, text="Equipo Local", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.15, anchor=tk.CENTER)
        self.eq_local = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.eq_local.place(relx=0.09, rely=0.2, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Categoria", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.15, anchor=tk.CENTER)
        self.categoria = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.categoria.place(relx=0.59, rely=0.2, relheight=0.06, relwidth=0.35)
        self.categoria.set("Seleccion")
        
        tk.Label(cont_p, text="Equipo Visitante", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.35, anchor=tk.CENTER)
        self.eq_visitante = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.eq_visitante.place(relx=0.09, rely=0.4, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Lugar", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.35, anchor=tk.CENTER)
        self.lugar = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.lugar.place(relx=0.59, rely=0.4, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Fecha del partido", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.55, anchor=tk.CENTER)
        self.fecha_partido = DateEntry(cont_p, width=12, selectmode='day', background='#212544', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd', font=("Arial", 12), state='normal')
        self.fecha_partido.place(relx=0.09, rely=0.6, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Hora del partido", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.55, anchor=tk.CENTER)
        self.hora = ctk.CTkComboBox(cont_p, state="readonly", values=[f"{h:02d}:00" for h in range(7, 22)], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.hora.place(relx=0.59, rely=0.6, relheight=0.06, relwidth=0.35)
        self.hora.set("Seleccion")
        
        tk.Label(cont_p, text="Profesor", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.75, anchor=tk.CENTER)
        self.profesor = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.profesor.place(relx=0.09, rely=0.8, relheight=0.06, relwidth=0.35)
        self.profesor.set("Seleccion")
        
        tk.Label(cont_p, text="Tipo de partido", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.75, anchor=tk.CENTER)
        self.tipo = ctk.CTkComboBox(cont_p, state="readonly", values=["Amistoso", "Torneo", "Liga", "Eliminatorio"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13), command=self.toggle_torneo_field)
        self.tipo.place(relx=0.59, rely=0.8, relheight=0.06, relwidth=0.35)
        self.tipo.set("Seleccion")
        
        # Campo de torneo (oculto por defecto, se muestra solo si tipo=Torneo)
        self.torneo_label = tk.Label(cont_p, text="Torneo", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w")
        self.torneo = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.torneo.set("Selecciona un torneo")
        # Inicialmente oculto
        
        rp_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar partido', t_font=13, fg_font="#FCFCFC", command=self.registrar_partido)
        rp_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.94)

        # Luego cargar los datos
        self.cargar_categorias()
        self.cargar_profesores()
        self.cargar_torneos()
        
        # Configurar navegación con Enter
        self.eq_local.bind("<Return>", lambda e: self.categoria.focus())
        self.categoria.bind("<Return>", lambda e: self.eq_visitante.focus())
        self.eq_visitante.bind("<Return>", lambda e: self.lugar.focus())
        self.lugar.bind("<Return>", lambda e: self.fecha_partido.focus())
        self.fecha_partido.bind("<Return>", lambda e: self.hora.focus())
        self.hora.bind("<Return>", lambda e: self.profesor.focus())
        self.profesor.bind("<Return>", lambda e: self.tipo.focus())
        self.tipo.bind("<Return>", lambda e: self.registrar_partido())

    def cargar_categorias(self):
        try:
            categorias = self.db.fetch_all("SELECT ID_Categoria, Nombre FROM CATEGORIA")
            if categorias:
                self.categorias_dict = {nombre: id for id, nombre in categorias}
                self.categoria.configure(values=list(self.categorias_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay categorias registradas en la base de datos")
        except Exception as e:
            print(f"Error al cargar categorias: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorias")

    def cargar_profesores(self):
        try:
            profesores = self.db.fetch_all("SELECT Id_Profesores, CONCAT(Nombre, ' ', Apellidos) FROM PROFESORES")
            if profesores:
                self.profesores_dict = {nombre: id for id, nombre in profesores}
                self.profesor.configure(values=list(self.profesores_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay profesores registrados en la base de datos")
        except Exception as e:
            print(f"Error al cargar profesores: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los profesores")
    
    def cargar_torneos(self):
        try:
            torneos = self.db.fetch_all("SELECT Id_Torneo, Nombre_torneo FROM TORNEO")
            if torneos:
                self.torneos_dict = {nombre: id for id, nombre in torneos}
                self.torneo.configure(values=list(self.torneos_dict.keys()))
            # Si no hay torneos, el combobox queda vacío (no es obligatorio)
        except Exception as e:
            print(f"Error al cargar torneos: {e}")
    
    def toggle_torneo_field(self, choice=None):
        """Muestra u oculta el campo de torneo según el tipo de partido"""
        if self.tipo.get() == "Torneo":
            # Mostrar campo de torneo
            self.torneo_label.place(relx=0.28, rely=0.88, anchor=tk.CENTER)
            self.torneo.place(relx=0.09, rely=0.93, relheight=0.06, relwidth=0.35)
        else:
            # Ocultar campo de torneo
            self.torneo_label.place_forget()
            self.torneo.place_forget()

    def registrar_partido(self):
        try:
            # Validar campos
            if (not self.eq_local.get() or not self.eq_visitante.get() or 
                self.categoria.get() == "Seleccion" or
                self.hora.get() == "Seleccion" or self.profesor.get() == "Seleccion" or
                self.tipo.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            # Validar que si el tipo es Torneo, se haya seleccionado un torneo
            if self.tipo.get() == "Torneo":
                if self.torneo.get() == "Selecciona un torneo" or not self.torneo.get():
                    messagebox.showerror("Error", "Por favor seleccione un torneo")
                    return

            # Obtener la fecha seleccionada
            fecha_partido = self.fecha_partido.get_date()
            
            # Calcular automáticamente el día de la semana desde la fecha
            dias_semana = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo']
            dia_semana = dias_semana[fecha_partido.weekday()]
            
            # Obtener ID del torneo si el tipo es Torneo
            id_torneo = None
            if self.tipo.get() == "Torneo" and self.torneo.get() in self.torneos_dict:
                id_torneo = self.torneos_dict[self.torneo.get()]

            query = """
            INSERT INTO PARTIDOS (Dia, Fecha, Hora, Equipo_Local, Equipo_Visitante, Profesor, Lugar, Categoria, Tipo, ID_Torneo)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (
                dia_semana,
                fecha_partido,
                self.hora.get(),
                self.eq_local.get(),
                self.eq_visitante.get(),
                self.profesores_dict[self.profesor.get()],
                self.lugar.get(),
                self.categorias_dict[self.categoria.get()],
                self.tipo.get(),
                id_torneo
            )
            
            if self.db.execute_query(query, params):
                # Registrar automáticamente en HORARIO  
                horario_query = "INSERT INTO HORARIO (Ocupacion, Hora, Dia, Disponibilidad) VALUES (%s, %s, %s, %s)"
                self.db.execute_query(horario_query, ('Partido', self.hora.get(), dia_semana, 0))
                
                messagebox.showinfo("Exito", "Partido registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el partido")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar partido: {str(e)}")

    def limpiar_campos(self):
        self.eq_local.delete(0, tk.END)
        self.eq_visitante.delete(0, tk.END)
        self.lugar.delete(0, tk.END)
        self.categoria.set("Seleccion")
        self.fecha_partido.set_date(datetime.date.today())
        self.hora.set("Seleccion")
        self.profesor.set("Seleccion")
        self.tipo.set("Seleccion")
        self.torneo.set("Selecciona un torneo")
        # Ocultar campo de torneo
        self.torneo_label.place_forget()
        self.torneo.place_forget()

class RegistroApp_horarios:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Horarios", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        tk.Label(cont_p, text="Ocupacion", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.15, anchor=tk.CENTER)
        self.ocupacion = ctk.CTkComboBox(cont_p, state="readonly", values=["Entrenamiento", "Partido", "Torneo", "Reunion"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.ocupacion.place(relx=0.09, rely=0.2, relheight=0.06, relwidth=0.35)
        self.ocupacion.set("Seleccion")
        
        tk.Label(cont_p, text="Dia", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.15, anchor=tk.CENTER)
        self.dia = ctk.CTkComboBox(cont_p, state="readonly", values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.dia.place(relx=0.59, rely=0.2, relheight=0.06, relwidth=0.35)
        self.dia.set("Seleccion")
        
        tk.Label(cont_p, text="Hora", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.35, anchor=tk.CENTER)
        self.hora = ctk.CTkComboBox(cont_p, state="readonly", values=[f"{h:02d}:00" for h in range(7, 22)], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.hora.place(relx=0.09, rely=0.4, relheight=0.06, relwidth=0.35)
        self.hora.set("Seleccion")
        
        tk.Label(cont_p, text="Disponibilidad", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.35, anchor=tk.CENTER)
        self.disponibilidad = ctk.CTkComboBox(cont_p, state="readonly", values=["Disponible", "Ocupado"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.disponibilidad.place(relx=0.59, rely=0.4, relheight=0.06, relwidth=0.35)
        self.disponibilidad.set("Seleccion")
        
        rh_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar horario', t_font=13, fg_font="#FCFCFC", command=self.registrar_horario)
        rh_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)
        
        # Configurar navegación con Enter
        self.ocupacion.bind("<Return>", lambda e: self.dia.focus())
        self.dia.bind("<Return>", lambda e: self.hora.focus())
        self.hora.bind("<Return>", lambda e: self.disponibilidad.focus())
        self.disponibilidad.bind("<Return>", lambda e: self.registrar_horario())

    def registrar_horario(self):
        try:
            if (self.ocupacion.get() == "Seleccion" or self.dia.get() == "Seleccion" or
                self.hora.get() == "Seleccion" or self.disponibilidad.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            disponibilidad_bool = 1 if self.disponibilidad.get() == "Disponible" else 0
            
            # Verificar si ya existe un registro para ese día y hora
            check_query = "SELECT * FROM HORARIO WHERE Dia = %s AND Hora = %s"
            if self.db.fetch_all(check_query, (self.dia.get(), self.hora.get())):
                # Si existe y está ocupado, avisar
                check_ocupado = "SELECT * FROM HORARIO WHERE Dia = %s AND Hora = %s AND Disponibilidad = 0"
                if self.db.fetch_all(check_ocupado, (self.dia.get(), self.hora.get())):
                    messagebox.showerror("Error", f"El horario del {self.dia.get()} a las {self.hora.get()} ya está ocupado y no se puede sobrescribir manualmente sin borrarlo primero.")
                    return
            
            query = """
            INSERT INTO HORARIO (Ocupacion, Hora, Dia, Disponibilidad)
            VALUES (%s, %s, %s, %s)
            """
            params = (
                self.ocupacion.get(),
                self.hora.get(),
                self.dia.get(),
                disponibilidad_bool
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Horario registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el horario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar horario: {str(e)}")

    def limpiar_campos(self):
        self.ocupacion.set("Seleccion")
        self.dia.set("Seleccion")
        self.hora.set("Seleccion")
        self.disponibilidad.set("Seleccion")

class RegistroApp_entrenamiento:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Entrenamientos", font=("Arial", 16, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        # Primero crear todos los widgets
        tk.Label(cont_p, text="Dia", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.2, anchor=tk.CENTER)
        self.dia = ctk.CTkComboBox(cont_p, state="readonly", values=["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.dia.place(relx=0.09, rely=0.25, relheight=0.06, relwidth=0.35)
        self.dia.set("Seleccion")
        
        tk.Label(cont_p, text="Categoria", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.2, anchor=tk.CENTER)
        self.categoria = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.categoria.place(relx=0.59, rely=0.25, relheight=0.06, relwidth=0.35)
        self.categoria.set("Seleccion")
        
        tk.Label(cont_p, text="Hora", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.4, anchor=tk.CENTER)
        self.hora = ctk.CTkComboBox(cont_p, state="readonly", values=[f"{h:02d}:00" for h in range(7, 22)], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.hora.place(relx=0.09, rely=0.45, relheight=0.06, relwidth=0.35)
        self.hora.set("Seleccion")
        
        tk.Label(cont_p, text="Profesor", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.4, anchor=tk.CENTER)
        self.profesor = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.profesor.place(relx=0.59, rely=0.45, relheight=0.06, relwidth=0.35)
        self.profesor.set("Seleccion")
        
        re_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar entrenamiento', t_font=13, fg_font="#FCFCFC", command=self.registrar_entrenamiento)
        re_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)

        # Luego cargar los datos
        self.cargar_categorias()
        self.cargar_profesores()
        
        # Configurar navegación con Enter
        self.dia.bind("<Return>", lambda e: self.categoria.focus())
        self.categoria.bind("<Return>", lambda e: self.hora.focus())
        self.hora.bind("<Return>", lambda e: self.profesor.focus())
        self.profesor.bind("<Return>", lambda e: self.registrar_entrenamiento())

    def cargar_categorias(self):
        try:
            categorias = self.db.fetch_all("SELECT ID_Categoria, Nombre FROM CATEGORIA")
            if categorias:
                self.categorias_dict = {nombre: id for id, nombre in categorias}
                self.categoria.configure(values=list(self.categorias_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay categorias registradas en la base de datos")
        except Exception as e:
            print(f"Error al cargar categorias: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorias")

    def cargar_profesores(self):
        try:
            profesores = self.db.fetch_all("SELECT Id_Profesores, CONCAT(Nombre, ' ', Apellidos) FROM PROFESORES")
            if profesores:
                self.profesores_dict = {nombre: id for id, nombre in profesores}
                self.profesor.configure(values=list(self.profesores_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay profesores registrados en la base de datos")
        except Exception as e:
            print(f"Error al cargar profesores: {e}")
            messagebox.showerror("Error", "No se pudieron cargar los profesores")

    def registrar_entrenamiento(self):
        try:
            if (self.dia.get() == "Seleccion" or self.hora.get() == "Seleccion" or
                self.categoria.get() == "Seleccion" or self.profesor.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Verificar disponibilidad en HORARIO
            check_query = "SELECT * FROM HORARIO WHERE Dia = %s AND Hora = %s AND Disponibilidad = 0"
            if self.db.fetch_all(check_query, (self.dia.get(), self.hora.get())):
                messagebox.showerror("Error", f"El horario del {self.dia.get()} a las {self.hora.get()} ya está ocupado")
                return

            query = """
            INSERT INTO ENTRENAMIENTO (Dia, Hora, Profesor, Categoria)
            VALUES (%s, %s, %s, %s)
            """
            params = (
                self.dia.get(),
                self.hora.get(),
                self.profesores_dict[self.profesor.get()],
                self.categorias_dict[self.categoria.get()]
            )
            
            if self.db.execute_query(query, params):
                # Registrar automáticamente en HORARIO
                horario_query = "INSERT INTO HORARIO (Ocupacion, Hora, Dia, Disponibilidad) VALUES (%s, %s, %s, %s)"
                self.db.execute_query(horario_query, ('Entrenamiento', self.hora.get(), self.dia.get(), 0))

                messagebox.showinfo("Exito", "Entrenamiento registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el entrenamiento")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar entrenamiento: {str(e)}")

    def limpiar_campos(self):
        self.dia.set("Seleccion")
        self.hora.set("Seleccion")
        self.categoria.set("Seleccion")
        self.profesor.set("Seleccion")

class RegistroApp_equipos:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Categorias", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        tk.Label(cont_p, text="Nombre de la categoria", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.2, anchor=tk.CENTER)
        self.nombre_categoria = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.nombre_categoria.place(relx=0.09, rely=0.25, relheight=0.06, relwidth=0.8)
        
        re_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar categoria', t_font=13, fg_font="#FCFCFC", command=self.registrar_categoria)
        re_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)
        
        # Configurar navegación con Enter
        self.nombre_categoria.bind("<Return>", lambda e: self.registrar_categoria())

    def registrar_categoria(self):
        try:
            if not self.nombre_categoria.get():
                messagebox.showerror("Error", "Por favor ingrese el nombre de la categoria")
                return

            query = "INSERT INTO CATEGORIA (Nombre) VALUES (%s)"
            params = (self.nombre_categoria.get(),)
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Categoria registrada correctamente")
                self.nombre_categoria.delete(0, tk.END)
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar la categoria")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar categoria: {str(e)}")

class RegistroApp_jugador:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Jugadores", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        # Primero crear todos los widgets
        tk.Label(cont_p, text="Nombre", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.1, anchor=tk.CENTER)
        self.nombre = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.nombre.place(relx=0.09, rely=0.15, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Apellidos", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.1, anchor=tk.CENTER)
        self.apellidos = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.apellidos.place(relx=0.59, rely=0.15, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="CURP", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.3, anchor=tk.CENTER)
        self.curp = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.curp.place(relx=0.09, rely=0.35, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Categoria", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.3, anchor=tk.CENTER)
        self.categoria = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.categoria.place(relx=0.59, rely=0.35, relheight=0.06, relwidth=0.35)
        self.categoria.set("Seleccion")
        
        tk.Label(cont_p, text="Numero de jugador", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.5, anchor=tk.CENTER)
        self.numero_jugador = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.numero_jugador.place(relx=0.09, rely=0.55, relheight=0.06, relwidth=0.35)
        self.numero_jugador.insert(0, "1")
        
        tk.Label(cont_p, text="Fecha de inscripcion", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.5, anchor=tk.CENTER)
        self.inscripcion = DateEntry(cont_p, selectmode='day', locale='es_ES', date_pattern='dd/mm/yyyy', showweeknumbers=False, state='normal')
        self.inscripcion.place(relx=0.59, rely=0.55, relheight=0.06, relwidth=0.35)
        
        rj_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar jugador', t_font=13, fg_font="#FCFCFC", command=self.registrar_jugador)
        rj_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)

        # Luego cargar los datos
        self.cargar_categorias()
        
        # Configurar navegación con Enter
        self.nombre.bind("<Return>", lambda e: self.apellidos.focus())
        self.apellidos.bind("<Return>", lambda e: self.curp.focus())
        self.curp.bind("<Return>", lambda e: self.categoria.focus())
        self.categoria.bind("<Return>", lambda e: self.numero_jugador.focus())
        self.numero_jugador.bind("<Return>", lambda e: self.inscripcion.focus())
        self.inscripcion.bind("<Return>", lambda e: self.registrar_jugador())

    def cargar_categorias(self):
        try:
            categorias = self.db.fetch_all("SELECT ID_Categoria, Nombre FROM CATEGORIA")
            if categorias:
                self.categorias_dict = {nombre: id for id, nombre in categorias}
                self.categoria.configure(values=list(self.categorias_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay categorias registradas en la base de datos")
        except Exception as e:
            print(f"Error al cargar categorias: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorias")

    def registrar_jugador(self):
        try:
            if (not self.nombre.get() or not self.apellidos.get() or not self.curp.get() or
                self.categoria.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Convertir fecha a formato MySQL
            fecha_inscripcion = self.inscripcion.get_date()
            
            query = """
            INSERT INTO JUGADORES (Nombre, Apellidos, CURP, Categoria, Numero_jugador, Inscripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                self.nombre.get(),
                self.apellidos.get(),
                self.curp.get(),
                self.categorias_dict[self.categoria.get()],
                int(self.numero_jugador.get()),
                fecha_inscripcion
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Jugador registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el jugador")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar jugador: {str(e)}")

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.apellidos.delete(0, tk.END)
        self.curp.delete(0, tk.END)
        self.categoria.set("Seleccion")
        self.numero_jugador.delete(0, tk.END)
        self.numero_jugador.insert(0, "1")
        self.inscripcion.set_date(datetime.date.today())

class RegistroApp_torneo:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Torneos", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        # Primero crear todos los widgets
        tk.Label(cont_p, text="Nombre del torneo", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.1, anchor=tk.CENTER)
        self.nombre_torneo = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.nombre_torneo.place(relx=0.09, rely=0.15, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Categoria", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.1, anchor=tk.CENTER)
        self.categoria = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.categoria.place(relx=0.59, rely=0.15, relheight=0.06, relwidth=0.35)
        self.categoria.set("Seleccion")
        
        tk.Label(cont_p, text="Cantidad de equipos", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.3, anchor=tk.CENTER)
        self.cantidad_equipos = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.cantidad_equipos.place(relx=0.09, rely=0.35, relheight=0.06, relwidth=0.35)
        self.cantidad_equipos.insert(0, "2")
        
        tk.Label(cont_p, text="Duracion", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.3, anchor=tk.CENTER)
        self.duracion = ctk.CTkComboBox(cont_p, state="readonly", values=["1 semana", "2 semanas", "1 mes", "2 meses", "3 meses"], corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.duracion.place(relx=0.59, rely=0.35, relheight=0.06, relwidth=0.35)
        self.duracion.set("Seleccion")
        
        tk.Label(cont_p, text="Fecha inicial", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.5, anchor=tk.CENTER)
        self.fecha_inicial = DateEntry(cont_p, selectmode='day', locale='es_ES', date_pattern='dd/mm/yyyy', showweeknumbers=False, state='normal')
        self.fecha_inicial.place(relx=0.09, rely=0.55, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Fecha de termino", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.5, anchor=tk.CENTER)
        self.fecha_termino = DateEntry(cont_p, selectmode='day', locale='es_ES', date_pattern='dd/mm/yyyy', showweeknumbers=False, state='normal')
        self.fecha_termino.place(relx=0.59, rely=0.55, relheight=0.06, relwidth=0.35)
        
        rt_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar torneo', t_font=13, fg_font="#FCFCFC", command=self.registrar_torneo)
        rt_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)

        # Luego cargar los datos
        self.cargar_categorias()
        
        # Configurar navegación con Enter
        self.nombre_torneo.bind("<Return>", lambda e: self.categoria.focus())
        self.categoria.bind("<Return>", lambda e: self.cantidad_equipos.focus())
        self.cantidad_equipos.bind("<Return>", lambda e: self.duracion.focus())
        self.duracion.bind("<Return>", lambda e: self.fecha_inicial.focus())
        self.fecha_inicial.bind("<Return>", lambda e: self.fecha_termino.focus())
        self.fecha_termino.bind("<Return>", lambda e: self.registrar_torneo())

    def cargar_categorias(self):
        try:
            categorias = self.db.fetch_all("SELECT ID_Categoria, Nombre FROM CATEGORIA")
            if categorias:
                self.categorias_dict = {nombre: id for id, nombre in categorias}
                self.categoria.configure(values=list(self.categorias_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay categorias registradas en la base de datos")
        except Exception as e:
            print(f"Error al cargar categorias: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorias")

    def registrar_torneo(self):
        try:
            if (not self.nombre_torneo.get() or self.categoria.get() == "Seleccion" or
                self.duracion.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            # Convertir fechas a formato MySQL
            fecha_inicial = self.fecha_inicial.get_date()
            fecha_termino = self.fecha_termino.get_date()
            
            query = """
            INSERT INTO TORNEO (Nombre_torneo, Categoria, Cantidad_Equipos, Duracion, Fecha_Inicial, Fecha_Termino)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            params = (
                self.nombre_torneo.get(),
                self.categorias_dict[self.categoria.get()],
                int(self.cantidad_equipos.get()),
                self.duracion.get(),
                fecha_inicial,
                fecha_termino
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Torneo registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el torneo")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar torneo: {str(e)}")

    def limpiar_campos(self):
        self.nombre_torneo.delete(0, tk.END)
        self.categoria.set("Seleccion")
        self.cantidad_equipos.delete(0, tk.END)
        self.cantidad_equipos.insert(0, "2")
        self.duracion.set("Seleccion")
        self.fecha_inicial.set_date(datetime.date.today())
        self.fecha_termino.set_date(datetime.date.today())

class RegistroApp_profesor:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Profesores", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        # Primero crear todos los widgets
        tk.Label(cont_p, text="Nombre", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.1, anchor=tk.CENTER)
        self.nombre = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.nombre.place(relx=0.09, rely=0.15, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Apellidos", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.1, anchor=tk.CENTER)
        self.apellidos = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.apellidos.place(relx=0.59, rely=0.15, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Categoria", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.3, anchor=tk.CENTER)
        self.categoria = ctk.CTkComboBox(cont_p, state="readonly", corner_radius=10, border_width=2, border_color="#D9D9D9", button_color="#212544", button_hover_color="#FFB93B", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.categoria.place(relx=0.09, rely=0.35, relheight=0.06, relwidth=0.35)
        self.categoria.set("Seleccion")
        
        rp_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar profesor', t_font=13, fg_font="#FCFCFC", command=self.registrar_profesor)
        rp_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)

        # Luego cargar los datos DESPUÉS de crear los widgets
        self.cargar_categorias()
        
        # Configurar navegación con Enter
        self.nombre.bind("<Return>", lambda e: self.apellidos.focus())
        self.apellidos.bind("<Return>", lambda e: self.categoria.focus())
        self.categoria.bind("<Return>", lambda e: self.registrar_profesor())

    def cargar_categorias(self):
        try:
            categorias = self.db.fetch_all("SELECT ID_Categoria, Nombre FROM CATEGORIA")
            if categorias:
                self.categorias_dict = {nombre: id for id, nombre in categorias}
                self.categoria.configure(values=list(self.categorias_dict.keys()))
            else:
                messagebox.showwarning("Advertencia", "No hay categorias registradas en la base de datos")
        except Exception as e:
            print(f"Error al cargar categorias: {e}")
            messagebox.showerror("Error", "No se pudieron cargar las categorias")

    def registrar_profesor(self):
        try:
            if (not self.nombre.get() or not self.apellidos.get() or 
                self.categoria.get() == "Seleccion"):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return

            query = """
            INSERT INTO PROFESORES (Nombre, Apellidos, Categoria)
            VALUES (%s, %s, %s)
            """
            params = (
                self.nombre.get(),
                self.apellidos.get(),
                self.categorias_dict[self.categoria.get()]
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Profesor registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el profesor")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar profesor: {str(e)}")

    def limpiar_campos(self):
        self.nombre.delete(0, tk.END)
        self.apellidos.delete(0, tk.END)
        self.categoria.set("Seleccion")

class RegistroApp_usuario:
    def __init__(self, parent_frame, on_success=None):
        self.frame = parent_frame
        self.db = Database()
        self.on_success = on_success
        
        cont_m = ContR(self.frame, n_rad=14, h=240, w=190, color="#E0E0E0", command=None)
        cont_m.place(relx=0.5, anchor=tk.CENTER, rely=0.414)
        tk.Label(cont_m, bg="#FFB93B").place(relwidth=0.42, relheight=0.162, relx=0.5, rely=0.08, anchor=tk.CENTER)
        TRegPt_lb = tk.Label(cont_m, bg="#212544", text="Registro de Usuarios", font=("Arial", 20, "bold"), fg="#FCFCFC")
        TRegPt_lb.place(relwidth=0.4, relheight=0.16, relx=0.5, rely=0.07, anchor=tk.CENTER)
        
        cont_p = ContR(cont_m, n_rad=14, h=174, w=176, color="#F2F2F2", command=None)
        cont_p.place(relx=0.5, anchor=tk.CENTER, rely=0.57)
        
        tk.Label(cont_p, text="Usuario", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.2, anchor=tk.CENTER)
        self.usuario = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.usuario.place(relx=0.09, rely=0.25, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Email", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.2, anchor=tk.CENTER)
        self.email = ctk.CTkEntry(cont_p, corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.email.place(relx=0.59, rely=0.25, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Password", font=("Arial", 12, "normal"), fg="black", width=30, anchor="w").place(relx=0.28, rely=0.4, anchor=tk.CENTER)
        self.password = ctk.CTkEntry(cont_p, show="*", corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.password.place(relx=0.09, rely=0.45, relheight=0.06, relwidth=0.35)
        
        tk.Label(cont_p, text="Confirmar Password", font=("Arial", 12, "normal"), fg="black", width=21, anchor="w").place(relx=0.72, rely=0.4, anchor=tk.CENTER)
        self.confirm_password = ctk.CTkEntry(cont_p, show="*", corner_radius=10, border_width=2, border_color="#D9D9D9", fg_color="#FFFFFF", text_color="#000000", font=("Arial", 13))
        self.confirm_password.place(relx=0.59, rely=0.45, relheight=0.06, relwidth=0.35)
        
        ru_bn = ContR(cont_p, n_rad=12, h=11, w=10, color="#212544", text='Registrar usuario', t_font=13, fg_font="#FCFCFC", command=self.registrar_usuario)
        ru_bn.place(relx=0.5, anchor=tk.CENTER, rely=0.894)
        
        # Configurar navegación con Enter
        self.usuario.bind("<Return>", lambda e: self.email.focus())
        self.email.bind("<Return>", lambda e: self.password.focus())
        self.password.bind("<Return>", lambda e: self.confirm_password.focus())
        self.confirm_password.bind("<Return>", lambda e: self.registrar_usuario())

    def validar_email(self, email):
        """Valida que el email tenga un formato correcto"""
        # Patrón de expresión regular para validar emails
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(patron, email) is not None
    
    def registrar_usuario(self):
        try:
            if (not self.usuario.get() or not self.email.get() or 
                not self.password.get() or not self.confirm_password.get()):
                messagebox.showerror("Error", "Por favor complete todos los campos")
                return
            
            # Validar formato de email
            if not self.validar_email(self.email.get()):
                messagebox.showerror("Error", "Por favor ingrese un correo electrónico válido\nEjemplo: usuario@ejemplo.com")
                return

            if self.password.get() != self.confirm_password.get():
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return

            # Hashear la contraseña antes de guardarla - DESHABILITADO POR PROBLEMAS CON BCRYPT
            # password_hash = bcrypt.hashpw(self.password.get().encode('utf-8'), bcrypt.gensalt())
            
            query = """
            INSERT INTO USUARIOS (usuario, email, password)
            VALUES (%s, %s, %s)
            """
            params = (
                self.usuario.get(),
                self.email.get(),
                self.password.get()  # Texto plano temporal
                # password_hash.decode('utf-8')  # DESHABILITADO
            )
            
            if self.db.execute_query(query, params):
                messagebox.showinfo("Exito", "Usuario registrado correctamente")
                self.limpiar_campos()
                if self.on_success:
                    self.on_success()
            else:
                messagebox.showerror("Error", "Error al registrar el usuario")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar usuario: {str(e)}")

    def limpiar_campos(self):
        self.usuario.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.confirm_password.delete(0, tk.END)