//"NoName_24", "Wdp57Hmx");   // add Wi-Fi networks you want to connect to
#include "ESP8266WiFi.h"
#include "ESP8266WebServer.h"
#include <microDS18B20.h>
MicroDS18B20<D2> sensor;

ESP8266WebServer server(80);
const char* ssid = ""; //wifi name
const char* password =  ""; //wifi password

byte tries = 10;  // Попыткок подключения к точке доступа

void setup() {
  WiFi.disconnect();
  WiFi.softAPdisconnect();
  WiFi.mode(WIFI_OFF);
  delay(500);
  WiFi.mode(WIFI_STA);
  //WiFi.config(IPAddress(192,168,1,222),IPAddress(192,168,1,1),IPAddress(255,255,255,0),IPAddress(192,168,1,1));
  //IPAddress static_ip(192,168,52,222);  установка лакального айпи

  Serial.begin(115200);
  WiFi.begin(ssid, password);

  while (--tries && WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  if (WiFi.status() != WL_CONNECTED)
  {
    Serial.println("Non Connecting to WiFi..");
  }
  else
  {
    // Иначе удалось подключиться отправляем сообщение
    // о подключении и выводим адрес IP
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());
  }



  server.on("/other", []() {  

    server.send(200, "text / plain", "Have a good day!");

  });

  server.on("/", handleRootPath);    //Свяжем функцию обработчика с путем
  server.begin();                    //Запускаем сервер
  Serial.println("Server listening");
  Serial.println(WiFi.localIP());
}

void loop() {

  server.handleClient();         //Обработка входящих запросов

}

void handleRootPath() {            //Обработчик для корневого пути
  // запрос температуры  
  sensor.requestTemp();
  
  // проверяем успешность чтения и отпраыляем на сервер
  if (sensor.readTemp()) {
    server.send(200, "text/plain", String(sensor.getTemp()));
  } else {
    Serial.println("error");
  }
 
}

