# =====================
# SOLUCIÓN
# =====================
# Error 1: El código emite nodo["valor"] incondicionalmente en todos los
#   nodos, pero el enunciado pide solo los valores de las hojas (nodos sin
#   hijos). Solución: emitir el valor solamente cuando el nodo no tiene
#   hijos, usando una comprobación sobre nodo["hijos"].
#
# Error 2: La llamada recursiva "hojas(hijo)" crea un generador pero no
#   consume sus valores. Un generador solo produce cuando alguien itera
#   sobre él, así que esta línea no tiene ningún efecto visible. Solución:
#   usar "yield from hojas(hijo)" para delegar la iteración del sub-generador
#   y reemitir todos sus valores.
#
# Error 3: Al no separar "emitir si es hoja" de "recorrer hijos si no lo es",
#   la lógica original mezcla ambos casos de forma incorrecta. Con la
#   comprobación del error 1 añadida, la estructura natural es un if/else:
#   si el nodo es hoja, emitir su valor; si no lo es, delegar en los hijos.
#
# ERRORES CORREGIDOS:
# 1. Emitir solo el valor cuando el nodo es una hoja
# 2. Usar yield from en la llamada recursiva
# 3. Separar el caso hoja del caso nodo interno con if/else


def hojas(nodo):
    if not nodo["hijos"]:
        yield nodo["valor"]
    else:
        for hijo in nodo["hijos"]:
            yield from hojas(hijo)


arbol = {
    "valor": 1,
    "hijos": [
        {
            "valor": 2,
            "hijos": [
                {"valor": 3, "hijos": []},
            ],
        },
        {
            "valor": 4,
            "hijos": [
                {"valor": 5, "hijos": []},
            ],
        },
    ],
}

resultado = list(hojas(arbol))
print(sorted(resultado))
