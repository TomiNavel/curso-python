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

# 1. Usuarios únicos en minúsculas
usuarios_unicos = {usuario.lower() for usuario, _ in accesos}
print("Usuarios únicos:", usuarios_unicos)

# 2. Ciudades únicas en formato título
ciudades_unicas = {ciudad.title() for _, ciudad in accesos}
print("Ciudades únicas:", ciudades_unicas)

# 3. Pares (usuario, ciudad) normalizados sin duplicados
accesos_unicos = {(usuario.lower(), ciudad.lower()) for usuario, ciudad in accesos}
print("Accesos únicos:", accesos_unicos)

# 4. Dominios únicos de email en minúsculas
dominios_unicos = {email.lower().split("@")[1] for email in dominios_email}
print("Dominios únicos:", dominios_unicos)

# 5. Usuarios que accedieron desde más de una ciudad distinta (tras normalizar)
todos_usuarios = {usuario.lower() for usuario, _ in accesos}
usuarios_multiciudad = {
    usuario
    for usuario in todos_usuarios
    if len({ciudad.lower() for u, ciudad in accesos if u.lower() == usuario}) > 1
}
print("Usuarios multiciudad:", usuarios_multiciudad)
