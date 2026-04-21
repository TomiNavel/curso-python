nombres = ["Ana", "Pedro", "Luis"]
edades = [28, 34, 22]
carreras = ["Medicina", "Derecho", "Ingeniería"]

# PASO 1
for i, (nombre, edad) in enumerate(zip(nombres, edades), start=1):
    print(f"{i}. {nombre} - {edad} años")

# PASO 2
print("---")
for nombre, carrera in zip(nombres, carreras):
    print(f"{nombre} estudia {carrera}")

# PASO 3
print("---")
edades_dict = dict(zip(nombres, edades))
print(edades_dict)
