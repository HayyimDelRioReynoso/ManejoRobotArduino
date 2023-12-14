#include <avr/wdt.h>

int velocidadIngresada = 0;
int pulsosIngresados = 0;
int sentidoSeleccionado = 0;

int motorSeleccionado = 0;

const int motorPin1 = 4;   // Pin de control del motor - dirección 1
const int motorPin2 = 5;   // Pin de control del motor - dirección 2
const int speedPin = 9;    // Pin de salida PWM para controlar la velocidad del motor
const int encoderPin = 2;  // Pin de lectura del encoder (canal A)

const int motor2Pin1 = 31;
const int motor2Pin2 = 33;
const int speedPin2 = 10;
const int encoder2Pin = 3;

const int limitSensorRightPin = 6;  // Pin del sensor de límite derecho
const int limitSensorLeftPin = 7;   // Pin del sensor de límite izquierdo

volatile int contador = 0;  // Variable para almacenar la posición del encoder


void setup() {
  // Configuración de pines
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);
  pinMode(encoderPin, INPUT_PULLUP);
  pinMode(speedPin, OUTPUT);

  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(encoder2Pin, INPUT_PULLUP);
  pinMode(speedPin2, OUTPUT);

  pinMode(limitSensorRightPin, INPUT_PULLUP);
  pinMode(limitSensorLeftPin, INPUT_PULLUP);



  // Iniciar el monitor serial
  Serial.begin(9600);

  // Interrupciones para lectura del encoder
  attachInterrupt(digitalPinToInterrupt(encoderPin), updatePosition, CHANGE);  // CHANGE, RISING, FALLING, LOW y HIGH
  attachInterrupt(digitalPinToInterrupt(encoder2Pin), updatePosition, CHANGE);
  attachInterrupt(digitalPinToInterrupt(limitSensorRightPin), detenerDerecha, CHANGE);
  attachInterrupt(digitalPinToInterrupt(limitSensorLeftPin), detenerIzquierda, CHANGE);
}

void loop() {
  // Flag para indicar si los datos ya fueron procesados
  static bool datosProcesados = false;

  // Solo procesar datos si no han sido procesados aún
  if (!datosProcesados && Serial.available() > 0) {
    // Reiniciar variables antes de procesar nuevos datos
    velocidadIngresada = 0;
    pulsosIngresados = 0;
    sentidoSeleccionado = "";

    // Procesar la línea de datos
    String receivedData = Serial.readStringUntil('\n');

    // Dividir la cadena en partes usando la coma como separador
    int coma1 = receivedData.indexOf(',');
    int coma2 = receivedData.indexOf(',', coma1 + 1);

    if (coma1 != -1 && coma2 != -1) {
      velocidadIngresada = receivedData.substring(0, coma1).toInt();
      pulsosIngresados = receivedData.substring(coma1 + 1, coma2).toInt();
      sentidoSeleccionado = receivedData.substring(coma2 + 1, receivedData.lastIndexOf(',')).toInt();
      motorSeleccionado = receivedData.substring(receivedData.lastIndexOf(',') + 1).toInt();


      // Imprimir los valores almacenados
      Serial.print("VelocidadA: ");
      Serial.print(velocidadIngresada);
      Serial.print(", PulsosA: ");
      Serial.print(pulsosIngresados);
      Serial.print(", SentidoA: ");
      Serial.print(sentidoSeleccionado);
      Serial.print(", MotorA: ");
      Serial.print(motorSeleccionado);



      // Marcar los datos como procesados
      datosProcesados = true;
    }
  }



  //Serial.println(sentidoSeleccionado);
  if (sentidoSeleccionado == 0 || sentidoSeleccionado == 1) {
    moverMotor(velocidadIngresada, sentidoSeleccionado, pulsosIngresados);
    delay(1000);
  } else {
    // Puedes agregar un mensaje de error o cualquier otra acción en caso de un valor inesperado.
    Serial.println("Valor inesperado para sentidoSeleccionado");
  }









  // Restablecer datosProcesados a false
  datosProcesados = false;
  velocidadIngresada = 0;
  pulsosIngresados = 0;
  sentidoSeleccionado = 0;
}


void moverMotor(int velocidad, int sentidoGiro, int pulsos) {





  if (motorSeleccionado == 1) {
    // Establecer dirección de giro
    digitalWrite(motorPin1, sentidoGiro);
    digitalWrite(motorPin2, !sentidoGiro);

    // Control del motor según los pulsos especificados
    contador = 0;  // Reiniciar el contador



    while (contador < pulsos) {
      // Controlar la velocidad utilizando la señal PWM (modulación por ancho de pulso)

      detenerDerecha();
      detenerIzquierda();
      analogWrite(speedPin, velocidad);


      // Esperar un breve período para permitir que la interrupción actualice el contador
      delay(1);
    }

    // Detener el motor
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);

    // Esperar un breve período para asegurar que el motor se detenga antes de salir de la función
    delay(100);
  } else if (motorSeleccionado == 2) {

    digitalWrite(motor2Pin1, sentidoGiro);
    digitalWrite(motor2Pin2, !sentidoGiro);

    // Control del motor según los pulsos especificados
    contador = 0;  // Reiniciar el contador

    while (contador < pulsos) {
      // Controlar la velocidad utilizando la señal PWM (modulación por ancho de pulso)
      analogWrite(speedPin2, velocidad);

      // Esperar un breve período para permitir que la interrupción actualice el contador
      delay(1);
    }

    // Detener el motor
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);

    // Esperar un breve período para asegurar que el motor se detenga antes de salir de la función
    delay(100);
  }
}



void updatePosition() {
  // Actualizar la posición del encoder en función de las transiciones del canal A
  contador++;
}

void detenerDerecha() {
  if (digitalRead(limitSensorRightPin) == HIGH) {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    Serial.flush();

    

    // Imprimir mensaje
    Serial.println("Llegando a limite derecho, volviendo a home");
    Serial.print("Cambiando dirección a: ");
    Serial.println(!sentidoSeleccionado);

    // Continuar moviendo el motor en la nueva dirección
    moverMotor(255, !sentidoSeleccionado, 400);

    wdt_enable(WDTO_15MS);  // Activar el temporizador de reinicio de 15 ms
    while (1);  // Esperar a que ocurra el reinicio

    
  }
}

void detenerIzquierda() {
  if (digitalRead(limitSensorLeftPin) == HIGH) {
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
    Serial.flush();

    

    // Imprimir mensaje
    Serial.println("Llegando a limite izquierdo, volviendo a home");
    Serial.print("Cambiando dirección a: ");
    Serial.println(!sentidoSeleccionado);

    // Continuar moviendo el motor en la nueva dirección
    moverMotor(255, !sentidoSeleccionado, 400);

    wdt_enable(WDTO_15MS);  // Activar el temporizador de reinicio de 15 ms
    while (1);  // Esperar a que ocurra el reinicio

    
  }
}
