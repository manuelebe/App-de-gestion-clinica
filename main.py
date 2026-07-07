#App de gestión con interfaz hecha en TKinter o en alguna otra biblioteca
from database import user_database, admin_database, medic_database
import getpass
from datetime import date

#Clase Usuario
class Usuario:
    def __init__(self):
        pass
    
    def registrar(self):
        usuario = input("Ingresar nombre de usuario: ").strip()
        if usuario in user_database or usuario in admin_database:
            raise Exception("El usuario ya existe.")
            return
        contraseña = input("Ingresar contraseña: ")
        user_database[usuario] = contraseña
        
    def login(self):
        usuario = input("Ingresar nombre de usuario: ").strip()
        contraseña = input("Ingresar contraseña: ")
        if usuario in user_database:
            if user_database[usuario] == contraseña:
                print("Logueado")
        elif usuario in admin_database:
            if admin_database[usuario] == contraseña:
                print("Logueado como admin")
        else:
            print("Error")
        

#Clase Administrador
class Administrador:
    def __init__(self):
        pass
    
    def añadir_medico(self, nombre, esp, dias, hor):
        medic_database.append(Medico(nombre, esp, dias, hor))
        
    def buscar_medico(self, nombre):
        contador = 0
        for i in medic_database:
            if i.get_nombre() == nombre:
                return contador
            else:
                contador += 1
    
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
        #Chequear si ya existe un turno con este horario y fecha.
        
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

#usuario1 = Usuario()
#usuario1.registrar()
#usuario1.login()

admin1 = Administrador()
admin1.añadir_medico("Manuel", "Pediatra", ["Monday", "Tuesday", "Friday"], [(13, 18), (19, 23)])
admin1.añadir_medico("Pedro", "Pediatra", ["Monday", "Tuesday", "Friday"], [(13, 18), (19, 23)])
admin1.añadir_medico("Juan", "Pediatra", ["Monday", "Tuesday", "Friday"], [(13, 18), (19, 23)])
indice_medico1 = admin1.buscar_medico("Pedro")
admin1.modificar_medico(indice_medico1, "Paula", "Nose", ["Wednesday", "Thursday", "Friday"], [(11, 15), (17, 22)])
#admin1.eliminar_medico(0)

paciente1 = Paciente()
#lista_medicos = paciente1.buscar_medico("Pediatra")
#for i in lista_medicos:
    #print(i.get_nombre(), i.get_especialidad(), i.get_dias_atencion(), i.get_horarios())
#print(paciente1.ver_disponibilidad(medic_database[indice_medico1]))
turno1 = paciente1.solicitar_turno(medic_database[indice_medico1], date(2026, 7, 8), 17)
print(turno1.get_paciente(), turno1.get_medico().get_nombre(), turno1.get_fecha(), turno1.get_horario())

#medico1 = Medico("Manuel", "Pediatra", ["Lunes", "Martes", "Viernes"], [(13, 18), (19, 23)])
#medic_database.append(medico1)

#for i in medic_database:
    #print(i.get_nombre(), i.get_especialidad(), i.get_dias_atencion(), i.get_horarios())