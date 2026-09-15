import os # Sirve para interactuar con el sistema operativo, manejar archivos y capartes, crear, borrar, etc
import pickle # Guardar objetos en un archivo binario y recuperarlos después en el mismo estado.
import hashlib #Sirve para encriptar la informacion 

USUARIOS_FILE = "usuarios.dat"
MEDICOS_FILE = "medicos.dat"
TURNOS_FILE = "turnos.dat"

def encriptar_contraseña(ctrñ: str) -> str:
    return hashlib.sha256(ctrñ.encode('utf-8')).hexdigest()

def verificar_contraseña(ctrñ: str, stored_hash_str: str) -> bool:
    return encriptar_contraseña(ctrñ) == stored_hash_str

def cargar_datos_binarios(arch):
    if not os.path.exists(arch):
        return []
    try:
        with open(arch, "rb") as f:
            return pickle.load(f)
    except (EOFError, pickle.UnpicklingError):
        return []

def guardar_datos_binarios(arch, datos):
    with open(arch, "wb") as f:
        pickle.dump(datos, f)

def cargar_datos():
    # Inicializar archivo de usuarios si no existe
    if not os.path.exists(USUARIOS_FILE):
        usuarios_iniciales = [
            {"id": 1, "usuario": "admin1", "contraseña": encriptar_contraseña("12345"), "rol": "Admin"},
            {"id": 2, "usuario": "paciente1", "contraseña": encriptar_contraseña("12345"), "rol": "Usuario"},
            {"id": 3, "usuario": "paciente2", "contraseña": encriptar_contraseña("12345"), "rol": "Usuario"},
            {"id": 4, "usuario": "paciente3", "contraseña": encriptar_contraseña("12345"), "rol": "Usuario"},
        ]
        guardar_datos_binarios(USUARIOS_FILE, usuarios_iniciales)

    # Inicializar archivo de médicos si no existe
    if not os.path.exists(MEDICOS_FILE):
        medicos_iniciales = [
            {"id": 1, "nombre": "Agustin", "especialidad": "Traumatologo", "dias": "Martes, Jueves", "horarios": "12-16"},
            {"id": 2, "nombre": "Maria Lopez", "especialidad": "Cardiologia", "dias": "Lunes, Miercoles", "horarios": "09-13"},
            {"id": 3, "nombre": "Carlos Gomez", "especialidad": "Pediatria", "dias": "Viernes", "horarios": "08-12"}
        ]
        guardar_datos_binarios(MEDICOS_FILE, medicos_iniciales)

    # Inicializar archivo de turnos si no existe
    if not os.path.exists(TURNOS_FILE):
        guardar_datos_binarios(TURNOS_FILE, [])
