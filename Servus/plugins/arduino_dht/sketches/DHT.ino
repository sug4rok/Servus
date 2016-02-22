#include <DHT.h>  //https://github.com/adafruit/DHT-sensor-library

boolean stringComplete = false;  // Данные c Serial прочитаны
String command = "";  // Тип выполняемой операции
String param = "";  // Параметр, передаваемый функции
boolean param_read = false;

void setup() {
  Serial.begin(9600);
  command.reserve(8);
  param.reserve(8);
}

void loop() {
  serialEvent();

  if (stringComplete) {
    if (command.substring(0, 3) == "dht") {
      dht_get(param.toInt(), command.substring(3).toInt());
    }
    else errorPrint("bad command " + command);

    stringComplete = false;
    command = "";
    param = "";
    param_read = false;
  }
}

void serialEvent() {
  /*
    Входная срока состоит из команды и параметра
    Например, dht22:10:
    dht22 - получить данные с датчика температуры DHT22;
    10 - датчик подключен к 10 выводу.
  */

  while (Serial.available()) {
    char inChar = (char)Serial.read();

    if (inChar == '\n') stringComplete = true;
    else if (!param_read && inChar == ':') param_read = true;
    else {
      if (param_read) param += inChar;
      else command += inChar;
    }
  }
}

void errorPrint(String err) {
  /* Функция вывода ошибки */

  Serial.println("Error: " + err);
}

void dht_get(int pin, int dht_type) {
  /*
    Функция для работы с датчиками DHT11, DHT21, DHT22.
    Чтение значений температуры и влажности занимает около 250 милисекунд!

    На входе: pin - номер ввода/вывода Arduino, к которому подключен датчик и
    dht_type - тип датчика.
    Функция генерирует текстовые данные, вида "h:t", где:
    h - значение относительной влажности в %;
    t - значение температуры в градусах Цельсия.
  */

  // Инициализация DHT сенсора
  DHT dht(pin, dht_type);
  dht.begin();

  char buff_hum[10], buff_temp[10];
  float hum, temp;

  delay(1000);
  hum = dht.readHumidity();
  temp = dht.readTemperature();

  if (isnan(temp) || isnan(hum)) errorPrint("failed to read from DHT sensor!");
  else {
    dtostrf(hum, 3, 0, buff_hum);
    dtostrf(temp, 3, 1, buff_temp);
    Serial.print(buff_hum);
    Serial.print(":");
    Serial.println(buff_temp);
  }
}
