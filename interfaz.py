import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from validaciones import *

# --- Datos predefinidos ---
marcas_modelos = {
    "Toyota": ["Corolla", "Hilux", "Yaris"],
    "Mazda": ["CX-5", "Mazda 3", "BT-50"],
    "Chevrolet": ["Onix", "Tracker", "Sail"],
    "Renault": ["Duster", "Sandero", "Kwid"]
}
propositos = ["Particular", "Trabajo", "Servicio público", "Otro"]
relaciones = ["Propietario", "Familiar", "Empleado", "Otro"]

class FormularioSeguro:
    def __init__(self, root):
        self.root = root
        self.root.title("Formulario de Solicitud de Seguro Vehicular")
        self.root.geometry("700x900")

        # --- Scroll principal ---
        self.canvas = tk.Canvas(self.root)
        self.scroll_y = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.frame = tk.Frame(self.canvas)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        self.conductores_extra = []  # lista de dicts/entradas de conductores extra

        self.crear_campos_usuario()
        self.crear_campos_vehiculo()
        self.crear_conductor_principal()
        self.crear_botones()

    # --- Usuario ---
    def crear_campos_usuario(self):
        tk.Label(self.frame, text="Datos del Usuario", font=("Arial", 13, "bold")).pack(pady=(10, 6))
        campos = [
            ("Nombre", "nombre"), ("Segundo nombre (opcional)", "segundo_nombre"),
            ("Apellido paterno", "apellido_p"), ("Apellido materno", "apellido_m"),
            ("Fecha de nacimiento", "fecha_nac"), ("Correo electrónico", "correo"),
            ("Teléfono", "telefono"), ("Dirección", "direccion"), ("Código postal", "postal")
        ]
        self.usuario_entries = {}
        for label, key in campos:
            row = tk.Frame(self.frame)
            row.pack(fill="x", padx=12, pady=4)
            tk.Label(row, text=label, width=26, anchor="w").pack(side="left")
            if key == "fecha_nac":
                entry = DateEntry(row, date_pattern="dd/mm/yyyy", width=28)
            else:
                entry = tk.Entry(row, width=30)
            entry.pack(side="left")
            self.usuario_entries[key] = entry

    # --- Vehículo (ahora en subframe con grid para mejor alineación) ---
    def crear_campos_vehiculo(self):
        tk.Label(self.frame, text="Datos del Vehículo", font=("Arial", 13, "bold")).pack(pady=(12, 6))

        # subframe para usar grid y lograr alineación
        vf = tk.Frame(self.frame)
        vf.pack(fill="x", padx=12, pady=3)

        # --- Placa ---
        tk.Label(vf, text="Placa del vehículo", width=26, anchor="w").grid(row=0, column=0, sticky="w", padx=2, pady=6)
        self.placa_entry = tk.Entry(vf, width=32)
        self.placa_entry.grid(row=0, column=1, sticky="w", padx=2, pady=6)

        # --- Año (Combobox) ---
        tk.Label(vf, text="Año del vehículo", width=26, anchor="w").grid(row=1, column=0, sticky="w", padx=2, pady=6)
        years = [str(y) for y in range(1900, 2027)]
        self.anio_cb = ttk.Combobox(vf, values=years, width=30, state="readonly")
        self.anio_cb.grid(row=1, column=1, sticky="w", padx=2, pady=6)

        # --- Marca ---
        tk.Label(vf, text="Marca del vehículo", width=26, anchor="w").grid(row=2, column=0, sticky="w", padx=2, pady=6)
        self.marca_cb = ttk.Combobox(vf, values=list(marcas_modelos.keys()), width=30, state="readonly")
        self.marca_cb.grid(row=2, column=1, sticky="w", padx=2, pady=6)
        self.marca_cb.bind("<<ComboboxSelected>>", self.on_marca_selected)

        # --- Modelo ---
        tk.Label(vf, text="Modelo del vehículo", width=26, anchor="w").grid(row=3, column=0, sticky="w", padx=2, pady=6)
        # inicialmente vacío y desactivado hasta que se elija marca
        self.modelo_cb = ttk.Combobox(vf, values=[], width=30, state="disabled")
        self.modelo_cb.grid(row=3, column=1, sticky="w", padx=2, pady=6)

        # --- Propósito ---
        tk.Label(vf, text="Propósito del vehículo", width=26, anchor="w").grid(row=4, column=0, sticky="w", padx=2, pady=6)
        self.proposito_cb = ttk.Combobox(vf, values=propositos, width=30, state="readonly")
        self.proposito_cb.grid(row=4, column=1, sticky="w", padx=2, pady=6)

        # Ajuste de columnas para que espacien adecuadamente
        vf.grid_columnconfigure(0, weight=0)
        vf.grid_columnconfigure(1, weight=1)

    def on_marca_selected(self, event):
        marca = self.marca_cb.get()
        modelos = marcas_modelos.get(marca, [])
        self.modelo_cb.configure(state="readonly")    # activar combobox
        self.modelo_cb["values"] = modelos
        # Si hay modelos, seleccionar el primero como sugerencia vacía
        if modelos:
            self.modelo_cb.set(modelos[0])
        else:
            self.modelo_cb.set("")

    # --- Conductor principal ---
    def crear_conductor_principal(self):
        tk.Label(self.frame, text="Conductor Principal", font=("Arial", 13, "bold")).pack(pady=(12, 6))
        self.conductor_principal = {}
        campos = [
            ("Nombre", "nombre"), ("Segundo nombre (opcional)", "segundo_nombre"),
            ("Apellido paterno", "apellido_p"), ("Apellido materno", "apellido_m"),
            ("Fecha de nacimiento", "fecha_nac"), ("Años de experiencia", "exp"),
            ("Relación con propietario", "rel")
        ]
        for label, key in campos:
            row = tk.Frame(self.frame)
            row.pack(fill="x", padx=12, pady=4)
            tk.Label(row, text=label, width=26, anchor="w").pack(side="left")
            if key == "fecha_nac":
                entry = DateEntry(row, date_pattern="dd/mm/yyyy", width=28)
            elif key == "rel":
                entry = ttk.Combobox(row, values=relaciones, width=28, state="readonly")
            else:
                entry = tk.Entry(row, width=30)
            entry.pack(side="left")
            self.conductor_principal[key] = entry

    # --- Botones: agregar conductor extra y enviar ---
    def crear_botones(self):
        frame_b = tk.Frame(self.frame)
        frame_b.pack(pady=12)
        tk.Button(frame_b, text="Agregar conductor adicional", command=self.abrir_popup_conductor, bg="#008CBA", fg="white").pack(side="left", padx=6)
        tk.Button(frame_b, text="Ver conductores añadidos", command=self.ver_conductores, bg="#FFA000").pack(side="left", padx=6)
        tk.Button(frame_b, text="Enviar formulario", command=self.validar_formulario, bg="#4CAF50", fg="white").pack(side="left", padx=6)

    # --- Pop-up para agregar conductor adicional ---
    def abrir_popup_conductor(self):
        win = tk.Toplevel(self.root)
        win.title("Agregar Conductor Adicional")
        campos = [
            ("Nombre", "nombre"), ("Segundo nombre (opcional)", "segundo_nombre"),
            ("Apellido paterno", "apellido_p"), ("Apellido materno", "apellido_m"),
            ("Fecha de nacimiento", "fecha_nac"), ("Años de experiencia", "exp"),
            ("Relación con propietario", "rel")
        ]
        entradas = {}
        for i, (label, key) in enumerate(campos):
            tk.Label(win, text=label).grid(row=i, column=0, padx=8, pady=4, sticky="w")
            if key == "fecha_nac":
                entry = DateEntry(win, date_pattern="dd/mm/yyyy", width=22)
            elif key == "rel":
                entry = ttk.Combobox(win, values=relaciones, width=20, state="readonly")
            else:
                entry = tk.Entry(win, width=24)
            entry.grid(row=i, column=1, padx=8, pady=4)
            entradas[key] = entry

        def guardar():
            # validación mínima: nombre y apellido paterno
            if not entradas["nombre"].get().strip() or not entradas["apellido_p"].get().strip():
                messagebox.showerror("Error", "El conductor debe tener al menos nombre y apellido paterno.")
                return
            # almacenar dict con valores
            self.conductores_extra.append({
                "nombre": entradas["nombre"].get().strip(),
                "segundo_nombre": entradas["segundo_nombre"].get().strip(),
                "apellido_p": entradas["apellido_p"].get().strip(),
                "apellido_m": entradas["apellido_m"].get().strip(),
                "fecha_nac": entradas["fecha_nac"].get().strip(),
                "exp": entradas["exp"].get().strip(),
                "rel": entradas["rel"].get().strip(),
            })
            win.destroy()
            messagebox.showinfo("Conductor agregado", "Se agregó un conductor adicional correctamente.")

        tk.Button(win, text="Guardar", command=guardar, bg="#4CAF50", fg="white").grid(row=len(campos), column=0, columnspan=2, pady=8)

    # --- Mostrar conductores añadidos en una ventana (ver/editar/eliminar) ---
    def ver_conductores(self):
        win = tk.Toplevel(self.root)
        win.title("Conductores añadidos")
        cols = ("Nombre", "Segundo nombre", "Apellido P", "Apellido M", "Fecha Nac", "Exp", "Rel")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=8)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=100)
        tree.pack(fill="both", expand=True, padx=6, pady=6)

        # --- Popular tabla ---
        for i, cd in enumerate(self.conductores_extra):
            tree.insert("", "end", iid=i, values=(
                cd["nombre"], cd["segundo_nombre"], cd["apellido_p"], cd["apellido_m"],
                cd["fecha_nac"], cd["exp"], cd["rel"]
            ))

        # --- Función para eliminar ---
        def eliminar_sel():
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Seleccione conductor(es) para eliminar.")
                return
            idxs = sorted([int(i) for i in sel], reverse=True)
            for idx in idxs:
                self.conductores_extra.pop(idx)
            win.destroy()
            messagebox.showinfo("Eliminado", "Conductor(es) eliminado(s).")

        # --- Función para editar ---
        def editar_sel():
            sel = tree.selection()
            if not sel:
                messagebox.showerror("Error", "Seleccione un conductor para editar.")
                return
            if len(sel) > 1:
                messagebox.showerror("Error", "Solo puede editar un conductor a la vez.")
                return

            idx = int(sel[0])
            conductor = self.conductores_extra[idx]

            # --- Ventana emergente para editar ---
            edit_win = tk.Toplevel(win)
            edit_win.title("Editar Conductor")
            campos = [
                ("Nombre", "nombre"), ("Segundo nombre (opcional)", "segundo_nombre"),
                ("Apellido paterno", "apellido_p"), ("Apellido materno", "apellido_m"),
                ("Fecha de nacimiento", "fecha_nac"), ("Años de experiencia", "exp"),
                ("Relación con propietario", "rel")
            ]
            entradas = {}
            for i, (label, key) in enumerate(campos):
                tk.Label(edit_win, text=label).grid(row=i, column=0, padx=8, pady=4, sticky="w")
                if key == "fecha_nac":
                    entry = DateEntry(edit_win, date_pattern="dd/mm/yyyy", width=22)
                    entry.set_date(conductor["fecha_nac"])
                elif key == "rel":
                    entry = ttk.Combobox(edit_win, values=relaciones, width=20, state="readonly")
                    entry.set(conductor["rel"])
                else:
                    entry = tk.Entry(edit_win, width=24)
                    entry.insert(0, conductor[key])
                entry.grid(row=i, column=1, padx=8, pady=4)
                entradas[key] = entry

            def guardar_cambios():
                # Validación mínima
                if not entradas["nombre"].get().strip() or not entradas["apellido_p"].get().strip():
                    messagebox.showerror("Error", "Debe tener al menos nombre y apellido paterno.")
                    return

                # Actualizar datos en la lista
                conductor_actualizado = {
                    "nombre": entradas["nombre"].get().strip(),
                    "segundo_nombre": entradas["segundo_nombre"].get().strip(),
                    "apellido_p": entradas["apellido_p"].get().strip(),
                    "apellido_m": entradas["apellido_m"].get().strip(),
                    "fecha_nac": entradas["fecha_nac"].get().strip(),
                    "exp": entradas["exp"].get().strip(),
                    "rel": entradas["rel"].get().strip(),
                }
                self.conductores_extra[idx] = conductor_actualizado

                # Actualizar visualmente la tabla
                tree.item(sel, values=tuple(conductor_actualizado.values()))
                edit_win.destroy()
                messagebox.showinfo("Éxito", "Conductor actualizado correctamente.")

            tk.Button(edit_win, text="Guardar cambios", command=guardar_cambios, bg="#4CAF50", fg="white").grid(row=len(campos), column=0, columnspan=2, pady=8)

        # --- Botones de acción ---
        btns = tk.Frame(win)
        btns.pack(pady=6)
        tk.Button(btns, text="Editar seleccionado", command=editar_sel, bg="#0288D1", fg="white").pack(side="left", padx=6)
        tk.Button(btns, text="Eliminar seleccionados", command=eliminar_sel, bg="#D32F2F", fg="white").pack(side="left", padx=6)

    # --- Validación final del formulario ---
    def validar_formulario(self):
        errores = []

        u = self.usuario_entries
        # nombres y apellidos se esperan en MAYÚSCULAS según tus ER
        if not validar_nombre(u["nombre"].get().strip()): errores.append("Nombre inválido (solo mayúsculas, mínimo 2 letras).")
        if not validar_segundo_nombre(u["segundo_nombre"].get().strip()): errores.append("Segundo nombre inválido (si está presente).")
        if not validar_apellido(u["apellido_p"].get().strip()): errores.append("Apellido paterno inválido.")
        if not validar_apellido(u["apellido_m"].get().strip()): errores.append("Apellido materno inválido.")
        # fecha de nacimiento: DateEntry evita mal formato, opcional validación adicional
        if not validar_correo(u["correo"].get().strip()): errores.append("Correo electrónico inválido.")
        if not validar_telefono(u["telefono"].get().strip()): errores.append("Teléfono inválido (debe iniciar en 3 y tener 10 dígitos).")
        if not validar_direccion(u["direccion"].get().strip()): errores.append("Dirección inválida.")
        if not validar_codigo_postal(u["postal"].get().strip()): errores.append("Código postal inválido (6 dígitos).")

        # vehículo
        if not validar_placa(self.placa_entry.get().strip().upper()): errores.append("Placa inválida (formato ABC123).")
        if not self.anio_cb.get().strip(): errores.append("Año del vehículo no seleccionado.")
        if not self.marca_cb.get().strip(): errores.append("Marca del vehículo no seleccionada.")
        if not self.modelo_cb.get().strip(): errores.append("Modelo del vehículo no seleccionado.")
        if not self.proposito_cb.get().strip(): errores.append("Propósito del vehículo no seleccionado.")

        # conductor principal
        c = self.conductor_principal
        if not validar_nombre(c["nombre"].get().strip()): errores.append("Nombre del conductor principal inválido.")
        if not validar_segundo_nombre(c["segundo_nombre"].get().strip()): errores.append("Segundo nombre del conductor principal inválido (si está presente).")
        if not validar_apellido(c["apellido_p"].get().strip()): errores.append("Apellido paterno del conductor principal inválido.")
        if not validar_apellido(c["apellido_m"].get().strip()): errores.append("Apellido materno del conductor principal inválido.")
        if not validar_experiencia(c["exp"].get().strip()): errores.append("Años de experiencia del conductor principal inválidos (0–99).")
        if not c["rel"].get().strip(): errores.append("Relación del conductor principal no seleccionada.")

        # al menos conductor principal debe estar completo; los adicionales son opcionales
        if errores:
            messagebox.showerror("Errores en el formulario", "\n".join(errores))
            return False

        # Si todo está bien:
        messagebox.showinfo("Éxito", "Formulario validado y enviado correctamente.")
        return True
