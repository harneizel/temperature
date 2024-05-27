//"NoName_24", "Wdp57Hmx");   // add Wi-Fi networks you want to connect to
#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"
#include <microDS18B20.h>
#include <ESP8266HTTPClient.h>
MicroDS18B20<D2> sensor;

ESP8266WebServer server(80);
const char* ssid = "esp"; //wifi name
const char* password =  "Sapsan777"; //wifi password

//const char* ssid = "NoName_24"; //wifi name
//const char* password =  "Wdp57Hmx"; //wifi password
const char* serverAddress = "192.168.254.184";
const int serverPort = 5000; // Порт сервера
WiFiClient client;
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
    if (count > 60) Serial.println(" cон на 1 минут"), ESP.deepSleep(1*60*1000000); // в случае не подключения засыпаем на 10 минут
  };

  Serial.print("WiFi подключен, ChipId: "), Serial.println(ESP.getChipId());
  Serial.print("IP Адрес: "), Serial.println(WiFi.localIP());
  Serial.print("MAC Адрес: "), Serial.println(WiFi.macAddress()), Serial.println();
}


void loop() {
//if (millis()> Time1 + 300000) Time1 = millis(), narodmonSend ();       // выполняем функцию narodmonSend каждые 10 сек для   теста
  temmperatureSend();
  Serial.println("Засыпаем на 10 секунд");
  delay(10000);
  //ESP.deepSleep(10*1000000);          // спать на 10 минут пины D16 и  RST должны быть соеденены между собой
  } 


void temmperatureSend() {            //забираем темпу и отправляем
  //запрос температуры  
  sensor.requestTemp();
  delay(1000); //задрежка чтобы датчик прочитал темпу
  // проверяем успешность чтения и отправляем на сервер
  if (sensor.readTemp()) {
    float temp = round(sensor.getTemp()*10)/10.0; //оругляем темпу до десятых
    float vcc = ESP.getVcc()/1000;
    String url = "http://" + String(serverAddress) + ":" + String(serverPort) + "/get-temperature"; //отправляем все это
    http.begin(url);
    http.addHeader("Content-Type","application/x-www-form-urlencoded");
    Serial.println(temp);
    String data = "temp="+String(temp)+"&vcc="+String(vcc);
    int httpCode = http.POST(data);
    Serial.println(httpCode);
    http.end();
  
  } 
  else {
    Serial.println("error");
  }

  
  
}

