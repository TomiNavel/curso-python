# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Mocks configurados incorrectamente
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "procesar_pedido" pide el stock al servicio. Si hay stock
# suficiente, llama a servicio.reservar con la cantidad y devuelve el
# identificador de reserva. Si no hay suficiente, lanza ValueError.
#
# Los tests deben verificar ambos caminos usando Mock.
#
# RESULTADO ESPERADO:
# Ran 2 tests in 0.000s
#
# OK
# =============================================================================

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
        servicio.consultar_stock = 50
        servicio.reservar.return_value = "R-001"

        resultado = procesar_pedido(servicio, 10)
        self.assertEqual(resultado, "R-001")
        servicio.reservar.assert_called_once_with(50)

    def test_sin_stock(self):
        servicio = Mock()
        servicio.consultar_stock.return_value = 5

        with self.assertRaises(RuntimeError):
            procesar_pedido(servicio, 10)


unittest.main(argv=[""], exit=False, verbosity=0)
