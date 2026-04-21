class CuentaBancaria:
    def __init__(self, titular, saldo=0):
        self.titular = titular
        self._saldo = float(saldo)

    @property
    def titular(self):
        return self._titular

    @titular.setter
    def titular(self, valor):
        if not valor or not valor.strip():
            raise ValueError("El titular no puede estar vacío")
        self._titular = valor.strip()

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self._saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self._saldo:
            raise ValueError("Saldo insuficiente")
        self._saldo -= monto

    def __str__(self):
        return f"Cuenta de {self._titular}: ${self._saldo:,.2f}"

    def __repr__(self):
        return f"CuentaBancaria({self._titular!r}, {self._saldo})"


c = CuentaBancaria("Ana", 1000)
print(c)
c.depositar(500)
print(c)
c.retirar(300)
print(c)

try:
    c.depositar(-100)
except ValueError as e:
    print(f"Error: {e}")

try:
    c.retirar(5000)
except ValueError as e:
    print(f"Error: {e}")

try:
    c.saldo = 999999
except AttributeError as e:
    print(f"Error: {e}")

print(repr(c))
