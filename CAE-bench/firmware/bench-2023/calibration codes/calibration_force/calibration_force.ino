#include "HX711.h"

#define DOUT 12
#define CLK 13
HX711 scale;

// Define the known loads and corresponding load cell output values
const float knownLoads[] = {0.1, 0.2, 0.3 /* Add your known loads in increasing order */};
const long loadCellOutputs[] = { /* Add corresponding load cell outputs for each known load */};

const int numLoads = sizeof(knownLoads) / sizeof(knownLoads[0]);

void setup() {
  Serial.begin(9600);
  scale.begin(DOUT, CLK);
  scale.set_scale();
  scale.tare();

  Serial.println("Load Cell Calibration");
  Serial.println("Follow the steps provided in the code comments.");

  // Wait for user input to start calibration
  Serial.println("Press any key in the Serial Monitor to start calibration.");
  while (!Serial.available()) {}
  Serial.read(); // Clear the input buffer

  performCalibration();
}

void loop() {
  // Your main program loop (if needed)
}

void performCalibration() {
  Serial.println("Calibration Procedure:");
  Serial.println("1. Securely mount the load cell and make sure it is free from any external loads.");
  Serial.println("2. Apply loads in increasing order and record the output values.");

  float calibrationFactors[numLoads];

  for (int i = 0; i < numLoads; ++i) {
    Serial.print("Apply load ");
    Serial.print(knownLoads[i]);
    Serial.println(" (in units of your choice) to the load cell.");

    // Wait for user input to proceed with the next step
    Serial.println("Press any key in the Serial Monitor to record the output value.");
    while (!Serial.available()) {}
    Serial.read(); // Clear the input buffer

    // Read and record the output value for the applied load
    long loadCellOutput = scale.read();

    // Calculate the calibration factor for the load cell
    calibrationFactors[i] = knownLoads[i] / loadCellOutput;

    Serial.print("Recorded Load Cell Output: ");
    Serial.println(loadCellOutput);
    Serial.println();
  }

  // Calculate the average calibration factor
  float totalCalibrationFactor = 0.0;
  for (int i = 0; i < numLoads; ++i) {
    totalCalibrationFactor += calibrationFactors[i];
  }
  float averageCalibrationFactor = totalCalibrationFactor / numLoads;

  Serial.println("Calibration Complete.");
  Serial.print("Average Calibration Factor: ");
  Serial.println(averageCalibrationFactor);
  Serial.println("Update the \"calibration_factor\" value in your Arduino code with the calculated calibration factor.");
}
