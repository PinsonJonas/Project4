#include <DHTesp.h>
#include <WiFi.h>
#include <ArduinoMqttClient.h>

char ssid[] = "YOUR_SSID_HERE";        // your network SSID (name)
char pass[] = "YOUR_WPAKEY_HERE";    // your network password (use for WPA, or use as key for WEP)

WiFiClient espClient;
MqttClient mqttClient(espClient);

const char broker[] = "iot.eclipse.org";
const char topic[]  = "project4/esp32/arduino/adcread";

unsigned long starttime;
unsigned long endtime;
int loopcount;
int photores;
int photoresPin = 36;

void setup() {
  // set pin modes
  // begin serial and connect to WiFi
  Serial.begin(115200);
  delay(100);
    
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
}

void loop() {
  loopcount = 0;
  
  starttime = millis();
  endtime = starttime;
  while((endtime - starttime) <=60000) // do this loop for up to 60000mS
  {
    photores = analogRead(photoresPin);
    loopcount = loopcount+1;
    endtime = millis();
  }
  Serial.println(loopcount,DEC);
  String loopcounter = String(loopcount);
  mqttClient.beginMessage(topic);
  mqttClient.print(loopcounter);
  mqttClient.endMessage();

}
