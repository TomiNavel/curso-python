# =====================
# SOLUCIÓN
# =====================
# Error 1: el patrón no usa raw string. En este caso concreto funciona
#   porque no hay barras invertidas, pero es mala práctica y se romperá
#   si alguien añade \b, \d o similares al modificar el regex.
#   Solución: usar r"...".
#
# Error 2: el cuantificador .+ es greedy. Aplicado a "<b>hola</b><i>mundo</i>",
#   captura todo desde el primer < hasta el último >, devolviendo
#   ["b>hola</b><i>mundo</i"]. Hay que usar lazy (.+?) o, mejor, ser
#   específico con [^>]+ para evitar cualquier ambigüedad.
#   Solución: cambiar .+ por [^>]+, que es más explícito y no depende del
#   modo lazy.
#
# Error 3: .replace("/", "") elimina TODAS las apariciones de "/", no solo
#   el slash inicial de cierre. Si una etiqueta contuviera otros caracteres
#   o el patrón se generalizara, esto introduciría bugs silenciosos. Lo
#   correcto es usar lstrip("/") para quitar solo el slash del principio.
#   Solución: cambiar replace por lstrip.
#
# ERRORES CORREGIDOS:
# 1. patrón sin prefijo r → añadir r
# 2. .+ greedy → [^>]+ más específico
# 3. replace("/", "") → lstrip("/")

import re


def extraer_etiquetas(html):
    patron = r"<([^>]+)>"
    coincidencias = re.findall(patron, html)
    return [c.lstrip("/") for c in coincidencias]


# Pruebas
print(extraer_etiquetas("<b>hola</b><i>mundo</i>"))
