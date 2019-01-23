
import sys
from machine import Pin, ADC
import network
import utime
from umqtt.robust import MQTTClient
import time

ESSID = "YOURSSIDHERE"
WPA_PSK = "YOURWPA HERE"

photores = ADC(Pin(36))


if sys.platform == 'esp32':
    def do_connect(essid, wpa_psk):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print('connecting to network...')
            wlan.connect(essid, wpa_psk)
            while not wlan.isconnected():
                time.sleep(1/10)
        print('network config:', wlan.ifconfig())

    do_connect(ESSID, WPA_PSK)


def sub_cb(topic, msg):
    print(msg)


client = MQTTClient("2304985032", "iot.eclipse.org", port=1883)

client.set_callback(sub_cb)
client.connect()


while True:
    starttime = utime.time()
    endtime = starttime
    counter = 0
    while ((endtime-starttime) <= 60):
        photores.read()
        counter += 1
        endtime = utime.time()

    print(counter)
    client.publish(topic="project/esp32/micropython/adcread", msg=str(counter))
