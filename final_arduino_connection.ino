// Define the pin numbers for the LED and motion sensor
const int ledPin = 4;       // Change this to the pin number where your LED is connected
const int motionSensorPin = 3; // Change this to the pin number where your motion sensor output is connected
int incomingByte;
void setup() {
  pinMode(ledPin, OUTPUT);         // Set the LED pin as an output
  pinMode(motionSensorPin, INPUT); // Set the motion sensor pin as an input
  Serial.begin(9600);              // Initialize serial communication for debugging
}
void loop() {
  int motionDetected = digitalRead(motionSensorPin); // Read the state of the motion sensor
  if (motionDetected == HIGH) {
    // Motion detected, turn on the LED
    digitalWrite(ledPin, HIGH);
    delay(1000);
    Serial.println("Motion detected");
  } else {
    // No motion detected, turn off the LED
    // digitalWrite(ledPin, LOW);
    Serial.println("No motion detected");
  }
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 'L') {
      digitalWrite(ledPin, LOW);
    }
  }
  delay(3000); // Delay to avoid reading the motion sensor too frequently
}
