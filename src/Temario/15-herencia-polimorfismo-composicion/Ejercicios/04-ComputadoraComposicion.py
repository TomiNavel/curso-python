# =============================================================================
# EJERCICIO 4: Computadora (Composición)
# =============================================================================
# Crea un sistema usando composición (NO herencia) para modelar una
# computadora con componentes intercambiables.
#
# Clase CPU:
# - Atributos: marca (str), nucleos (int), ghz (float)
# - __str__: "Intel 8 núcleos @ 3.6GHz"
#
# Clase RAM:
# - Atributos: capacidad_gb (int), tipo (str, ej: "DDR5")
# - __str__: "16GB DDR5"
#
# Clase Disco:
# - Atributos: capacidad_gb (int), tipo (str, ej: "SSD", "HDD")
# - __str__: "512GB SSD"
#
# Clase Computadora:
# - Atributos: nombre (str), cpu (CPU), ram (RAM), disco (Disco)
# - especificaciones(): devuelve string con todas las specs (ver formato abajo)
# - upgrade_ram(nueva_ram): reemplaza la RAM actual por una nueva
# - upgrade_disco(nuevo_disco): reemplaza el disco actual por uno nuevo
# - __str__: "PC Gaming"
#
# RESULTADO ESPERADO:
# === PC Gaming ===
# CPU: AMD 12 núcleos @ 4.2GHz
# RAM: 16GB DDR5
# Disco: 512GB SSD
#
# Después del upgrade:
# === PC Gaming ===
# CPU: AMD 12 núcleos @ 4.2GHz
# RAM: 32GB DDR5
# Disco: 1000GB SSD
# =============================================================================

# Tu código aquí

# pc = Computadora(
#     "PC Gaming",
#     CPU("AMD", 12, 4.2),
#     RAM(16, "DDR5"),
#     Disco(512, "SSD"),
# )
# print(pc.especificaciones())
#
# pc.upgrade_ram(RAM(32, "DDR5"))
# pc.upgrade_disco(Disco(1000, "SSD"))
# print("Después del upgrade:")
# print(pc.especificaciones())
