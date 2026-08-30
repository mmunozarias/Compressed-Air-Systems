#include <ArduinoJson.h>

// System settings
const int baudRate = 19200; // Baud rate of system

// Pins to which the sensors are connected on the system, only pin 2 and 3 of the uno support interrupt
const int pressureInput = A0; // Pin to which the pressure sensor data is connected on the Arduino
const int irInput = 3; // Pin to which the IR sensor data is connected on the Arduino
const int flowSensorPin = 2; // Connect the flow sensor to digital pin 2

// Calibration values of the pressure sensor
const int pressureZero = 98;
const int pressureMax = 800;
const float pressuretransducermaxPSI = 100;
const float psiToBarConversion = 0.0689476;
float pressureValue = 0;

// IR sensor pulse count
volatile int irPulseCount = 0;

// Flow sensor calibration values
volatile int pulseCount = 0;
const float calibrationFactor = 7.5; // Calibration factor for the flow sensor

float flowRate = 0.0;

void setup() {
  Serial.begin(baudRate);       // Initializes serial (USB) connection with baudRate
  pinMode(irInput, INPUT);      // Sets pin mode for IR sensor

  // Set the pin mode for the flow sensor
  pinMode(flowSensorPin, INPUT_PULLUP);

  // Attach interrupt to the flow sensor
  attachInterrupt(digitalPinToInterrupt(flowSensorPin), flowPulseCounter, RISING);

  // Attach interrupt to the IR sensor
  attachInterrupt(digitalPinToInterrupt(irInput), irPulseCounter, FALLING);
}

void loop() {
  // Read the value of the IR sensor and invert the logic
  bool irValue = !digitalRead(irInput);
  int sensorValue = analogRead(pressureInput);

  // Calculate the actual Pressure value
  pressureValue = ((float)sensorValue - pressureZero) * (pressuretransducermaxPSI / (pressureMax - pressureZero));

  // If calculated pressure is lower than 0 set it to 0
  pressureValue = max(pressureValue, 0.0);

  // Calculate pressure in Bar
  float pressureValueInBar = (pressureValue * psiToBarConversion) + 1;

  // Calculate flow rate in L/min
  noInterrupts(); // Disable interrupts while calculating flow rate
  flowRate = (pulseCount / calibrationFactor) * 60;
  pulseCount = 0; // Reset the pulse count
  interrupts(); // Enable interrupts

  // Convert data to JSON file format to be exported to Python
  StaticJsonDocument<200> doc;              // Creates JSON file with max length 200 and type doc
  doc["pressure_bar"] = pressureValueInBar; // Adds data from the pressure sensor to the document
  doc["ir_pulse_count"] = irPulseCount;     // Adds IR pulse count to the document
  doc["flow_rate"] = flowRate;              // Adds data from flow sensor to the document
  doc["irValue"] = irValue;                 // Adds data from IR sensor to the doc
  serializeJson(doc, Serial);               // Sends the JSON file using serial
  Serial.println(); // Add a newline character for better readability

  // Reset IR pulse count after sending data
  irPulseCount = 0;

  // Set delay before initiating next loop
  delay(200); // Reduced delay to 200 milliseconds
}

void flowPulseCounter() {
  pulseCount++;
}

void irPulseCounter() {
  irPulseCount++;
}
