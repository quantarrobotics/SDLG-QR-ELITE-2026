from pybricks.hubs import InventorHub
from pybricks.tools import wait

hub = InventorHub()

while True:

    # Leer voltaje de batería
    voltaje = hub.battery.voltage()

    # Calcular porcentaje aproximado
    porcentaje = int((voltaje - 6000) * 100 / 2400)

    # Limitar valores
    porcentaje = max(0, min(100, porcentaje))

    # Mostrar porcentaje en matriz LED
    if porcentaje == 100:
        hub.display.text("100", on=700, off=200)
    else:
        hub.display.number(porcentaje)

    # Actualizar cada 2 segundos
    wait(2000)
