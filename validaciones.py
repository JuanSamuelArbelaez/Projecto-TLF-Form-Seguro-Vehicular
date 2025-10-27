import re

# Expresiones regulares
ER = {
    "nombre": re.compile(r"^[A-ZÑÁÉÍÓÚ]{2,}$"),
    "segundo_nombre": re.compile(r"^([A-ZÑÁÉÍÓÚ]{2,})?$"),
    "apellido": re.compile(r"^[A-ZÑÁÉÍÓÚ]{2,}$"),
    "correo": re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
    "telefono": re.compile(r"^3\d{9}$"),
    "direccion": re.compile(r"^[A-Za-z0-9#\-\.\s]+$"),
    "codigo_postal": re.compile(r"^\d{6}$"),
    "placa": re.compile(r"^[A-Z]{3}\d{3}$"),
    "experiencia": re.compile(r"^(?:[0-9]|[1-9][0-9])$")  # 0–99 años
}

# Validadores individuales
def validar_nombre(nombre): return bool(ER["nombre"].match(nombre.strip()))
def validar_segundo_nombre(nombre): return bool(ER["segundo_nombre"].match(nombre.strip()))
def validar_apellido(apellido): return bool(ER["apellido"].match(apellido.strip()))
def validar_correo(correo): return bool(ER["correo"].match(correo.strip()))
def validar_telefono(tel): return bool(ER["telefono"].match(tel.strip()))
def validar_direccion(dir): return bool(ER["direccion"].match(dir.strip()))
def validar_codigo_postal(cp): return bool(ER["codigo_postal"].match(cp.strip()))
def validar_placa(placa): return bool(ER["placa"].match(placa.strip().upper()))
def validar_experiencia(exp): return bool(ER["experiencia"].match(exp.strip()))
