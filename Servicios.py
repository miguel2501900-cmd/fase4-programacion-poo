from excepciones import ServicioNoDisponibleError


class Sala:
    def __init__(self, codigo, nombre, capacidad, estado="Disponible"):
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
        except ValueError:
            raise ServicioNoDisponibleError("La capacidad debe ser un número entero.")
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


class Equipo:
    def __init__(self, codigo, nombre, tipo, estado="Disponible"):
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


class Asesoria:
    def __init__(self, codigo, tema, duracion, estado="Disponible"):
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
        except ValueError:
            raise ServicioNoDisponibleError("La duración debe ser un número entero.")
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