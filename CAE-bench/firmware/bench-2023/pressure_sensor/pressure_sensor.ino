const int pressureInput = A0; // Select the analog input pin for the pressure transducer
const int pressureZero = 98; // Analog reading of pressure transducer at 0psi
const int pressureMax = 800; // Analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 100; // PSI value of the transducer being used
const int baudRate = 9600; // Constant integer to set the baud rate for serial monitor
const int sensorreadDelay = 250; // Constant integer to set the sensor read delay in milliseconds

float pressureValue = 0; // Variable to store the value coming from the pressure transducer

void setup() {
  Serial.begin(baudRate); // Initializes serial communication at the set baud rate
}

void loop() {
  pressureValue = analogRead(pressureInput); // Reads value from input pin and assigns it to the variable
  pressureValue = ((pressureValue - pressureZero) * pressuretransducermaxPSI) / (pressureMax - pressureZero); // Conversion equation to convert analog reading to psi
  Serial.print(pressureValue, 1); // Prints value to serial monitor with 1 decimal place
  Serial.println(" psi"); // Prints label to serial monitor
  delay(sensorreadDelay); // Delay in milliseconds between reading values
  Serial.println(pressureValue);
}
