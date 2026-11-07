from excepciones import ClienteInvalidoError

class Cliente:
    def __init__(self, cedula, nombre, correo, telefono):
        self.cedula = cedula
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def cedula(self):
        return self.__cedula

    @cedula.setter
    def cedula(self, valor):
        if not valor:
            raise ClienteInvalidoError("La cédula no puede estar vacía.")
        if not str(valor).isnumeric():
            raise ClienteInvalidoError(f"Error en cédula '{valor}': Debe ser estrictamente numérico.")
        self.__cedula = valor

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or not str(valor).strip():
            raise ClienteInvalidoError("El nombre no puede estar vacío.")
        self.__nombre = valor

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not valor:
            raise ClienteInvalidoError("El correo electrónico no puede estar vacío.")
        if "@" not in str(valor):
            raise ClienteInvalidoError(f"Error en correo '{valor}': Debe llevar '@'.")
        self.__correo = valor

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor or not str(valor).strip():
            raise ClienteInvalidoError("El teléfono de contacto no puede estar vacío.")
        self.__telefono = valor