"""
Solución: Extraer dominio
"""

email = "ana.garcia@empresa.com"

usuario, _, dominio = email.partition("@")
print(f"Usuario: {usuario}")
print(f"Dominio: {dominio}")

nombre_dominio, _, extension = dominio.partition(".")
print(f"Nombre dominio: {nombre_dominio}")
print(f"Extensión: {extension}")
