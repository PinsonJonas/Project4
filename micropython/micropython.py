

import sys
import time
import ujson
from machine import Pin, ADC, I2C
from dht import DHT11
import network

from mpl3115a2 import MPL3115A2

ESSID = "YOURSSIDHERE"
WPA_PSK = "YOURWPA HERE"

dht11 = DHT11(Pin(33))
mq135 = ADC(Pin(32))
photoresistor = ADC(Pin(36))
mpl = MPL3115A2(sda=Pin(21), scl=Pin(22), mode=1)


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

    from umqtt.robust import MQTTClient


def sub_cb(topic, msg):
    print(msg)


client = MQTTClient("device_id", "iot.eclipse.org", port=1883)

client.set_callback(sub_cb)
client.connect()
client.subscribe(topic="weatherstation/jonas/project4/espmicropython")


while True:
    dht11.measure()
    temperature = dht11.temperature()
    humidity = dht11.humidity()
    ppm = mq135.read()

    pressure = mpl.pressure()/100
    mpl_temp = mpl.temperature()

    photores = photoresistor.read()
    jsonmsg = {"DHT11-temperature": temperature,
               "DHT11-humidity": humidity,
               "MQ135-ppm": ppm,
               "photoresistor": photores,
               "Pressure-sensor-pressure": pressure,
               "Pressure-sensor-temperature": mpl_temp}
    jsonmsg = ujson.dumps(jsonmsg)
    client.publish(
        topic="weatherstation/jonas/project4/espmicropython", msg=jsonmsg)
    time.sleep(10)
