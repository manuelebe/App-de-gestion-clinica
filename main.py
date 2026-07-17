#App de gestión con interfaz hecha en TKinter o en alguna otra biblioteca
from database import user_database, admin_database, medic_database
import getpass
from datetime import date

class Main:
    def __init__(self):
        pass
    
    # Carga como instancias de la clase Medico a los datos precargados en database
    def cargar_medicos(self):
        global medic_database
        
        if medic_database and isinstance(medic_database[0], Medico):
            return
        
        medic_database = [
            Medico(
                i["Nombre"],
                i["Especialidad"],
                i["Dias"],
                i["Horarios"]
            )
            for i in medic_database
        ]
        print(medic_database)
#Clase Usuario
class Usuario:
    def __init__(self):
        pass
    
    def registrar(self, usuario, contraseña):
        if len(usuario) < 6:
            raise Exception("El nombre de usuario debe contener al menos 6 carácteres.")
        if len(contraseña) < 5:
            raise Exception("La contraseña debe contener al menos 5 carácteres.")
        if usuario in user_database or usuario in admin_database:
            raise Exception("El usuario ya existe.")
        user_database[usuario] = contraseña
        return ("Usuario registrado correctamente.")
        
    def login(self, usuario, contraseña):
        if usuario in user_database:
            if user_database[usuario] == contraseña:
                return ("Usuario", usuario) 
        elif usuario in admin_database:
            if admin_database[usuario] == contraseña:
                return ("Admin", usuario) 
        raise Exception("El usuario o la contraseña son incorrectos.")
        

#Clase Administrador
class Administrador:
    def __init__(self):
        pass
    
    def añadir_medico(self, nombre, esp, dias, hor):
        medic_database.append(Medico(nombre, esp, dias, hor))
        
    def buscar_medico(self, nombre):
        contador = 0
        #for i in medic_database:
            #if i.get_nombre() == nombre:
                #return contador
            #else:
                #contador += 1
    
    def modificar_medico(self, indice_medico, nombre, esp, dias, hor):
        medic_database[indice_medico].set_nombre(nombre)
        medic_database[indice_medico].set_especialidad(esp)
        medic_database[indice_medico].set_dias_atencion(dias)
        medic_database[indice_medico].set_horarios(hor)
    
    def eliminar_medico(self, indice_medico):
        medic_database.pop(indice_medico)
    
#Clase Paciente
class Paciente:
    def __init__(self):
        pass
    
    def buscar_medico(self, esp):
        medicos_encontrados = []
        for i in medic_database:
            if i.get_especialidad() == esp:
                medicos_encontrados.append(i)
        return medicos_encontrados
    
    def ver_disponibilidad(self, medico):
        return medico.get_dias_atencion(), medico.get_horarios()
    
    def solicitar_turno(self, medico, fecha, horario):
        dia = fecha.strftime("%A")
        if dia in medico.get_dias_atencion():
            for i in medico.get_horarios():
                rango = i
                if rango[0] <= horario <= rango[1]:
                    return Turno(self, medico, fecha, horario)
            raise Exception("Horario no disponible")
        else:
            raise Exception("Este día no esta disponible.")
        # Chequear si ya existe un turno con este horario y fecha.
        
#Clase Médico
class Medico:
    def __init__(self, nombre, especialidad, dias_atencion, horarios):
        self.__nombre = nombre
        self.__especialidad = especialidad
        self.__dias_atencion = dias_atencion
        self.__horarios = horarios
        
    def get_nombre(self):
        return self.__nombre
    
    def get_especialidad(self):
        return self.__especialidad
    
    def get_dias_atencion(self):
        return self.__dias_atencion
    
    def get_horarios(self):
        return self.__horarios
    
    def set_nombre(self, nuevo_nombre):
        self.__nombre = nuevo_nombre
    
    def set_especialidad(self, nueva_esp):
        self.__especialidad = nueva_esp
    
    def set_dias_atencion(self, nuevo_dias):
        self.__dias_atencion = nuevo_dias
    
    def set_horarios(self, nuevo_hor):
        self.__horarios = nuevo_hor
    
#Clase Turno
class Turno:
    def __init__(self, paciente, medico, fecha, horario):
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha = fecha
        self.__horario = horario
    
    def get_paciente(self):
        return self.__paciente
    
    def get_medico(self):
        return self.__medico
    
    def get_fecha(self):
        return self.__fecha
    
    def get_horario(self):
        return self.__horario
    
    def set_paciente(self, nuevo_pac):
        self.__paciente = nuevo_pac
    
    def set_medico(self, nuevo_med):
        self.__medico = nuevo_med
    
    def set_fecha(self, nueva_fecha):
        self.__fecha = nueva_fecha
    
    def set_horario(self, nuevo_hor):
        self.__horario = nuevo_hor

# Convertir decimales a tiempo (19.50 a 19:30)
def decimal_a_tiempo(self, horas_decimal):
        horas = int(horas_decimal)
        minutos = int(round((horas_decimal - horas) * 60))
        return horas, minutos
    
main = Main()
#main.cargar_medicos()