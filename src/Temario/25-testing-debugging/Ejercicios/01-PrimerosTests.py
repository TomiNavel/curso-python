# =============================================================================
# EJERCICIO 1: Escribir tus primeros tests con unittest
# =============================================================================
# Completa la clase "TestCalculadora" con tres tests para la función
# "sumar" definida abajo:
#   - test_positivos: sumar(2, 3) debe dar 5.
#   - test_negativos: sumar(-1, -1) debe dar -2.
#   - test_cero: sumar(0, 5) debe dar 5.
#
# Usa self.assertEqual para las comprobaciones.
#
# Nota: usamos unittest (biblioteca estándar) en lugar de pytest, que
# funciona igual conceptualmente pero no está disponible en este entorno.
#
# RESULTADO ESPERADO (aproximado):
# Ran 3 tests in 0.000s
#
# OK
# =============================================================================

import unittest


def sumar(a, b):
    return a + b


class TestCalculadora(unittest.TestCase):
    # Tu código aquí

    pass


unittest.main(argv=[""], exit=False, verbosity=0)
