import tkinter as tk
from tkinter import ttk, messagebox
from Servicios import Sala, Equipo,  Asesoria
import excepciones  # Importamos el archivo de excepciones y logs que creamos

class AplicacionSoftwareFJ(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Software FJ")
        self.geometry("700x500")

        # Aqui agregamos las listas para almacenar los objetos de clientes, servicios y reservas 
        self.lista_clientes = []
        self.lista_servicios = []
        self.lista_reservas = []

        # Aquí armamos el sistema de pestañas (Notebook) para ordenar la interfaz
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Creamos las cuatro pestañas principales de la aplicación
        self.tab_clientes = ttk.Frame(self.notebook)
        self.tab_servicios = ttk.Frame(self.notebook)
        self.tab_reservas = ttk.Frame(self.notebook)
        self.tab_auditoria = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_clientes, text="Gestión de Clientes")
        self.notebook.add(self.tab_servicios, text="Gestión de Servicios")
        self.notebook.add(self.tab_reservas, text="Gestión de Reservas")
        self.notebook.add(self.tab_auditoria, text="Auditoría y Logs")

        # Llamamos a los métodos que dibujan los elementos dentro de cada pestaña
        self.crear_tab_clientes()
        self.crear_tab_servicios()
        self.crear_tab_reservas()
        self.crear_tab_auditoria()

    # --- PESTAÑA 1: CLIENTES (Módulo de Enrique) ---
    def crear_tab_clientes(self):
        lbl = ttk.Label(self.tab_clientes, text="Formulario de Registro de Clientes", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)
        
        frame_form = ttk.Frame(self.tab_clientes)
        frame_form.pack(pady=10)
        
        # Campos del formulario
        ttk.Label(frame_form, text="Cédula:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_cedula = ttk.Entry(frame_form)
        self.ent_cedula.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_form, text="Nombre:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_nombre = ttk.Entry(frame_form)
        self.ent_nombre.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Correo:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_correo = ttk.Entry(frame_form)
        self.ent_correo.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_form, text="Teléfono:").grid(row=3, column=0, padx=5, pady=5)
        self.ent_telefono = ttk.Entry(frame_form)
        self.ent_telefono.grid(row=3, column=1, padx=5, pady=5)
        
        btn_guardar = ttk.Button(self.tab_clientes, text="Registrar Cliente", command=self.registrar_cliente)
        btn_guardar.pack(pady=10)

    def registrar_cliente(self):
        try:
            # Llama a tu clase Cliente; si algo falla, dispara ClienteInvalidoError
            from clientes import Cliente
            nuevo_cliente = Cliente(
                self.ent_cedula.get(),
                self.ent_nombre.get(),
                self.ent_correo.get(),
                self.ent_telefono.get()
            )
            self.lista_clientes.append(nuevo_cliente)
            messagebox.showinfo("Éxito", f"Cliente {nuevo_cliente.nombre} registrado.")
            
            # Limpiar campos
            self.ent_cedula.delete(0, 'end')
            self.ent_nombre.delete(0, 'end')
            self.ent_correo.delete(0, 'end')
            self.ent_telefono.delete(0, 'end')
            
        except excepciones.ClienteInvalidoError as e:
            messagebox.showerror("Error de Validación", str(e.mensaje))

    # -- PESTAÑA 2: SERVICIOS (Aquí José conectará su módulo) --
    
    # Esta función crea la interfaz de la pestaña de servicios, con botones y un cuadro visual para mostrar los servicios registrados
    def crear_tab_servicios(self):
        lbl = ttk.Label(self.tab_servicios, text="Catálogo de Servicios", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        # Botones para cada tipo de servicio
        frame_botones = ttk.Frame(self.tab_servicios)
        frame_botones.pack(pady=10)

        ttk.Button(
            frame_botones,
            text="Registrar Sala",
            command=self.registrar_sala
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            frame_botones,
            text="Registrar Equipo",
            command=self.registrar_equipo
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            frame_botones,
            text="Registrar Asesoría",
            command=self.registrar_asesoria
        ).grid(row=0, column=2, padx=5)

        # Cuadro visual: Le ponemos "visor_servicios_ui" para que sea más fácil de identificar en el código
        self.visor_servicios_ui = tk.Listbox(
            self.tab_servicios,
            width=80,
            height=12
        )
        self.visor_servicios_ui.pack(pady=15)

    # Estas funciones se ejecutan SOLO cuando haces clic en los botones

    def registrar_sala(self):
        import excepciones
        try:
            from Servicios import Sala 
            
            nueva_sala = Sala(codigo="S01", nombre="Sala Juntas", capacidad=15)
            
            # Guardamos el objeto en la memoria real (Backend)
            self.lista_servicios.append(nueva_sala)
            
            # Mostramos el texto en el cuadro visual (Frontend)
            self.visor_servicios_ui.insert('end', nueva_sala.mostrar_informacion())
            
            messagebox.showinfo("Éxito", f"Sala {nueva_sala.codigo} registrada.")
        except excepciones.ServicioNoDisponibleError as e:
            messagebox.showerror("Error de Servicio", str(e.mensaje))

    def registrar_equipo(self):
        messagebox.showinfo("Info", "Botón de Equipo conectado. Funcionalidad en desarrollo.")

    def registrar_asesoria(self):
        messagebox.showinfo("Info", "Botón de Asesoría conectado. Funcionalidad en desarrollo.")
    # --- PESTAÑA 3: RESERVAS (Aquí se gestionará la lógica de reservas) ---
     def crear_tab_reservas(self):
        lbl = ttk.Label(self.tab_reservas, text="Control y Solicitud de Reservas", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)
        
        frame_reserva = ttk.Frame(self.tab_reservas)
        frame_reserva.pack(pady=10)

        # Campos para solicitar la reserva
        ttk.Label(frame_reserva, text="ID de la Reserva:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_id_reserva = ttk.Entry(frame_reserva)
        self.ent_id_reserva.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_reserva, text="Cédula del Cliente:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_cedula_res = ttk.Entry(frame_reserva)
        self.ent_cedula_res.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_reserva, text="ID del Servicio:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_id_servicio = ttk.Entry(frame_reserva)
        self.ent_id_servicio.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_reserva, text="Duración (Horas/Días):").grid(row=3, column=0, padx=5, pady=5)
        self.ent_duracion = ttk.Entry(frame_reserva)
        self.ent_duracion.grid(row=3, column=1, padx=5, pady=5)

        btn_procesar = ttk.Button(self.tab_reservas, text="Procesar y Confirmar", command=self.ejecutar_reserva)
        btn_procesar.pack(pady=15)

    def ejecutar_reserva(self):
        try:
            from reserva import Reserva
            import excepciones
            
            cedula_buscar = self.ent_cedula_res.get()
            codigo_servicio_buscar = self.ent_id_servicio.get() 

            # Busca el cliente por cédula
            cliente_obj = next((c for c in self.lista_clientes if c.cedula == cedula_buscar), None)
            
            # Busca el servicio por CODIGO (usando getattr para evitar errores si el objeto no tiene 'codigo')
            servicio_obj = next((s for s in self.lista_servicios if getattr(s, 'codigo', None) == codigo_servicio_buscar), None)

            if cliente_obj is None:
                raise excepciones.ReservaFallidaError("El cliente no se encuentra registrado.")
            if servicio_obj is None:
                raise excepciones.ReservaFallidaError("El código de servicio no existe.")

            if not self.ent_duracion.get().replace('.', '', 1).isdigit():
                 raise excepciones.ReservaFallidaError("La duración debe ser un valor numérico.")
            
            duracion_val = float(self.ent_duracion.get())

            nueva_reserva = Reserva(
                id_reserva=self.ent_id_reserva.get(),
                cliente=cliente_obj,
                servicio=servicio_obj,
                duracion=duracion_val
            )
            # Procesa aplicando validaciones
            nueva_reserva.procesar()

            # Guarda la reserva
            self.lista_reservas.append(nueva_reserva)
            messagebox.showinfo("Operación Exitosa", f"Reserva {nueva_reserva.id_reserva} confirmada. Servicio actualizado a: {servicio_obj.estado}")

            # Limpia los campos
            self.ent_id_reserva.delete(0, 'end')
            self.ent_cedula_res.delete(0, 'end')
            self.ent_id_servicio.delete(0, 'end')
            self.ent_duracion.delete(0, 'end')

        except excepciones.ReservaFallidaError as e:
            messagebox.showerror("Error al procesar reserva", str(e.mensaje))
            
    # --- PESTAÑA 4: AUDITORÍA Y PRUEBAS (Nuestra zona de control de errores) ---
    def crear_tab_auditoria(self):
        lbl = ttk.Label(self.tab_auditoria, text="Consola de Auditoría y Simulación de Excepciones", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)

        # Botón práctico para probar que el sistema escriba en el archivo de logs
        btn_probar_excepcion = ttk.Button(
            self.tab_auditoria, 
            text="Simular Error de Cliente Inválido", 
            command=self.probando_excepcion
        )
        btn_probar_excepcion.pack(pady=20)

    def probando_excepcion(self):
        # Disparamos una excepción controlada para verificar el funcionamiento del log
        try:
            raise excepciones.ClienteInvalidoError("Prueba de validación desde la interfaz Tkinter.")
        except excepciones.ClienteInvalidoError as e:
            messagebox.showerror("Error de Auditoría", f"Se ha registrado una excepción:\n{e.mensaje}")

if __name__ == "__main__":
    app = AplicacionSoftwareFJ()
    app.mainloop()
