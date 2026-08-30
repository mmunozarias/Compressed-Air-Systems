# Sensor calibration — MC/DC experimental pneumatic set-up, IEM

**Authors: Jelmer Veenhuizen & Quentin Hopman, 6 November 2023**

Transcribed from `MCDC_Sensor_calibration_procedure (1).pdf`. Figures omitted.

## 1.1 Pressure sensor

The pressure sensor is calibrated against the atmosphere. Thus the measured value
when the sensor is exposed to the atmosphere corresponds to 1 bar. The spec sheets
indicate a 0.5 % error in output, caused by nonlinear, hysteresis and repeatability.
Therefore, it is assumed that the zeroing against the atmosphere provides accurate
results at 8 bar.

### 1.1.1 Procedure

1. Expose the sensor to the atmosphere by decoupling and closing valves.
2. Connect the sensor to the Arduino/breadboard. Connect black to ground, red to 5 V,
   and green to A0 Arduino. Connect the Arduino to a computer and start Arduino IDE.
3. Run the calibration code provided below.
4. Insert calibrated `pressureZero` and `pressureMax` in the experimental setup code.
5. Connect the sensor to the fire extinguisher pressurized at 8 bar. Measure with
   compressor pneumatic pistol pressure dial. Make sure it is a closed environment.
6. Check if the calibration value is correct. Keep in mind that any difference can be
   caused by multiple things, such as the pressure dial, leaks, incorrect calibration
   etc.

Code: `calibration_pressure.ino` —
https://drive.google.com/file/d/1N5TNWYmDKPXWIamPsnneZvXHBETUde2X/view

## 1.2 Flow sensor

This is a difficult sensor to calibrate without a well-known flow. Here we will
approximate the flow using the choking principle. If the pressure ratio between the
tank and the outside is two or greater, it can be assumed the flow is choking on the
small tube. In these cases, the flow rate is equal to the speed of sound
approximately 343 m/s. This can be supported by a 2D model in Comsol.

The airflow is defined by `Q_tube = A v`, where A is the area of the tube,
`A = pi r^2 = pi (6.25e-3)^2 m^2` and `v = 343 m/s`.

### Procedure

1. Close the pneumatic system and load it to 8 bars. Connect the sensor to the Arduino
   and check the pins in the code against reality.
2. Start the code, get ready to act quickly. Open the valve quick, when the flow is
   fully developed start the code and let the pressure run out. Reduce the sampling
   time if the flow does not stay high long enough.
3. Input the calibration factor into the test setup code.

In this code, the `knownFlowRate` variable is set to your actual known flow rate. The
`calculateCalibrationFactor` function uses this known flow rate, along with the tube
area and speed of sound, to determine the correct calibration factor. Adjust the
values of `knownFlowRate`, `tubeRadius`, and `speedOfSound` based on your specific
setup.

**The manufacturer states that the calibration factor for water should be 11.**

Code: `calibration_flow.ino` —
https://drive.google.com/file/d/1NYfv6ezN-nQ1ZO533Tar7QxmUWB7ZQNv/view

## 1.3 Force sensor

For this calibration, you need the provided weights with masses.

1. Securely mount the load cell and make sure it is free from any external loads.
2. Apply load i to the load cell.
3. Read and record the output value for the applied load.
4. Repeat steps 2 and 3 for all loads.
5. Calculate the calibration factor for the load cell by dividing the known loads by
   the corresponding load cell output values.
6. Update the "calibration factor" value in your Arduino code with the calculated
   calibration factor.

Note: Make sure to replace the placeholder comments with actual known loads and
corresponding load cell outputs. Additionally, ensure that you're using units
consistent with your application (e.g., grams, kilograms, pounds).
**Consider low loads corresponding with the engine torques to enhance accuracy.**

Code: `calibration_force.ino` —
https://drive.google.com/file/d/1Nakx0HwFnjOQpSjgHod1vDwGDWDcIyK0/view
