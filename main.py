import tkinter as tk
from tkinter import ttk, messagebox
from Servicios import Sala, Equipo, Asesoria  # <- Corregido a 'Servicios'
import excepciones

class AplicacionSoftwareFJ(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Software FJ")
        self.geometry("850x700")

        # Listas para almacenar los objetos en memoria
        self.lista_clientes = []
        self.lista_servicios = []
        self.lista_reservas = []

        # Sistema de pestañas (Notebook)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Creamos las cuatro pestañas principales
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_servicios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_auditoria = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes, text="Gestión de Clientes")
        self.notebook.add(self.tab_servicios, text="Gestión de Servicios")
        self.notebook.add(self.tab_reservas, text="Gestión de Reservas")
        self.notebook.add(self.tab_auditoria, text="Auditoría y Logs")

        # Dibujar elementos dentro de cada pestaña
        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()
        self.crear_tab_auditoria()

    # --- PESTAÑA 1: CLIENTES ---
    def crear_tab_clientes(self):
        lbl = ttk.Label(self.tab_clientes, text="Gestión y Registro de Clientes", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        lbl_info = ttk.Label(self.tab_clientes, text="Ingrese la información del cliente para habilitarlo en el sistema de reservas.", font=("Arial", 9, "italic"), foreground="gray")
        lbl_info.pack(pady=2)
        
        container_form = ttk.Frame(self.tab_clientes)
        container_form.pack(pady=5)

        frame_form_cliente = ttk.LabelFrame(container_form, text=" Datos del Cliente ")
        frame_form_cliente.pack(padx=10, pady=5, ipadx=15, ipady=5)
        
        ttk.Label(frame_form_cliente, text="Cédula / Documento:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.ent_cedula = ttk.Entry(frame_form_cliente, width=28)
        self.ent_cedula.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        
        ttk.Label(frame_form_cliente, text="Nombre Completo:").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.ent_nombre = ttk.Entry(frame_form_cliente, width=28)
        self.ent_nombre.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame_form_cliente, text="Correo Electrónico:").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.ent_correo = ttk.Entry(frame_form_cliente, width=28)
        self.ent_correo.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame_form_cliente, text="Teléfono de Contacto:").grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.ent_telefono = ttk.Entry(frame_form_cliente, width=28)
        self.ent_telefono.grid(row=3, column=1, padx=10, pady=6, sticky="w")
        
        btn_guardar = ttk.Button(frame_form_cliente, text="Registrar Cliente", command=self.registrar_cliente)
        btn_guardar.grid(row=4, column=0, columnspan=2, pady=10)

        lbl_visor_cli = ttk.Label(self.tab_clientes, text="Historial de Clientes Registrados en el Sistema:", font=("Arial", 10, "bold"))
        lbl_visor_cli.pack(anchor="w", padx=55, pady=(10, 2))

        self.visor_clientes_ui = tk.Listbox(self.tab_clientes, width=95, height=7)
        self.visor_clientes_ui.pack(padx=50, pady=5)

    def registrar_cliente(self):
        try:
            from clientes import Cliente
            nuevo_cliente = Cliente(
                self.ent_cedula.get(),
                self.ent_nombre.get(),
                self.ent_correo.get(),
                self.ent_telefono.get()
            )
            self.lista_clientes.append(nuevo_cliente)
            info_cliente = f"Cédula: {nuevo_cliente.cedula} | Nombre: {nuevo_cliente.nombre} | Correo: {nuevo_cliente.correo} | Teléfono: {nuevo_cliente.telefono}"
            self.visor_clientes_ui.insert('end', info_cliente)
            messagebox.showinfo("Éxito", f"Cliente {nuevo_cliente.nombre} registrado correctamente.")
            
            self.ent_cedula.delete(0, 'end')
            self.ent_nombre.delete(0, 'end')
            self.ent_correo.delete(0, 'end')
            self.ent_telefono.delete(0, 'end')
            
        except excepciones.ClienteInvalidoError as e:
            messagebox.showerror("Error de Validación", str(e.mensaje))

    # --- PESTAÑA 2: SERVICIOS ---
    def crear_tab_servicios(self):
        lbl = ttk.Label(self.tab_servicios, text="Catálogo y Gestión de Servicios", font=("Arial", 12, "bold"))
        lbl.pack(pady=8)

        lbl_info = ttk.Label(self.tab_servicios, text="Registre las salas, equipos y asesorías disponibles para las reservas del sistema.", font=("Arial", 9, "italic"), foreground="gray")
        lbl_info.pack(pady=2)

        self.notebook_servicios = ttk.Notebook(self.tab_servicios)
        self.notebook_servicios.pack(fill="both", expand=True, padx=15, pady=5)

        self.subtab_sala = ttk.Frame(self.notebook_servicios)
        self.subtab_equipo = ttk.Frame(self.notebook_servicios)
        self.subtab_asesoria = ttk.Frame(self.notebook_servicios)

        self.notebook_servicios.add(self.subtab_sala, text="Gestión de Salas")
        self.notebook_servicios.add(self.subtab_equipo, text="Gestión de Equipos")
        self.notebook_servicios.add(self.subtab_asesoria, text="Gestión de Asesorías")

        self.crear_formulario_salas()
        self.crear_formulario_equipos()
        self.crear_formulario_asesorias()

    def crear_formulario_salas(self):
        container = ttk.Frame(self.subtab_sala)
        container.pack(pady=10)

        frame = ttk.LabelFrame(container, text=" Registrar Sala ")
        frame.pack(padx=10, pady=5, ipadx=15, ipady=5)

        ttk.Label(frame, text="Código Automático:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.ent_codigo = ttk.Entry(frame, width=28)
        self.ent_codigo.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.actualizar_siguiente_codigo_sala()

        ttk.Label(frame, text="Nombre (Ej: Sala VIP):").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.ent_nombre_sala = ttk.Entry(frame, width=28)
        self.ent_nombre_sala.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame, text="Capacidad (Personas):").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.ent_capacidad = ttk.Entry(frame, width=28)
        self.ent_capacidad.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        ttk.Button(frame, text="Guardar Sala", command=self.registrar_sala).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.subtab_sala, text="Salas Registradas en el Sistema:", font=("Arial", 9, "bold")).pack(anchor="w", padx=35, pady=(5, 2))
        self.visor_salas_ui = tk.Listbox(self.subtab_sala, width=95, height=6)
        self.visor_salas_ui.pack(padx=30, pady=5)

    def crear_formulario_equipos(self):
        container = ttk.Frame(self.subtab_equipo)
        container.pack(pady=10)

        frame = ttk.LabelFrame(container, text=" Registrar Equipo ")
        frame.pack(padx=10, pady=5, ipadx=15, ipady=5)

        ttk.Label(frame, text="Código Automático:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.ent_cod_eq = ttk.Entry(frame, width=28)
        self.ent_cod_eq.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.actualizar_siguiente_codigo_equipo()

        ttk.Label(frame, text="Nombre (Ej: Laptop HP):").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.ent_nombre_eq = ttk.Entry(frame, width=28)
        self.ent_nombre_eq.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame, text="Tipo (Ej: Portátil):").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.ent_tipo_eq = ttk.Entry(frame, width=28)
        self.ent_tipo_eq.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        ttk.Button(frame, text="Guardar Equipo", command=self.registrar_equipo).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.subtab_equipo, text="Equipos Registrados en el Sistema:", font=("Arial", 9, "bold")).pack(anchor="w", padx=35, pady=(5, 2))
        self.visor_equipos_ui = tk.Listbox(self.subtab_equipo, width=95, height=6)
        self.visor_equipos_ui.pack(padx=30, pady=5)

    def crear_formulario_asesorias(self):
        container = ttk.Frame(self.subtab_asesoria)
        container.pack(pady=10)

        frame = ttk.LabelFrame(container, text=" Registrar Asesoría ")
        frame.pack(padx=10, pady=5, ipadx=15, ipady=5)

        ttk.Label(frame, text="Código Automático:").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.ent_cod_as = ttk.Entry(frame, width=28)
        self.ent_cod_as.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.actualizar_siguiente_codigo_asesoria()

        ttk.Label(frame, text="Tema de la Asesoría:").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.ent_tema_as = ttk.Entry(frame, width=28)
        self.ent_tema_as.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame, text="Duración Mínima (Min):").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.ent_duracion_as = ttk.Entry(frame, width=28)
        self.ent_duracion_as.grid(row=2, column=1, padx=10, pady=6, sticky="w")
        self.ent_duracion_as.insert(0, "60")

        ttk.Button(frame, text="Guardar Asesoría", command=self.registrar_asesoria).grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Label(self.subtab_asesoria, text="Asesorías Registradas en el Sistema:", font=("Arial", 9, "bold")).pack(anchor="w", padx=35, pady=(5, 2))
        self.visor_asesorias_ui = tk.Listbox(self.subtab_asesoria, width=95, height=6)
        self.visor_asesorias_ui.pack(padx=30, pady=5)

    # --- MÉTODOS AUXILIARES DE CONSECUTIVOS ---
    def actualizar_siguiente_codigo_sala(self):
        cantidad_salas = sum(1 for s in self.lista_servicios if isinstance(s, Sala))
        codigo_auto = f"S{cantidad_salas + 1:02d}"
        self.ent_codigo.config(state='normal')
        self.ent_codigo.delete(0, 'end')
        self.ent_codigo.insert(0, codigo_auto)
        self.ent_codigo.config(state='readonly')

    def actualizar_siguiente_codigo_equipo(self):
        cantidad_equipos = sum(1 for s in self.lista_servicios if isinstance(s, Equipo))
        codigo_auto = f"EQ{cantidad_equipos + 1:02d}"
        self.ent_cod_eq.config(state='normal')
        self.ent_cod_eq.delete(0, 'end')
        self.ent_cod_eq.insert(0, codigo_auto)
        self.ent_cod_eq.config(state='readonly')

    def actualizar_siguiente_codigo_asesoria(self):
        cantidad_asesorias = sum(1 for s in self.lista_servicios if isinstance(s, Asesoria))
        codigo_auto = f"AS{cantidad_asesorias + 1:02d}"
        self.ent_cod_as.config(state='normal')
        self.ent_cod_as.delete(0, 'end')
        self.ent_cod_as.insert(0, codigo_auto)
        self.ent_cod_as.config(state='readonly')

    def actualizar_siguiente_codigo_reserva(self):
        cantidad_reservas = len(self.lista_reservas)
        codigo_auto = f"R{cantidad_reservas + 1:02d}"
        self.ent_id_reserva.config(state='normal')
        self.ent_id_reserva.delete(0, 'end')
        self.ent_id_reserva.insert(0, codigo_auto)
        self.ent_id_reserva.config(state='readonly')

    def actualizar_visores_servicios(self):
        self.visor_salas_ui.delete(0, 'end')
        self.visor_equipos_ui.delete(0, 'end')
        self.visor_asesorias_ui.delete(0, 'end')

        for s in self.lista_servicios:
            if isinstance(s, Sala):
                self.visor_salas_ui.insert('end', s.mostrar_informacion())
            elif isinstance(s, Equipo):
                self.visor_equipos_ui.insert('end', s.mostrar_informacion())
            elif isinstance(s, Asesoria):
                self.visor_asesorias_ui.insert('end', s.mostrar_informacion())

    # --- ACCIONES DE REGISTRO DE SERVICIOS ---
    def registrar_sala(self):
        try:
            codigo_auto = self.ent_codigo.get()
            if any(s.codigo == codigo_auto for s in self.lista_servicios):
                raise excepciones.ServicioNoDisponibleError(f"El código {codigo_auto} ya existe.")

            nueva_sala = Sala(
                codigo_auto, 
                self.ent_nombre_sala.get(), 
                self.ent_capacidad.get()
            )
            self.lista_servicios.append(nueva_sala)
            self.visor_salas_ui.insert('end', nueva_sala.mostrar_informacion())
            messagebox.showinfo("Éxito", f"Sala {nueva_sala.codigo} registrada correctamente.")
            
            self.ent_nombre_sala.delete(0, 'end')
            self.ent_capacidad.delete(0, 'end')
            self.actualizar_siguiente_codigo_sala()
            
        except excepciones.ServicioNoDisponibleError as e:
            messagebox.showerror("Error de Servicio", str(e.mensaje) if hasattr(e, 'mensaje') else str(e))
        except ValueError as e:
            messagebox.showerror("Error de Validación", "Verifique que los campos numéricos sean válidos.")

    def registrar_equipo(self):
        try:
            codigo_auto = self.ent_cod_eq.get()
            if any(s.codigo == codigo_auto for s in self.lista_servicios):
                raise excepciones.ServicioNoDisponibleError(f"El código {codigo_auto} ya existe.")

            nuevo_equipo = Equipo(
                codigo_auto, 
                self.ent_nombre_eq.get(), 
                self.ent_tipo_eq.get()
            )
            self.lista_servicios.append(nuevo_equipo)
            self.visor_equipos_ui.insert('end', nuevo_equipo.mostrar_informacion())
            messagebox.showinfo("Éxito", f"Equipo {nuevo_equipo.codigo} registrado correctamente.")
            
            self.ent_nombre_eq.delete(0, 'end')
            self.ent_tipo_eq.delete(0, 'end')
            self.actualizar_siguiente_codigo_equipo()
            
        except excepciones.ServicioNoDisponibleError as e:
            messagebox.showerror("Error de Servicio", str(e.mensaje) if hasattr(e, 'mensaje') else str(e))
        except ValueError as e:
            messagebox.showerror("Error de Validación", "Verifique que los campos numéricos sean válidos.")

    def registrar_asesoria(self):
        try:
            codigo_auto = self.ent_cod_as.get()
            if any(s.codigo == codigo_auto for s in self.lista_servicios):
                raise excepciones.ServicioNoDisponibleError(f"El código {codigo_auto} ya existe.")

            nueva_asesoria = Asesoria(
                codigo_auto, 
                self.ent_tema_as.get(), 
                self.ent_duracion_as.get()
            )
            self.lista_servicios.append(nueva_asesoria)
            self.visor_asesorias_ui.insert('end', nueva_asesoria.mostrar_informacion())
            messagebox.showinfo("Éxito", f"Asesoría {nueva_asesoria.codigo} registrada correctamente.")
            
            self.ent_tema_as.delete(0, 'end')
            self.actualizar_siguiente_codigo_asesoria()
            
        except excepciones.ServicioNoDisponibleError as e:
            messagebox.showerror("Error de Servicio", str(e.mensaje) if hasattr(e, 'mensaje') else str(e))
        except ValueError as e:
            messagebox.showerror("Error de Validación", "Verifique que los campos numéricos sean válidos.")

    # --- PESTAÑA 3: RESERVAS ---
    def crear_tab_reservas(self):
        lbl = ttk.Label(self.tab_reservas, text="Control y Solicitud de Reservas", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        lbl_info = ttk.Label(self.tab_reservas, text="Vincule un cliente registrado con un servicio disponible para procesar la reserva.", font=("Arial", 9, "italic"), foreground="gray")
        lbl_info.pack(pady=2)
        
        container = ttk.Frame(self.tab_reservas)
        container.pack(pady=5)

        frame_reserva = ttk.LabelFrame(container, text=" Datos de la Reserva ")
        frame_reserva.pack(padx=10, pady=5, ipadx=15, ipady=5)

        ttk.Label(frame_reserva, text="ID de la Reserva (Auto):").grid(row=0, column=0, padx=10, pady=6, sticky="e")
        self.ent_id_reserva = ttk.Entry(frame_reserva, width=28)
        self.ent_id_reserva.grid(row=0, column=1, padx=10, pady=6, sticky="w")
        self.actualizar_siguiente_codigo_reserva()

        ttk.Label(frame_reserva, text="Cédula del Cliente:").grid(row=1, column=0, padx=10, pady=6, sticky="e")
        self.ent_cedula_res = ttk.Entry(frame_reserva, width=28)
        self.ent_cedula_res.grid(row=1, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame_reserva, text="ID del Servicio (Ej: S01/EQ01):").grid(row=2, column=0, padx=10, pady=6, sticky="e")
        self.ent_id_servicio = ttk.Entry(frame_reserva, width=28)
        self.ent_id_servicio.grid(row=2, column=1, padx=10, pady=6, sticky="w")

        ttk.Label(frame_reserva, text="Duración (Horas/Días):").grid(row=3, column=0, padx=10, pady=6, sticky="e")
        self.ent_duracion = ttk.Entry(frame_reserva, width=28)
        self.ent_duracion.grid(row=3, column=1, padx=10, pady=6, sticky="w")
        self.ent_duracion.insert(0, "1")

        btn_procesar = ttk.Button(frame_reserva, text="Procesar y Confirmar", command=self.ejecutar_reserva)
        btn_procesar.grid(row=4, column=0, columnspan=2, pady=12)

        lbl_visor_res = ttk.Label(self.tab_reservas, text="Historial de Reservas Procesadas:", font=("Arial", 9, "bold"))
        lbl_visor_res.pack(anchor="w", padx=35, pady=(5, 2))

        self.visor_reservas_ui = tk.Listbox(self.tab_reservas, width=95, height=6)
        self.visor_reservas_ui.pack(padx=30, pady=5)

    def ejecutar_reserva(self):
        try:
            from reserva import Reserva  # <- Corregido a 'reserva'
            id_res = self.ent_id_reserva.get()
            cedula_buscar = self.ent_cedula_res.get()
            codigo_servicio_buscar = self.ent_id_servicio.get() 

            cliente_obj = next((c for c in self.lista_clientes if c.cedula == cedula_buscar), None)
            servicio_obj = next((s for s in self.lista_servicios if getattr(s, 'codigo', None) == codigo_servicio_buscar), None)

            if cliente_obj is None:
                raise excepciones.ReservaFallidaError("El cliente no se encuentra registrado.")
            if servicio_obj is None:
                raise excepciones.ReservaFallidaError("El código de servicio no existe.")

            if not self.ent_duracion.get().replace('.', '', 1).isdigit():
                 raise excepciones.ReservaFallidaError("La duración debe ser un valor numérico.")
            
            duracion_val = float(self.ent_duracion.get())

            nueva_reserva = Reserva(
                id_reserva=id_res,
                cliente=cliente_obj,
                servicio=servicio_obj,
                duracion=duracion_val
            )
            
            nueva_reserva.procesar()
            self.lista_reservas.append(nueva_reserva)
            
            info_reserva = f"Reserva: {nueva_reserva.id_reserva} | Cliente: {cliente_obj.nombre} | Servicio: {servicio_obj.codigo} | Estado: {nueva_reserva.estado}"
            self.visor_reservas_ui.insert('end', info_reserva)
            
            self.actualizar_visores_servicios()

            messagebox.showinfo("Operación Exitosa", f"Reserva {nueva_reserva.id_reserva} confirmada correctamente. El servicio cambió a estado: {servicio_obj.estado}")

            self.actualizar_siguiente_codigo_reserva()
            self.ent_cedula_res.delete(0, 'end')
            self.ent_id_servicio.delete(0, 'end')
            self.ent_duracion.delete(0, 'end')
            self.ent_duracion.insert(0, "1")

        except excepciones.ReservaFallidaError as e:
            mensaje_error = e.mensaje if hasattr(e, 'mensaje') else str(e)
            messagebox.showerror("Error al procesar reserva", mensaje_error)

    # --- PESTAÑA 4: AUDITORÍA ---
    def crear_tab_auditoria(self):
        lbl = ttk.Label(self.tab_auditoria, text="Consola de Auditoría y Simulación de Excepciones", font=("Arial", 12, "bold"))
        lbl.pack(pady=15)

        container = ttk.Frame(self.tab_auditoria)
        container.pack(pady=10)

        frame_audit = ttk.LabelFrame(container, text=" Pruebas de Sistema ")
        frame_audit.pack(padx=10, pady=5, ipadx=20, ipady=15)

        btn_probar_excepcion = ttk.Button(
            frame_audit, 
            text="Simular Error de Cliente Inválido", 
            command=self.probando_excepcion
        )
        btn_probar_excepcion.pack(pady=10)

    def probando_excepcion(self):
        try:
            raise excepciones.ClienteInvalidoError("Prueba de validación desde la interfaz Tkinter.")
        except excepciones.ClienteInvalidoError as e:
            messagebox.showerror("Error de Auditoría", f"Se ha registrado una excepción:\n{e.mensaje}")

if __name__ == "__main__":
    app = AplicacionSoftwareFJ()
    app.mainloop()