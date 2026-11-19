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
def mover_con_tiempo(Movimiento, velocidad, distancia_objetivo_mm, tiempo_max_ms):

    """
    Mueve el robot una distancia objetivo, pero pasa a la siguiente línea 
    si se acaba el tiempo máximo, incluso si no ha terminado de recorrerla.
    
    :param Movimiento: Objeto DriveBase asignado a la variable 'Movimiento'
    :param velocidad: Velocidad en mm/s
    :param distancia_objetivo_mm: Distancia que se desea recorrer en milímetros
    :param tiempo_max_ms: Tiempo límite en milisegundos
    """
    # Guardamos la posición inicial de distancia del robot
    distancia_inicial = Movimiento.distance()
    
    # Determinamos la dirección (positiva o negativa) según la distancia objetivo
    signo = 1 if distancia_objetivo_mm >= 0 else -1
    velocidad_ajustada = abs(velocidad) * signo
    
    # Iniciamos el movimiento continuo (no bloqueante)
    Movimiento.drive(velocidad_ajustada, 0)
    
    # Creamos e iniciamos el cronómetro
    cronometro = StopWatch()
    
    # Bucle que evalúa constantemente el progreso
    while True:
        # Calculamos cuánto llevamos recorrido desde el inicio de la función
        distancia_actual = abs(Movimiento.distance() - distancia_inicial)
        
        # 1. Condición de éxito: ¿Llegó a la distancia objetivo?
        if distancia_actual >= abs(distancia_objetivo_mm):
            break
            
        # 2. Condición de límite: ¿Se acabó el tiempo?
        if cronometro.time() >= tiempo_max_ms:
            break
            
        # Pequeña pausa de 10ms para liberar un poco al procesador del Hub
        wait(10)
        
    # Detenemos el robot al salir del bucle (ya sea por distancia o por tiempo)
    Movimiento.stop()
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