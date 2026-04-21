# =====================
# SOLUCIÓN
# =====================
# Error 1: El campo "roles" no tiene anotación de tipo. Sin anotación, no es
#   un campo de la dataclass: es un atributo de clase compartido por todas las
#   instancias. La línea "roles = []" crea una sola lista compartida.
#   Solución: añadir anotación "roles: list".
#
# Error 2: Aun con anotación, "roles: list = []" es ilegal en dataclasses
#   porque las listas (y otros mutables) no pueden usarse como valor por
#   defecto. Python detecta esto y lanza ValueError al definir la clase.
#   Solución: usar field(default_factory=list).
#
# Error 3: El campo "roles" se declara antes que "nombre" y "edad", pero
#   "nombre" no tiene valor por defecto mientras que "roles" sí. En
#   dataclasses, los campos sin valor por defecto deben ir antes que los
#   campos con valor por defecto. Solución: reordenar los campos, poniendo
#   "roles" al final.
#
# ERRORES CORREGIDOS:
# 1. Añadir anotación de tipo a "roles"
# 2. Usar field(default_factory=list) en lugar de []
# 3. Reordenar los campos para que los obligatorios vayan primero


from dataclasses import dataclass, field


@dataclass
class Usuario:
    nombre: str
    edad: int = 0
    roles: list = field(default_factory=list)


u1 = Usuario("Ana", 30)
u1.roles.append("admin")

u2 = Usuario("Luis", 25)

print(u1)
print(u2)
print(u1.roles is u2.roles)
