# =====================
# SOLUCIÓN
# =====================
# Error 1: todas las lambdas capturan una referencia a la misma variable exp.
#   Cuando el bucle termina, exp vale 4 y todas devuelven 2 ** 4 = 16.
#   Corrección: lambda exp=exp: 2 ** exp
#
# Error 2: todas las funciones capturan una referencia a la misma variable nombre.
#   Cuando el bucle termina, nombre vale "Luis" y todas devuelven "Hola, Luis".
#   Corrección: def crear_saludo(nombre=nombre):
#
# ERRORES CORREGIDOS:
# 1. lambda: 2 ** exp → lambda exp=exp: 2 ** exp
# 2. def crear_saludo(): → def crear_saludo(nombre=nombre):


potencias = []
for exp in range(5):
    potencias.append(lambda exp=exp: 2 ** exp)

print(f"Potencias: {[f() for f in potencias]}")


nombres = ["Ana", "Pedro", "Luis"]
saludos = []
for nombre in nombres:
    def crear_saludo(nombre=nombre):
        return f"Hola, {nombre}"
    saludos.append(crear_saludo)

print(f"Saludos: {[f() for f in saludos]}")
