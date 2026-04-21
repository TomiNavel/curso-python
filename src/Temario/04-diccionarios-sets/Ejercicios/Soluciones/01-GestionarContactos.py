# PASO 1
contacto = {"nombre": "Ana", "edad": 28, "email": "ana@ejemplo.com"}

# PASO 2
print(contacto["nombre"])
print(contacto.get("telefono", "N/A"))

# PASO 3
contacto["edad"] = 29
contacto["ciudad"] = "Madrid"
print(contacto)

# PASO 4
edad = contacto.pop("edad")
print(edad)
contacto.update({"telefono": "555-1234"})
print(contacto)

# PASO 5
print("nombre" in contacto)
print("edad" in contacto)

# PASO 6
print(contacto.keys())
print(contacto.values())

# PASO 7
nombre = contacto["nombre"]
ciudad = contacto["ciudad"]
print(f"{nombre} vive en {ciudad}")
