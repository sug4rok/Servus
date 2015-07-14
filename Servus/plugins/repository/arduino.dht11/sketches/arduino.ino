#include "DHT.h"

boolean stringComplete = false;
char operation_type;   // Тип выполняемой операции
String sensor_pin;  // Номер ввода/вывода Arduino

void send_data(String data) {
  // Функция для отправки данных.
  Serial.println(data); 
}

void setup() {
  Serial.begin(9600);
}

void loop() {
  if (stringComplete) {
    if (operation_type == 't') {
      get_temp(sensor_pin.toInt());
    }
    else send_data("Wrong data receive!");
    sensor_pin = "";
    stringComplete = false;
  }
}

void serialEvent() {
  /*
  Входная срока состоит из типа операции и номер вывода
  Например, t11:
  t - получить данные с датчика температуры;
  11 - датчик подключен к 11 выводу.
  */
  
  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') stringComplete = true;
    else if (isDigit(inChar)) sensor_pin += inChar;
    else operation_type = inChar;
  }
}

void get_temp(int pin) {
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
  
  DHT dht(pin, DHT11);
  dht.begin();
  
  char buffer[20];
  int cur_hum, cur_temp;
  
  cur_hum = dht.readHumidity();
  delay(300);
  cur_temp = dht.readTemperature();
  delay(300);
  
  /*
  Проверяем, является ли полученное значение числом и не превышаю ли полученные данные
  возможные пределы:
  - для DHT11 0<t<50 +-2C, 20<h<80 +-5%;
  - для DHT22 -40<t<125 +-0.5C, 0<h<100 +-5%
  */
  if (isnan(cur_temp) || cur_temp > 52 || cur_temp < -2) sprintf(buffer, "%d:%s", cur_hum, "e");
  else if (isnan(cur_hum) || cur_hum > 85 || cur_hum < 15) sprintf(buffer, "%s:%d", "e", cur_temp);
  else sprintf(buffer, "%d:%d", cur_hum, cur_temp);
  
  send_data(buffer);
}
