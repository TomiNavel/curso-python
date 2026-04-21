"""
Solución: Contar palabras
"""

texto = "python es un lenguaje interpretado"

palabras = texto.split()

# Total de palabras
print(f"Total palabras: {len(palabras)}")

# Orden inverso: slicing con paso -1 sobre la lista, luego join
print(f"Orden inverso: {' '.join(palabras[::-1])}")

