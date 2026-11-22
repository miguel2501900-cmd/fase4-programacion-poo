import datetime

# Archivo único donde quedan los errores y los eventos del sistema.
ARCHIVO_LOG = "sistema_logs.txt"


def escribir_en_log(tipo, texto):
    """Agrega una línea con fecha y hora al archivo de logs.

    tipo: "EXCEPCIÓN" para errores o "EVENTO" para operaciones normales.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open(ARCHIVO_LOG, "a", encoding="utf-8") as archivo:
            archivo.write(f"[{timestamp}] {tipo}: {texto}\n")
    except OSError as e:
        # Si el disco falla, el sistema sigue funcionando y avisa por consola.
        print(f"Error crítico al escribir en el archivo de logs: {e}")


def registrar_evento(mensaje):
    """Registra en el log un evento relevante que no es un error (registros, reservas, cancelaciones)."""
    escribir_en_log("EVENTO", mensaje)

class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones personalizadas de Software FJ."""
    def __init__(self, mensaje):
        super().__init__(mensaje)
        self.mensaje = mensaje
        self.registrar_log()

    def registrar_log(self):
        """Registra automáticamente el error en el archivo sistema_logs.txt."""
        escribir_en_log("EXCEPCIÓN", f"{self.__class__.__name__} -> {self.mensaje}")


class ClienteInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los datos del cliente no cumplen las validaciones."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta solicitar un servicio inexistente o inactivo."""
    pass


class ReservaFallidaError(ErrorSistemaFJ):
    """Se lanza cuando ocurre un fallo al procesar, confirmar o cancelar una reserva."""
    pass


class ParametroInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando falta un parámetro o su valor está fuera de lo permitido."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se pide una operación que el estado actual no admite."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza cuando un cálculo de costos recibe o produce valores sin sentido."""
    pass
