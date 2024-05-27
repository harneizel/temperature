//"NoName_24", "Wdp57Hmx");   // add Wi-Fi networks you want to connect to
#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"
#include <microDS18B20.h>
#include <ESP8266HTTPClient.h>
MicroDS18B20<D2> sensor;

ESP8266WebServer server(80);
const char* ssid = ""; //wifi name
const char* password =  ""; //wifi password
const char* server_addr = ""
HTTPClient http;
ADC_MODE(ADC_VCC);
float Vbat,V_min = 3.00;  

void setup() {
  Serial.begin(115200);  
  Serial.print("Загрузка модуля: ");
  Vbat =  ESP.getVcc();         // читаем напряжение на ноге VCC модуля ESP8266
  Vbat =  Vbat / 1023;          
  Serial.print("Заряд батареи: "), Serial.print(Vbat), Serial.println(" вольт");
  if (Vbat < V_min ) Serial.println("Низкий заряд батареи, засыпаю на  30 минут"), ESP.deepSleep(1800*1000000);
  
  WiFi.disconnect();
  WiFi.softAPdisconnect();
  WiFi.mode(WIFI_OFF);
  delay(500);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("Подключаюсь к сети "),      Serial.println(ssid);
  int count = 0;
  while (WiFi.status() != WL_CONNECTED)  {
    delay(500), Serial.print("."), count++ ;
    if (count > 60) Serial.println(" cон на 10 минут"), ESP.deepSleep(10*60*1000000); // в случае не подключения засыпаем на 10 минут
  };

  Serial.print("WiFi подключен, ChipId: "), Serial.println(ESP.getChipId());
  Serial.print("IP Адрес: "),             Serial.println(WiFi.localIP());
  Serial.print("MAC Адрес: "),            Serial.println(WiFi.macAddress()), Serial.println();
  sensors.begin(); 
  sensors.requestTemperatures(); 


#include <DallasTemperature.h>     // https://github.com/milesburton/Arduino-Temperature-Control-Library
#define ONE_WIRE_BUS 0              
OneWire oneWire(ONE_WIRE_BUS);     // https://github.com/PaulStoffregen/OneWire
DallasTemperature sensors(&oneWire);
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
WiFiClient client;
#define PIN_POWER_DS 5             // Шина питания датчика температуры
const char* ssid = "AAA";          // имя удаленной точки доступа роутера 
const char* password = "BBB";      // пароль удаленной точки доступа
unsigned long Time1 = 0; 
ADC_MODE(ADC_VCC);
float Vbat,V_min = 3.00;                       // напряжение батарейки, и минимальный порог напряжения для разрешения работы

void setup()   {
Serial.begin(115200);  
Serial.print("Загрузка модуля: ");
Vbat =  ESP.getVcc();         // читаем напряжение на ноге VCC модуля ESP8266
Vbat =  Vbat / 1023;          
Serial.print("Заряд батареи: "), Serial.print(Vbat), Serial.println(" вольт");
if (Vbat < V_min ) Serial.println("Низкий заряд батареи, засыпаю на  30 минут"), ESP.deepSleep(1800*1000000);
pinMode     (PIN_POWER_DS, OUTPUT); 
digitalWrite(PIN_POWER_DS, HIGH); 
WiFi.mode   (WIFI_AP_STA);         // запускаем смешенный режим 
WiFi.softAP ("ESP","martinhol");   // поднимаем соaт точку доступа
WiFi.begin  (ssid, password);
Serial.println("Подключаюсь к сети "),      Serial.println(ssid);
int count = 0;
while (WiFi.status() != WL_CONNECTED)  {
  delay(500), Serial.print("."), count++ ;
  if (count > 60) Serial.println(" cон на 10 минут"), ESP.deepSleep(10*60*1000000); // в случае не подключения засыпаем на 10 минут
  };
Serial.print("WiFi подключен, ChipId: "), Serial.println(ESP.getChipId());
Serial.print("IP Адрес: "),             Serial.println(WiFi.localIP());
Serial.print("MAC Адрес: "),            Serial.println(WiFi.macAddress()), Serial.println();

               }

void loop()    {
//if (millis()> Time1 + 300000) Time1 = millis(), narodmonSend ();       // выполняем функцию narodmonSend каждые 10 сек для   теста
  temmperatureSend();
  Serial.println("Засыпаем на 10 минут");
  ESP.deepSleep(10*60*1000000);          // спать на 10 минут пины D16 и  RST должны быть соеденены между собой
  } 


void temmperatureSend {            //забираем темпу и отправляем
  // запрос температуры  
  sensor.requestTemp();
  
  // проверяем успешность чтения и отпраыляем на сервер
  if (sensor.readTemp()) {
    temp = String(sensor.getTemp());
    vcc = ESP.getVcc();
    http.begin(server_addr);
    http.addHeader("Content-type","text/plain");
    String httpRequestData = "temperature="+temp+"&vcc="+vcc;
    int httpCode = http.POST(httpRequestData);
    Serial.println(httpCode);
    http.end();
  
  } 
  else {
    Serial.println("error");
  }

  
  
}

