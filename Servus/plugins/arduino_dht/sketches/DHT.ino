#include "DHT.h"

boolean stringComplete = false;
String command = "";   // Тип выполняемой операции
String sensor_pin = "";  // Номер ввода/вывода Arduino

void send_data(String data) {
  // Функция для отправки данных.
  Serial.println(data);
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  serialEvent();
  
  if (stringComplete) {
    if (sensor_pin != ""){
      if (command.substring(0, 3) == "dht") {
        dht_get(sensor_pin.toInt(), command.substring(3).toInt());
      }
      else send_data("Wrong data receive!");
      
      command = "";
      sensor_pin = "";
      stringComplete = false;
    }
  }
}

void serialEvent() {
  /*
    Входная срока состоит из типа операции и номер вывода
    Например, t11:
    t - получить данные с датчика температуры;
    11 - датчик подключен к 11 выводу.
  */

  boolean pin_read = false;
  
  while (Serial.available()) {
    char inChar = (char)Serial.read();
  
    if (inChar == '\n') stringComplete = true;
    else if (inChar == '_') pin_read = true;
    else if (pin_read) sensor_pin += inChar;
    else command += inChar;
  }
}

void dht_get(int pin, int dht_type) {
  /*
    Функция для работы с датчиками DHT11, DHT21, DHT22.
    Чтение значений температуры и влажности занимает около 250 милисекунд!

    На входе: pin - номер ввода/вывода Arduino, к которому подключе датчик
    Функция генерирует текстовые данные, вида "h:t", где:
    h - значение влажности;
    t - значение температуры.
    Если в ходе получения данных произошла ошибка, соответствующее значение
    будет равно "e" (например, "e:25" - сбой получения значения влажности).
  */

  // Инициализация DHT сенсора
  DHT dht(pin, dht_type);
  dht.begin();

  char buffer[20];
  float cur_hum, cur_temp;

  delay(2000);
  cur_hum = dht.readHumidity();
  cur_temp = dht.readTemperature();

  /*
    Проверяем, является ли полученное значение числом и не превышаю ли полученные данные
    возможные пределы:
    - для DHT11 и DHT21 0<t<50 +-2C, 20<h<80 +-5%;
    - для DHT22 -40<t<125 +-0.5C, 0<h<100 +-5%
  */
  if (dht_type == 11 || dht_type == 21){
    if (isnan(cur_temp) || cur_temp > 52 || cur_temp < -2) sprintf(buffer, "%d:%s", cur_hum, "e");
    else if (isnan(cur_hum) || cur_hum > 85 || cur_hum < 15) sprintf(buffer, "%s:%d", "e", cur_temp);
  }
  else if (dht_type == 22){
    if (isnan(cur_temp) || cur_temp > 126 || cur_temp < -41) sprintf(buffer, "%d:%s", cur_hum, "e");
    else if (isnan(cur_hum) || cur_hum > 100 || cur_hum < 0) sprintf(buffer, "%s:%d", "e", cur_temp);
  }
  else sprintf(buffer, "%d:%d", cur_hum, cur_temp);

  send_data(buffer);
}
