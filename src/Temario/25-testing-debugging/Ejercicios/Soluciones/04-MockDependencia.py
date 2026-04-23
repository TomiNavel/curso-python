# =============================================================================
# SOLUCIÓN
# =============================================================================

import unittest
from unittest.mock import Mock


def enviar_alerta(servicio, mensaje):
    try:
        servicio.enviar(mensaje)
        return True
    except Exception:
        return False


class TestEnviarAlerta(unittest.TestCase):
    def test_envio_correcto(self):
        # Mock sin configurar side_effect no lanza nada. assert_called_once_with
        # verifica que el método se llamó exactamente una vez con el argumento
        # esperado, cubriendo dos cosas: que se llamó y que se llamó bien.
        servicio = Mock()
        resultado = enviar_alerta(servicio, "hola")
        self.assertTrue(resultado)
        servicio.enviar.assert_called_once_with("hola")

    def test_envio_falla(self):
        # side_effect=Excepción hace que la llamada al mock lance esa excepción.
        # Es la forma estándar de simular errores de dependencias externas.
        servicio = Mock()
        servicio.enviar.side_effect = RuntimeError("fallo")
        resultado = enviar_alerta(servicio, "hola")
        self.assertFalse(resultado)


unittest.main(argv=[""], exit=False, verbosity=0)
