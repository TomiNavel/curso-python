# =============================================================================
# EJERCICIO 4: Extraer campos de un log
# =============================================================================
# Cada línea del log tiene el formato:
#   [YYYY-MM-DD HH:MM:SS] NIVEL: mensaje
#
# Escribe una función "parsear_log(linea)" que devuelva un diccionario con
# las claves "fecha", "nivel" y "mensaje". Si la línea no encaja con el
# formato, devuelve None.
#
# Usa grupos con nombre para extraer cada campo.
#
# RESULTADO ESPERADO:
# {'fecha': '2026-04-22 10:15:32', 'nivel': 'ERROR', 'mensaje': 'conexión rechazada'}
# {'fecha': '2026-04-22 10:16:04', 'nivel': 'INFO', 'mensaje': 'reintento satisfactorio'}
# None
# =============================================================================


# Tu código aquí


# Pruebas
print(parsear_log("[2026-04-22 10:15:32] ERROR: conexión rechazada"))
print(parsear_log("[2026-04-22 10:16:04] INFO: reintento satisfactorio"))
print(parsear_log("formato libre sin corchetes"))
