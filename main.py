#
# sample code for the WS2812 class
#
# Connections:
# xxPy | WS2812
# -----|-------
# Vin  |  Vcc
# GND  |  GND
# P11  |  DATA
#
import ws2812
from utime import sleep

data = [
    (255, 0,0)
    ]

blank = [(0,0,0)]

ws2812 = ws2812.WS2812("P11")
ws2812.show(data)


while True:
    ws2812.show(data)
    sleep(2)
    ws2812.show(blank)
    sleep(2) 