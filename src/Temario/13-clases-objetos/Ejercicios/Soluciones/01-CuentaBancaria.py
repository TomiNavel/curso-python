class CuentaBancaria:
    total_cuentas = 0

    def __init__(self, titular, saldo=0.0):
        self.titular = titular
        self.saldo = float(saldo)
        CuentaBancaria.total_cuentas += 1

    def depositar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        self.saldo += monto

    def retirar(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")
        if monto > self.saldo:
            raise ValueError(f"Saldo insuficiente: {self.saldo}")
        self.saldo -= monto

    def transferir(self, destino, monto):
        self.retirar(monto)
        destino.depositar(monto)

    def __repr__(self):
        return f"CuentaBancaria({self.titular!r}, {self.saldo})"

    def __str__(self):
        return f"Cuenta de {self.titular}: ${self.saldo:,.2f}"


cuenta_ana = CuentaBancaria("Ana", 1000)
cuenta_bob = CuentaBancaria("Bob", 500)
print(cuenta_ana)
cuenta_ana.depositar(300)
print(cuenta_ana)
cuenta_bob.depositar(200)
print(cuenta_bob)
cuenta_ana.transferir(cuenta_bob, 500)
print(cuenta_ana)
print(f"Total cuentas: {CuentaBancaria.total_cuentas}")
print(repr(cuenta_ana))
