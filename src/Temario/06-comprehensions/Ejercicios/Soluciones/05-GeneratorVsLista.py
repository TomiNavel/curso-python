lecturas_celsius = [18.2, 19.5, 21.0, 23.4, 25.1, 27.8, 29.3, 31.2, 30.5,
                    28.9, 26.4, 24.1, 22.6, 20.8, 19.1, 17.5, 16.2, 15.8,
                    15.1, 14.9, 15.3, 16.0, 17.2, 18.0]
umbrales_alerta = [35.0, 36.5, 34.2, 38.0, 33.8]

# 1. Temperatura media
temp_media = round(sum(t for t in lecturas_celsius) / len(lecturas_celsius), 2)
print(f"Temperatura media: {temp_media}°C")

# 2. Temperatura máxima en Fahrenheit
max_fahrenheit = round(max(c * 9 / 5 + 32 for c in lecturas_celsius), 2)
print(f"Máxima en Fahrenheit: {max_fahrenheit}°F")

# 3. ¿Alguna lectura supera 30°C?
hay_calor_extremo = any(t > 30 for t in lecturas_celsius)
print(f"Hay calor extremo (>30°C): {hay_calor_extremo}")

# 4. ¿Todas las lecturas están sobre 10°C?
todas_sobre_10 = all(t > 10 for t in lecturas_celsius)
print(f"Todas sobre 10°C: {todas_sobre_10}")

# 5. Suma de temperaturas en horas punta (índices 6 a 9 incluidos)
suma_horas_punta = round(sum(t for i, t in enumerate(lecturas_celsius) if 6 <= i <= 9), 2)
print(f"Suma horas punta (índices 6-9): {suma_horas_punta}")

# 6. Cuántos umbrales de alerta superan la media
alertas_sobre_media = sum(1 for u in umbrales_alerta if u > temp_media)
print(f"Alertas sobre la media: {alertas_sobre_media}")
