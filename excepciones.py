import datetime

class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas de Software FJ."""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.registrar_log()

    def registrar_log(self):
        """Registra automáticamente el error en el archivo sistema_logs.txt."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entrada_log = f"[{timestamp}] EXCEPCIÓN: {self.__class__.__name__} -> {self.mensaje}\n"
        try:
            with open("sistema_logs.txt", "a", encoding="utf-8") as archivo:
                archivo.write(entrada_log)
        except Exception as e:
            print(f"Error crítico al escribir en el archivo de logs: {e}")


class ClienteInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los datos del cliente no cumplen las validaciones."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta solicitar un servicio inexistente o inactivo."""
    pass


class ReservaFallidaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un fallo al procesar, confirmar o cancelar una reserva."""
    pass