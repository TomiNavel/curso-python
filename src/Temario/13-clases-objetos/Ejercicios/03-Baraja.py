# =============================================================================
# EJERCICIO 3: Baraja de Cartas
# =============================================================================
# Crea dos clases: `Carta` y `Baraja`.
#
# Clase Carta:
# - Atributos: valor (str), palo (str)
# - __repr__: Carta('As', 'Picas')
# - __str__: "As de Picas"
#
# Clase Baraja:
# - Atributo de clase: PALOS = ["Corazones", "Diamantes", "Tréboles", "Picas"]
# - Atributo de clase: VALORES = ["2","3","4","5","6","7","8","9","10","J","Q","K","As"]
# - Atributo de instancia: cartas (lista de 52 Carta, generada en __init__)
# - mezclar(): mezcla las cartas usando random.shuffle
# - repartir(n=1): saca y devuelve las últimas n cartas. Si no hay suficientes,
#   lanzar ValueError("No hay suficientes cartas")
# - cartas_restantes(): devuelve cuántas cartas quedan
# - @classmethod crear_baraja_reducida(cls): crea una baraja solo con cartas
#   del 7 al As (7,8,9,10,J,Q,K,As) — 32 cartas en total
# - __repr__: Baraja(52 cartas) o Baraja(32 cartas)
#
# RESULTADO ESPERADO:
# Baraja(52 cartas)
# Mano: [Carta('...', '...'), ...]  (5 cartas aleatorias)
# Quedan: 47
# Baraja reducida: Baraja(32 cartas)
# =============================================================================

# Tu código aquí

# import random
# random.seed(42)
# b = Baraja()
# print(repr(b))
# b.mezclar()
# mano = b.repartir(5)
# print(f"Mano: {mano}")
# print(f"Quedan: {b.cartas_restantes()}")
# reducida = Baraja.crear_baraja_reducida()
# print(f"Baraja reducida: {repr(reducida)}")
