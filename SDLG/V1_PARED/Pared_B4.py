from pybricks.hubs import InventorHub, PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch
from pybricks.iodevices import UARTDevice
from pybricks.tools import wait
state = 0
hub = InventorHub()
señal = 0
cronometro = StopWatch ()
MotorIZQ = Motor (Port.B, Direction.COUNTERCLOCKWISE)
MotorDER = Motor(Port.F, Direction.CLOCKWISE)
Movimiento = DriveBase (left_motor= MotorIZQ, right_motor= MotorDER, wheel_diameter=83, axle_track= 161)
rampita = Motor(Port.C, Direction.CLOCKWISE)
Ligas = Motor (Port.D, Direction.COUNTERCLOCKWISE)
Movimiento.settings (straight_speed= 1400, straight_acceleration= 2800)
Movimiento.use_gyro (True)
hub.imu.reset_heading(0)
rampita.run_time (-1000, 400)
Phub = PrimeHub()

def giroscopio(velocidad, duracion_ms, kp=2.5):
    hub.imu.reset_heading(0)
    reloj = StopWatch()
    reloj.reset()
    rumbo_objetivo = hub.imu.heading()
    while reloj.time() < duracion_ms:
        error = rumbo_objetivo - hub.imu.heading()
        velocidad_giro = error * kp
        Movimiento.drive(velocidad, velocidad_giro)
        wait(1) 
    Movimiento.stop() 

def estado_4 ():
    Movimiento.straight (620)
    Ligas.run (1500)
    wait (500)
    Movimiento.turn (-90)
    Ligas.stop ()
    Movimiento.straight (-400)
    rampita.run_time (1000,500)
    Movimiento.straight (300)
    Movimiento.turn (90)
    Movimiento.straight(-620)

def ciclo ():
    wait (300)
    MotorDER.run (5000)
    MotorIZQ.run (50)
    wait (130)
    MotorIZQ.run (1500)
    wait (800)
    Movimiento.stop ()
    Ligas.run (450)
    mover_con_tiempo(Movimiento, 1500, 1500, 1500)
    Movimiento.straight (-75)
    Movimiento.straight (100)
    wait (170)
    Ligas.stop ()
    while True :
     # Esta pegado a la pared
     Movimiento.turn (70)
     Movimiento.stop()
     mover_con_tiempo (Movimiento, 1500, 1500, 750)
     #Esquina superior derecha
     Movimiento.turn(70)
     MotorDER.run (2300)
     MotorIZQ.run (1200)
     wait (400)
     mover_con_tiempo(Movimiento, 1500, 2000, 2000)
     #Pared de inicio
     Movimiento.turn(70)
     mover_con_tiempo(Movimiento,1500,1500,1000)
     #Esquina inferior izquierda
     Ligas.run(670)
     wait(600)
     Ligas.stop()
     Movimiento.straight(-175)
     Movimiento.turn(90)
     MotorIZQ.run (-1500)
     MotorDER.run (-1500)
     wait (700)
     # medio
     giroscopio (1400, 1000, 25)
     Ligas.run (450)
     giroscopio (2000, 1500, 8)
     Movimiento.straight (-75)
     Movimiento.straight (75)
     #Pegado a la pared denuevo
     wait (270)
     Ligas.stop ()
     Movimiento.turn (70)
     mover_con_tiempo (Movimiento,1500, 1000, 750)
     #Esquina superior derecha
     Movimiento.turn(75)
     mover_con_tiempo(Movimiento, 1500, 2000, 1750)
     #Pared de inicio
     Movimiento.turn(70)
     mover_con_tiempo(Movimiento,1500,1500,1000)
     #Esquina inferior izquierda
     Movimiento.turn (77)
     Movimiento.straight (450)
     Ligas.run (450)
     mover_con_tiempo(Movimiento, 1500, 1000,1500)
     Movimiento.straight (-75)
     Movimiento.straight (75)
     wait (650)
     Ligas.stop ()
     Movimiento.stop ()
wait(200)

estado_4 ()
ciclo ()