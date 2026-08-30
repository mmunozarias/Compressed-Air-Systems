#include <Servo.h>

Servo myServo;  // Create servo object

void setup() {
  myServo.attach(9);  // Attach servo to pin 9
}

void loop() {
  for (int pos = 0; pos <= 180; pos += 1) {  // Sweep servo from 0 to 180 degrees
    myServo.write(pos);
    delay(15);
  }

  for (int pos = 180; pos >= 0; pos -= 1) {  // Sweep servo from 180 to 0 degrees
    myServo.write(pos);
    delay(15);
  }
}
