import tkinter as tk
from tkinter import ttk, messagebox
from database import cargar_datos
from main import Usuario, Administrador, Paciente, Main

class Interfaz:
    def __init__(self, principal):
        cargar_datos()
        self.principal = principal
        self.principal.title("Clínica - Sistema Médico")
        self.usuario = Usuario()
        self.admin = Administrador()
        self.paciente = Paciente()

        # notebook es una funcion para crear pestañas en la misma pagina
        self.notebook = ttk.Notebook(principal)
        self.notebook.pack(expand=True, fill="both")

        # Pestaña inicial
        frame_inicio = tk.Frame(self.notebook, bg="#E6F2F8")
        self.notebook.add(frame_inicio, text="Inicio")

        # --- Encabezado ---
        header_frame = tk.Frame(frame_inicio, bg="#E6F2F8")
        header_frame.pack(fill="x")

        #Logo
        tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466").pack(side="left", padx=20, pady=10)


         # --- Contenido central ---
        content_frame = tk.Frame(frame_inicio, bg="#E6F2F8")
        content_frame.pack(expand=True)

        tk.Label(content_frame, text="Bienvenido a la Clínica", font=("Roboto", 20, "bold"), bg="#E6F2F8", fg="#003366").pack(pady=(20, 10))
        tk.Label(content_frame, text="Gestione sus turnos e información desde un solo lugar", font=("Roboto", 12), bg="#E6F2F8", fg="#333333").pack(pady=(0, 20))

        # Botones de inicio sesion y register
        btn_login = tk.Button(content_frame, text="🔑 Iniciar sesión", font=("Roboto", 12, "bold"), bg="#007ACC", fg="white", width=20, relief="flat", cursor="hand2", command=self.crear_login)
        btn_login.pack(pady=10)

        btn_register = tk.Button(content_frame, text="🩺 Registrarse", font=("Roboto", 12, "bold"), bg="#00A86B", fg="white", width=20, relief="flat", cursor="hand2", command=self.crear_register)
        btn_register.pack(pady=10)


    # ------Animaciones Hover-------
        def on_enter(e):
            e.widget['background'] = '#005F99'

        def on_leave(e):
            e.widget['background'] = '#007ACC'

        btn_login.bind("<Enter>", on_enter)
        btn_login.bind("<Leave>", on_leave)

        def on_enter_reg(e):
            e.widget['background'] = '#008F5A'

        def on_leave_reg(e):
            e.widget['background'] = '#00A86B'

        btn_register.bind("<Enter>", on_enter_reg)
        btn_register.bind("<Leave>", on_leave_reg)

    # Variables de control (para que solo exista una pestaña de cada tipo)
        self.login_ventana = None
        self.register_ventana = None

    def crear_login(self):
        if self.login_ventana is not None:
            messagebox.showwarning("Aviso", "La pestaña de Login ya está abierta.")
            return

        # Frame principal de la pestaña del login
        self.login_ventana = tk.Frame(self.notebook, bg="#E6F2F8")

        header_frame = tk.Frame(self.login_ventana, bg="#E6F2F8")
        header_frame.pack(fill="x")
        
        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20, pady=10)

        # Frame interno con tamaño fijo
        frame_contenido = tk.Frame(self.login_ventana, bg="white", width=400, height=350, bd=1, relief="solid")
        frame_contenido.pack(expand=True, pady=20)
        frame_contenido.pack_propagate(False)# evita que crezca más allá del tamaño fijo

        tk.Label(frame_contenido, text="Iniciar Sesión", font=("Segoe UI", 16, "bold"), fg="#004080", bg="white").pack(pady=(20, 10))

        tk.Label(frame_contenido,text="Acceda a su cuenta para gestionar turnos y su historial médico", 
        font=("Segoe UI", 9), fg="#555", bg="white", wraplength=350, justify="center").pack(pady=(0, 10))

        tk.Label(frame_contenido, text="Usuario", font=("Roboto", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))

        entry_usuario = ttk.Entry(frame_contenido, font=("Roboto", 11))
        entry_usuario.pack(fill="x", padx=30, pady=(0, 10))

        tk.Label(frame_contenido, text="Contraseña", font=("Roboto", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))

        entry_contraseña = ttk.Entry(frame_contenido, show="*", font=("Roboto", 11))
        entry_contraseña.pack(fill="x", padx=30, pady=(0, 15))

        def ejecutar_login():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            try:
                rol, nombre = self.usuario.login(usuario, contraseña)
                messagebox.showinfo("Éxito", f"Bienvenido/a {nombre} ({rol})")
                self.cerrar_login()

                if rol == "Admin":
                    self.mostrar_panel_admin(nombre)
                else:
                    self.mostrar_panel_usuario(nombre)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame_contenido, text="Iniciar sesión", bg="#007BFF", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=ejecutar_login).pack(fill="x", padx=30, pady=5)
        tk.Button(frame_contenido, text="Cerrar pestaña", bg="#BE0606", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=self.cerrar_login).pack(fill="x", padx=30, pady=5)

        #Se agrega como pestaña de login en el paartado de notebook
        self.notebook.add(self.login_ventana, text="Login")
        self.notebook.select(self.login_ventana)

    def cerrar_login(self):
        if self.login_ventana is not None:
            self.notebook.forget(self.login_ventana)
            self.login_ventana.destroy()
            self.login_ventana = None

    def crear_register(self):
        if self.register_ventana is not None:
            messagebox.showwarning("Aviso", "La pestaña de Registro ya está abierta.")
            return
        
        # Pestaña principal
        self.register_ventana = tk.Frame(self.notebook, bg="#E6F2F8")
        
        header_frame = tk.Frame(self.register_ventana, bg="#E6F2F8")
        header_frame.pack(fill="x")
                
        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20, pady=10)

        frame_contenido = tk.Frame(self.register_ventana, bg="white", width=400, height=380, bd=1, relief="solid")
        frame_contenido.pack(expand=True, pady=20)
        frame_contenido.pack_propagate(False)

        tk.Label(frame_contenido, text="Registrarse", font=("Segoe UI", 16, "bold"), fg="#004080", bg="white").pack(pady=(15, 5))

        tk.Label(frame_contenido, text="Usuario", font=("Roboto", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))
        entry_usuario = ttk.Entry(frame_contenido, font=("Roboto", 11))
        entry_usuario.pack(fill="x", padx=30, pady=(0, 5))

        tk.Label(frame_contenido, text="Contraseña", font=("Roboto", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))
        entry_contraseña = ttk.Entry(frame_contenido, show="*", font=("Roboto", 11))
        entry_contraseña.pack(fill="x", padx=30, pady=(0, 5))

        tk.Label(frame_contenido, text="Confirmar Contraseña", font=("Roboto", 10), bg="white").pack(anchor="w", padx=30, pady=(5, 2))
        entry_confirmar = ttk.Entry(frame_contenido, show="*", font=("Roboto", 11))
        entry_confirmar.pack(fill="x", padx=30, pady=(0, 10))

        # Función de registro
        def ejecutar_register():
            usuario = entry_usuario.get().strip()
            contraseña = entry_contraseña.get()
            confirmar = entry_confirmar.get()

            if contraseña != confirmar:
                messagebox.showerror("Error", "Las contraseñas no coinciden")
                return
            try:
                res = self.usuario.registrar(usuario, contraseña)
                messagebox.showinfo("Éxito", res)
                self.cerrar_register()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame_contenido, text="Registrarse", bg="#00A86B", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=ejecutar_register).pack(fill="x", padx=30, pady=5)
        tk.Button(frame_contenido, text="Cerrar pestaña", bg="#BE0606", fg="white", font=("Segoe UI", 10, "bold"), relief="flat", command=self.cerrar_register).pack(fill="x", padx=30, pady=5)

    #Se agrega como pestaña de login en el paartado de notebook
        self.notebook.add(self.register_ventana, text="Registro")
        self.notebook.select(self.register_ventana)

    def cerrar_register(self):
        if self.register_ventana is not None:
            self.notebook.forget(self.register_ventana)
            self.register_ventana.destroy()
            self.register_ventana = None

    def mostrar_panel_admin(self, nombre):
        panel_admin = tk.Frame(self.notebook, bg="#E6F2F8")

        header_admin = tk.Frame(panel_admin, bg="#E6F2F8")
        header_admin.pack(fill="x", padx=10, pady=5)

        tk.Label(header_admin, text=f"⚙️ Panel de Gestión Administrativa - Admin: {nombre}",
                 font=("Roboto", 13, "bold"), bg="#E6F2F8", fg="#003366").pack(side="left")

        def salir_admin():
            self.notebook.forget(panel_admin)
            panel_admin.destroy()

        btn_cerrar = tk.Button(header_admin, text=" ❌ ", bg="#E53935", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=salir_admin) 
        btn_cerrar.pack(side="right", padx=5)

        #Cuerpo
        contendor_main = tk.Frame(panel_admin, bg="#E6F2F8")
        contendor_main.pack(fill="both", expand=True, padx=10, pady=10)

        #Tabla con los medicos
        frame_tabla = tk.Frame(contendor_main)
        frame_tabla.pack(side="left", fill="both", expand=True, padx=5)

        #Se crea una tabla y se le da efectos, headings solo salen lo solicitado
        columnas = ("ID", "Nombre", "Especialidad", "Días", "Horarios")
        contenido = ttk.Treeview(frame_tabla, columns=columnas, show="headings") 

        for col in columnas:
            contenido.heading(col, text=col)
            contenido.column(col, width=90)
        
        barra_scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=contenido.yview)
        contenido.configure(yscrollcommand=barra_scroll.set)
        barra_scroll.pack(side="right", fill="y")
        contenido.pack(side="left", fill="both", expand=True)

        #Se establece el frame a la derecha para modificar, ingresar y elimar medicos
        frame_modif = tk.Frame(contendor_main, bg="white", bd=1, relief="solid", padx=10, pady=10)
        frame_modif.pack(side="right", fill="y", padx=5)

        tk.Label(frame_modif, text="Gestión de Médicos", font=("Roboto", 11, "bold"), bg="white", fg="#004080").pack(pady=5)

        tk.Label(frame_modif, text="Nombre:", bg="white").pack(anchor="w")
        entry_nombre = ttk.Entry(frame_modif, width=28)
        entry_nombre.pack(fill="x", pady=2)

        tk.Label(frame_modif, text="Especialidad:", bg="white").pack(anchor="w")
        entry_esp = ttk.Entry(frame_modif, width=28)
        entry_esp.pack(fill="x", pady=2)

        tk.Label(frame_modif, text="Días de atención:", bg="white").pack(anchor="w")
        entry_dias = ttk.Entry(frame_modif, width=28)
        entry_dias.pack(fill="x", pady=2)

        tk.Label(frame_modif, text="Horarios:", bg="white").pack(anchor="w")
        entry_hor = ttk.Entry(frame_modif, width=28)
        entry_hor.pack(fill="x", pady=2)

        selected_id = [None]

        def cargar_tabla():
            for fila in contenido.get_children():
                contenido.delete(fila)
            #Se obtine una tupla "m" y se la inserta como fila
            for m in self.admin.obtener_medicos():
                contenido.insert("", tk.END, values=m)

        def seleccionar_registro(event):
            valor = contenido.selection()
            if valor:
                valores = contenido.item(valor[0], "values") #obtenemos la tupla de contenido, el values = m
                selected_id[0] = valores[0]
                entry_nombre.delete(0, tk.END); entry_nombre.insert(0, valores[1])
                entry_esp.delete(0, tk.END); entry_esp.insert(0, valores[2])
                entry_dias.delete(0, tk.END); entry_dias.insert(0, valores[3])
                entry_hor.delete(0, tk.END); entry_hor.insert(0, valores[4])

        contenido.bind("<<TreeviewSelect>>", seleccionar_registro)

        def limpiar_campos():
            selected_id[0] = None
            entry_nombre.delete(0, tk.END)
            entry_esp.delete(0, tk.END)
            entry_dias.delete(0, tk.END)
            entry_hor.delete(0, tk.END)

        def btn_agregar():
            if not entry_nombre.get():
                messagebox.showwarning("Aviso", "Ingrese al menos el nombre.")
                return
            try:
                self.admin.añadir_medico(entry_nombre.get(), entry_esp.get(), entry_dias.get(), entry_hor.get())
                limpiar_campos()
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def btn_modificar():
            if selected_id[0] is None:
                messagebox.showwarning("Aviso", "Seleccione un médico de la lista.")
                return
            try:
                self.admin.modificar_medico(selected_id[0], entry_nombre.get(), entry_esp.get(), entry_dias.get(), entry_hor.get())
                limpiar_campos()
                cargar_tabla()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def btn_eliminar():
            if selected_id[0] is None:
                messagebox.showwarning("Aviso", "Seleccione un médico de la lista.")
                return
            self.admin.eliminar_medico(selected_id[0])
            limpiar_campos()
            cargar_tabla()

        tk.Button(frame_modif, text="➕ Agregar Médico", bg="#00A86B", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=btn_agregar).pack(fill="x", pady=4)
        tk.Button(frame_modif, text="✏️ Modificar Médico", bg="#F58C46", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=btn_modificar).pack(fill="x", pady=4)
        tk.Button(frame_modif, text="🗑️ Eliminar Médico", bg="#E53935", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=btn_eliminar).pack(fill="x", pady=4)
        tk.Button(frame_modif, text="🧹 Limpiar Campos", bg="#777777", fg="white", font=("Segoe UI", 9), relief="flat", command=limpiar_campos).pack(fill="x", pady=4)

        cargar_tabla()
        self.notebook.add(panel_admin, text=f"Panel Admin ({nombre})")
        self.notebook.select(panel_admin)

    def mostrar_panel_usuario(self, nombre):
        panel_usuario = tk.Frame(self.notebook, bg="#E6F2F8")

        header_usuario = tk.Frame(panel_usuario, bg="#E6F2F8")
        header_usuario.pack(fill="x", padx=15, pady=8)

        tk.Label(header_usuario, text=f"👤 Panel del Paciente - Bienvenid@ {nombre}", 
                 font=("Roboto", 12, "bold"), bg="#E6F2F8", fg="#003366").pack(side="left")

        def salir_usuario():
            self.notebook.forget(panel_usuario)
            panel_usuario.destroy()

        btn_cerrar = tk.Button(header_usuario, text=" ❌ ", bg="#E53935", fg="white", 
                               font=("Segoe UI", 9, "bold"), relief="flat", cursor="hand2", command=salir_usuario)
        btn_cerrar.pack(side="right")

        main_container = tk.Frame(panel_usuario, bg="#E6F2F8")
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Lado Izquierdo: Médicos
        frame_medicos = tk.Frame(main_container)
        frame_medicos.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(frame_medicos, text="Médicos Disponibles", font=("Roboto", 10, "bold")).pack(anchor="w")

        columns_m = ("ID", "Médico", "Especialidad", "Días", "Horarios")
        tabla_medicos = ttk.Treeview(frame_medicos, columns=columns_m, show="headings")
        for col in columns_m:
            tabla_medicos.heading(col, text=col)
            tabla_medicos.column(col, width=80)
        tabla_medicos.pack(fill="both", expand=True)

        # Formulario Turno
        frame_solicitar_turno = tk.Frame(main_container, bg="white", bd=1, relief="solid", padx=10, pady=10)
        frame_solicitar_turno.pack(side="right", fill="y", padx=5)

        tk.Label(frame_solicitar_turno, text="Solicitar Turno", font=("Roboto", 11, "bold"), bg="white", fg="#004080").pack(pady=5)

        tk.Label(frame_solicitar_turno, text="ID Médico Seleccionado:", bg="white").pack(anchor="w")
        entry_medico_id = ttk.Entry(frame_solicitar_turno, width=25)
        entry_medico_id.pack(fill="x", pady=2)

        tk.Label(frame_solicitar_turno, text="Fecha (AAAA-MM-DD):", bg="white").pack(anchor="w")
        entry_fecha = ttk.Entry(frame_solicitar_turno, width=25)
        entry_fecha.pack(fill="x", pady=2)

        tk.Label(frame_solicitar_turno, text="Horarios Disponibles:", bg="white").pack(anchor="w")
        combo_hora = ttk.Combobox(frame_solicitar_turno, width=23, state="readonly")
        combo_hora.pack(fill="x", pady=2)

        #La funcion obtiene los horarios del medico con la id correspondiente y los carga en combo_hora, para seleccionar el deseado
        def actualizar_horarios_disponibles(*args):
            medico_id = entry_medico_id.get().strip()
            fecha = entry_fecha.get().strip()
            if medico_id and fecha:
                libres = self.paciente.obtener_horarios_disponibles(medico_id, fecha)
                combo_hora['values'] = libres
                if libres:
                    combo_hora.set(libres[0])
                else:
                    combo_hora.set('')
            else:
                combo_hora['values'] = []
                combo_hora.set('')

        entry_fecha.bind("<KeyRelease>", actualizar_horarios_disponibles) #Cada vez que se ingrese fecha del turno se llama a la funcion

        def seleccionar_medico(event):
            medico = tabla_medicos.selection()
            if medico:
                vals = tabla_medicos.item(medico[0], "values")
                entry_medico_id.delete(0, tk.END)
                entry_medico_id.insert(0, vals[0])
                actualizar_horarios_disponibles()

        tabla_medicos.bind("<<TreeviewSelect>>", seleccionar_medico)

        def cargar_medicos_paciente():
            for fila in tabla_medicos.get_children():
                tabla_medicos.delete(fila)
            for m in self.admin.obtener_medicos():
                tabla_medicos.insert("", tk.END, values=m)

        def cargar_turnos_paciente():
            for fila in conten_turnos.get_children():
                conten_turnos.delete(fila)
            for t in self.paciente.obtener_turnos_paciente(nombre):
                conten_turnos.insert("", tk.END, values=t)

        def btn_reservar():
            medico_id = entry_medico_id.get().strip()
            fecha = entry_fecha.get().strip()
            hora = combo_hora.get().strip()

            if not medico_id or not hora:
                messagebox.showwarning("Aviso", "Seleccione un médico, ingrese una fecha válida y elija un horario disponible.")
                return
            try:
                msg = self.paciente.solicitar_turno(nombre, medico_id, fecha, hora)
                messagebox.showinfo("Éxito", msg)
                combo_hora.set('')
                cargar_turnos_paciente()
                actualizar_horarios_disponibles()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(frame_solicitar_turno, text="Confirmar Turno", bg="#007ACC", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=btn_reservar).pack(fill="x", pady=10)

        # Mis Turnos
        frame_turnos = tk.Frame(panel_usuario, bg="#E6F2F8")
        frame_turnos.pack(fill="both", expand=True, padx=15, pady=(0, 10))

        frame_turnos = tk.Frame(frame_turnos)
        frame_turnos.pack(side="left", fill="both", expand=True)

        tk.Label(frame_turnos, text="Mis Turnos Reservados", font=("Roboto", 10, "bold")).pack(anchor="w")

        columns_t = ("ID Turno", "Médico", "Especialidad", "Fecha", "Hora")
        conten_turnos = ttk.Treeview(frame_turnos, columns=columns_t, show="headings")
        for col in columns_t:
            conten_turnos.heading(col, text=col)
            conten_turnos.column(col, width=90)
        conten_turnos.pack(fill="both", expand=True)

        def btn_cancelar_turno():
            item = conten_turnos.selection()
            if not item:
                messagebox.showwarning("Aviso", "Seleccione un turno reservado para cancelar.")
                return
            turno_id = conten_turnos.item(item[0], "values")[0]
            if messagebox.askyesno("Confirmar", "¿Desea cancelar este turno?"):
                try:
                    msg = self.paciente.cancelar_turno(turno_id, nombre)
                    messagebox.showinfo("Éxito", msg)
                    cargar_turnos_paciente()
                    actualizar_horarios_disponibles()
                except Exception as e:
                    messagebox.showerror("Error", str(e))

        frame_cancelar = tk.Frame(frame_turnos, bg="#E6F2F8")
        frame_cancelar.pack(side="right", fill="y", padx=(25, 0))

        tk.Button(frame_cancelar, text="❌ Cancelar Turno", bg="#BE0606", fg="white", font=("Segoe UI", 9, "bold"), relief="flat", command=btn_cancelar_turno).pack(pady=20)

        cargar_medicos_paciente()
        cargar_turnos_paciente()

        self.notebook.add(panel_usuario, text=f"Paciente ({nombre})")
        self.notebook.select(panel_usuario)

if __name__ == "__main__":
    main = Main()
    principal = tk.Tk()
    principal.geometry("850x600")
    app = Interfaz(principal)
    principal.mainloop()
