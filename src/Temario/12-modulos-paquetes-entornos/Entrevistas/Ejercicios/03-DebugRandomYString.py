# =============================================================================
# EJERCICIO DE ENTREVISTA 3: Debug — random y string
# =============================================================================
# El siguiente código tiene 3 errores. Encuéntralos y corrígelos.
#
# RESULTADO ESPERADO (con seed=42, los valores son deterministas):
# Código generado: A7X2K9
# Elemento elegido: banana
# Lista mezclada: ['cherry', 'banana', 'date', 'apple'] (orden varía con seed)
# =============================================================================

import random
import string

random.seed(42)

def generar_codigo(longitud=6):
    caracteres = string.ascii_uppercase + string.digits
    codigo = random.choices(caracteres, longitud)
    return "".join(codigo)

print(f"Código generado: {generar_codigo()}")

frutas = ["apple", "banana", "cherry", "date"]
elegida = random.choice[frutas]
print(f"Elemento elegido: {elegida}")

mezclada = random.shuffle(frutas)
print(f"Lista mezclada: {mezclada}")
