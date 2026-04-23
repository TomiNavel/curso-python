# =============================================================================
# SOLUCIÓN
# =============================================================================

import unittest


def es_par(n):
    return n % 2 == 0


class TestEsPar(unittest.TestCase):
    def test_es_par(self):
        casos = [
            (0, True),
            (1, False),
            (2, True),
            (-4, True),
            (-7, False),
            (100, True),
        ]
        # subTest convierte cada iteración en un subcaso independiente:
        # si uno falla, el test continúa y reporta solo el que falló. En
        # pytest el patrón equivalente es @pytest.mark.parametrize.
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(es_par(entrada), esperado)


unittest.main(argv=[""], exit=False, verbosity=0)
