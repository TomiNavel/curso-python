# =====================
# SOLUCIÓN
# =====================
# La solución encadena tres generadores perezosos:
# 1. enteros_positivos produce 1, 2, 3, ... de forma infinita con yield.
# 2. Una generator expression filtra los múltiplos de 3 (perezosa).
# 3. Otra generator expression eleva al cuadrado cada valor filtrado.
# 4. islice(..., 10) corta el pipeline a los primeros 10 elementos.
#
# En ningún momento se construye una lista completa: cada valor fluye por
# la tubería de generador en generador, y solo se pide lo necesario. Por eso
# partir de un generador infinito es seguro — islice detiene el consumo antes
# de que el generador base agote la memoria.


from itertools import islice


def enteros_positivos():
    n = 1
    while True:
        yield n
        n += 1


multiplos_de_tres = (n for n in enteros_positivos() if n % 3 == 0)
cuadrados = (n * n for n in multiplos_de_tres)
resultado = islice(cuadrados, 10)


print(list(resultado))
