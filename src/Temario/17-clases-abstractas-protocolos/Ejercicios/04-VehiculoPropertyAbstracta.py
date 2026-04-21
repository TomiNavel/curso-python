# =============================================================================
# EJERCICIO 4: Vehículo con property abstracta
# =============================================================================
# Crea una clase abstracta `Vehiculo` que use properties abstractas para
# obligar a las subclases a declarar características fijas como atributos
# conceptuales (no métodos).
#
# Clase abstracta Vehiculo:
# - __init__(marca, modelo)
# - @property @abstractmethod num_ruedas
# - @property @abstractmethod consumo_medio  (litros por 100 km)
# - Método concreto ficha() que devuelve:
#   "{marca} {modelo}: {num_ruedas} ruedas, {consumo_medio} l/100km"
#
# Subclases:
# - Coche: num_ruedas = 4, consumo_medio = 6.5
# - Moto: num_ruedas = 2, consumo_medio = 4.2
# - Camion: num_ruedas = 6, consumo_medio = 22.0
#
# IMPORTANTE: el orden de los decoradores debe ser @property encima
# de @abstractmethod.
#
# RESULTADO ESPERADO:
# Toyota Corolla: 4 ruedas, 6.5 l/100km
# Yamaha MT-07: 2 ruedas, 4.2 l/100km
# Volvo FH: 6 ruedas, 22.0 l/100km
# =============================================================================

# Tu código aquí

# vehiculos = [
#     Coche("Toyota", "Corolla"),
#     Moto("Yamaha", "MT-07"),
#     Camion("Volvo", "FH"),
# ]
#
# for v in vehiculos:
#     print(v.ficha())
