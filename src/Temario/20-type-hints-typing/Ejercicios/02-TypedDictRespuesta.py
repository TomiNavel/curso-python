# =============================================================================
# EJERCICIO 2: TypedDict para respuesta de API
# =============================================================================
# Define un TypedDict llamado "RespuestaAPI" con las siguientes claves:
#   - status: int
#   - mensaje: str
#   - datos: list[dict[str, str]]
#
# Implementa una función "crear_respuesta" que reciba un código de estado (int)
# y una lista de usuarios (list[dict[str, str]]) y devuelva un RespuestaAPI.
# Si el código es 200, el mensaje debe ser "OK". En cualquier otro caso, "Error".
#
# RESULTADO ESPERADO:
# {'status': 200, 'mensaje': 'OK', 'datos': [{'nombre': 'Ana'}, {'nombre': 'Luis'}]}
# {'status': 404, 'mensaje': 'Error', 'datos': []}
# =============================================================================

# Tu código aquí


# Pruebas
usuarios = [{"nombre": "Ana"}, {"nombre": "Luis"}]
print(crear_respuesta(200, usuarios))
print(crear_respuesta(404, []))
