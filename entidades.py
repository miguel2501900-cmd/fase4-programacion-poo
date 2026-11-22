from abc import ABC, abstractmethod


class Entidad(ABC):
    """Clase abstracta que representa a las entidades generales del sistema.

    Cliente y Servicio heredan de ella. No se puede crear una Entidad directamente:
    solo define lo que toda entidad de Software FJ debe saber hacer.
    """

    @abstractmethod
    def identificador(self):
        """Devuelve el dato que distingue a la entidad dentro de su lista (cédula o código)."""

    @abstractmethod
    def describir(self):
        """Devuelve un texto con la información de la entidad, listo para mostrar."""

    def __str__(self):
        # Imprimir cualquier entidad muestra su descripción, sin importar de qué clase sea.
        return self.describir()
