# =============================================================================
# EJERCICIO 5: Leer y escribir CSV con DictReader/DictWriter
# =============================================================================
# Dada la lista "productos" con diccionarios, escribe dos funciones:
#   - exportar_csv(ruta, productos): genera un CSV con las columnas
#     "codigo", "nombre" y "precio". Incluye la cabecera.
#   - cargar_caros(ruta, umbral): lee el CSV y devuelve la lista de
#     nombres de productos cuyo precio sea estrictamente mayor que el
#     umbral. Recuerda que CSV siempre lee strings.
#
# Usa encoding="utf-8" y newline="" al abrir los archivos.
#
# RESULTADO ESPERADO:
# ['Portátil', 'Monitor']
# =============================================================================

productos = [
    {"codigo": "A1", "nombre": "Teclado", "precio": 45},
    {"codigo": "A2", "nombre": "Ratón", "precio": 25},
    {"codigo": "B1", "nombre": "Portátil", "precio": 950},
    {"codigo": "B2", "nombre": "Monitor", "precio": 220},
]


# Tu código aquí


# Pruebas
exportar_csv("productos.csv", productos)
print(cargar_caros("productos.csv", 100))
