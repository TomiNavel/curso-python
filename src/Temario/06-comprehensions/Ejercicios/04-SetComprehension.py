# =============================================================================
# EJERCICIO 4: Set comprehensions
# =============================================================================
# Tienes registros de accesos a un sistema con datos sucios (duplicados,
# formatos inconsistentes). Usa set comprehensions para limpiar y analizar.
#
# DATOS:
accesos = [
    ("usuario1", "Madrid"),
    ("Usuario2", "barcelona"),
    ("USUARIO1", "madrid"),
    ("usuario3", "Valencia"),
    ("usuario2", "Barcelona"),
    ("usuario1", "MADRID"),
    ("Usuario4", "Valencia"),
    ("usuario3", "valencia"),
    ("USUARIO5", "Sevilla"),
    ("usuario4", "VALENCIA"),
]
dominios_email = [
    "ana@gmail.com",
    "pedro@HOTMAIL.com",
    "ANA@Gmail.COM",
    "luis@yahoo.es",
    "Pedro@hotmail.com",
    "maria@gmail.com",
    "LUIS@Yahoo.ES",
]
#
# TAREAS:
# 1. Crea un set con los nombres de usuario únicos en minúsculas (usuarios_unicos)
# 2. Crea un set con las ciudades únicas en formato título (Ciudad) (ciudades_unicas)
# 3. Crea un set con los pares (usuario, ciudad) normalizados a minúsculas — sin duplicados (accesos_unicos)
# 4. Crea un set con los dominios únicos de email (la parte después del @), en minúsculas (dominios_unicos)
# 5. Crea un set con los usuarios que accedieron desde más de una ciudad distinta
#    Pista: para cada usuario, cuenta cuántas ciudades únicas tiene en accesos (usuarios_multiciudad)
#
# RESULTADO ESPERADO:
# Usuarios únicos: {'usuario1', 'usuario2', 'usuario3', 'usuario4', 'usuario5'}
# Ciudades únicas: {'Madrid', 'Barcelona', 'Valencia', 'Sevilla'}
# Accesos únicos: {('usuario1', 'madrid'), ('usuario2', 'barcelona'), ('usuario3', 'valencia'), ('usuario4', 'valencia'), ('usuario5', 'sevilla')}
# Dominios únicos: {'gmail.com', 'hotmail.com', 'yahoo.es'}
# Usuarios multiciudad: set() vacío (ningún usuario accedió desde ciudades realmente distintas tras normalizar)
# =============================================================================

# Tu código aquí
