# =====================
# SOLUCIÓN
# =====================
# Error 1: En la clase abstracta Dispositivo, el orden de los decoradores está
#   invertido. Debe ser @property encima y @abstractmethod debajo. Con el orden
#   actual (@abstractmethod encima), el comportamiento de property no se aplica
#   correctamente sobre la declaración abstracta.
#
# Error 2: Portatil implementa voltaje como un método normal (sin @property).
#   Al ser una clase abstracta con property abstracta, la subclase debe definir
#   también una property, no un método. Con el código actual, self.voltaje en
#   ficha() devolvería el método (función) en lugar del valor.
#
# Error 3: DispositivoDefectuoso no implementa la property voltaje. Es una
#   subclase incompleta, pero el error solo se verá al instanciar. El ejercicio
#   ya prevé este caso con el try/except, así que no es un error a "corregir",
#   sino a verificar que funciona correctamente una vez arreglados los errores 1 y 2.
#
# ERRORES CORREGIDOS:
# 1. Invertir @abstractmethod / @property en Dispositivo
# 2. Añadir @property en Portatil


from abc import ABC, abstractmethod


class Dispositivo(ABC):
    def __init__(self, nombre):
        self.nombre = nombre

    @property
    @abstractmethod
    def voltaje(self):
        pass

    def ficha(self):
        return f"{self.nombre}: {self.voltaje}V"


class Portatil(Dispositivo):
    @property
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
