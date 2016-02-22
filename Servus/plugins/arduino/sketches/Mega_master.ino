HardwareSerial *port;  // Serial port class. Predefined instances are Serial1, Serial2, and Serial3.

boolean stringComplete = false;  // Данные c Serial прочитаны
String command = "";  // Тип выполняемой операции
String param = "";  // Параметр, передаваемый функции
boolean param_read = false;

boolean portStringComplete = false;  // Данные c Serial1 (Serial2, Serial3) прочитаны
String portResult = "";  // Ответ от Serial1 (Serial2, Serial3)

void setup() {
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial2.begin(9600);
  Serial3.begin(9600);

  command.reserve(8);
  param.reserve(8);
}

void loop() {
  serialEvent();

  if (stringComplete) {

    if (command.substring(0, 3) == "ser") {
      serialCommunicate(command.substring(3, 4));
      if (portStringComplete) {
        Serial.println(portResult);
      }
    }
    // else if (command == "your_command") {
    //   run_your_function();
    // }
    else errorPrint("bad command " + command);

    stringComplete = false;
    command = "";
    param = "";
    param_read = false;
    portStringComplete = false;
    portResult = "";
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

void serialCommunicate(String port_number) {
  /*
    Функция, осуществляющая обмен с указанным параметром port_number
    последовательным портом.
  */

  if (port_number == "1") port = &Serial1;
  else if (port_number == "2") port = &Serial2;
  else if (port_number == "3") port = &Serial3;
  else errorPrint("wrong number of serial port");

  if (port) {
    String str = "aa" + param;  // Два символа добавлены, т.к. при коммуникации Mega и Mini Pro где-то
    port->println(param);       // теряются первые два символы. На стенде повторить баг не удалось.
    delay(2000);

    while (Serial1.available()) {
      char inChar = (char)port->read();

      if (inChar == '\n') portStringComplete = true;
      else portResult += inChar;
    }
  }
}

