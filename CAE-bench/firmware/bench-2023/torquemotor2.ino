#include "HX711.h"
#define calibration_factor 2150.0
#define DOUT  A0
#define CLK  A1
HX711 scale;

const int irPin = 4;
int triggers = 0;
unsigned long elapsedTime;
int laststate = 0;
const unsigned long sampleTime = 1000;
int rpmMax = 0;

void setup() {
  pinMode(irPin, INPUT);
  Serial.begin(9600);
  scale.begin(DOUT, CLK); // Initialize HX711 with DOUT and CLK pins
  scale.set_scale(calibration_factor);
  scale.tare();
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
