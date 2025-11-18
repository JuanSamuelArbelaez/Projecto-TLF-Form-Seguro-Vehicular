# Projecto TLF - Form Seguro Vehicular

Resumen
- Aplicación de escritorio simple creada con Tkinter que muestra un formulario para solicitar seguro vehicular.
- El propósito principal es demostrar validación de campos mediante expresiones regulares (regex) en Python.

Qué incluye
- interfaz.py: UI y lógica de interacción (Tkinter).
- validaciones.py: expresiones regulares y funciones que validan cada campo del formulario.
- main.py: punto de entrada para lanzar la aplicación.
- requirements.txt: dependencias externas (ej. tkcalendar).
- .gitignore: reglas para ignorar venv y cachés de Python.

Características principales
- Validaciones en tiempo de envío para:
  - Nombres y apellidos (formato en mayúsculas según reglas internas).
  - Correo electrónico.
  - Teléfono (ej.: empieza en 3 y 10 dígitos).
  - Dirección y código postal.
  - Placa del vehículo (formato ABC123).
  - Años de experiencia (0–99).
- Soporta agregar, ver, editar y eliminar conductores adicionales.
- Interfaz con DateEntry (tkcalendar) para fechas.

Instalación (Python)
1. Crear y activar un entorno virtual (recomendado):
   - Windows:
     python -m venv venv
     venv\Scripts\activate
   - macOS / Linux:
     python3 -m venv venv
     source venv/bin/activate
2. Instalar dependencias:
   pip install -r requirements.txt

Ejecución
- Ejecutar la aplicación:
  python main.py
- La ventana muestra el formulario; complete los campos y presione "Enviar formulario" para ejecutar las validaciones.
