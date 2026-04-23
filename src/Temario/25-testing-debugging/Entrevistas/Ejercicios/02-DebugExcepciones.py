# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Testeo de excepciones
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "crear_usuario" valida edad y nombre, lanzando ValueError
# si no cumplen. Los tests deben verificar que las excepciones se lanzan
# correctamente.
#
# RESULTADO ESPERADO:
# Ran 3 tests in 0.000s
#
# OK
# =============================================================================

import unittest


def crear_usuario(nombre, edad):
    if not nombre:
        raise ValueError("nombre vacío")
    if edad < 0:
        raise ValueError("edad negativa")
    return {"nombre": nombre, "edad": edad}


class TestCrearUsuario(unittest.TestCase):
    def test_usuario_valido(self):
        usuario = crear_usuario("Ana", 30)
        self.assertEqual(usuario, {"nombre": "Ana", "edad": 30})

    def test_nombre_vacio(self):
        self.assertRaises(ValueError, crear_usuario("", 30))

    def test_edad_negativa(self):
        with self.assertRaises(TypeError):
            crear_usuario("Ana", -5)


unittest.main(argv=[""], exit=False, verbosity=0)
