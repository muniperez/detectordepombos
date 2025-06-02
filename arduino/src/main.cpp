// Copyright (c) 2025 Muni Perez
/*
    Projeto para o curso de Microcontroladores da Universidade Estácio de Sá.

    Objetivo:
        Desenvolver um sistema de detecção e combate a pombos para estabelecimentos do ramo alimentício.
        O sistema utiliza um sensor ultrassônico para detectar a presença de movimento e uma câmera para identificar se o movimento é de um pombo.
        Caso seja identificado um pombo, um canhão de água é acionado para afastá-lo.

        Esta implementação não inclui a parte do canhão de água, que deve ser feita com um relé ou transistor para controlar uma bomba d'água.
*/

#include <Servo.h>
#include <HardwareSerial.h>
#include <Arduino.h>

const int sonarTriggerPin = 5; // Pino do gatilho do canhão de água
const int sonarReceiverPin = 6; // Pino para receber o eco do sensor ultrassônico
const int waterCannonPin = 9; // Somente para demonstração. O canhão não está implementado.

// Servos para conjunto sonar e câmera
Servo sonarServo;

int angle = 0;
bool scanningForward = true;

const int detectionThreshold = 150; // Distância em cm para detecção de movimento

void setup() {
  Serial.begin(9600);
  sonarServo.attach(3); // Associa o pino do servo do sonar ao objeto Servo do código
  pinMode(sonarTriggerPin, OUTPUT);
  pinMode(sonarReceiverPin, INPUT);
  pinMode(waterCannonPin, OUTPUT); // Configura o pino do canhão de água como saída
  digitalWrite(waterCannonPin, LOW); // Garante que o canhão de água esteja desligado inicialmente
}

void loop() {
  sonarServo.write(angle);
  delay(100); // Pequena pausa para permitir que o servo se mova

  long duration, distance;
  digitalWrite(sonarTriggerPin, LOW);
  delayMicroseconds(2);
  digitalWrite(sonarTriggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(sonarTriggerPin, LOW);
  duration = pulseIn(sonarReceiverPin, HIGH);
  distance = duration * 0.034 / 2;

  if (distance < detectionThreshold && distance > 5) {
    
    // Envia sinal de detecção de movimento para o monitor serial.
    // Ainda não implementado.
    Serial.println("motion_detected");
    
    // Espera até 5s pelo retorno do comando de detecção de objeto que foi enviado pela porta serial.
    // O identificador de pombo irá mandar um retorno com a identificação positiva ou negativa do objeto detectado.
    unsigned long t0 = millis();
    while (millis() - t0 < 5000) {
      if (Serial.available()) {
        String result = Serial.readStringUntil('\n');
        result.trim();
        if (result == "pigeon") { // Se o resultado for "pigeon", significa que um pombo foi identificado
          digitalWrite(waterCannonPin, HIGH); // Executa um disparo no canhão de água
          delay(500);
          digitalWrite(waterCannonPin, LOW); // Desliga o canhão de água após o disparo
        }
        break; // Interrompe o loop após expulsar o pombo.
      }
    }
  }

  // Ângulo de varredura do servo do sonar/câmera
  if (scanningForward) {
    angle += 10;
    if (angle >= 180) scanningForward = false;
  } else {
    angle -= 10;
    if (angle <= 0) scanningForward = true;
  }
}