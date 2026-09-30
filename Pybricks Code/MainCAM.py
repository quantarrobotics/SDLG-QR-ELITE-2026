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
Ligas = Motor (Port.D, Direction.CLOCKWISE)
Movimiento.settings (straight_speed= 1400, straight_acceleration= 2800)
Movimiento.use_gyro (True)
hub.imu.reset_heading(0)
rampita.run_time (-1000, 400)
Phub = PrimeHub()
Wi = 320
He = 240
Mid_X = Wi // 2
Mid_Y = He // 2
uart = UARTDevice(Port.A, baudrate=115200, timeout=10)

def get_zone(cx, cy):
    limcx = 195
    limcy = 95
    if cx > limcx  and cy < limcy :
        return 4
    elif cx < limcx and 30 < cy < limcy:
        return 2
    elif cx > limcx and cy > limcy:
        return 3
    else:
        return 1

def parse_state(data):
    try:
        text = "".join(chr(b) for b in data).strip()
        lines = [l for l in text.split("\n") if l.startswith("S:")]
        if not lines:
            return None
        last = lines[-1]
        return last.split(":")[1]
    except Exception as e:
     print("ERROR:", e)
     return None

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

def estado_1 ():
  Movimiento.straight (230) 
  Movimiento.turn (45)
  Movimiento.straight (270)
  Movimiento.turn (45)
  Movimiento.straight (-380)
  rampita.run_time (1000, 400)
  Movimiento.straight(180)
  Movimiento.turn (-90)
  Movimiento.straight (-490)

def estado_2 () :
    Ligas.run (300)
    Movimiento.straight (380) 
    Ligas.stop ()
    Movimiento.turn (45)
    Movimiento.straight (270)
    Movimiento.turn (45)
    Movimiento.straight (-380)
    rampita.run_time (1000, 400)
    Movimiento.straight(180)
    Movimiento.turn (-90)
    Movimiento.straight (-630)

def estado_3 ():
  Ligas.run(1500)
  Movimiento.straight (475)
  Ligas.stop()
  Movimiento.turn (-90)
  Movimiento.straight(-400)
  rampita.run_time (1000,500)
  Movimiento.straight (300)
  Movimiento.turn (90)
  Movimiento.straight(-490)

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
    MotorIZQ.run (150)
    wait (260)
    MotorIZQ.run (1500)
    wait (800)
    Movimiento.stop ()
    Ligas.run (450)
    giroscopio (2000, 1500, 8)
    Movimiento.straight (-75)
    Movimiento.straight (100)
    wait (170)
    Ligas.stop ()
    while True :
     Movimiento.turn (70)
     MotorIZQ.run (1500)
     MotorDER.run (1500)
     wait (1000)
     Movimiento.turn (70)
     MotorIZQ.run (1400)
     MotorDER.run (800)
     wait (1000)
     giroscopio (400, 1200, 8)
     Movimiento.turn (70)
     MotorDER.run (1500)
     MotorIZQ.run (1500)
     wait (1000)
     Movimiento.turn (90)
     Movimiento.turn (-90)
     Movimiento.straight (-175)
     Movimiento.turn(90)
     MotorIZQ.run (-1500)
     MotorDER.run (-1500)
     wait (700)
     giroscopio (1400, 1000, 25)
     Ligas.run (450)
     giroscopio (2000, 1500, 8)
     Movimiento.straight (-75)
     Movimiento.straight (75)
     wait (270)
     Ligas.stop ()
     Movimiento.turn (70)
     MotorIZQ.run (1500)
     MotorDER.run (1500)
     wait (1000)
     Movimiento.turn (70)
     MotorIZQ.run (1400)
     MotorDER.run (800)
     wait (1000)
     giroscopio (400, 1200, 8)
     Movimiento.turn (70)
     MotorDER.run (1500)
     MotorIZQ.run (1500)
     wait (1000)
     Movimiento.turn (77)
     Movimiento.straight (450)
     Ligas.run (450)
     Movimiento.stop()
     giroscopio (2000, 1000, 25)
     wait (750)
     Movimiento.straight (-75)
     Movimiento.straight (75)
     wait (650)
     Ligas.stop ()
     Movimiento.stop ()
wait(2400)
print("Buscando datos de la cámara M-Vision...")

for i in range(20):
    if uart.waiting() > 0:
        datos_brutos = uart.read_all()
        numero_estado = parse_state(datos_brutos)
        try:
          if numero_estado is not None:
            print("Estado recibido de M-Vision:", numero_estado)
            numero_estado = numero_estado.strip("[]")
            partes = numero_estado.split(",")
            lista = [int(x) for x in partes]
            cx = lista[0]
            cy = lista[1]
            state = get_zone(cx, cy)
            print("El lugar morado es:", state)
         
        except Exception as e:
         print("ERROR:", e)
         wait(50)

if state == 1:
    estado_1 ()
elif state == 2:
    estado_2 ()
elif state == 3:
    estado_3 ()
elif state == 4:
    estado_4 ()
else:
    ciclo ()

ciclo ()
