# =====================
# SOLUCIÓN
# =====================
# Error 1: "assertRaises(ValueError, crear_usuario("", 30))" invoca la
#   función ANTES de pasarla a assertRaises. Python evalúa el argumento,
#   crear_usuario lanza ValueError, y el test falla con una excepción
#   sin capturar. La forma correcta es pasar la función SIN llamarla,
#   con los argumentos aparte, o usar el patrón con context manager:
#     with self.assertRaises(ValueError):
#         crear_usuario("", 30)
#   Solución: usar el patrón context manager, que es el idiomático.
#
# Error 2: test_edad_negativa espera TypeError, pero el código lanza
#   ValueError. El test falla porque la excepción concreta no coincide.
#   Ser específico con el tipo de excepción es correcto (evita enmascarar
#   errores), pero hay que usar el tipo correcto.
#   Solución: cambiar TypeError por ValueError.
#
# Error 3: aunque pequeño, test_usuario_valido no tiene error evidente
#   en la ejecución, pero la redacción del test con assertRaises a la
#   vieja (pasando función + argumentos) nunca debería usarse; por
#   consistencia se convierten todos los tests de excepciones al patrón
#   context manager (with assertRaises). Esto es más legible y uniforme.
#
# ERRORES CORREGIDOS:
# 1. assertRaises(..., funcion(args)) → with self.assertRaises: funcion(args)
# 2. TypeError → ValueError
# 3. (estilo) mantener patrón context manager en todos los tests de excepción

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
        with self.assertRaises(ValueError):
            crear_usuario("", 30)

    def test_edad_negativa(self):
        with self.assertRaises(ValueError):
            crear_usuario("Ana", -5)


unittest.main(argv=[""], exit=False, verbosity=0)
