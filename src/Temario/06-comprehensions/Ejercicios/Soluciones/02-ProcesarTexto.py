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

# 1. Reseñas con más de 4 palabras
resenas_largas = [r for r in resenas if len(r.split()) > 4]
print("Reseñas largas:", resenas_largas)

# 2. Cantidad de palabras por reseña
conteo_palabras = [len(r.split()) for r in resenas]
print("Conteo palabras:", conteo_palabras)

# 3. Primera palabra de cada reseña en minúsculas
primeras_palabras = [r.split()[0].lower() for r in resenas]
print("Primeras palabras:", primeras_palabras)

# 4. True si la reseña contiene alguna palabra clave (comparación en minúsculas)
tiene_palabra_clave = [
    any(pk in r.lower() for pk in palabras_clave)
    for r in resenas
]
print("Tiene palabra clave:", tiene_palabra_clave)

# 5. Todas las palabras de todas las reseñas con 6 letras o más (aplanadas)
palabras_largas = [
    palabra
    for resena in resenas
    for palabra in resena.split()
    if len(palabra) >= 6
]
print("Palabras largas:", palabras_largas)
