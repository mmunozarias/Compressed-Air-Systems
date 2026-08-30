#include "HX711.h"
#include "Wire.h"

#define calibration_factor 2150.0
#define DOUT  12
#define CLK  13
HX711 scale;

const int irPin = 4;
int triggers = 0;
unsigned long elapsedTime;
int laststate = 0;
const unsigned long sampleTime = 1000;
int rpmMax = 0;

const int pressureInput = A0;
const int pressureZero = 98;
const int pressureMax = 800;
const int pressuretransducermaxPSI = 100;
const int baudRate = 9600;
const int sensorreadDelay = 250;

volatile int flow_frequency;
unsigned int l_hour;
unsigned char flowsensor = 2;
unsigned long currentTime;
unsigned long cloopTime;

float pressureValue = 0;

void flow () {
  flow_frequency++;
}

void setup() {
  pinMode(irPin, INPUT);
  pinMode(flowsensor, INPUT);
  digitalWrite(flowsensor, HIGH);
  Serial.begin(baudRate);
  attachInterrupt(0, flow, RISING);
  sei();
  scale.begin(DOUT, CLK);
  scale.set_scale(calibration_factor);
  scale.tare();
  currentTime = millis();
  cloopTime = currentTime;
}

void loop() {
  int rpm = rpmGet();
  if (rpm > rpmMax) {
    rpmMax = rpm;
  }
  Serial.print("MaxRpm. : ");
  Serial.println(rpm);
  torque();

  Serial.print("raw rpm data:");
  Serial.println(rpm);
  Serial.print("raw force data:");
  Serial.println(scale.read());

  currentTime = millis();

  if (currentTime >= (cloopTime + 1000)) {
    cloopTime = currentTime;

    l_hour = (flow_frequency * 60 / 7.5);
    flow_frequency = 0;

    pressureValue = analogRead(pressureInput);
    pressureValue = ((pressureValue - pressureZero) * pressuretransducermaxPSI) / (pressureMax - pressureZero);

    Serial.print("Flow Rate: ");
    Serial.print(l_hour, DEC);
    Serial.println(" L/hour");

    Serial.print("Pressure: ");
    Serial.print(pressureValue, 1);
    Serial.println(" psi");

    delay(sensorreadDelay);
  }
}

void torque() {
  float force = ((scale.get_units()) / 100);
  float arm = (28);
  int torque = (force * arm);
  Serial.print("Torque: ");
  Serial.print(torque);
  Serial.println(" Nmm");
}

int rpmGet() {
  unsigned long currentTime = 0;
  unsigned long startTime = millis();
  while (currentTime <= sampleTime) {
    int val = digitalRead(irPin);
    if (!val) {
      if (laststate) {
        triggers++;
        laststate = 0;
      }
    } else {
      laststate = 1;
    }
    currentTime = millis() - startTime;
  }
  int countRpm = int(60000 / float(sampleTime)) * (triggers / 2);
  triggers = 0;
  return countRpm;
}
