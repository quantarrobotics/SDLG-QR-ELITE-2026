from pybricks.hubs import PrimeHub, InventorHub
from pybricks.pupdevices import Motor
from pybricks.parameters import Port, Direction
from pybricks.iodevices import UARTDevice
from pybricks.tools import wait

# 1. Inicializar el Hub y el puerto UART de la M-Vision
hub = PrimeHub()
Wi = 320
He = 240
Mid_X = Wi // 2
Mid_Y = He // 2

# IMPORTANTE: Cambia 'Port.A' por el puerto físico donde conectaste la cámara.
# La cámara M-Vision por defecto se comunica a una velocidad de 115200 baudios.
uart = UARTDevice(Port.A, baudrate=115200, timeout=10)


def get_zone(cx, cy):
    limcx = 195
    limcy = 33
    if cx > limcx  and cy < limcy :
        return 4
    elif cx < limcx and cy < limcy-5:
        return 2
    elif cx > limcx and cy > limcy:
        return 3
    else:
        return 1

def parse_state(data):
    try:
        text = "".join(chr(b) for b in data).strip()

        # Puede llegar más de una línea en el buffer; toma la última completa
        lines = [l for l in text.split("\n") if l.startswith("S:")]
        if not lines:
            return None
        last = lines[-1]
        
        return last.split(":")[1]
    except Exception as e:
     print("ERROR:", e)
     return None
    
print("Buscando datos de la cámara M-Vision...")

# 2. Bucle principal de lectura
while True:
    # Comprobamos si la cámara ha enviado bytes al buffer
    if uart.waiting() > 0:
        # Leemos TODO lo que esté acumulado en el buffer en ese instante
        datos_brutos = uart.read_all()
        print(datos_brutos)
        # Pasamos los bytes por tu función de filtrado
        numero_estado = parse_state(datos_brutos)
        # Si la función logró extraer un número válido (no es None)
        try:
          if numero_estado is not None:
            numero_estado = numero_estado.strip("[]")
            partes = numero_estado.split(",")
            print(partes)
            lista = [int(x) for x in partes]
            cx = lista[0]
            cy = lista[1]
            state = get_zone(cx, cy)
            print("El lugar morado es:", state)
         
        except Exception as e:
             print("ERROR:", e)
    else: print("no llega nada")        
    # Una pequeña pausa de 10 milisegundos para no saturar el procesador del Spike
    wait(50) 