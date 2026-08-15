import tkinter as tk
from tkinter import ttk, messagebox
from main import Usuario, Administrador, Main

class Interfaz:
    def __init__(self, principal):
        self.principal = principal
        self.principal.title("Clínica")
        self.usuario = Usuario()
        self.admin = Administrador()

        # notebook es una funcion para crear pestañas en la misma pagina
        self.notebook = ttk.Notebook(principal)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña inicial
        frame_inicio = tk.Frame(self.notebook, bg="#E6F2F8")
        self.notebook.add(frame_inicio, text="Inicio")

      
        # --- Encabezado ---
        header_frame = tk.Frame(frame_inicio, bg="#E6F2F8")
        header_frame.pack(fill="x")

        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20)

        menu = tk.Label(header_frame, text="Inicio", font=("Roboto", 12), bg="#E6F2F8", fg="#004466")
        menu.pack(side="right", padx=20)

        # --- Contenido central ---
        content_frame = tk.Frame(frame_inicio, bg="#E6F2F8")
        content_frame.pack(expand=True)

        title = tk.Label(content_frame, text="Bienvenido a la Clínica", font=("Roboto", 20, "bold"), bg="#E6F2F8", fg="#003366")
        title.pack(pady=(20, 10))

        subtitle = tk.Label(content_frame, text="Gestione sus turnos y su historial médico fácilmente",
                            font=("Roboto", 12), bg="#E6F2F8", fg="#333333")
        subtitle.pack(pady=(0, 20))
        
        # Botones para crear pestañas
        self.btn_login = tk.Button(content_frame, text="🔑 Iniciar sesión", font=("Roboto", 12, "bold"),
                      bg="#007ACC", fg="white", width=20, relief="flat", cursor="hand2", command=self.crear_login)
        self.btn_login.pack(pady=10)
        

        self.btn_register = tk.Button(content_frame,text="🩺 Registrarse", font=("Roboto", 12, "bold"),
                         bg="#00A86B", fg="white", width=20, relief="flat", cursor="hand2", command=self.crear_register)
        self.btn_register.pack(pady=10) 

        
        # ------Animaciones Hover-------
        def on_enter(e):
            e.widget['background'] = '#005F99'

        def on_leave(e):
            e.widget['background'] = '#007ACC'

        self.btn_login.bind("<Enter>", on_enter)
        self.btn_login.bind("<Leave>", on_leave)

        def on_enter_reg(e):
            e.widget['background'] = '#008F5A'

        def on_leave_reg(e):
            e.widget['background'] = '#00A86B'

        self.btn_register.bind("<Enter>", on_enter_reg)
        self.btn_register.bind("<Leave>", on_leave_reg)

        # --- footer---
        footer = tk.Label(frame_inicio, text="Tu salud, nuestra prioridad", font=("Roboto", 10, "italic"),
                          bg="#E6F2F8", fg="#555555")
        footer.pack(side="bottom", pady=10)
        

        # Variables de control (para que solo exista una pestaña de cada tipo)
        self.login_ventana = None
        self.register_ventana = None

    def crear_login(self):
        if self.login_ventana is not None:
            messagebox.showwarning("Aviso", "Ya existe la pestaña de Login. Ciérrala primero.")
            return

        # Frame principal de la pestaña
        self.login_ventana = tk.Frame(self.notebook, bg="#E6F2F8")

        header_frame = tk.Frame(self.login_ventana, bg="#E6F2F8")
        header_frame.pack(fill="x")

        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20)

        menu = tk.Label(header_frame, text="Login", font=("Roboto", 12), bg="#E6F2F8", fg="#004466")
        menu.pack(side="right", padx=20)

        # Frame interno con tamaño fijo
        content_frame = tk.Frame(self.login_ventana, bg="white", width=450, height=450, bd=2, relief="solid")
        content_frame.pack(expand=True)
        content_frame.pack_propagate(False)  # evita que crezca más allá del tamaño fijo

        # --- Contenido dentro del frame limitado ---
        titulo = tk.Label(content_frame, text="Iniciar Sesión",
                         font=("Segoe UI", 16, "bold"), fg="#004080", bg="white")
        titulo.pack(pady=(15, 5))

        subtitulo = tk.Label(content_frame,text="Acceda a su cuenta para gestionar turnos y su historial médico", 
                             font=("Segoe UI", 9), fg="#555", bg="white", wraplength=350, justify="center")
        subtitulo.pack(pady=(0, 10))
        
        # Usuario
        tk.Label(content_frame, text="Usuario", font=("Roboto", 11), bg="white", fg="#333333").pack(anchor="w", padx=20, pady=(5, 2))
        entry_usuario = ttk.Entry(content_frame, font=("Roboto", 12))
        entry_usuario.pack(fill="x", padx=20, pady=(0, 10))

        # Contraseña
        tk.Label(content_frame, text="Contraseña", font=("Roboto", 11), bg="white", fg="#333333").pack(anchor="w", padx=20, pady=(5, 2))
        entry_contraseña = ttk.Entry(content_frame, show="*", font=("Roboto", 12))
        entry_contraseña.pack(fill="x", padx=20, pady=(0, 10))

        def ejecutar_login():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            try:
                rol, nombre = self.usuario.login(usuario, contraseña)
                messagebox.showinfo("Éxito", f"Bienvenido {nombre} ({rol})")
                self.cerrar_login()
                self.mostrar_panel_usuario(rol, nombre)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        register = tk.Label(content_frame, text="¿Aún no tienes cuenta?",
                                font=("Segoe UI", 9, "underline"), fg="#28a745",
                                bg="white", cursor="hand2")
        register.pack()
        register.bind("<Button-1>", lambda e: self.crear_register()) #Funcion encargada de si se realiza algun click en el label "¿Aún no tienes cuenta?", llama a la funcion crear_register
        
        tk.Button(content_frame, text="Iniciar sesión", bg="#007BFF", fg="white", font=("Segoe UI", 10, "bold"), 
                  relief="flat", command=ejecutar_login).pack(pady=(25, 0), fill="x", padx=20)
        

        tk.Button(content_frame, text="❌ Cerrar pestaña", bg="#BE0606", fg="white", 
                  font=("Segoe UI", 10, "bold"), relief="flat", command=self.cerrar_login).pack(pady=(10), fill="x", padx=20)

        self.notebook.add(self.login_ventana, text="Login")
        self.notebook.select(self.login_ventana)

    def cerrar_login(self):
        if self.login_ventana is not None:
            self.notebook.forget(self.login_ventana)
            self.login_ventana.destroy()
            self.login_ventana = None

    def mostrar_panel_usuario(self, rol, nombre):
        panel_user = tk.Frame(self.notebook, bg="#E6F2F8")  # Fondo suave

        # Encabezado con estilo
        header_frame = tk.Frame(panel_user, bg="#E6F2F8")
        header_frame.pack(fill="x")

        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20)

        menu = tk.Label(header_frame, text="Cuenta", font=("Roboto", 12), bg="#E6F2F8", fg="#004466")
        menu.pack(side="right", padx=20)

        
        tk.Label(panel_user, text=f"👤 Usuario: {nombre}",
                 font=("Arial", 14, "bold"), bg="#E6F2F8", fg="#2c3e50").pack(pady=10)

        # Linea 
        ttk.Separator(panel_user, orient="horizontal").pack(fill="x", padx=20, pady=5)

        #Le agregue emojis porque quedaba fachero pero con el bold se ven feos, se pueden borrar si se desea
        if rol == "Usuario":
            tk.Label(panel_user, text="Opciones disponibles:", font=("Arial", 13, "italic"), bg="#E6F2F8").pack(pady=5)

            tk.Button(panel_user, text="🩺 Ver Médicos", command=self.disponibilidad_medicos,
                      bg="#42A5F5", fg="white", relief="raised", width=25, font=("Segoe UI", 10, "bold")).pack(pady=5)

            tk.Button(panel_user, text="📅 Solicitar Turno", command=self.solicitar_turno,
                      bg="#66BB6A", fg="white", relief="raised", width=25, font=("Segoe UI", 10, "bold")).pack(pady=5)

        elif rol == "Admin":
            tk.Label(panel_user, text="⚙️ Opciones de administrador:", font=("Arial", 12, "italic"), bg="#E6F2F8").pack(pady=5)

            tk.Button(panel_user, text="➕ Agregar Médico", command=self.agregar_medico,
                      bg="#4CAF50", fg="white", relief="raised", width=25, font=("Segoe UI", 10, "bold")).pack(pady=5)

            tk.Button(panel_user, text="✏️ Modificar Médico", command=self.modificar_medico,
                      bg="#F58C46", fg="white", relief="raised", width=25, font=("Segoe UI", 10, "bold")).pack(pady=5)

            tk.Button(panel_user, text="🗑️ Eliminar Médico", command=self.eliminar_medico,
                      bg="#E53935", fg="white", relief="raised", width=25, font=("Segoe UI", 10, "bold")).pack(pady=5)

        # Linea 
        ttk.Separator(panel_user, orient="horizontal").pack(fill="x", padx=20, pady=10)

        def cerrar_panel():
            self.notebook.forget(panel_user)
            panel_user.destroy()

        tk.Button(panel_user, text="❌ Cerrar pestaña", bg="#BE0606", fg="white", width=25, font=("Segoe UI", 10, "bold"), relief="flat", command=cerrar_panel).pack(pady=10)
        
        # Agregar la pestaña al notebook
        self.notebook.add(panel_user, text=f"Panel {nombre}")
        self.notebook.select(panel_user)

    def crear_register(self):
        if self.register_ventana is not None:
            messagebox.showwarning("Aviso", "Ya existe la pestaña de Registro. Ciérrala primero.")
            return

        # Pestaña principal
        self.register_ventana = tk.Frame(self.notebook, bg="#E6F2F8")

        header_frame = tk.Frame(self.register_ventana, bg="#E6F2F8")
        header_frame.pack(fill="x")

        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20)

        menu = tk.Label(header_frame, text="Register", font=("Roboto", 12), bg="#E6F2F8", fg="#004466")
        menu.pack(side="right", padx=20)

        # Frame interno con tamaño fijo
        content_frame = tk.Frame(self.register_ventana, bg="#F8FBFF", width=450, height=450, bd=2, relief="solid")
        content_frame.pack(expand=True)
        content_frame.pack_propagate(False)  # evita que se expanda más allá del tamaño fijo

        # --- Contenido ---
        titulo = tk.Label(content_frame, text="Registresé",
                         font=("Segoe UI", 16, "bold"), fg="#004080", bg="#F8FBFF")
        titulo.pack(pady=(15, 5))

        subtitulo = tk.Label(content_frame,
                            text="Cree su cuenta para gestionar turnos y su historial médico",
                            font=("Segoe UI", 9), fg="#555", bg="#F8FBFF", wraplength=350, justify="center")
        subtitulo.pack(pady=(0, 5))

        # Usuario
        tk.Label(content_frame, text="Usuario", font=("Roboto", 11), bg="#F8FBFF", fg="#333333").pack(anchor="w", padx=20, pady=(5, 2))
        entry_usuario = ttk.Entry(content_frame, font=("Roboto", 12))
        entry_usuario.pack(fill="x", padx=20, pady=(0, 10))

        # Contraseña
        tk.Label(content_frame, text="Contraseña", font=("Roboto", 11), bg="#F8FBFF", fg="#333333").pack(anchor="w", padx=20, pady=(5, 2))
        entry_contraseña = ttk.Entry(content_frame, show="*", font=("Roboto", 12))
        entry_contraseña.pack(fill="x", padx=20, pady=(0, 10))

        # Confirmar contraseña OPCIONAL
        tk.Label(content_frame, text="Confirmar Contraseña", font=("Roboto", 11), bg="#F8FBFF", fg="#333333").pack(anchor="w", padx=20, pady=(5, 2))
        entry_confirmar = ttk.Entry(content_frame, show="*", font=("Roboto", 12))
        entry_confirmar.pack(fill="x", padx=20, pady=(0, 10))

        # Función de registro
        def ejecutar_register():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            confirmar = entry_confirmar.get()
            if contraseña != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            try:
                resultado = self.usuario.registrar(usuario, contraseña)
                messagebox.showinfo("Éxito", resultado)
                self.cerrar_register()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Botones más abajo para mejor distribución
        tk.Button(content_frame, text="Registrarse", bg="#00A86B", fg="white", font=("Segoe UI", 10, "bold"), 
                  relief="flat", command=ejecutar_register).pack(pady=(20, 0), fill="x", padx=20)

        tk.Button(content_frame, text="❌ Cerrar pestaña", bg="#BE0606", fg="white", font=("Segoe UI", 10, "bold"), 
                  relief="flat", command=self.cerrar_register).pack(pady=(10), fill="x", padx=20)

        # Agregar al notebook
        self.notebook.add(self.register_ventana, text="Register")
        self.notebook.select(self.register_ventana)

    def cerrar_register(self):
        if self.register_ventana is not None:
            self.notebook.forget(self.register_ventana)
            self.register_ventana.destroy()
            self.register_ventana = None
            
    # Todo debería funcionar de aca para arriba, menos las funcionalidades de los botones de mostrar_panel_usuario.

    def agregar_medico(self):
        top = tk.Toplevel(self.principal)
        top.title("Agregar Médico")
        top.geometry("400x250")
        top.resizable(False, False)

        # Etiquetas y entradas
        tk.Label(top, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_nombre = tk.Entry(top, width=30)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(top, text="Especialidad:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_esp = tk.Entry(top, width=30)
        entry_esp.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(top, text="Días:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_dias = tk.Entry(top, width=30)
        entry_dias.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(top, text="Horarios (ej: 9-12,14-18):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_hor = tk.Entry(top, width=30)
        entry_hor.grid(row=3, column=1, padx=10, pady=5)

    
        def guardar():
            try:
                nombre = entry_nombre.get().strip()
                especialidad = entry_esp.get().strip()
                dias = [d.strip() for d in entry_dias.get().split(",")]
                horarios = [(int(h.split("-")[0]), int(h.split("-")[1])) for h in entry_hor.get().split(",")]
                self.admin.añadir_medico(nombre, especialidad, dias, horarios)
                messagebox.showinfo("Exito", f"Médico {nombre} agregado")
                top.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

         # Botón Guardar
        btn_guardar = tk.Button(top, text="Guardar", width=15, bg="#4CAF50", fg="white", command=guardar)
        btn_guardar.grid(row=4, column=1, columnspan=2, pady=25)

    def modificar_medico(self):
        pass

    def eliminar_medico(self):
        pass

    def disponibilidad_medicos(self): 
        pass 
    def solicitar_turno(self):
        pass

if __name__ == "__main__":
    main = Main()
    main.cargar_medicos()
    principal = tk.Tk()
    principal.geometry("650x450")
    app = Interfaz(principal) 
    principal.mainloop() 
