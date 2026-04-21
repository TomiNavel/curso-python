"""
Solución: Limpiar datos
"""

nombre_raw = "  ana_maría   GARCÍA  "

# strip() elimina espacios de los extremos
# replace() cambia guiones bajos por espacios
# split() + join() normaliza los espacios múltiples en uno solo
# title() pone cada palabra con mayúscula inicial
nombre_limpio = " ".join(nombre_raw.strip().replace("_", " ").split()).title()
print(f"Nombre limpio: {nombre_limpio}")

print(f"En mayúsculas: {nombre_limpio.upper()}")

# Sin guiones bajos: se aplica replace sobre el string original sin normalizar
print(f"Sin guiones bajos: {nombre_raw.strip().replace('_', ' ')}")
