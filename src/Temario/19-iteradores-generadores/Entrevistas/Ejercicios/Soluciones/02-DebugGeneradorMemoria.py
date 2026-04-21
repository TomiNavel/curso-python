# =====================
# SOLUCIÓN
# =====================
# Error 1: "multiplos_de_cinco" construye una list comprehension completa,
#   materializando todos los múltiplos en memoria antes de continuar. Si el
#   límite es grande, esto consume mucha RAM innecesariamente. Solución:
#   convertirlo en una función generadora con yield, o devolver una generator
#   expression. Usamos yield para mantener el estilo explícito.
#
# Error 2: "cuadrados" acumula los resultados en una lista "resultado" y la
#   devuelve al final. Esto también materializa todos los valores en memoria.
#   Solución: convertirlo en un generador con yield, que produce cada cuadrado
#   bajo demanda sin guardar nada.
#
# Error 3: "sum([x for x in pipeline])" envuelve el generador en una list
#   comprehension, materializando todos los cuadrados antes de sumarlos.
#   Esto anula cualquier beneficio de usar generadores. Solución: pasar
#   directamente el generador a sum(), o usar una generator expression con
#   paréntesis en lugar de corchetes.
#
# ERRORES CORREGIDOS:
# 1. Convertir multiplos_de_cinco en generador (yield)
# 2. Convertir cuadrados en generador (yield)
# 3. Eliminar la list comprehension dentro de sum()


def multiplos_de_cinco(limite):
    for n in range(limite):
        if n % 5 == 0:
            yield n


def cuadrados(numeros):
    for n in numeros:
        yield n * n


limite = 100_000
pipeline = cuadrados(multiplos_de_cinco(limite))
print(sum(pipeline))
