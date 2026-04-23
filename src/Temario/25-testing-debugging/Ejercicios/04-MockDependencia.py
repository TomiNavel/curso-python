# =============================================================================
# EJERCICIO 4: Usar Mock para sustituir una dependencia
# =============================================================================
# La función "enviar_alerta" recibe un servicio con un método "enviar" y
# un mensaje. Debe llamar a servicio.enviar(mensaje) y devolver True si
# la llamada no lanzó excepción, False si lanzó.
#
# Completa dos tests:
#   - test_envio_correcto: configura un Mock cuyo método enviar no lance
#     nada. La función debe devolver True y el Mock debe haber sido
#     llamado una vez con el mensaje.
#   - test_envio_falla: configura un Mock cuyo método enviar lance una
#     excepción (usa side_effect=RuntimeError("fallo")). La función debe
#     devolver False.
#
# Pistas:
#   servicio.enviar.assert_called_once_with("hola")
#   servicio.enviar.side_effect = RuntimeError("fallo")
#
# RESULTADO ESPERADO:
# Ran 2 tests in 0.000s
#
# OK
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
    # Tu código aquí

    pass


unittest.main(argv=[""], exit=False, verbosity=0)
