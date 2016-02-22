#include <Wire.h>
#include <BH1750.h>  // https://github.com/claws/BH1750

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

    if (command == "bh1750") {
      bh1750_get();
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

void bh1750_get() {
  /*
    Функция для работы с датчикам освещения BH1750.
    Датчик должен быть подключен к I2C портам Arduino (для arduino Mini Pro это A4 и A5)
  */

  // Инициализация сенсора BH1750
  BH1750 lightMeter;
  lightMeter.begin();

  uint16_t lux = lightMeter.readLightLevel();
  Serial.println(lux);
}

