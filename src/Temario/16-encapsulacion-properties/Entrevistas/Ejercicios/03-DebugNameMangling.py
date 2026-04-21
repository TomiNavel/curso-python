# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Name mangling y encapsulación
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO:
# Saldo: 1000
# Saldo tras depósito: 1500
# Intentando acceso directo: no accesible como __saldo
# Acceso vía name mangling: 1500
# Property: 1500
# =============================================================================

class CajaFuerte:
    def __init__(self, saldo_inicial):
        self.__saldo = saldo_inicial

    def consultar(self):
        return self.__saldo

    def depositar(self, monto):
        self._saldo = self._saldo + monto  # un solo guion bajo

    @property
    def saldo_disponible(self):
        return self._saldo  # un solo guion bajo

    def __str__(self):
        return f"CajaFuerte(saldo={self._saldo})"  # un solo guion bajo


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
