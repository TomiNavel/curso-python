# =============================================================================
# EJERCICIO 5: Configuración Encapsulada
# =============================================================================
# Crea una clase `Configuracion` que use diferentes niveles de encapsulación.
#
# Atributos:
# - nombre (público): nombre de la configuración
# - _entorno (protegido): "dev", "staging" o "prod" — solo estos valores
#   permitidos (ValueError si otro). Property con getter y setter.
# - __secreto (privado con name mangling): string, accesible solo vía métodos.
#
# Properties:
# - entorno: getter y setter con validación (solo "dev", "staging", "prod")
# - es_produccion: property calculada, True si entorno == "prod"
#
# Métodos:
# - obtener_secreto(clave): devuelve el secreto solo si la clave es "admin".
#   Si no, devuelve "Acceso denegado".
# - cambiar_secreto(clave, nuevo_secreto): cambia el secreto solo si la
#   clave es "admin". Si no, lanza PermissionError.
#
# __str__: "Config 'API' [prod] (producción: True)"
# __repr__: Configuracion('API', 'prod')
#
# RESULTADO ESPERADO:
# Config 'API' [prod] (producción: True)
# Config 'API' [dev] (producción: False)
# Error entorno: Entorno inválido: test
# Secreto con clave correcta: s3cr3t_k3y
# Secreto con clave incorrecta: Acceso denegado
# Secreto cambiado: nueva_clave_123
# Name mangling: s3cr3t_k3y existe como _Configuracion__secreto
# =============================================================================

# Tu código aquí

# c = Configuracion("API", "prod", "s3cr3t_k3y")
# print(c)
# c.entorno = "dev"
# print(c)
#
# try:
#     c.entorno = "test"
# except ValueError as e:
#     print(f"Error entorno: {e}")
#
# print(f"Secreto con clave correcta: {c.obtener_secreto('admin')}")
# print(f"Secreto con clave incorrecta: {c.obtener_secreto('user')}")
#
# c.cambiar_secreto("admin", "nueva_clave_123")
# print(f"Secreto cambiado: {c.obtener_secreto('admin')}")
#
# # Demostrar name mangling
# print(f"Name mangling: s3cr3t_k3y existe como _Configuracion__secreto")
