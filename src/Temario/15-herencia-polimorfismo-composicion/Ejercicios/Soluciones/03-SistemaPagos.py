class TarjetaCredito:
    def __init__(self, numero):
        self.numero = numero

    def procesar(self, monto):
        return f"Pago de ${monto:.2f} con tarjeta *{self.numero}"

    def nombre_metodo(self):
        return "Tarjeta de crédito"


class PayPal:
    def __init__(self, email):
        self.email = email

    def procesar(self, monto):
        return f"Pago de ${monto:.2f} vía PayPal ({self.email})"

    def nombre_metodo(self):
        return "PayPal"


class Transferencia:
    def __init__(self, banco):
        self.banco = banco

    def procesar(self, monto):
        return f"Transferencia de ${monto:.2f} desde {self.banco}"

    def nombre_metodo(self):
        return "Transferencia bancaria"


def ejecutar_pagos(procesadores, monto):
    for proc in procesadores:
        print(f"[{proc.nombre_metodo()}] {proc.procesar(monto)}")


procesadores = [
    TarjetaCredito("1234"),
    PayPal("ana@mail.com"),
    Transferencia("BBVA"),
]
ejecutar_pagos(procesadores, 50)
