# =============================================================================
# SOLUCIÓN
# =============================================================================

import unittest


def sumar(a, b):
    return a + b


class TestCalculadora(unittest.TestCase):
    def test_positivos(self):
        self.assertEqual(sumar(2, 3), 5)

    def test_negativos(self):
        self.assertEqual(sumar(-1, -1), -2)

    def test_cero(self):
        self.assertEqual(sumar(0, 5), 5)


# argv=[""] evita que unittest interprete argumentos de línea de comandos;
# exit=False impide que termine el programa al acabar los tests.
unittest.main(argv=[""], exit=False, verbosity=0)
