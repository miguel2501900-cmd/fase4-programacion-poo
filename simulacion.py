"""Simulación de operaciones completas del sistema Software FJ.

Ejecuta 16 operaciones seguidas, válidas e inválidas, sobre clientes, servicios y reservas.
Demuestra que el sistema registra cada error en sistema_logs.txt y sigue funcionando.

Se ejecuta sola con:  python simulacion.py
"""

from clientes import Cliente
from excepciones import ErrorSistemaFJ, registrar_evento
from reserva import Reserva
from Servicios import Asesoria, Equipo, Sala


def ejecutar_simulacion():
    """Corre todas las operaciones y devuelve una lista con el resultado de cada una."""
    # Toda la información vive en listas en memoria: no hay base de datos.
    clientes = []
    servicios = []
    reservas = []
    resultados = []

    def buscar_servicio(codigo):
        # next(...) lanza StopIteration si el código no existe; aquí siempre existe.
        return next(s for s in servicios if s.identificador() == codigo)

    def operacion(descripcion, accion):
        """Ejecuta una operación sin dejar que un error detenga las siguientes."""
        numero = len(resultados) + 1
        try:
            detalle = accion()
        except ErrorSistemaFJ as error:
            # Error previsto del sistema: ya quedó en el log al crearse la excepción.
            causa = f" [causa: {type(error.__cause__).__name__}]" if error.__cause__ else ""
            linea = f"{numero:02d}. FALLO CONTROLADO | {descripcion} -> {type(error).__name__}: {error.mensaje}{causa}"
        except Exception as error:
            # Error no previsto: también se registra y la simulación continúa.
            registrar_evento(f"Error inesperado en la operación {numero}: {error!r}")
            linea = f"{numero:02d}. ERROR INESPERADO | {descripcion} -> {error!r}"
        else:
            # Solo si no hubo error: se registra el evento exitoso.
            registrar_evento(f"Operación {numero} exitosa: {descripcion}")
            linea = f"{numero:02d}. OK | {descripcion} -> {detalle}"
        finally:
            # Pase lo que pase, la operación queda contada.
            registrar_evento(f"Operación {numero} finalizada.")
        resultados.append(linea)

    # --- Acciones reutilizables ---
    def registrar_cliente(cedula, nombre, correo, telefono):
        cliente = Cliente(cedula, nombre, correo, telefono)
        clientes.append(cliente)
        return cliente.describir()

    def registrar_servicio(clase, *datos, **opciones):
        servicio = clase(*datos, **opciones)
        servicios.append(servicio)
        return servicio.describir()

    def reservar(id_reserva, cliente, codigo_servicio, duracion, descuento=0.0):
        reserva = Reserva(id_reserva, cliente, buscar_servicio(codigo_servicio), duracion, descuento)
        reserva.procesar()
        reservas.append(reserva)
        return f"{reserva.estado}, costo ${reserva.costo:,.0f}"

    def cancelar(id_reserva):
        reserva = next(r for r in reservas if r.id_reserva == id_reserva)
        reserva.cancelar()
        return f"{reserva.estado}, servicio {reserva.servicio.codigo} {reserva.servicio.estado}"

    # --- Clientes: uno válido y dos inválidos ---
    operacion("Registrar cliente válido", lambda: registrar_cliente("1098765432", "Laura Gómez", "laura@correo.com", "3104567890"))
    operacion("Registrar cliente con cédula no numérica", lambda: registrar_cliente("10A98", "Carlos Pérez", "carlos@correo.com", "3157894561"))
    operacion("Registrar cliente con correo sin arroba", lambda: registrar_cliente("52894316", "María Rodríguez", "maria.correo.com", "3012345678"))

    # --- Servicios: tres válidos y dos inválidos ---
    operacion("Crear sala válida", lambda: registrar_servicio(Sala, "S01", "Sala de juntas", 30))
    operacion("Crear equipo válido", lambda: registrar_servicio(Equipo, "EQ01", "Portátil Lenovo", "Portátil"))
    operacion("Crear asesoría válida", lambda: registrar_servicio(Asesoria, "AS01", "Arquitectura de software", 60))
    operacion("Crear sala con capacidad no numérica", lambda: registrar_servicio(Sala, "S02", "Sala pequeña", "muchas"))
    operacion("Crear equipo con tarifa negativa", lambda: registrar_servicio(Equipo, "EQ02", "Proyector", "Video", tarifa=-5000))

    # --- Reservas: exitosas y fallidas ---
    # Si el primer registro falló no habría cliente; se usa None para que la reserva lo detecte.
    laura = clientes[0] if clientes else None
    operacion("Reservar la sala S01 por 3 horas", lambda: reservar("R01", laura, "S01", 3))
    operacion("Reservar la sala S01 que ya está ocupada", lambda: reservar("R02", laura, "S01", 2))
    operacion("Reservar el equipo EQ01 por 45 días (máximo 30)", lambda: reservar("R03", laura, "EQ01", 45))
    operacion("Reservar la asesoría AS01 por 2 horas con 10 % de descuento", lambda: reservar("R04", laura, "AS01", 2, descuento=0.10))
    operacion("Reservar el equipo EQ01 con descuento del 150 %", lambda: reservar("R05", laura, "EQ01", 2, descuento=1.5))

    # --- Cancelaciones: una permitida y otra no ---
    operacion("Cancelar la reserva R01", lambda: cancelar("R01"))
    operacion("Cancelar otra vez la reserva R01", lambda: cancelar("R01"))
    operacion("Reservar de nuevo la sala S01, ya liberada", lambda: reservar("R06", laura, "S01", 1))

    exitosas = sum(1 for linea in resultados if ". OK |" in linea)
    resultados.append(
        f"Resumen: {len(resultados)} operaciones, {exitosas} exitosas y {len(resultados) - exitosas} con error controlado. "
        f"En memoria: {len(clientes)} cliente(s), {len(servicios)} servicio(s) y {len(reservas)} reserva(s)."
    )
    return resultados


if __name__ == "__main__":
    for linea in ejecutar_simulacion():
        print(linea)
