const int pressureInput = A0; // Analog input pin for the pressure transducer
const int baudRate = 9600; // Baud rate for serial communication
const int sensorreadDelay = 1000; // Delay between readings in milliseconds

int pressureZero = 0; // Variable to store pressure transducer reading at 0 psi
int pressureMax = 0; // Variable to store pressure transducer reading at 8 bar

void setup() {
  Serial.begin(baudRate); // Initializes serial communication at the set baud rate
  Serial.println("  ");
  Serial.println("Calibration Mode - Open the system to atmospheric pressure");
  Serial.println("When the system is open, press any key in the Serial Monitor to proceed.");
  while (!Serial.available()) {} // Wait for user input
  Serial.read(); // Clear the input buffer
}

void loop() {
  int sensorReading = analogRead(pressureInput); // Read value from input pin

  // Check if the calibration for pressureZero is complete
  if (pressureZero == 0) {
    pressureZero = sensorReading;
    Serial.println("Calibration Complete for pressureZero");
    Serial.println("pressureZero=");
    Serial.println(pressureZero);
    Serial.println("Pressurize the system to 8 bar for pressureMax calibration.");
    Serial.println("When the system is pressurized, press any key in the Serial Monitor to proceed.");
    while (!Serial.available()) {} // Wait for user input
    Serial.read(); // Clear the input buffer
    delay(2000); // Allow time to pressurize the system
  }

  // Check if the calibration for pressureMax is complete
  else if (pressureMax == 0) {
    while (!Serial.available()) {} // Wait for user input
    Serial.read(); // Clear the input buffer
    pressureMax = sensorReading;
    Serial.println("Calibration Complete for pressureMax");
    Serial.println("pressureMax=");
    Serial.println(pressureMax);
    Serial.println("Now you can use the obtained values for pressure calibration in your main code.");
    while (true) {} // Infinite loop to halt the program
  }
}
