from excepciones import ReservaFallidaError

class Reserva:
    def __init__(self, id_reserva, cliente, servicio, duracion):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.estado = "PENDIENTE"

    def procesar(self):
        try:
            if not self.cliente or not self.servicio:
                raise ReservaFallidaError(f"Reserva {self.id_reserva}: Faltan datos del cliente o servicio.")
            
            if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
                raise ReservaFallidaError(f"Reserva {self.id_reserva}: La duración debe ser mayor a 0.")
            
            # Verifica si el servicio está disponible antes de confirmar la reserva
            if self.servicio.estado != "Disponible":
                raise ReservaFallidaError(
                    f"Reserva {self.id_reserva}: El servicio {self.servicio.codigo} no se puede reservar porque está {self.servicio.estado}."
                )

        except ReservaFallidaError as e:
            self.estado = "CANCELADA"
            raise # Relanza el error hacia la interfaz gráfica
        except Exception as e:
            self.estado = "CANCELADA"
            raise ReservaFallidaError(f"Fallo inesperado al procesar reserva: {e}")
        else:
            self.confirmar()
        finally:
            print(f"[{self.id_reserva}] Estado actual de la reserva: {self.estado}")

    def confirmar(self):
        if self.estado == "CANCELADA":
            raise ReservaFallidaError("No se puede confirmar una reserva previamente cancelada.")
        
        self.estado = "CONFIRMADA"
        
        # ACTUALIZACIÓN: cambiar el estado del servicio según su tipo 
        tipo_servicio = self.servicio.__class__.__name__
        if tipo_servicio == "Sala":
            self.servicio.estado = "Ocupada"
        elif tipo_servicio == "Equipo":
            self.servicio.estado = "Reservado"
        elif tipo_servicio == "Asesoria":
            self.servicio.estado = "Reservada"

    def cancelar(self):
        self.estado = "CANCELADA"
        if self.servicio:
            self.servicio.estado = "Disponible" # Libera el servicio
