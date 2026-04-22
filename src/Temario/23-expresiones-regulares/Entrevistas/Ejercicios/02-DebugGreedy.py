# =============================================================================
# EJERCICIO DE ENTREVISTA 2: Debug — Extraer etiquetas HTML simples
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
# La función "extraer_etiquetas(html)" debe devolver una lista con los
# nombres de las etiquetas (sin los corchetes y sin el slash de cierre).
# Por ejemplo, para "<b>hola</b><i>mundo</i>" debe devolver ['b', 'b', 'i', 'i'].
#
# No hace falta un parser HTML real: asume que las etiquetas son nombres
# simples sin atributos, y que el texto es el de las pruebas.
#
# RESULTADO ESPERADO:
# ['b', 'b', 'i', 'i']
# =============================================================================

import re


def extraer_etiquetas(html):
    patron = "<(.+)>"
    coincidencias = re.findall(patron, html)
    return [c.replace("/", "") for c in coincidencias]


# Pruebas
print(extraer_etiquetas("<b>hola</b><i>mundo</i>"))
