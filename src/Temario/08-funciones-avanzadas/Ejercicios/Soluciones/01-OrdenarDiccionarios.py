personas = [
    {"nombre": "Ana", "edad": 28},
    {"nombre": "Pedro", "edad": 22},
    {"nombre": "Luis", "edad": 35},
]

# PASO 1
por_edad = sorted(personas, key=lambda p: p["edad"])
linea = ", ".join(f'{p["nombre"]} ({p["edad"]})' for p in por_edad)
print(f"Por edad: {linea}")

# PASO 2
por_nombre = sorted(personas, key=lambda p: p["nombre"])
linea = ", ".join(f'{p["nombre"]} ({p["edad"]})' for p in por_nombre)
print(f"Por nombre: {linea}")

# PASO 3
por_edad_desc = sorted(personas, key=lambda p: p["edad"], reverse=True)
linea = ", ".join(f'{p["nombre"]} ({p["edad"]})' for p in por_edad_desc)
print(f"Por edad desc: {linea}")

# PASO 4
joven = min(personas, key=lambda p: p["edad"])
mayor = max(personas, key=lambda p: p["edad"])
print(f'Más joven: {joven["nombre"]} ({joven["edad"]})')
print(f'Mayor: {mayor["nombre"]} ({mayor["edad"]})')
