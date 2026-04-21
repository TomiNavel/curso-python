from collections import Counter

# PASO 1
letras = Counter("banana")
print(letras)

# PASO 2
print(letras.most_common(2))

# PASO 3
print(letras["a"])
print(letras["z"])

# PASO 4
frutas = Counter(["manzana", "pera", "manzana", "uva", "manzana", "pera"])
print(frutas)
print(frutas.most_common(1))

# PASO 5
mas_frutas = Counter(["manzana", "pera", "kiwi", "manzana"])
print(frutas + mas_frutas)

# PASO 6
print(frutas - mas_frutas)
