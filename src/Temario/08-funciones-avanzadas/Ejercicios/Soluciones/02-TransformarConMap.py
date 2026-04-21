# PASO 1
valores = ["1", "2", "3", "4", "5"]
print(list(map(int, valores)))

# PASO 2
nombres = ["ana", "pedro", "luis"]
print(list(map(lambda n: n.upper(), nombres)))

# PASO 3
precios = [100.0, 25.0, 75.0]
print(list(map(lambda p: p * 0.9, precios)))

# PASO 4
palabras = ["Ana", "Pedro", "Luis"]
print(list(map(len, palabras)))
