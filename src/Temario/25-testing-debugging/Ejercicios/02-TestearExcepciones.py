# =============================================================================
# EJERCICIO 2: Testear que una función lanza excepciones
# =============================================================================
# La función "dividir(a, b)" debe lanzar ValueError si b es 0. Completa
# los dos tests:
#   - test_division_normal: dividir(10, 2) debe devolver 5.
#   - test_division_por_cero: dividir(10, 0) debe lanzar ValueError.
#
# Para el segundo test, usa self.assertRaises como context manager:
#     with self.assertRaises(ValueError):
#         dividir(10, 0)
#
# RESULTADO ESPERADO:
# Ran 2 tests in 0.000s
#
# OK
# =============================================================================

import unittest


def dividir(a, b):
    if b == 0:
        raise ValueError("no se puede dividir por cero")
    return a / b


class TestDividir(unittest.TestCase):
    # Tu código aquí

    pass


unittest.main(argv=[""], exit=False, verbosity=0)
