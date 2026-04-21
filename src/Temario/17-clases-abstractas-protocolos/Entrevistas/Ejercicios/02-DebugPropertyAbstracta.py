# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Property abstracta con decoradores invertidos
# =============================================================================
# El siguiente código intenta definir una clase abstracta Dispositivo con
# una property abstracta `voltaje`. Tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Portátil: 19.5V
# Móvil: 5.0V
# Error al instanciar DispositivoDefectuoso
# =============================================================================

from abc import ABC, abstractmethod


class Dispositivo(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod
    @property
    def voltaje(self):
        pass

    def ficha(self):
        return f"{self.nombre}: {self.voltaje}V"


class Portatil(Dispositivo):
    def voltaje(self):
        return 19.5


class Movil(Dispositivo):
    @property
    def voltaje(self):
        return 5.0


class DispositivoDefectuoso(Dispositivo):
    pass


print(Portatil("Portátil").ficha())
print(Movil("Móvil").ficha())

try:
    d = DispositivoDefectuoso("Roto")
except TypeError:
    print("Error al instanciar DispositivoDefectuoso")
