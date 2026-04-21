from abc import ABC, abstractmethod


class Vehiculo(ABC):
    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo

    @property
    @abstractmethod
    def num_ruedas(self):
        pass

    @property
    @abstractmethod
    def consumo_medio(self):
        pass

    def ficha(self):
        return f"{self.marca} {self.modelo}: {self.num_ruedas} ruedas, {self.consumo_medio} l/100km"


class Coche(Vehiculo):
    @property
    def num_ruedas(self):
        return 4

    @property
    def consumo_medio(self):
        return 6.5


class Moto(Vehiculo):
    @property
    def num_ruedas(self):
        return 2

    @property
    def consumo_medio(self):
        return 4.2


class Camion(Vehiculo):
    @property
    def num_ruedas(self):
        return 6

    @property
    def consumo_medio(self):
        return 22.0


vehiculos = [
    Coche("Toyota", "Corolla"),
    Moto("Yamaha", "MT-07"),
    Camion("Volvo", "FH"),
]

for v in vehiculos:
    print(v.ficha())
