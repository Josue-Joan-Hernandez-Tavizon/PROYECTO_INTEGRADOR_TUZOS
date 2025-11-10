from src.controllers.auth_controller import validar_credenciales
from src.components.plantilla import plantilla_f
from tkinter import messagebox
from PIL import ImageTk, Image
from src.components.panel_r import PanelR
from src.components.cont_r import ContR
import tkinter as tk
import customtkinter as ctk
import pywinstyles

class LoginApp(plantilla_f):
    def __init__(self, root_p, on_login_success=None):
        plantilla_f.__init__(self, root_p)
        self.on_login_success = on_login_success
        self.root_p = root_p
        
        panel_prin = PanelR(self.frame_prin, self.root.winfo_width()*0.4, self.root.winfo_height()*0.64, 12, 10, "#E6E6E6", "#E6E6E6")
        panel_prin.place(relx=0.5, anchor=tk.CENTER, y=320)
        
        lb_us = tk.Label(self.frame_prin, text=" Usuario ", font=("Arial", 12, "normal"), bg="#D9D9D9", fg="#000000", width=15)
        pywinstyles.set_opacity(lb_us, value=0.8, color="#D9D9D9")
        lb_us.place(relx=0.5, anchor=tk.CENTER, y=240)
        
        try:
            us_icon = ImageTk.PhotoImage(Image.open("assets\\imagenes\\log_ust.png").resize((140,140), Image.LANCZOS))
            us_icon_lb = tk.Label(self.frame_prin, image=us_icon, bg="#E8E8E8")
            us_icon_lb.image = us_icon
            pywinstyles.set_opacity(us_icon_lb, value=0.7, color="#E8E8E8")
            us_icon_lb.place(relx=0.5, y=158, anchor='center')
        except:
            pass
        
        us_lb = tk.Label(self.frame_prin, text="Usuario:", font=("Arial", 14,), bg="white")
        us_lb.place(relx=0.38, anchor=tk.CENTER, y=270)
        pywinstyles.set_opacity(us_lb, color="white")
        
        cont_nus = ContR(self.frame_prin, n_rad=10, h=10, w=100, color="#D9D9D9", text="", command=None)
        cont_nus.place(relx=0.5, anchor=tk.CENTER, y=310)
        self.entry_us = ctk.CTkEntry(
            cont_nus, 
            placeholder_text="Ingrese su usuario",
            corner_radius=10,
            border_width=0,
            fg_color="#D9D9D9",
            text_color="#000000",
            placeholder_text_color="#808080",
            font=("Arial", 13),
            width=400,
            height=35
        )
        self.entry_us.place(relx=0.5, anchor=tk.CENTER, rely=0.5)
        
        pass_lb = tk.Label(self.frame_prin, text="Contraseña:", font=("Arial", 14,), bg="white")
        pass_lb.place(relx=0.39, anchor=tk.CENTER, y=360)
        pywinstyles.set_opacity(pass_lb, color="white")
        
        cont_pass = ContR(self.frame_prin, n_rad=10, h=10, w=100, color="#D9D9D9", text="", command=None)
        cont_pass.place(relx=0.5, anchor=tk.CENTER, y=400)
        self.entry_pass = ctk.CTkEntry(
            cont_pass, 
            placeholder_text="Ingrese su contraseña",
            corner_radius=10,
            border_width=0,
            fg_color="#D9D9D9",
            text_color="#000000",
            placeholder_text_color="#808080",
            font=("Arial", 13),
            show="*",
            width=400,
            height=35
        )
        self.entry_pass.place(relx=0.5, anchor=tk.CENTER, rely=0.5)
        
        # Botón para mostrar/ocultar contraseña
        self.password_visible = False
        self.btn_toggle_password = ctk.CTkButton(
            cont_pass,
            text="🔒",
            width=35,
            height=35,
            corner_radius=10,
            fg_color="#3B5998",
            hover_color="#2D4373",
            font=("Arial", 16),
            command=self.toggle_password_visibility
        )
        self.btn_toggle_password.place(relx=0.95, anchor=tk.CENTER, rely=0.5)
        
        ContR(self.frame_prin, n_rad=12, h=10, w=16, color="#FFFFFF", text="Cancelar ", t_font=11, command=self.cancelar).place(relx=0.5, anchor=tk.CENTER, y=472)
        
        self.bt_conf = ContR(self.frame_prin, n_rad=12, h=10, w=16, color="#212544", text="Aceptar ", t_font=11, fg_font="white", command=self.login)
        self.bt_conf.place(relx=0.603, anchor=tk.CENTER, y=472)
        
        self.fondo_lb.pack()
        
        # Binding para pasar al campo de contraseña con Enter
        self.entry_us.bind('<Return>', lambda event: self.entry_pass.focus())
        self.entry_pass.bind('<Return>', lambda event: self.login())
        
        # Binding para mostrar contraseña mientras se presiona '|' (pipe)
        def mostrar_pass(event):
            self.entry_pass.configure(show="")
            return "break"  # Evita que se escriba el carácter
        
        def ocultar_pass(event):
            self.entry_pass.configure(show="*")
            return "break"
        
        self.entry_pass.bind('<KeyPress-bar>', mostrar_pass)  # | key
        self.entry_pass.bind('<KeyRelease-bar>', ocultar_pass)
    
    def login(self):
        usuario = self.entry_us.get().strip()
        password = self.entry_pass.get().strip()
        
        if not (usuario and password):
            messagebox.showinfo(title="Ups... algo salio mal *^* ", 
                              message="Faltan datos. Favor de ingresar usuario y contraseña")
            return
        
        if validar_credenciales(usuario, password):
            messagebox.showinfo(title="Acceso permitido", 
                              message=f"Bienvenido {usuario}")
            if self.on_login_success:
                self.on_login_success(usuario)
        else:
            messagebox.showerror(title="Acceso denegado", 
                               message="Tus credenciales son incorrectas")
    
    def toggle_password_visibility(self):
        """Alterna entre mostrar y ocultar la contraseña"""
        if self.password_visible:
            # Ocultar contraseña
            self.entry_pass.configure(show="*")
            self.btn_toggle_password.configure(text="🔒")
            self.password_visible = False
        else:
            # Mostrar contraseña
            self.entry_pass.configure(show="")
            self.btn_toggle_password.configure(text="🔓")
            self.password_visible = True
    
    def cancelar(self):
        self.root.destroy()

# Función independiente para usar solo el login
def iniciar_login(on_login_success=None):
    root = tk.Tk() 
    app = LoginApp(root, on_login_success)
    img = tk.PhotoImage(file="assets\\imagenes\\icon_fb.png")
    root.iconphoto(True, img)
    pywinstyles.change_header_color(root, color="black")
    root.mainloop()

# Para uso independiente
if __name__ == "__main__":
    def on_login(usuario):
        print(f"Login exitoso: {usuario}")
        # Aquí puedes abrir tu menú principal
    
    iniciar_login(on_login)