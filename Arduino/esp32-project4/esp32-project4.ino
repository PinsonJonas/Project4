#include <WiFi.h>
#include <ArduinoMqttClient.h>
#include <DHTesp.h>
#include <Wire.h>
#include <Adafruit_BMP085.h>


char ssid[] = "YOUR_SSID_HERE";        // your network SSID (name)
char pass[] = "YOUR_WPAKEY_HERE";    // your network password (use for WPA, or use as key for WEP)

WiFiClient espClient;
MqttClient mqttClient(espClient);
DHTesp dht;
Adafruit_BMP085 bmp;

const char broker[] = "iot.eclipse.org";
const char topic[]  = "weatherstation/jonas/project4/esparduino";

int dhtPin = 33;
int mq135Pin = 32;
int photoresPin = 36;

void setup()
{
  // set pin modes
   // begin serial and connect to WiFi
  Serial.begin(115200);
  delay(100);
  
  dht.setup(dhtPin, DHTesp::DHT11);
  
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  Serial.print("Attempting to connect to the MQTT broker: ");
  Serial.println(broker);

  if (!mqttClient.connect(broker, 1883)) {
    Serial.print("MQTT connection failed! Error code = ");
    Serial.println(mqttClient.connectError());

    while (1);
  }

  Serial.println("You're connected to the MQTT broker!");
  Serial.println();

  if (!bmp.begin()) {
  Serial.println("Could not find a valid BMP085 sensor, check wiring!");
  while (1) {}
  }

}


void loop()
{
    // call poll() regularly to allow the library to send MQTT keep alives which
    // avoids being disconnected by the broker
    mqttClient.poll();

    TempAndHumidity lastValues = dht.getTempAndHumidity();
    int dhttemp = lastValues.temperature;
    int dhthum = lastValues.humidity;
    
//    dhttemp = 25;
//    dhthum = 20;
    
    Serial.println("Temperature: " + String(dhttemp));
    Serial.println("Humidity: " + String(dhthum));
    int mq135 = analogRead(mq135Pin);
    Serial.println("PPM: "+String(mq135));
    int photores = analogRead(photoresPin);
    Serial.println("Photoresistor: "+String(photores));
    int bmppressure =  bmp.readPressure()/100;
    Serial.println("BmpPressure: "+String(bmppressure));
    float bmptemp = bmp.readTemperature();
    Serial.println("BmpTemp: "+String(bmptemp));
    
    
    
    

    String json = "{\"DHT11-temperature\":"+String(dhttemp)+",\"DHT11-humidity\":"+String(dhthum)+",\"MQ135-ppm\":"+mq135+",\"photoresistor\":"+String(photores)+",\"Pressure-sensor-pressure\":"+String(bmppressure)+",\"Pressure-sensor-temperature\":"+String(bmptemp)+"}";
    mqttClient.beginMessage(topic);
    mqttClient.print(json);
    mqttClient.endMessage();
    delay(10000);
    

}
