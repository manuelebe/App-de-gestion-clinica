import tkinter as tk
from tkinter import ttk, messagebox
from main import Usuario, Administrador 
from database import medic_database

class Interfaz:
    def __init__(self, principal):
        self.principal = principal
        self.principal.title("Clínica")
        self.usuario = Usuario()
        self.admin = Administrador()

        #notebook es una funcion para crear pestañas en la misma pagina
        self.notebook = ttk.Notebook(principal)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña inicial
        frame_inicio = tk.Frame(self.notebook)
        tk.Label(frame_inicio, text="Bienvenido a la Clínica").pack(pady=20)
        self.notebook.add(frame_inicio, text="Inicio")

        # Botones para crear pestañas
        self.btn_login = tk.Button(frame_inicio, text="Login", width=20, command=self.crear_login)
        self.btn_login.pack(pady=5)

        self.btn_register = tk.Button(frame_inicio, text="Register", width=20, command=self.crear_register)
        self.btn_register.pack(pady=5)


        # Variables de control (para que solo exista una pestaña de cada tipo)
        self.login_ventana = None
        self.register_ventana = None

    def crear_login(self):
        if self.login_ventana is not None:
            messagebox.showwarning("Aviso", "Ya existe la pestaña de Login. Ciérrala primero.")
            return

        self.login_ventana = tk.Frame(self.notebook)
        tk.Label(self.login_ventana, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(self.login_ventana)
        entry_usuario.pack(pady=5)

        tk.Label(self.login_ventana, text="Contraseña:").pack(pady=5)
        entry_contraseña = tk.Entry(self.login_ventana, show="*")
        entry_contraseña.pack(pady=5)

        def ejecutar_login():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            try:
                rol, nombre = self.usuario.login(usuario, contraseña)
                messagebox.showinfo("Éxito", f"Bienvenido {nombre} ({rol})")
                self.mostrar_panel_usuario(rol, nombre)
            except Exception as e:
                messagebox.showerror("Error hubo un problema", str(e))

        tk.Button(self.login_ventana, text="Iniciar Sesion", command=ejecutar_login).pack(pady=10)
        tk.Button(self.login_ventana, text="Cerrar pestaña", command=self.cerrar_login).pack(pady=10)

        self.notebook.add(self.login_ventana, text="Login")
        self.notebook.select(self.login_ventana)

    def cerrar_login(self):
        if self.login_ventana is not None:
            self.notebook.forget(self.login_ventana)
            self.login_ventana.destroy()
            self.login_ventana = None

    
    def mostrar_panel_usuario(self, rol, nombre):
        panel = tk.Frame(self.notebook)
        tk.Label(panel, text=f"Usuario: {nombre}").pack(pady=10)

        if rol == "usuario":
            tk.Label(panel, text="Opciones disponibles:").pack()
            tk.Button(panel, text="Ver Médicos", command=self.disponibilidad_medicos).pack(pady=5)
            tk.Button(panel, text="Solicitar Turno", command=self.solicitar_turno).pack(pady=5)
        elif rol == "admin":
            tk.Label(panel, text="Opciones de administrador:").pack()
            tk.Button(panel, text="Agregar Médico", command=self.agregar_medico).pack(pady=5)
            tk.Button(panel, text="Modificar Médico", command=self.modificar_medico).pack(pady=5)
            tk.Button(panel, text="Eliminar Médico", command=self.eliminar_medico).pack(pady=5)

        def cerrar_panel():
            self.notebook.forget(panel)
            panel.destroy()

        tk.Button(panel, text="Cerrar pestaña", command=cerrar_panel).pack(pady=10)

        self.notebook.add(panel, text=f"Panel {nombre}")
        self.notebook.select(panel)


    def crear_register(self):
        if self.register_ventana is not None:
            messagebox.showwarning("Aviso", "Ya existe la pestaña de Registro. Ciérrala primero.")
            return

        self.register_ventana = tk.Frame(self.notebook)
        tk.Label(self.register_ventana, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(self.register_ventana)
        entry_usuario.pack(pady=5)

        tk.Label(self.register_ventana, text="Contraseña:").pack(pady=5)
        entry_contraseña = tk.Entry(self.register_ventana, show="*")
        entry_contraseña.pack(pady=5)


        def ejecutar_register():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            try:
                resultado = self.usuario.registrar(usuario, contraseña)
                messagebox.showinfo("Éxito", resultado)
            except Exception as e:
                messagebox.showerror("Error hubo un problema", str(e))

        tk.Button(self.register_ventana, text="Registrar", command=ejecutar_register).pack(pady=10)
        tk.Button(self.register_ventana, text="Cerrar pestaña", command=self.cerrar_register).pack(pady=10)

        self.notebook.add(self.register_ventana, text="Register")
        self.notebook.select(self.register_ventana)

    def cerrar_register(self):
        if self.register_ventana is not None:
            self.notebook.forget(self.register_ventana)
            self.register_ventana.destroy()
            self.register_ventana = None

    def agregar_medico(self):
        top = tk.Toplevel(self.principal); top.title("Agregar Médico")
        tk.Label(top, text="Nombre:").grid(row=0, column=0); entry_nombre = tk.Entry(top); entry_nombre.grid(row=0, column=1)
        tk.Label(top, text="Especialidad:").grid(row=1, column=0); entry_esp = tk.Entry(top); entry_esp.grid(row=1, column=1)
        tk.Label(top, text="Dias:").grid(row=2, column=0); entry_dias = tk.Entry(top); entry_dias.grid(row=2, column=1)
        tk.Label(top, text="Horarios (ej: 9-12,14-18):").grid(row=3, column=0); entry_hor = tk.Entry(top); entry_hor.grid(row=3, column=1)

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

        tk.Button(top, text="Guardar", command=guardar).grid(row=4, column=0, columnspan=2)

    def modificar_medico(self):
        pass

    def eliminar_medico(self):
        pass

    def disponibilidad_medicos(self): 
        pass 
    def solicitar_turno(self):
        pass

if __name__ == "__main__":
    principal = tk.Tk()
    app = Interfaz(principal)
    principal.mainloop()
