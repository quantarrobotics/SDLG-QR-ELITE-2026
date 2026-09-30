import sensor
import time
from pyb import UART

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.
sensor.set_vflip(True)
sensor.set_hmirror(True)
sensor.set_auto_gain(False)       # Desactivar para que el color no varíe
sensor.set_auto_whitebal(False)   # Desactivar para que el color no varíe
clock = time.clock()  # Create a clock object to track the FPS.
img = sensor.snapshot()
uart = UART(3, 115200, timeout_char=1000)
uart.init(115200, bits=8, parity=None, stop=1, timeout_char=1000)

while True:
    clock.tick()  # Update the FPS clock.
    vision = sensor.snapshot()  # Take a picture and return the image.
    time.sleep_ms(25)
    Pelota_morada = [(15, 70, 37, 127, -75, 21)]
    blobs = vision.find_blobs(Pelota_morada, pixels_threshold=200, area_threshold=200, merge=True)
    if blobs:
        # Tomamos el blob más grande (más probable que sea la pelota)
        pelota = max(blobs, key=lambda b: b.pixels)
        cx = (pelota[4])
        cy = (pelota[5])
        print(cx, cy)
        tuplaC = (pelota[4], pelota[5])  # centro X # centro Y
        tuplaR = (pelota[0], pelota[1], pelota[2], pelota[3])
        print(tuplaC)
        vision.draw_cross(tuplaC, color=(255, 0, 0))
        vision.draw_rectangle(tuplaR, color=(255, 0, 0))
        print("pelota detectada")
        uart.write("S:{}\n".format([cx, cy]))
    else:
        print("Pelota no detectada")
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.
