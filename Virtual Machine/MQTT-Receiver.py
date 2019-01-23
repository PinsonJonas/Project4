from datetime import datetime as dt
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db as db1
import paho.mqtt.client as mqtt
import json

cred = credentials.Certificate('firebase-auth.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Hier_komt_je_DatabaseURL',
    'projectId': 'Hier_komt_je_projectID',
})

broker_address = "iot.eclipse.org"

print("creating new instance")
client = mqtt.Client("234984752492")  # create new instance
print("connecting to broker")
client.connect(broker_address)  # connect to broker
print("Subscribing to topic", "weatherstation/jonas/project4/esparduino")
print("Subscribing to topic", "weatherstation/jonas/project4/espmicropython")
client.subscribe("weatherstation/jonas/project4/espmicropython")
client.subscribe("weatherstation/jonas/project4/esparduino")


def on_message(client, userdata, message):
    print("message received ", str(message.payload.decode("utf-8")))
    print("message topic=", message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    if message.topic == "weatherstation/jonas/project4/espmicropython":
        time = dt.utcnow().strftime("%s")
        receivedmsg = json.loads(message.payload.decode("utf-8"))
        ref2 = db1.reference('esp32-micropython')
        ref2.update({time: receivedmsg})
    if message.topic == "weatherstation/jonas/project4/esparduino":
        time = dt.utcnow().strftime("%s")
        receivedmsg = json.loads(message.payload.decode("utf-8"))
        ref2 = db1.reference('esp32-arduino')
        ref2.update({time: receivedmsg})


client.on_message = on_message  # attach function to callback

client.loop_forever()  # start the loop
