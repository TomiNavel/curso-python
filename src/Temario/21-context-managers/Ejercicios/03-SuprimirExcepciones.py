# =============================================================================
# EJERCICIO 3: Suprimir excepciones con suppress
# =============================================================================
# Implementa una función "obtener_valor" que reciba un diccionario y una
# lista de claves. La función debe intentar acceder a cada clave del
# diccionario y devolver el primer valor que encuentre. Si ninguna clave
# existe, debe devolver None.
#
# Usa suppress(KeyError) para manejar las claves inexistentes de forma
# limpia, sin bloques try/except explícitos.
#
# RESULTADO ESPERADO:
# Ana
# 30
# None
# =============================================================================

from contextlib import suppress

# Tu código aquí


# Pruebas
datos = {"nombre": "Ana", "edad": 30}

print(obtener_valor(datos, ["nombre", "edad"]))
print(obtener_valor(datos, ["altura", "peso", "edad"]))
print(obtener_valor(datos, ["altura", "peso"]))
