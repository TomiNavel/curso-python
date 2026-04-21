# =====================
# SOLUCIÓN
# =====================
# El generador recorre el iterable de entrada y, por cada línea, aplica strip()
# para eliminar espacios y saltos de línea. Si el resultado de strip() es una
# cadena no vacía (truthy), se produce con yield. Este patrón es el equivalente
# perezoso de una list comprehension con condición, con la ventaja de que no
# materializa la lista completa en memoria y funciona con iterables arbitrarios,
# incluidos archivos muy grandes.


def lineas_no_vacias(lineas):
    for linea in lineas:
        limpia = linea.strip()
        if limpia:
            yield limpia


entrada1 = ["hola", "", "mundo", "   ", "python", ""]
print(list(lineas_no_vacias(entrada1)))

entrada2 = ["  linea uno  ", "\n", "linea dos", "   "]
print(list(lineas_no_vacias(entrada2)))
