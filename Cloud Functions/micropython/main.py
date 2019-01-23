import pandas as pd
import requests
import firebase_admin
from datetime import datetime
from firebase_admin import credentials, db

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'databaseURL': 'Hier_komt_je_DatabaseURL',
    'projectId': 'Hier_komt_je_projectID',
})


def loading_data(list_data, timestamp):

    DHT11Humidity = list_data[0]
    DHT11Temperature = list_data[1]
    MQ135Ppm = list_data[2]
    PSPressure = list_data[3]
    PSTemperature = list_data[4]
    Photoresistor = list_data[5]
    Time = datetime.fromtimestamp(int(timestamp))
    return DHT11Humidity, DHT11Temperature, MQ135Ppm, PSPressure, PSTemperature, Photoresistor, Time


def update_esp32_micropython(data, context):
    """ Triggered by a change to a Firebase RTDB reference.
    Args:
        data (dict): The event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    trigger_resource = context.resource
    global timestamp
    timestamp = trigger_resource.split('/')

    timestamp = timestamp[-1]

    print('Function triggered by change to: %s' % trigger_resource)
    ref = db.reference('esp32-micropython/{0}'.format(timestamp))
    result = ref.get()
    values = result.values()
    list_values = []
    for value in values:
        list_values.append(value)
    REST_API_URL = 'VUL JE EIGEN POWERBI API LINK IN'

    data_raw = []
    row = loading_data(list_values, timestamp)
    data_raw.append(row)
    # print("Raw data - ", data_raw)

    HEADER = ["DHT11 - Humidity", "DHT11 - Temperature", "MQ135 - Ppm",
              "Pressure_sensor - Pressure", "Pressure_sensor - Temperature", "Photoresistor", "Time"]

    data_df = pd.DataFrame(data_raw, columns=HEADER)
    data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')

    # Post the data on the Power BI API
    req = requests.post(REST_API_URL, data_json)

    print("Data posted in Power BI API")
