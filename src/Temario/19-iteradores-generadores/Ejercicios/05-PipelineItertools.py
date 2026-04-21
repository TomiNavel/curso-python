# =============================================================================
# EJERCICIO 5: Pipeline perezoso con itertools
# =============================================================================
# Dado un generador infinito de enteros positivos (1, 2, 3, ...), construye
# una tubería perezosa que obtenga los primeros 10 cuadrados de números
# múltiplos de 3.
#
# Requisitos:
# - Define un generador "enteros_positivos" que produzca 1, 2, 3, ... sin fin
# - Usa una generator expression para filtrar múltiplos de 3
# - Usa otra generator expression para elevarlos al cuadrado
# - Usa itertools.islice para tomar solo los primeros 10 resultados
# - No construyas ninguna lista intermedia completa
#
# RESULTADO ESPERADO:
# [9, 36, 81, 144, 225, 324, 441, 576, 729, 900]
# =============================================================================

from itertools import islice


# Tu código aquí


# Tests
print(list(resultado))
