class LogMixin:
    _contador_log = 0

    def __init__(self):
        self._log = []

    def registrar(self, mensaje):
        LogMixin._contador_log += 1
        self._log.append((LogMixin._contador_log, mensaje))

    def ver_log(self):
        return [f"[{num}] {msg}" for num, msg in self._log]


class Calculadora(LogMixin):
    def __init__(self):
        super().__init__()
        self.resultado = 0.0

    def sumar(self, n):
        self.resultado += n
        self.registrar(f"sumar {n}")

    def restar(self, n):
        self.resultado -= n
        self.registrar(f"restar {n}")

    def __str__(self):
        return f"Resultado: {self.resultado}"


class Inventario(LogMixin):
    def __init__(self):
        super().__init__()
        self.items = {}

    def agregar(self, nombre, cantidad):
        self.items[nombre] = self.items.get(nombre, 0) + cantidad
        self.registrar(f"agregar {nombre}: {cantidad}")

    def retirar(self, nombre, cantidad):
        actual = self.items.get(nombre, 0)
        if actual < cantidad:
            raise ValueError(f"Stock insuficiente de {nombre}: {actual} < {cantidad}")
        self.items[nombre] -= cantidad
        if self.items[nombre] == 0:
            del self.items[nombre]
        self.registrar(f"retirar {nombre}: {cantidad}")

    def __str__(self):
        return f"Inventario: {len(self.items)} productos"


calc = Calculadora()
calc.sumar(10)
calc.sumar(5)
print(calc)
print("Log calculadora:")
for linea in calc.ver_log():
    print(linea)
print()

inv = Inventario()
inv.agregar("Laptop", 5)
inv.agregar("Mouse", 10)
inv.retirar("Mouse", 3)
print(inv)
print("Log inventario:")
for linea in inv.ver_log():
    print(linea)
