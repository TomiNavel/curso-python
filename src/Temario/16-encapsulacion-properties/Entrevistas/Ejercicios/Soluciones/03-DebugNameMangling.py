# =====================
# SOLUCIÓN
# =====================
# Error 1: En depositar(), self._saldo accede con un solo guion bajo.
#   El atributo se definió como self.__saldo (doble guion bajo), por lo que
#   Python aplica name mangling y lo almacena como _CajaFuerte__saldo.
#   self._saldo es un atributo distinto que no existe.
#   Solución: self.__saldo = self.__saldo + monto
#
# Error 2: En saldo_disponible property, self._saldo tiene el mismo problema.
#   Solución: return self.__saldo
#
# Error 3: En __str__, self._saldo tiene el mismo problema.
#   Solución: self.__saldo
#
# ERRORES CORREGIDOS:
# 1. self._saldo = self._saldo + monto -> self.__saldo = self.__saldo + monto
# 2. return self._saldo -> return self.__saldo en property
# 3. self._saldo -> self.__saldo en __str__


class CajaFuerte:
    def __init__(self, saldo_inicial):
        self.__saldo = saldo_inicial

    def consultar(self):
        return self.__saldo

    def depositar(self, monto):
        self.__saldo = self.__saldo + monto

    @property
    def saldo_disponible(self):
        return self.__saldo

    def __str__(self):
        return f"CajaFuerte(saldo={self.__saldo})"


cf = CajaFuerte(1000)
print(f"Saldo: {cf.consultar()}")
cf.depositar(500)
print(f"Saldo tras depósito: {cf.consultar()}")

try:
    print(cf.__saldo)
except AttributeError:
    print("Intentando acceso directo: no accesible como __saldo")

print(f"Acceso vía name mangling: {cf._CajaFuerte__saldo}")
print(f"Property: {cf.saldo_disponible}")
