def aplanar(lista):
    resultado = []
    for elemento in lista:
        if isinstance(elemento, list):
            resultado.extend(aplanar(elemento))
        else:
            resultado.append(elemento)
    return resultado

# PASO 1
print(aplanar([1, [2, 3], [4, [5, 6]]]))

# PASO 2
print(aplanar([1, [2, [3, [4, [5, [6, [7]]]]]]]))

# PASO 3
print(aplanar(["a", ["b", "c"], [["d"], "e"]]))

# PASO 4
print(aplanar([1, 2, 3]))
