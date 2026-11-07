import tkinter as tk
from tkinter import ttk, messagebox
import excepciones  # Importamos el archivo de excepciones y logs que creamos

class AplicacionSoftwareFJ(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestión - Software FJ")
        self.geometry("700x500")

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

    # --- PESTAÑA 1: CLIENTES (Aquí Enrique conectará su módulo) ---
    def crear_tab_clientes(self):
        lbl = ttk.Label(self.tab_clientes, text="Formulario de Registro de Clientes", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)
        # Espacio reservado para los campos de texto y botones del cliente

    # --- PESTAÑA 2: SERVICIOS (Aquí José conectará su módulo) ---
    def crear_tab_servicios(self):
        lbl = ttk.Label(self.tab_servicios, text="Catálogo de Servicios", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)
        # Espacio reservado para mostrar las opciones y tipos de servicio

    # --- PESTAÑA 3: RESERVAS (Aquí se gestionará la lógica de reservas) ---
    def crear_tab_reservas(self):
        lbl = ttk.Label(self.tab_reservas, text="Control y Solicitud de Reservas", font=("Arial", 12, "bold"))
        lbl.pack(pady=10)
        # Espacio reservado para enlazar la creación de reservas

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