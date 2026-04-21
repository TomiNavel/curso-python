from abc import ABC, abstractmethod


class Empleado(ABC):
    def __init__(self, nombre, horas_trabajadas):
        self.nombre = nombre
        self.horas_trabajadas = horas_trabajadas

    @abstractmethod
    def tarifa_hora(self):
        pass

    def calcular_sueldo(self):
        return self.horas_trabajadas * self.tarifa_hora()

    def __str__(self):
        return f"{self.nombre}: ${self.calcular_sueldo():,.2f}"


class EmpleadoJunior(Empleado):
    def tarifa_hora(self):
        return 15


class EmpleadoSenior(Empleado):
    def tarifa_hora(self):
        return 40


class EmpleadoManager(Empleado):
    def tarifa_hora(self):
        return 60


empleados = [
    EmpleadoJunior("Ana", 160),
    EmpleadoSenior("Luis", 160),
    EmpleadoManager("María", 160),
]

for e in empleados:
    print(e)
