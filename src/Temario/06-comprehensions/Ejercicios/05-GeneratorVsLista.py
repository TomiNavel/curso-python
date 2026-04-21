# =============================================================================
# EJERCICIO 5: Generator expressions
# =============================================================================
# Tienes datos de sensores de temperatura registrados durante un día.
# Usa generator expressions con sum(), max(), min(), any() y all().
#
# DATOS:
lecturas_celsius = [18.2, 19.5, 21.0, 23.4, 25.1, 27.8, 29.3, 31.2, 30.5,
                    28.9, 26.4, 24.1, 22.6, 20.8, 19.1, 17.5, 16.2, 15.8,
                    15.1, 14.9, 15.3, 16.0, 17.2, 18.0]  # 24 lecturas (una por hora)
umbrales_alerta = [35.0, 36.5, 34.2, 38.0, 33.8]  # temperaturas de alerta de otros sensores
nombres_sensores = ["sensor_norte", "sensor_sur", "sensor_este", "sensor_oeste", "sensor_central"]
#
# TAREAS:
# 1. Calcula la temperatura media usando sum() y len() con generator expressions (temp_media)
# 2. Encuentra la temperatura máxima en Fahrenheit (°F = °C * 9/5 + 32) usando max() (max_fahrenheit)
# 3. Comprueba con any() si alguna lectura supera 30°C (hay_calor_extremo)
# 4. Comprueba con all() si todas las lecturas están por encima de 10°C (todas_sobre_10)
# 5. Calcula la suma de temperaturas solo de las horas punta (índices 6 a 9 incluidos,
#    que corresponden a las horas de mayor calor) usando sum() y enumerate() (suma_horas_punta)
# 6. Con los umbrales_alerta, comprueba cuántos superan la media calculada en la tarea 1.
#    Usa sum() con una generator expression que produzca 1 o 0 (alertas_sobre_media)
#
# RESULTADO ESPERADO:
# Temperatura media: 21.41°C
# Máxima en Fahrenheit: 88.16°F
# Hay calor extremo (>30°C): True
# Todas sobre 10°C: True
# Suma horas punta (índices 6-9): 119.9
# Alertas sobre la media: 5
# =============================================================================

# Tu código aquí
