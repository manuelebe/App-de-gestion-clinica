#App de gestión con interfaz hecha en TKinter o en alguna otra biblioteca 
from datetime import datetime, date, timedelta
from database import (
    cargar_datos, cargar_datos_binarios, guardar_datos_binarios,
    encriptar_contraseña, verificar_contraseña,
    USUARIOS_FILE, MEDICOS_FILE, TURNOS_FILE
)

class Main:
    def __init__(self):
        cargar_datos() # Se precargan datos como usuarios, administradors y medicos

#Clase Usuario
class Usuario:
    def registrar(self, usuario, contraseña, rol="Usuario"):
        cargar_datos()
        if len(usuario) < 6:
            raise Exception("El nombre de usuario debe contener al menos 6 carácteres.")
        if len(contraseña) < 5:
            raise Exception("La contraseña debe contener al menos 5 carácteres.")
        
        usuarios = cargar_datos_binarios(USUARIOS_FILE)
        for u in usuarios:
            if u["usuario"].lower() == usuario.lower():
                raise Exception("El nombre de usuario ya se encuentra registrado.")

        # Autoincrementar ID para el nuevo registro
        nuevo_id = max([u["id"] for u in usuarios], default=0) + 1
        nuevo_usuario = {
            "id": nuevo_id,
            "usuario": usuario,
            "contraseña": encriptar_contraseña(contraseña),
            "rol": rol
        }
        usuarios.append(nuevo_usuario)
        guardar_datos_binarios(USUARIOS_FILE, usuarios)
        return "Usuario registrado correctamente."

    def login(self, usuario, contraseña):
        cargar_datos()
        usuarios = cargar_datos_binarios(USUARIOS_FILE)
        for u in usuarios:
            if u["usuario"] == usuario and verificar_contraseña(contraseña, u["contraseña"]):
                return u["rol"], u["usuario"]
        raise Exception("Usuario o contraseña incorrectos.")

#Clase Administrador
class Administrador:
    def obtener_medicos(self):
        medicos = cargar_datos_binarios(MEDICOS_FILE)

        # Formato de tupla: (id, nombre, especialidad, dias, horarios)
        return [(m["id"], m["nombre"], m["especialidad"], m["dias"], m["horarios"]) for m in medicos]

    def añadir_medico(self, nombre, esp, dias, hor):
        medicos = cargar_datos_binarios(MEDICOS_FILE)
        for m in medicos:
            if m["nombre"].lower() == nombre.strip().lower() and m["especialidad"].lower() == esp.strip().lower():
                raise Exception("El médico ya se encuentra registrado con esa especialidad.")

        nuevo_id = max([m["id"] for m in medicos], default=0) + 1
        nuevo_medico = {
            "id": nuevo_id,
            "nombre": nombre.strip(),
            "especialidad": esp.strip(),
            "dias": dias.strip(),
            "horarios": hor.strip()
        }
        medicos.append(nuevo_medico)
        guardar_datos_binarios(MEDICOS_FILE, medicos)

    def modificar_medico(self, id_medico, nombre, esp, dias, hor):
        medicos = cargar_datos_binarios(MEDICOS_FILE)
        encontrado = False
        for m in medicos:
            if str(m["id"]) == str(id_medico):
                m["nombre"] = nombre.strip()
                m["especialidad"] = esp.strip()
                m["dias"] = dias.strip()
                m["horarios"] = hor.strip()
                encontrado = True
                break
        if encontrado:
            guardar_datos_binarios(MEDICOS_FILE, medicos)

    def eliminar_medico(self, id_medico):
        medicos = cargar_datos_binarios(MEDICOS_FILE)
        medicos = [m for m in medicos if str(m["id"]) != str(id_medico)] #Se obtienen todos lo medicos que no coincida con ese id_medico
        guardar_datos_binarios(MEDICOS_FILE, medicos)

