# =============================================================================
# EJERCICIO 5: Testear múltiples casos con subTest
# =============================================================================
# Escribe un test "test_es_par" que verifique, para una lista de pares
# (entrada, esperado), que la función "es_par" devuelve el resultado
# esperado en cada caso.
#
# En pytest esto se haría con @pytest.mark.parametrize. En unittest se
# usa self.subTest, que ejecuta varios casos dentro de un mismo test y
# muestra individualmente cuál falla.
#
# Patrón:
#   for entrada, esperado in casos:
#       with self.subTest(entrada=entrada):
#           self.assertEqual(es_par(entrada), esperado)
#
# Casos a probar:
#   (0, True), (1, False), (2, True), (-4, True), (-7, False), (100, True)
#
# RESULTADO ESPERADO:
# Ran 1 test in 0.000s
#
# OK
# =============================================================================

import unittest


def es_par(n):
    return n % 2 == 0


class TestEsPar(unittest.TestCase):
    def test_es_par(self):
        # Tu código aquí
        pass


unittest.main(argv=[""], exit=False, verbosity=0)
