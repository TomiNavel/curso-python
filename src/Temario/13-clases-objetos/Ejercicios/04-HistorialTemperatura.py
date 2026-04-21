# =============================================================================
# EJERCICIO 4: Historial de Temperaturas
# =============================================================================
# Crea una clase `HistorialTemperatura` que registre mediciones de temperatura.
#
# Atributos de instancia:
# - ciudad (str)
# - mediciones (lista, inicializada vacía)
#
# Métodos:
# - registrar(temperatura): añade la temperatura a mediciones.
#   Lanzar TypeError si no es int o float.
# - media(): devuelve la media de las mediciones (redondear a 1 decimal).
#   Lanzar ValueError si no hay mediciones.
# - maxima(): devuelve la temperatura máxima.
# - minima(): devuelve la temperatura mínima.
# - rango(): devuelve la diferencia entre máxima y mínima.
# - por_encima_de(umbral): devuelve lista de mediciones > umbral.
# - __repr__: HistorialTemperatura('Madrid', 5 mediciones)
# - __str__: "Madrid: 5 mediciones, media 22.4°C"
#
# Método de clase:
# - @classmethod desde_lista(cls, ciudad, temperaturas): crea un historial
#   con todas las temperaturas ya registradas.
#
# RESULTADO ESPERADO:
# Madrid: 5 mediciones, media 23.6°C
# Máxima: 30.5, Mínima: 18.0, Rango: 12.5
# Por encima de 25: [28.0, 30.5]
# HistorialTemperatura('Madrid', 5 mediciones)
#
# Desde lista:
# Barcelona: 4 mediciones, media 21.5°C
# =============================================================================

# Tu código aquí

# h = HistorialTemperatura("Madrid")
# for t in [22.5, 18.0, 28.0, 19.0, 30.5]:
#     h.registrar(t)
# print(h)
# print(f"Máxima: {h.maxima()}, Mínima: {h.minima()}, Rango: {h.rango()}")
# print(f"Por encima de 25: {h.por_encima_de(25)}")
# print(repr(h))
# print()
# h2 = HistorialTemperatura.desde_lista("Barcelona", [20.0, 22.5, 19.0, 24.5])
# print(h2)
