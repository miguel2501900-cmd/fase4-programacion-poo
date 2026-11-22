import math
from abc import abstractmethod

from entidades import Entidad
from excepciones import (
    CalculoInconsistenteError,
    ParametroInvalidoError,
    ServicioNoDisponibleError,
)

# Impuesto que se aplica por defecto al costo de una reserva (IVA del 19 %).
IVA = 0.19


class Servicio(Entidad):
    """Clase abstracta de la que heredan los servicios de Software FJ.

    Cada servicio especializado (Sala, Equipo, Asesoria) sobrescribe calcular_costo,
    describir y validar_parametros. Así la reserva trata a todos por igual (polimorfismo).
    """

    # Cada clase hija define su tarifa por defecto, su unidad de cobro,
    # la duración máxima que admite y el estado que toma al reservarse.
    TARIFA_BASE = 0
    UNIDAD = "hora"
    DURACION_MAXIMA = 0
    ESTADO_RESERVADO = "Reservado"

    @property
    def tarifa(self):
        return self.__tarifa

    @tarifa.setter
    def tarifa(self, valor):
        # Sin tarifa explícita se usa la tarifa por defecto de la clase.
        if valor is None:
            valor = self.TARIFA_BASE
        try:
            valor = float(valor)
        except (TypeError, ValueError) as error:
            # Encadenamiento: el error original queda guardado como causa.
            raise ParametroInvalidoError(f"La tarifa '{valor}' no es un número.") from error
        if valor <= 0:
            raise ParametroInvalidoError("La tarifa debe ser mayor que cero.")
        self.__tarifa = valor

    def identificador(self):
        # Un servicio se distingue por su código (S01, EQ01, AS01...).
        return self.codigo

    def esta_disponible(self):
        return self.estado == "Disponible"

    @abstractmethod
    def calcular_costo(self, duracion):
        """Devuelve el costo base del servicio para la duración indicada, sin impuestos."""

    @abstractmethod
    def describir(self):
        """Devuelve la descripción del servicio, incluida su tarifa."""

    def validar_parametros(self, duracion):
        """Revisa que la duración pedida sea un número dentro del tope del servicio.

        Las clases hijas la amplían con sus propias reglas.
        """
        if duracion is None:
            raise ParametroInvalidoError(f"Falta la duración para el servicio {self.codigo}.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)):
            raise ParametroInvalidoError(f"La duración '{duracion}' no es un número.")
        if duracion <= 0:
            raise ParametroInvalidoError("La duración debe ser mayor que cero.")
        if duracion > self.DURACION_MAXIMA:
            raise ParametroInvalidoError(
                f"El servicio {self.codigo} admite máximo {self.DURACION_MAXIMA} {self.UNIDAD}s y se pidieron {duracion:g}."
            )

    def calcular_costo_total(self, duracion, impuesto=IVA, descuento=0.0):
        """Costo final de una reserva. Hace de método sobrecargado con parámetros opcionales:

        calcular_costo_total(3)                      -> costo con IVA
        calcular_costo_total(3, impuesto=0)          -> costo sin impuesto
        calcular_costo_total(3, descuento=0.10)      -> costo con IVA y 10 % de descuento
        calcular_costo_total(3, 0.19, 0.10)          -> impuesto y descuento explícitos
        """
        try:
            impuesto = float(impuesto)
            descuento = float(descuento)
        except (TypeError, ValueError) as error:
            raise CalculoInconsistenteError("El impuesto y el descuento deben ser números.") from error
        if impuesto < 0 or not 0 <= descuento <= 1:
            raise CalculoInconsistenteError(
                f"Impuesto ({impuesto}) o descuento ({descuento}) fuera de rango: el descuento va de 0 a 1."
            )
        # calcular_costo es polimórfico: se ejecuta el de la clase hija.
        total = self.calcular_costo(duracion) * (1 - descuento) * (1 + impuesto)
        if not math.isfinite(total) or total < 0:
            raise CalculoInconsistenteError(f"El costo calculado para {self.codigo} no es válido: {total}.")
        return round(total, 2)


class Sala(Servicio):
    """Reserva de salas. Se cobra por hora; las salas grandes llevan recargo."""

    TARIFA_BASE = 50000
    UNIDAD = "hora"
    DURACION_MAXIMA = 12
    ESTADO_RESERVADO = "Ocupada"
    # Las salas de más de 20 personas cuestan un 10 % más.
    CAPACIDAD_CON_RECARGO = 20
    RECARGO = 0.10

    def __init__(self, codigo, nombre, capacidad, estado="Disponible", tarifa=None):
        self.tarifa = tarifa
        self.codigo = codigo
        self.nombre = nombre
        self.capacidad = capacidad
        self.estado = estado

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El código de la sala no puede estar vacío.")
        self.__codigo = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El nombre de la sala no puede estar vacío.")
        self.__nombre = valor

    @property
    def capacidad(self):
        return self.__capacidad

    @capacidad.setter
    def capacidad(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError) as error:
            raise ServicioNoDisponibleError("La capacidad debe ser un número entero.") from error
        if valor <= 0:
            raise ServicioNoDisponibleError("La capacidad debe ser mayor que cero.")
        self.__capacidad = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        estados_validos = ["Disponible", "Ocupada", "Mantenimiento"]
        if valor not in estados_validos:
            raise ServicioNoDisponibleError(f"Estado inválido. Debe ser uno de: {estados_validos}")
        self.__estado = valor

    def mostrar_informacion(self):
        return f"Sala {self.codigo} - {self.nombre} | Capacidad: {self.capacidad} | Estado: {self.estado}"

    # --- Métodos sobrescritos de Servicio ---
    def calcular_costo(self, duracion):
        # duracion en horas.
        costo = self.tarifa * duracion
        if self.capacidad > self.CAPACIDAD_CON_RECARGO:
            costo *= 1 + self.RECARGO
        return costo

    def describir(self):
        return f"{self.mostrar_informacion()} | Tarifa: ${self.tarifa:,.0f} por hora"


class Equipo(Servicio):
    """Alquiler de equipos. Se cobra por día completo."""

    TARIFA_BASE = 30000
    UNIDAD = "día"
    DURACION_MAXIMA = 30
    ESTADO_RESERVADO = "Reservado"

    def __init__(self, codigo, nombre, tipo, estado="Disponible", tarifa=None):
        self.tarifa = tarifa
        self.codigo = codigo
        self.nombre = nombre
        self.tipo = tipo
        self.estado = estado

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El código del equipo no puede estar vacío.")
        self.__codigo = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El nombre del equipo no puede estar vacío.")
        self.__nombre = valor

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El tipo de equipo no puede estar vacío.")
        self.__tipo = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        estados_validos = ["Disponible", "Reservado", "Mantenimiento"]
        if valor not in estados_validos:
            raise ServicioNoDisponibleError(f"Estado inválido. Debe ser uno de: {estados_validos}")
        self.__estado = valor

    def mostrar_informacion(self):
        return f"Equipo {self.codigo} - {self.nombre} | Tipo: {self.tipo} | Estado: {self.estado}"

    # --- Métodos sobrescritos de Servicio ---
    def calcular_costo(self, duracion):
        # duracion en días.
        return self.tarifa * duracion

    def describir(self):
        return f"{self.mostrar_informacion()} | Tarifa: ${self.tarifa:,.0f} por día"

    def validar_parametros(self, duracion):
        # Primero las reglas generales y luego la propia: los equipos se alquilan por días completos.
        super().validar_parametros(duracion)
        if duracion != int(duracion):
            raise ParametroInvalidoError(f"El equipo {self.codigo} se alquila por días completos, no por {duracion:g}.")


class Asesoria(Servicio):
    """Asesoría especializada. Se cobra por hora, con un mínimo de minutos facturables."""

    TARIFA_BASE = 80000
    UNIDAD = "hora"
    DURACION_MAXIMA = 8
    ESTADO_RESERVADO = "Reservada"

    def __init__(self, codigo, tema, duracion, estado="Disponible", tarifa=None):
        self.tarifa = tarifa
        self.codigo = codigo
        self.tema = tema
        self.duracion = duracion
        self.estado = estado

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El código de la asesoría no puede estar vacío.")
        self.__codigo = valor

    @property
    def tema(self):
        return self.__tema

    @tema.setter
    def tema(self, valor):
        if not valor or not str(valor).strip():
            raise ServicioNoDisponibleError("El tema de la asesoría no puede estar vacío.")
        self.__tema = valor

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError) as error:
            raise ServicioNoDisponibleError("La duración debe ser un número entero.") from error
        if valor <= 0:
            raise ServicioNoDisponibleError("La duración debe ser mayor que cero.")
        self.__duracion = valor

    @property
    def estado(self):
        return self.__estado

    @estado.setter
    def estado(self, valor):
        estados_validos = ["Disponible", "Reservada", "Cancelada"]
        if valor not in estados_validos:
            raise ServicioNoDisponibleError(f"Estado inválido. Debe ser uno de: {estados_validos}")
        self.__estado = valor

    def mostrar_informacion(self):
        return f"Asesoría {self.codigo} - {self.tema} | Duración: {self.duracion} minutos | Estado: {self.estado}"

    # --- Métodos sobrescritos de Servicio ---
    def calcular_costo(self, duracion):
        # duracion en horas; se cobra como mínimo la duración mínima de la asesoría (en minutos).
        horas_facturadas = max(duracion, self.duracion / 60)
        return self.tarifa * horas_facturadas

    def describir(self):
        return f"{self.mostrar_informacion()} | Tarifa: ${self.tarifa:,.0f} por hora"
