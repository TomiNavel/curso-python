# =============================================================================
# SOLUCIÓN
# =============================================================================

import unittest


class Cuenta:
    def __init__(self, saldo):
        self.saldo = saldo

    def ingresar(self, cantidad):
        self.saldo += cantidad


class TestCuenta(unittest.TestCase):
    def setUp(self):
        # setUp se ejecuta antes de cada test, así que cada test parte de
        # una cuenta nueva. Esto garantiza que test_ingresar no contamine
        # el saldo visto por test_saldo_inicial.
        self.cuenta = Cuenta(100)

    def test_saldo_inicial(self):
        self.assertEqual(self.cuenta.saldo, 100)

    def test_ingresar(self):
        self.cuenta.ingresar(50)
        self.assertEqual(self.cuenta.saldo, 150)


unittest.main(argv=[""], exit=False, verbosity=0)
