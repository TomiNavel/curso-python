nombres = ["Pedro", "Luis", "Ana", "Carlos", "Elena"]

# PASO 1
for i, nombre in enumerate(nombres):
    if nombre == "Ana":
        print(f"Ana encontrada en posición {i}")
        break
else:
    print("Ana no está en la lista")

# PASO 2
for i, nombre in enumerate(nombres):
    if nombre == "María":
        print(f"María encontrada en posición {i}")
        break
else:
    print("María no está en la lista")
