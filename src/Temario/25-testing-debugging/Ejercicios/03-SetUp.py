# =============================================================================
# EJERCICIO 3: Usar setUp para preparar datos comunes
# =============================================================================
# Completa la clase "TestCuenta" con el método "setUp" y dos tests:
#   - setUp: crea una cuenta con saldo inicial de 100, accesible como
#     self.cuenta.
#   - test_saldo_inicial: comprueba que self.cuenta.saldo == 100.
#   - test_ingresar: ingresa 50 y comprueba que el saldo queda en 150.
#
# setUp se ejecuta antes de cada test, así que cada uno parte de una
# cuenta nueva con saldo 100.
#
# RESULTADO ESPERADO:
# Ran 2 tests in 0.000s
#
# OK
# =============================================================================

import unittest


class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

    def ingresar(self, cantidad):
        self.saldo += cantidad


class TestCuenta(unittest.TestCase):
    # Tu código aquí

    pass


unittest.main(argv=[""], exit=False, verbosity=0)
