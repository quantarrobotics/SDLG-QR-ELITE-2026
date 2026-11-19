from pybricks.hubs import InventorHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = InventorHub()
v_min = 6800  # Batería descargada (mV)
v_max = 8300  # Batería llena (mV)

voltaje = hub.battery.voltage()
porcentaje = int(((voltaje - v_min) / (v_max - v_min)) * 100)

# Limitar el rango entre 0% y 100%
porcentaje = max(0, min(100, porcentaje))

print("Nivel de batería:", porcentaje, "%")
