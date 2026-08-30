#include "HX711.h"

// Define the pins for the HX711 interface
const int HX711_DOUT_PIN = A0; // Replace with your DT pin
const int HX711_SCK_PIN = A1;  // Replace with your SCK pin

HX711 scale;

void setup() {
  // Initialize the serial communication
  Serial.begin(9600);

  // Initialize the HX711 load cell
  scale.begin(HX711_DOUT_PIN, HX711_SCK_PIN);
}

void loop() {
  // Check if the scale is ready
  if (scale.is_ready()) {
    // Read the weight from the scale
    float weight = scale.get_units(10); // 10 readings for better stability

    // Print the weight to the Serial Monitor
    Serial.print("Weight: ");
    Serial.print(weight);
    Serial.println(" grams");

    // You can change the units to suit your application (e.g., kilograms, ounces, etc.)
    // See the HX711 library documentation for details.

    // Add a delay to prevent rapid updates
    delay(1000); // Adjust the delay as needed
  }
  else {
    Serial.println("Error: Unable to detect the HX711. Please check your connections.");
    delay(1000);
  }
}
