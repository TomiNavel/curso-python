class Empleado:
    def __init__(self, nombre, salario_base):
        self.nombre = nombre
        self.salario_base = salario_base

    def salario_total(self):
        return self.salario_base

    def resumen(self):
        return f"{self.nombre} - Empleado: ${self.salario_total():,.2f}"

    def __repr__(self):
        return f"Empleado({self.nombre!r}, {self.salario_base})"


class Gerente(Empleado):
    def __init__(self, nombre, salario_base, bono):
        super().__init__(nombre, salario_base)
        self.bono = bono

    def salario_total(self):
        return super().salario_total() + self.bono

    def resumen(self):
        return f"{super().resumen()} [Gerente, bono: ${self.bono:,.2f}]"


class Desarrollador(Empleado):
    def __init__(self, nombre, salario_base, lenguaje):
        super().__init__(nombre, salario_base)
        self.lenguaje = lenguaje

    def resumen(self):
        return f"{super().resumen()} [Dev: {self.lenguaje}]"


class TechLead(Desarrollador, Gerente):
    def __init__(self, nombre, salario_base, bono, lenguaje):
        # super() sigue el MRO: TechLead -> Desarrollador -> Gerente -> Empleado
        # Necesitamos pasar todos los argumentos correctamente
        Empleado.__init__(self, nombre, salario_base)
        self.bono = bono
        self.lenguaje = lenguaje

    def salario_total(self):
        return self.salario_base + self.bono

    def resumen(self):
        return f"{Desarrollador.resumen(self)} + TechLead"


ana = Empleado("Ana", 3000)
bob = Gerente("Bob", 5000, 1000)
carlos = Desarrollador("Carlos", 4000, "Python")
diana = TechLead("Diana", 4500, 1500, "Go")

for emp in [ana, bob, carlos, diana]:
    print(emp.resumen())

mro = " -> ".join(c.__name__ for c in TechLead.__mro__)
print(f"MRO de TechLead: {mro}")
