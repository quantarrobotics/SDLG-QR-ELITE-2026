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
uart = UART(3, 9600, timeout_char=1000)
WIDTH = 320
HEIGHT = 240
MID_X = WIDTH // 2
MID_Y = HEIGHT // 2

while True:
    clock.tick()  # Update the FPS clock.
    vision = sensor.snapshot()  # Take a picture and return the image.
    time.sleep_ms(25)
    Pelota_morada = [(16, 71, 27, 127, -54, 20)]
    blobs = vision.find_blobs(Pelota_morada, pixels_threshold=200, area_threshold=200, merge=True)
    if blobs:
        # Tomamos el blob más grande (más probable que sea la pelota)
        pelota = max(blobs, key=lambda b: b.pixels)
        print(pelota)
        cx = (pelota[4])
        cy = (pelota[5])
        tuplaC = (pelota[4], pelota[5])  # centro X # centro Y
        tuplaR = (pelota[0], pelota[1], pelota[2], pelota[3])
        print(tuplaC)
        print(tuplaR)
        print("tipo tupla:", type(tuplaC), type(tuplaR))
        vision.draw_cross(tuplaC, color=(255, 0, 0))
        vision.draw_rectangle(tuplaR, color=(255, 0, 0))

        def get_zone(cx, cy):
            if cx < 195  and cy > 76:
                return 1
            elif cx < 195 and cy < 75:
                return 2
            elif cx > 195 and cy > 80:
                return 3
            else:
                return 4
        state = get_zone(cx, cy)
        print(state)
        uart.write("S:{}\n".format(state))
    else:
        print("Pelota no detectada")

    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.
