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

import json
import logging
import time
from uuid import UUID
from ws2812 import WS2812
from machine import Pin

#used for mqtt connection
from mqtt import MQTTClient
from network import WLAN
import machine

# Pycom specifics
import pycom
import wifi
from pyboard import Pysense, Pytrack

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from wifi import set_time



def sub_cb(topic, msg):
    print(msg)


# data = [
#     (255, 0,0)
#     ]

# blank = [(0,0,0)]

# ws2812 = ws2812.WS2812("P11")
# ws2812.show(data)


# while True:
#     ws2812.show(data)
#     sleep(2)
#     ws2812.show(blank)
#     sleep(2) 

class Main:
    """
    |  UBIRCH example for pycom modules.
    |
    |  The devices creates a unique UUID and sends data to the ubirch data and auth services.
    |  At the initial start these steps are required:
    |
    |  - start the pycom module with this code
    |  - take note of the UUID printed on the serial console
    |  - register your device at the Ubirch Web UI
    |
    """

    def __init__(self) -> None:


        # p_out = Pin('P11', mode=Pin.OUT, pull=Pin.PULL_DOWN) 
        chain = WS2812(ledNumber=1, brightness=100, dataPin='P22')


        while True:
            chain.show([(0, 0, 255)])
            time.sleep(5)

            chain.show([(0, 255, 0)])
            time.sleep(5)

            chain.show([(255, 0, 0)])
            time.sleep(5)

        # generate UUID
        self.uuid = UUID(b'UBIR' + 2 * machine.unique_id())
        print("\n** UUID   : " + str(self.uuid) + "\n")

        # load configuration from config.json file
        # the config.json should be placed next to this file
        # {
        #    "connection": "<'wifi' or 'nbiot'>",
        #    "networks": {
        #      "<WIFI SSID>": "<WIFI PASSWORD>"
        #    },
        #    "apn": "<APN for NB IoT connection",
        #    "type": "<TYPE: 'pysense' or 'pytrack'>",
        #    "password": "<password for ubirch auth and data service>",
        #    "keyService": "<URL of key registration service>",
        #    "niomon": "<URL of authentication service>",
        #    "data": "<URL of data service>"
        # }
        try:
            with open('config.json', 'r') as c:
                self.cfg = json.load(c)
        except OSError:
            print(setup_help_text)
            while True:
                machine.idle()

        if self.cfg["connection"] == "wifi":
            # try to connect via wifi, throws exception if no success
            wifi.connect(self.cfg['networks'])
            set_time()  # fixme doesnt set time with nbiot
            # wlan = WLAN(mode=WLAN.STA)
        elif self.cfg["connection"] == "nbiot":
            from nb_iot_client import NbIotClient
            self.nbiot = NbIotClient(self.uuid, self.cfg)

    def loop(self, interval: int = 60):
        # disable blue heartbeat blink
        # pycom.heartbeat(False)
        
        client = MQTTClient(str(self.uuid), "mqtt.eclipse.org")
        client.set_callback(sub_cb)
        client.connect()
        client.subscribe(topic="europelight/fuerstenberg")

        while True:
            client.wait_msg()

main = Main()
main.loop(60)


