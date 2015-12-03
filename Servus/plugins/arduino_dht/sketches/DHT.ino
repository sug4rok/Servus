#include "DHT.h"

boolean pin_read = false;
boolean stringComplete = false;
String command = "";   // Тип выполняемой операции
String sensor_pin = "";  // Номер ввода/вывода Arduino

void setup() {
  Serial.begin(9600);
  command.reserve(8);
  sensor_pin.reserve(2);
}

void loop() {
  serialEvent();

  if (stringComplete) {
    if (sensor_pin != "") {
      if (command.substring(0, 3) == "dht") {
        dht_get(sensor_pin.toInt(), command.substring(3).toInt());
      }
      else Serial.println("Wrong data receive!");

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

  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') stringComplete = true;
    else if (inChar == ':') pin_read = true;
    else {
      if (pin_read) sensor_pin += inChar;
      else command += inChar;
    }
  }
}

void dht_get(int pin, int dht_type) {
  /*
    Функция для работы с датчиками DHT11, DHT21, DHT22.
    Чтение значений температуры и влажности занимает около 250 милисекунд!

    На входе: pin - номер ввода/вывода Arduino, к которому подключен датчик и
    dht_type - тип датчика.
    Функция генерирует текстовые данные, вида "h:t", где:
    h - значение влажности;
    t - значение температуры.
  */

  // Инициализация DHT сенсора
  DHT dht(pin, dht_type);
  dht.begin();

  char buff_hum[10], buff_temp[10];
  float hum, temp;

  delay(2000);
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  if (isnan(temp) || isnan(hum)) Serial.println("Failed to read from DHT sensor!");

  dtostrf(hum, 3, 0, buff_hum);
  dtostrf(temp, 3, 1, buff_temp);
  Serial.print(buff_hum);
  Serial.print(":");
  Serial.println(buff_temp);
}
