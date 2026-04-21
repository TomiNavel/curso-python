# =============================================================================
# EJERCICIO 5: Simulador de Dados con Estadísticas
# =============================================================================
# Crea funciones que simulen lanzamientos de dados usando `random` y calculen
# estadísticas usando `math` y `collections.Counter`.
#
# Funciones a crear:
#
# 1. `lanzar_dados(n_dados, caras=6)`: lanza n dados con el número de caras
#    indicado y devuelve una lista con los resultados.
#
# 2. `frecuencia_resultados(lanzamientos)`: recibe una lista de resultados y
#    devuelve un diccionario ordenado {valor: cantidad} usando Counter.
#
# 3. `simulacion_completa(n_lanzamientos, n_dados, caras=6, semilla=None)`:
#    - Si se proporciona semilla, fijarla con random.seed
#    - Realizar n_lanzamientos, cada uno con n_dados dados
#    - Calcular la suma de cada lanzamiento
#    - Devolver un diccionario con:
#      - "sumas": lista con la suma de cada lanzamiento
#      - "media": media de las sumas (redondear a 2 decimales)
#      - "minimo": suma mínima obtenida
#      - "maximo": suma máxima obtenida
#      - "frecuencia_sumas": diccionario {suma: veces} ordenado por suma
#
# RESULTADO ESPERADO (con semilla=42):
# lanzar_dados(3): [1, 1, 6] (varía sin semilla)
# frecuencia_resultados([1, 3, 3, 5, 5, 5]): {1: 1, 3: 2, 5: 3}
# simulacion_completa(1000, 2, semilla=42):
#   media: ~7.0
#   minimo: 2
#   maximo: 12
#   frecuencia_sumas: {2: ..., 3: ..., ..., 12: ...}
# =============================================================================

# Tu código aquí

# resultado = simulacion_completa(1000, 2, semilla=42)
# print(f"Media: {resultado['media']}")
# print(f"Mínimo: {resultado['minimo']}")
# print(f"Máximo: {resultado['maximo']}")
# print(f"Frecuencia de sumas: {resultado['frecuencia_sumas']}")
