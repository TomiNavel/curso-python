# =============================================================================
# EJERCICIO 1: Explorar un Módulo
# =============================================================================
# Crea una función `explorar_modulo` que reciba el nombre de un módulo (como
# string) y devuelva un diccionario con información sobre él.
#
# La función debe:
# - Importar el módulo dinámicamente usando __import__
# - Devolver un diccionario con:
#   - "nombre": el nombre del módulo
#   - "funciones": lista de nombres públicos (no empiezan con _) que son callable
#   - "constantes": lista de nombres públicos que están en MAYÚSCULAS y no son callable
#   - "total_publicos": número total de nombres públicos (no empiezan con _)
# - Si el módulo no existe, devolver {"error": "Módulo 'nombre' no encontrado"}
#
# RESULTADO ESPERADO:
# math:
#   nombre: math
#   funciones incluyen: ['ceil', 'floor', 'sqrt'] (entre otras)
#   constantes incluyen: ['e', 'pi'] (entre otras)
#   total_publicos: > 40
#
# string:
#   nombre: string
#   constantes incluyen: ['ascii_letters', 'digits'] (entre otras)
#
# modulo_falso:
#   {'error': "Módulo 'modulo_falso' no encontrado"}
# =============================================================================

# Tu código aquí

# info_math = explorar_modulo("math")
# print(f"Nombre: {info_math['nombre']}")
# print(f"Funciones (primeras 5): {info_math['funciones'][:5]}")
# print(f"Constantes: {info_math['constantes']}")
# print(f"Total públicos: {info_math['total_publicos']}")
# print()
# info_string = explorar_modulo("string")
# print(f"Nombre: {info_string['nombre']}")
# print(f"Constantes: {info_string['constantes']}")
# print()
# info_falso = explorar_modulo("modulo_falso")
# print(info_falso)
