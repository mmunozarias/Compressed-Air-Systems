#include <Servo.h>
#include "HX711.h"
#include "Wire.h"

HX711 scale;

Servo myServo;  // Create servo object
const int irPin = 5;
const int baudRate = 19200;

const int pressureInput = A0;
const int pressureZero = 98;
const int pressureMax = 800;
const float pressuretransducermaxPSI = 100;
const float psiToBarConversion = 0.0689476;

float pressureValue = 0;

volatile int flow_frequency = 0;

void setup() {
  pinMode(irPin, INPUT);
  Serial.begin(baudRate);  // Initialize serial communication
  myServo.attach(6);   // Attach servo to pin 6
  myServo.write(0);

  // Attach interrupt to the flow sensor pin
  attachInterrupt(digitalPinToInterrupt(2), flow, RISING); // Assuming the flow sensor is connected to pin 2
}

void loop() {

  int val = !digitalRead(irPin);
  // Send the number of triggers (raw data) in CSV format

  pressureValue = analogRead(pressureInput);
  pressureValue = ((pressureValue - pressureZero) * pressuretransducermaxPSI) / (pressureMax - pressureZero);
  float pressureValueBar = (pressureValue * psiToBarConversion) + 1;

  
  Serial.print(val);
  Serial.print(',');
  Serial.print(pressureValueBar, 2); // Print pressureValue with 2 decimal places
  Serial.print(',');
  Serial.println(flow_frequency);

  flow_frequency = 0; // Reset the counter for the next second

  if (Serial.available() > 0) {
    // Check if the incoming data starts with the header '2'
    if (Serial.peek() == '2') {
      // Skip the '2'
      Serial.read();
      Serial.setTimeout(10); // Set timeout to 100 milliseconds

      int angle = Serial.parseInt();
      myServo.write(angle); 
    }
    while (Serial.available() > 0) {
      Serial.read();
    }
  }
}

void flow() {
  // This function is called on a rising edge (change this based on your sensor's behavior)
  flow_frequency++;
}
