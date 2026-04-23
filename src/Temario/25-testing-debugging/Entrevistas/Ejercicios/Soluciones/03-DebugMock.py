# =====================
# SOLUCIÓN
# =====================
# Error 1: "servicio.consultar_stock = 50" sustituye el método del mock
#   por un entero. Cuando el código llama servicio.consultar_stock(),
#   Python intenta invocar a un int y lanza TypeError. La forma correcta
#   de configurar el valor que devuelve un método del mock es
#   "servicio.consultar_stock.return_value = 50".
#   Solución: usar return_value.
#
# Error 2: "servicio.reservar.assert_called_once_with(50)" verifica que
#   se llamó con la cantidad 50 (el stock), pero procesar_pedido llama
#   a reservar con la cantidad pedida (10). El test debe comprobar que
#   se pasó 10.
#   Solución: cambiar 50 por 10.
#
# Error 3: test_sin_stock espera RuntimeError, pero la función lanza
#   ValueError. Aunque ambos sean excepciones, ser específico es
#   importante — capturar la excepción equivocada enmascara bugs reales
#   del código productivo.
#   Solución: cambiar RuntimeError por ValueError.
#
# ERRORES CORREGIDOS:
# 1. consultar_stock = 50 → consultar_stock.return_value = 50
# 2. assert_called_once_with(50) → assert_called_once_with(10)
# 3. assertRaises(RuntimeError) → assertRaises(ValueError)

import unittest
from unittest.mock import Mock


def procesar_pedido(servicio, cantidad):
    stock = servicio.consultar_stock()
    if stock < cantidad:
        raise ValueError("sin stock suficiente")
    return servicio.reservar(cantidad)


class TestProcesarPedido(unittest.TestCase):
    def test_reserva_correcta(self):
        servicio = Mock()
        servicio.consultar_stock.return_value = 50
        servicio.reservar.return_value = "R-001"

        resultado = procesar_pedido(servicio, 10)
        self.assertEqual(resultado, "R-001")
        servicio.reservar.assert_called_once_with(10)

    def test_sin_stock(self):
        servicio = Mock()
        servicio.consultar_stock.return_value = 5

        with self.assertRaises(ValueError):
            procesar_pedido(servicio, 10)


unittest.main(argv=[""], exit=False, verbosity=0)
