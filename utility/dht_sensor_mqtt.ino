#include <ESP8266WiFi.h>
#include <DHT.h>
#include <PubSubClient.h>


#define DHTPIN 4

#define WIFI_SSID "Tenda_475860"
#define WIFI_PASSWORD "4slovavsecapsom"

String GLOBAL_ID = "9823134124";

IPAddress mqtt_server;

DHT dht(DHTPIN, DHT11);
WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
char msg[50];
int value = 0;

String client_id_hum = "-";
String client_id_temp = "-";

float temperature = 0;
float humidity = 0;


void setup() {
  Serial.begin(9600);
  dht.begin();

  setup_wifi();

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);
   
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  Serial.println("Gateway IP address: ");
  Serial.println(WiFi.gatewayIP());
  mqtt_server = WiFi.gatewayIP();
  //mqtt_server = IPAddress(192, 168, 0, 106);
}

String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length()-1;

  for(int i=0; i<=maxIndex && found<=index; i++){
    if(data.charAt(i)==separator || i==maxIndex){
        found++;
        strIndex[0] = strIndex[1]+1;
        strIndex[1] = (i == maxIndex) ? i+1 : i;
    }
  }

  return found>index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void callback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();

  // Register handle
  if (String(topic) == "broker/register") {
    // If ACK for me
    if (messageTemp.substring(0, 4 + GLOBAL_ID.length()) == String("ACK;")+GLOBAL_ID)
    {
        Serial.println("Register ACK for me recieved.");
        String ids = getValue(messageTemp, ';', 2);
        Serial.print("Recieved IDs: ");
        Serial.println(ids);
        client_id_temp = getValue(ids, ',', 0);
        client_id_hum = getValue(ids, ',', 1);
        Serial.print("Temperature channel: ");
        Serial.println(client_id_temp);
        Serial.print("Humidity channel: ");
        Serial.println(client_id_hum);
    }
  }
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect((String("client") + GLOBAL_ID).c_str())) {
      Serial.println("connected");

      // Subscribe
      client.subscribe("broker/register");
      if (client_id_hum != "-"){
          client.subscribe((String("client") + client_id_hum + String("/status")).c_str());
      }
      if (client_id_temp != "-"){
          client.subscribe((String("client") + client_id_temp + String("/status")).c_str());
      }

    } 
    else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  long now = millis();
  if (now - lastMsg > 4000) {
    lastMsg = now;
    
    if (client_id_temp == "-" && client_id_hum == "-") {
      client.publish("broker/register", (GLOBAL_ID + String(";temperature,humidity")).c_str());
      return;
    }

    // Read data
    humidity = dht.readHumidity();
    temperature = dht.readTemperature();
      
    if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Error reading data!");
    return;
  }
    
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    client.publish(("client" + client_id_temp + "/data/temperature").c_str(), tempString);
    Serial.print("Sent data to ");
    Serial.print("client" + client_id_temp + "/data/temperature");
    Serial.println(" topic.");

    char humString[8];
    dtostrf(humidity, 1, 2, humString);
    Serial.print("Humidity: ");
    Serial.println(humString);
    client.publish(("client" + client_id_hum + "/data/humidity").c_str(), humString);
    Serial.print("Sent data to ");
    Serial.print("client" + client_id_temp + "/data/humidity");
    Serial.println(" topic.");

  }
}
