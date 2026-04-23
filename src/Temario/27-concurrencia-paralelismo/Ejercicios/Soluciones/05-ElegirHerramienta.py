# =============================================================================
# SOLUCIÓN
# =============================================================================


def recomendar_herramienta(descripcion):
    cpu = descripcion["cpu_intensivo"]
    io = descripcion["espera_io"]

    if cpu and io:
        return "mixto: considerar analizar más"
    if cpu:
        return "multiprocessing"
    if io:
        return "threading"
    return "asyncio"


# Pruebas
print(recomendar_herramienta({"cpu_intensivo": True, "espera_io": False}))
print(recomendar_herramienta({"cpu_intensivo": False, "espera_io": True}))
print(recomendar_herramienta({"cpu_intensivo": True, "espera_io": True}))
print(recomendar_herramienta({"cpu_intensivo": False, "espera_io": False}))
