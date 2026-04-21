# =============================================================================
# EJERCICIO 2: Procesar texto con list comprehensions
# =============================================================================
# Tienes reseñas de películas. Usa list comprehensions para extraer y
# transformar información del texto.
#
# DATOS:
resenas = [
    "Película increíble con una trama fascinante",
    "Aburrida y predecible",
    "Efectos visuales espectaculares aunque historia floja",
    "Gran actuación del protagonista",
    "No recomendable para menores",
    "Obra maestra del cine moderno",
    "Regular",
]
palabras_clave = ["increíble", "espectaculares", "maestra", "aburrida", "floja", "predecible"]
#
# TAREAS:
# 1. Crea una lista con las reseñas que tienen más de 4 palabras (resenas_largas)
# 2. Crea una lista con la cantidad de palabras de cada reseña (conteo_palabras)
# 3. Crea una lista con la primera palabra de cada reseña en minúsculas (primeras_palabras)
# 4. Crea una lista con True/False indicando si cada reseña contiene alguna palabra clave
#    (usa any() dentro de la comprehension) (tiene_palabra_clave)
# 5. Crea una lista con todas las palabras de todas las reseñas aplanadas en una sola lista,
#    solo las que tienen 6 letras o más (palabras_largas)
#
# RESULTADO ESPERADO:
# Reseñas largas: ['Película increíble con una trama fascinante', 'Efectos visuales espectaculares aunque historia floja', 'Obra maestra del cine moderno']
# Conteo palabras: [6, 3, 6, 4, 4, 5, 1]
# Primeras palabras: ['película', 'aburrida', 'efectos', 'gran', 'no', 'obra', 'regular']
# Tiene palabra clave: [True, True, True, False, False, True, False]
# Palabras largas: ['Película', 'increíble', 'fascinante', 'Aburrida', 'predecible', 'Efectos', 'visuales', 'espectaculares', 'aunque', 'historia', 'actuación', 'protagonista', 'recomendable', 'menores', 'maestra', 'moderno', 'Regular']
# =============================================================================

# Tu código aquí
