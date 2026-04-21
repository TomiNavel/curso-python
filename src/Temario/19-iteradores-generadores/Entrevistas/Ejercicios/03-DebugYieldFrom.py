# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — Generador recursivo con yield from
# =============================================================================
# El siguiente código intenta recorrer un árbol (representado como
# diccionarios anidados) y producir todos los valores de las hojas (nodos
# sin hijos). Tiene 3 errores. Encuéntralos y corrígelos.
#
# Un nodo es un diccionario con la clave "valor" (entero) y la clave "hijos"
# (lista de nodos, posiblemente vacía). Una hoja es un nodo cuya lista de
# hijos está vacía.
#
# RESULTADO ESPERADO:
# [3, 5]
# =============================================================================


def hojas(nodo):
    yield nodo["valor"]
    for hijo in nodo["hijos"]:
        hojas(hijo)


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
