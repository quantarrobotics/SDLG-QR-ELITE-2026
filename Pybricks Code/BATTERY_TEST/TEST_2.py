rom pybricks.hubs import InventorHub
from pybricks.tools import wait

hub = InventorHub()

# TABLA DE CALIBRACION
# Formato: (voltaje en mV, porcentaje)
# Sustituye estos valores por mediciones de tu batería.

CALIBRACION = [
    (8400, 100),
    (8200, 90),
    (8000, 80),
    (7800, 70),
    (7600, 60),
    (7400, 50),
    (7200, 40),
    (7000, 30),
    (6800, 20),
    (6600, 10),
    (6400, 0)
]

# Calcular porcentaje mediante interpolación
def calcular_porcentaje(voltaje):

    if voltaje >= CALIBRACION[0][0]:
        return 100

    if voltaje <= CALIBRACION[-1][0]:
        return 0

    for i in range(len(CALIBRACION) - 1):

        v1, p1 = CALIBRACION[i]
        v2, p2 = CALIBRACION[i + 1]

        if v1 >= voltaje >= v2:

            porcentaje = p2 + (
                (voltaje - v2) * (p1 - p2) / (v1 - v2)
            )

            return round(porcentaje)

    return 0


# Promediar las mediciones para estabilizar el resultado
def leer_bateria():

    lecturas = []

    for i in range(8):
        lecturas.append(hub.battery.voltage())
        wait(100)

    return sum(lecturas) / len(lecturas)


# PROGRAMA PRINCIPAL
while True:

    voltaje = leer_bateria()

    porcentaje = calcular_porcentaje(voltaje)

    # Mostrar porcentaje en la matriz LED
    hub.display.text(str(porcentaje), on=700, off=200)

    wait(1000)