#Clase Paciente
class Paciente:
    def solicitar_turno(self, paciente_username, medico_id, fecha_str, hora_str):
        if not fecha_str or not hora_str:
            raise Exception("Debe ingresar la fecha y la hora del turno.")

        # Validar fecha
        try:
            fecha_d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            raise Exception("Formato de fecha inválido. Use AAAA-MM-DD.")

        if fecha_d < date.today():
            raise Exception("No puede solicitar un turno para una fecha pasada.")

        # Validar que la hora esté en los horarios disponibles
        horarios_disponibles = self.obtener_horarios_disponibles(medico_id, fecha_str)
        if hora_str not in horarios_disponibles:
            raise Exception("La hora seleccionada no está disponible para ese médico en esa fecha.")

        # Verificar si el paciente ya tiene turno en esa hora
        turnos = cargar_datos_binarios(TURNOS_FILE)
        for t in turnos:
            if t["paciente"] == paciente_username and t["fecha"] == fecha_str and t["hora"] == hora_str:
                raise Exception("Ya tienes otro turno registrado a esta misma hora.")

        # Crear nuevo turno
        nuevo_id = max([t["id"] for t in turnos], default=0) + 1
        nuevo_turno = {
            "id": nuevo_id,
            "paciente": paciente_username,
            "medico_id": int(medico_id),
            "fecha": fecha_str,
            "hora": hora_str
        }
        turnos.append(nuevo_turno)
        guardar_datos_binarios(TURNOS_FILE, turnos)
        return "Turno reservado exitosamente."


    def limpiar_turnos_vencidos(self):
        hoy_str = date.today().strftime("%Y-%m-%d")
        turnos = cargar_datos_binarios(TURNOS_FILE)
        turnos_validos = [t for t in turnos if t["fecha"] >= hoy_str]
        guardar_datos_binarios(TURNOS_FILE, turnos_validos)

    def obtener_turnos_paciente(self, paciente_username):
        self.limpiar_turnos_vencidos()
        turnos = cargar_datos_binarios(TURNOS_FILE)
        medicos = cargar_datos_binarios(MEDICOS_FILE)
        medicos_dict = {m["id"]: m for m in medicos} #Se crear un dict dentro de otro dict, donde la clave es el id

        resultado = []
        for t in turnos:
            if t["paciente"] == paciente_username:
                medicos = medicos_dict.get(t["medico_id"], {"nombre": "Desconocido", "especialidad": "N/A"})
                resultado.append((t["id"], medicos["nombre"], medicos["especialidad"], t["fecha"], t["hora"]))

        # Ordenar por fecha y hora
        resultado.sort(key=lambda x: (x[3], x[4]))
        return resultado

    def cancelar_turno(self, turno_id, paciente_username):
        turnos = cargar_datos_binarios(TURNOS_FILE)
        turnos_filtrados = [t for t in turnos if not (str(t["id"]) == str(turno_id) and t["paciente"] == paciente_username)]

        if len(turnos) == len(turnos_filtrados):
            raise Exception("No se pudo cancelar el turno o el turno no te pertenece.")

        guardar_datos_binarios(TURNOS_FILE, turnos_filtrados)
        return "Turno cancelado con éxito."

    def obtener_horarios_disponibles(self, medico_id, fecha_str):
        self.limpiar_turnos_vencidos()

        #Si no ingresa fecha devulve una lista vacia
        if not fecha_str:
            return []

        # convierte la fecha a tipo date
        try:
            fecha_d = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            return []

        # Verifica que no ingrese fechas antiguas
        if fecha_d < date.today():
            return []

        medicos = cargar_datos_binarios(MEDICOS_FILE)
        medico = next((m for m in medicos if str(m["id"]) == str(medico_id)), None) # El next delvuelve el proximo objeto de la lista que cumpla con la  condicion y ,None es el valor por defecto que se le da a la variable en caso de que no se encunetre ningun medico con ese ID
        if not medico:
            return []

        dias_atencion, rango_horario = medico["dias"].lower(), medico["horarios"]

        dias_map = {
            'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miercoles',
            'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sabado', 'sunday': 'domingo'
        }
        dia_ingresado = dias_map[fecha_d.strftime('%A').lower()]
        dias_atencion_clean = dias_atencion.replace('é', 'e').replace('á', 'a').replace('í', 'i')
        
        if dia_ingresado not in dias_atencion_clean:
            return []

        # Es la funcion encargada de realizar los intervalos de 30 minutos y mostrar los horarios disponibles
        horarios_posibles = []
        try:
            inicio_str, fin_str = rango_horario.split('-')
            hora_inicio = int(inicio_str.strip())
            hora_fin = int(fin_str.strip())

            actual = datetime.combine(fecha_d, datetime.min.time()).replace(hour=hora_inicio)
            limite = datetime.combine(fecha_d, datetime.min.time()).replace(hour=hora_fin)

            while actual < limite:
                horarios_posibles.append(actual.strftime("%H:%M"))
                actual += timedelta(minutes=30)
        except ValueError:
            return []

        #Funcion encragada de cargar los tunros ya reservados para un medico en especifico en una fecha
        turnos = cargar_datos_binarios(TURNOS_FILE)
        ocupados = []
        for t in turnos:
            if str(t["medico_id"]) == str(medico_id) and t["fecha"] == fecha_str:
                hora_str = t["hora"].strip()
                if len(hora_str) == 4 and hora_str[1] == ':':
                    hora_str = "0" + hora_str #Setea el formato en tipo horario 9:00, lo pasa a 09:00
                ocupados.append(hora_str)

        return [h for h in horarios_posibles if h not in ocupados]
