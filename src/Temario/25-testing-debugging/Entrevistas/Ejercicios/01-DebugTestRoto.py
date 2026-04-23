# =============================================================================
# EJERCICIO DE ENTREVISTA 1: Debug — Test que no se ejecuta
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# El objetivo es testear la función "invertir_lista" con tres casos:
# lista normal, lista vacía y lista de un único elemento. Cuando se
# ejecuta, unittest debería mostrar que corre 3 tests y que todos pasan.
#
# RESULTADO ESPERADO (aproximado):
# Ran 3 tests in 0.000s
#
# OK
# =============================================================================

import unittest


def invertir_lista(lista):
    return lista[::-1]


class TestInvertir(unittest.TestCase):
    def verificar_normal(self):
        self.assertEqual(invertir_lista([1, 2, 3]), [3, 2, 1])

    def test_vacia(self):
        self.assertEquals(invertir_lista([]), [])

    def test_un_elemento():
        self.assertEqual(invertir_lista([42]), [42])


unittest.main(argv=[""], exit=False, verbosity=0)
