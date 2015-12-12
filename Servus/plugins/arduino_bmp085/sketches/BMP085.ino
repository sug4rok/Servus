#include <Wire.h>
#include <Adafruit_BMP085.h>  // https://github.com/adafruit/Adafruit-BMP085-Library

boolean stringComplete = false;
String command = "";   // Тип выполняемой операции
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
    if (command == "bmp") {
      bmp085_get(param.toFloat());
    }
    else Serial.println("Wrong data receive!");

    command = "";
    param = "";
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
    else if (inChar == ':') param_read = true;
    else {
      if (param_read) param += inChar;
      else command += inChar;
    }
  }
}

void bmp085_get(int alt) {
  /* Функция для работы с датчиком BMP085/BMP180 (он же GY-68).

    На входе: alt - высота над уровне море, где установлен датчик.
    Функция генерирует текстовые данные, вида "p:t", где:
    p - значение атмосферного давленя в мм рт.ст.;
    t - значение температуры в градусах Цельсия.
  */

  // Инициализация датчика давления
  Adafruit_BMP085 bmp;

  if (!bmp.begin()) Serial.println("Could not find a valid BMP085 sensor!");
  else {
    char buff_press[10], buff_temp[10];
    float pressure, temp;

    temp = bmp.readTemperature();
    pressure = (bmp.readSealevelPressure(alt) / 133.3);

    if (isnan(temp) || isnan(pressure)) Serial.println("Failed to read from BMP sensor!");

    dtostrf(temp, 3, 1, buff_temp);
    dtostrf(pressure, 3, 1, buff_press);
    Serial.print(buff_press);
    Serial.print(":");
    Serial.println(buff_temp);
  }
}

