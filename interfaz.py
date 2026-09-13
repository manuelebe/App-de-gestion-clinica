import tkinter as tk
from tkinter import ttk, messagebox
from main import Usuario, Paciente, Administrador, Main
import calendar
from datetime import datetime

class Interfaz:
    def __init__(self, principal):
        self.principal = principal
        self.principal.title("Clínica")
        self.usuario = Usuario()
        self.paciente = Paciente()
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
        self.medicos_ventana = None

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
        titulo = tk.Label(content_frame, text="Registro",
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
        #Faltaria darle mas estilo y hacer q se vea su disponibilidad mas claramente
        if self.medicos_ventana is not None:
            messagebox.showwarning("Aviso", "Ya existe la pestaña de Médicos. Ciérrala primero.")
            return
        
        # Pestaña principal
        self.medicos_ventana = tk.Frame(self.notebook, bg="#E6F2F8")
        
        header_frame = tk.Frame(self.medicos_ventana, bg="#E6F2F8")
        header_frame.pack(fill="x")
        
        logo = tk.Label(header_frame, text="➕ Clínica", font=("Roboto", 16, "bold"), bg="#E6F2F8", fg="#004466")
        logo.pack(side="left", padx=20)
        
        menu = tk.Label(header_frame, text="Médicos disponibles", font=("Roboto", 12), bg="#E6F2F8", fg="#004466")
        menu.pack(side="right", padx=20)
        
        # Linea 
        ttk.Separator(self.medicos_ventana, orient="horizontal").pack(fill="x", padx=20, pady=5)
        
        # Lista de items
        columnas = ("item_nombre", "item_esp", "item_dias", "item_horarios")
        tree = ttk.Treeview(self.medicos_ventana, columns=columnas, show="headings")
        
        tree.heading("item_nombre", text="Nombre")
        tree.heading("item_esp", text="Especialidad")
        tree.heading("item_dias", text="Días de atención")
        tree.heading("item_horarios", text="Horarios")
        
        tree.column("item_nombre", width=80)
        tree.column("item_esp", width=80)
        tree.column("item_dias", width=80)
        tree.column("item_horarios", width=80)
        
        # Llenar la lista
        for medico in self.paciente.retornar_medicos():
            nombre_med = medico.get_nombre()
            esp_med = medico.get_especialidad()
            dias_med = medico.get_dias_atencion()
            horarios_med = []
            for horarios in medico.get_horarios():
                horario_texto = []
                for horario in horarios:
                    horas = horario[0]
                    minutos = horario[1]
                    if horas < 10:
                        horas = f"0{horas}"
                    if minutos < 10:
                        minutos = f"0{minutos}"
                    horario_texto.append(f"{horas}:{minutos}")
                horario_texto_unido = ", ".join(horario_texto)
                horarios_med.append(horario_texto_unido)
                
            horarios_med_unido = " - ".join(horarios_med)
            
            tree.insert("", tk.END, values=(nombre_med, esp_med, dias_med, horarios_med_unido))
            
        # Estilo (falta)
        
        tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Agregar al notebook
        self.notebook.add(self.medicos_ventana, text="Lista de médicos")
        self.notebook.select(self.medicos_ventana)
        
    
    def solicitar_turno(self):
        vent_solic_turn = tk.Toplevel(self.principal)
        vent_solic_turn.title("Solicitar Turno")
        vent_solic_turn.geometry("325x600")
        vent_solic_turn.resizable(False, False)
        
        # Fecha actual
        now = datetime.now()

        # Entrys
        tk.Label(vent_solic_turn, text="Seleccione un médico:").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        lista = tk.Listbox(vent_solic_turn, height=10, width=50)
        lista.grid(row=1, column=0, padx=10, pady=5)

        for medico in self.paciente.retornar_medicos():
            lista.insert(tk.END, f"{medico.get_nombre()} - {medico.get_especialidad()}")

        tk.Label(vent_solic_turn, text="Ingrese su nombre:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        entry_nombre = tk.Entry(vent_solic_turn, width=40)
        entry_nombre.grid(row=3, column=0, padx=10, pady=5)
        
        # Dropdowns de fecha y hora
        
        def actualizar_dias():
            # Ahora mismo los turnos no se guardan en ningun lado, falta guardarlos, poder verlos y no dejar que registren 2 turnos en el mismo dia y horario
            
            # Ajusta los dias mostrados segun el mes y año
            anio = int(self.anio_cb.get())
            mes = int(self.mes_cb.get())
        
            # calendar.monthrange retorna(primer dia de la semana, numero de dias en mes)
            _, num_dias = calendar.monthrange(anio, mes)
        
            # guardar seleccion previa si es valida
            dia_anterior = self.dia_cb.get()
        
            # actualizar dropdown dias
            lista_dias = [f"{d:02d}" for d in range(1, num_dias + 1)]
            self.dia_cb["values"] = lista_dias
        
            # si el dia previo no es valido, resetear al primero
            if dia_anterior in lista_dias:
                self.dia_cb.set(dia_anterior)
            else:
                self.dia_cb.set("01")
        
        # Año
        ttk.Label(vent_solic_turn, text="Año: ").grid(
            row = 4, column = 0, sticky = "w", padx = 10, pady = 5
        )
        self.anio_cb = ttk.Combobox(
            vent_solic_turn,
            values = [str(y) for y in range(now.year - 5, now.year + 10)],
            width = 6,
            state = "readonly",
        )
        self.anio_cb.set(str(now.year))
        self.anio_cb.grid(row = 5, column = 0, padx = 10, pady = 5)
        self.anio_cb.bind("<<ComboboxSelected>>", actualizar_dias)
        
        # Mes
        ttk.Label(vent_solic_turn, text="Mes:").grid(
            row=6, column=0, sticky="w", padx=10, pady=5
        )
        self.mes_cb = ttk.Combobox(
            vent_solic_turn,
            values=[f"{m:02d}" for m in range(1, 13)],
            width=4,
            state="readonly",
        )
        self.mes_cb.set(f"{now.month:02d}")
        self.mes_cb.grid(row=7, column=0, padx=10, pady=5)
        self.mes_cb.bind("<<ComboboxSelected>>", actualizar_dias)
        
        # Dia
        ttk.Label(vent_solic_turn, text="Dia:").grid(
            row=8, column=0, sticky="w", padx=10, pady=5
        )
        self.dia_cb = ttk.Combobox(vent_solic_turn, width=4, state="readonly")
        self.dia_cb.grid(row=9, column=0, padx=10, pady=5)

        # Hora
        ttk.Label(vent_solic_turn, text="Hora:").grid(
            row=10, column=0, sticky="w", padx=10, pady=5
        )
        self.hora_cb = ttk.Combobox(
            vent_solic_turn,
            values=[f"{h:02d}:00" for h in range(24)],
            width=6,
            state="readonly",
        )
        self.hora_cb.set(f"{now.hour:02d}:00")
        self.hora_cb.grid(row=11, column=0, padx=10, pady=5)
        
        # Llena el dropdown de dias
        actualizar_dias()
        self.dia_cb.set(f"{now.day:02d}")
        
        def confirmar_turno():
            seleccion = lista.curselection()
            if not seleccion:
                messagebox.showwarning("Atención", "Seleccione un médico primero")
                return
            
            def turno_registrado_con_exito():
                messagebox.showinfo("Éxito", f"Turno reservado con {medico['Nombre']} el {dia} a las {hora} hs")
                vent_solic_turn.destroy()
            
            medico = self.paciente.retornar_medicos()[seleccion[0]]
            nombre_paciente = entry_nombre.get().strip()
            anio = int(self.anio_cb.get())
            mes = int(self.mes_cb.get())
            dia = int(self.dia_cb.get())
            hora = self.hora_cb.get().split(":")
            print(hora)
            fecha = datetime(anio, mes, dia)
            dia_indice = fecha.weekday()
            
            # Convierte el indice de dia de semana a español
            dias_esp = [
                "Lunes",
                "Martes",
                "Miercoles",
                "Jueves",
                "Viernes",
                "Sabado",
                "Domingo",
            ]
            dia_actual = dias_esp[dia_indice]

            if not nombre_paciente or not anio or not mes or not dia or not hora:
                messagebox.showwarning("Atención", "Complete todos los campos")
                return

            # Validación de disponibilidad
            if dia_actual in medico.get_dias_atencion():
                for horario_med in medico.get_horarios():
                    if hora[0] > horario_med[0]:
                        turno_registrado_con_exito()
                    elif hora[0] == horario_med[0]:
                        if hora[1] >= horario_med[1]:
                            turno_registrado_con_exito()
                        else:
                            messagebox.showerror("Error", "El médico no está disponible en ese horario")
                    else:
                        messagebox.showerror("Error", "El médico no está disponible en ese horario")
            else:
                messagebox.showerror("Error", "El médico no está disponible en ese día")

        # Botón Confirmar
        btn_confirmar = tk.Button(vent_solic_turn, text="Confirmar Turno", width=20, bg="#00A86B", fg="white", font=("Segoe UI", 10, "bold"), 
            relief="flat", command=confirmar_turno)
        btn_confirmar.grid(row=12, column=0, pady=10)

        # Botón Cancelar
        btn_cerrar = tk.Button(vent_solic_turn, text="Cancelar",  bg="#BE0606", fg="white", font=("Segoe UI", 10, "bold"), 
            relief="flat", command=vent_solic_turn.destroy)
        btn_cerrar.grid(row=13, column=0, pady=5) 

if __name__ == "__main__":
    main = Main()
    main.cargar_medicos()
    principal = tk.Tk()
    principal.geometry("800x700")
    app = Interfaz(principal) 
    principal.mainloop() 
