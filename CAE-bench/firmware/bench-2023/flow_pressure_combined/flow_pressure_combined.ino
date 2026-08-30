#include "Wire.h" // allows communication over i2c devices
const int pressureInput = A0; // select the analog input pin for the pressure transducer
const int pressureZero = 98; // analog reading of pressure transducer at 0psi
const int pressureMax = 800; // analog reading of pressure transducer at 100psi
const int pressuretransducermaxPSI = 100; // psi value of transducer being used
const int baudRate = 9600; // constant integer to set the baud rate for serial monitor
const int sensorreadDelay = 250; // constant integer to set the sensor read delay in milliseconds

volatile int flow_frequency; // Measures flow sensor pulses
unsigned int l_hour; // Calculated litres/hour
unsigned char flowsensor = 2; // Sensor Input
unsigned long currentTime;
unsigned long cloopTime;

float pressureValue = 0; // variable to store the value coming from the pressure transducer

void flow () // Interrupt function
{
  flow_frequency++;
}

void setup()
{
  pinMode(flowsensor, INPUT);
  digitalWrite(flowsensor, HIGH); // Optional Internal Pull-Up
  Serial.begin(baudRate); // initializes serial communication at set baud rate bits per second
  attachInterrupt(0, flow, RISING); // Setup Interrupt
  sei(); // Enable interrupts
  currentTime = millis();
  cloopTime = currentTime;
}

void loop()
{
  currentTime = millis();
  
  // Every second, calculate and print litres/hour
  if(currentTime >= (cloopTime + 1000))
  {
    cloopTime = currentTime; // Updates cloopTime
    
    // Pulse frequency (Hz) = 7.5Q, Q is flow rate in L/min.
    l_hour = (flow_frequency * 60 / 7.5); // (Pulse frequency x 60 min) / 7.5Q = flowrate in L/hour
    flow_frequency = 0; // Reset Counter
    
    pressureValue = analogRead(pressureInput); // reads value from input pin and assigns to variable
    pressureValue = ((pressureValue-pressureZero)*pressuretransducermaxPSI)/(pressureMax-pressureZero); // conversion equation to convert analog reading to psi
    
    Serial.print("Flow Rate: ");
    Serial.print(l_hour, DEC); // Print litres/hour
    Serial.println(" L/hour");
    
    Serial.print("Pressure: ");
    Serial.print(pressureValue, 1); // prints value from previous line to serial
    Serial.println(" psi");
    
    delay(sensorreadDelay); // delay in milliseconds between read values
  }
}
