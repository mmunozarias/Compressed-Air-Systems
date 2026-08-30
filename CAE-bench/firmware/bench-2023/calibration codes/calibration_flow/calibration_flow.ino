byte statusLed = 13;

byte sensorInterrupt = 0; // Change this to the appropriate interrupt number for your pin
byte sensorPin = 7; // Change this to the pin connected to your flow sensor

volatile byte pulseCount;

float calibrationFactor = 11.0; // Initial guess for calibration factor

// Known flow rate in liters per minute
float knownFlowRate = 10.0; // Replace this with your actual known flow rate

float tubeRadius = 6.25e-3; // Radius of the tube in meters
float tubeArea; // Area of the tube in square meters
float speedOfSound = 343.0; // Speed of sound in m/s

void setup()
{
  Serial.begin(9600);
  pinMode(statusLed, OUTPUT);
  digitalWrite(statusLed, HIGH);
  pinMode(sensorPin, INPUT);
  digitalWrite(sensorPin, HIGH);

  pulseCount = 0;

  attachInterrupt(sensorInterrupt, pulseCounter, FALLING);

  Serial.println("Flow Sensor Calibration");
  Serial.println("Press any key in the Serial Monitor to start calibration.");
  while (!Serial.available()) {} // Wait for user input
  Serial.read(); // Clear the input buffer

  calibrateFor0_5Seconds();

  // Calculate the correct calibration factor using the known flow rate
  calibrationFactor = calculateCalibrationFactor(knownFlowRate);

  Serial.print("Calibration Factor: ");
  Serial.println(calibrationFactor);

  // Stop the program
  while (true) {}
}

void calibrateFor0_5Seconds()
{
  pulseCount = 0;
  unsigned long oldTime = millis(); // Gets the current time before the sample loop
  unsigned long sampleTime = oldTime + 500; // Sets the sampling time as 0.5 seconds

  while (millis() < sampleTime)
  {
    oldTime = millis(); // Gets the current time during the sample loop
    byte currentFlowValue = digitalRead(sensorPin); // Sampling flow sensor
    byte initialFlowValue = currentFlowValue;

    while (millis() < sampleTime)
    {
      oldTime = millis();
      currentFlowValue = digitalRead(sensorPin); // Sampling flow sensor
      if (initialFlowValue != currentFlowValue)
      {
        pulseCount++; // Increment pulseCount
        initialFlowValue = currentFlowValue; // Set the initial flow value to be the same as the current value.
      }
    }
  }
}

float calculateCalibrationFactor(float knownFlowRate)
{
  // Calculate the expected flow rate using the known speed of sound and tube area
  tubeArea = PI * tubeRadius * tubeRadius; // Calculate the area of the tube
  float expectedFlowRate = tubeArea * speedOfSound;

  // Calculate the calibration factor
  return knownFlowRate / expectedFlowRate;
}

void pulseCounter()
{
  pulseCount++;
}
