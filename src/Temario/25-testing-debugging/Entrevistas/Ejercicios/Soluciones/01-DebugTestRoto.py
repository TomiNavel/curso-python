# =====================
# SOLUCIÓN
# =====================
# Error 1: "verificar_normal" no empieza por "test_", así que unittest no
#   lo descubre como test. El método no falla — simplemente nunca se ejecuta.
#   Este fallo es especialmente silencioso: el test suite pasa "OK" pero
#   con menos tests de los esperados.
#   Solución: renombrar a "test_normal".
#
# Error 2: usa "assertEquals" (con s). Existe como alias histórico pero
#   está deprecado y en versiones modernas emite warning o falla. El
#   método canónico es "assertEqual" sin s.
#   Solución: cambiar a assertEqual.
#
# Error 3: "test_un_elemento" no recibe "self" como parámetro. Los métodos
#   de una clase TestCase son métodos de instancia y deben tener self.
#   Sin self, Python lanza TypeError al intentar ejecutarlo.
#   Solución: añadir self al parámetro.
#
# ERRORES CORREGIDOS:
# 1. verificar_normal → test_normal (unittest descubre solo test_*)
# 2. assertEquals → assertEqual
# 3. test_un_elemento() → test_un_elemento(self)

import unittest


def invertir_lista(lista):
    return lista[::-1]


class TestInvertir(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(invertir_lista([1, 2, 3]), [3, 2, 1])

    def test_vacia(self):
        self.assertEqual(invertir_lista([]), [])

    def test_un_elemento(self):
        self.assertEqual(invertir_lista([42]), [42])


unittest.main(argv=[""], exit=False, verbosity=0)
