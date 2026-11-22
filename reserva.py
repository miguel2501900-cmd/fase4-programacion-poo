from excepciones import OperacionNoPermitidaError, ReservaFallidaError, registrar_evento


class Reserva:
    """Une un cliente con un servicio durante una duración y lleva el estado de esa reserva."""

    def __init__(self, id_reserva, cliente, servicio, duracion, descuento=0.0):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        # Descuento opcional entre 0 y 1 (0.10 = 10 %).
        self.descuento = descuento
        # El costo se calcula al procesar la reserva.
        self.costo = 0
        self.estado = "PENDIENTE"

    def procesar(self):
        """Valida la reserva, calcula su costo y la confirma. Si algo falla queda CANCELADA."""
        try:
            if not self.cliente or not self.servicio:
                raise ReservaFallidaError(f"Reserva {self.id_reserva}: Faltan datos del cliente o servicio.")

            if not isinstance(self.duracion, (int, float)) or self.duracion <= 0:
                raise ReservaFallidaError(f"Reserva {self.id_reserva}: La duración debe ser mayor a 0.")

            if str(self.servicio.estado).strip() != "Disponible":
                raise ReservaFallidaError(
                    f"Reserva {self.id_reserva}: El servicio {self.servicio.codigo} no se puede reservar porque está {self.servicio.estado}."
                )

            # Polimorfismo: cada servicio valida la duración y calcula el costo a su manera.
            self.servicio.validar_parametros(self.duracion)
            self.costo = self.servicio.calcular_costo_total(self.duracion, descuento=self.descuento)

        except ReservaFallidaError as e:
            self.estado = "CANCELADA"
            raise
        except Exception as e:
            self.estado = "CANCELADA"
            # Encadenamiento: la reserva falla, pero conserva el error que la causó (e.__cause__).
            raise ReservaFallidaError(f"Reserva {self.id_reserva}: no se pudo procesar. {e}") from e
        else:
            # Solo se confirma cuando ninguna validación falló.
            self.confirmar()
        finally:
            # Se ejecuta siempre, haya fallado o no: deja constancia del resultado.
            print(f"[{self.id_reserva}] Estado actual de la reserva: {self.estado}")
            registrar_evento(f"Reserva {self.id_reserva} procesada. Estado final: {self.estado}")

    def confirmar(self):
        if self.estado == "CANCELADA":
            raise ReservaFallidaError("No se puede confirmar una reserva previamente cancelada.")

        self.estado = "CONFIRMADA"
        # Cada tipo de servicio sabe qué estado toma al reservarse (Ocupada, Reservado, Reservada).
        self.servicio.estado = self.servicio.ESTADO_RESERVADO

    def cancelar(self):
        """Cancela una reserva confirmada y libera el servicio."""
        if self.estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(
                f"Reserva {self.id_reserva}: no se puede cancelar porque está {self.estado}."
            )
        self.estado = "CANCELADA"
        self.servicio.estado = "Disponible"
        registrar_evento(f"Reserva {self.id_reserva} cancelada. El servicio {self.servicio.codigo} quedó disponible.")
