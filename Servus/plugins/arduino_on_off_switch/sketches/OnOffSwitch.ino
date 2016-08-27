#include <Wire.h>

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

    if (command == "sw_state") {
      sw_state_get(param.toInt());
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

void sw_state_get(int pin) {
  /*
    Функция, предоставляющая данные с переключателей с двумя состояниями (on/off)

    На входе: pin - номер ввода/вывода Arduino, к которому подключен переключатель.
    На выходе: 0 или 1 - состояние переключателя разомкнут/замкнут соотвественно.
  */

  pinMode(pin, INPUT);
  Serial.println(digitalRead(pin));
}

