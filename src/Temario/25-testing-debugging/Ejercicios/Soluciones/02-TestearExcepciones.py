# =============================================================================
# SOLUCIÓN
# =============================================================================

import unittest


def dividir(a, b):
    if b == 0:
        raise ValueError("no se puede dividir por cero")
    return a / b


class TestDividir(unittest.TestCase):
    def test_division_normal(self):
        self.assertEqual(dividir(10, 2), 5)

    def test_division_por_cero(self):
        # assertRaises funciona como context manager: el bloque with ejecuta
        # el código y espera que lance la excepción indicada. Si no la lanza,
        # el test falla.
        with self.assertRaises(ValueError):
            dividir(10, 0)


unittest.main(argv=[""], exit=False, verbosity=0)
