#include <Servo.h>

const int TRIGGER_PIN = 2;
const int ECHO_PIN = 3;
const int SERVO_PIN = 9;

const int STARTING_ANGLE = 90;
const int MINIMUM_ANGLE = 6;
const int MAXIMUM_ANGLE = 175;
const int ROTATION_SPEED = 1;

Servo myservo;

void setup() {
  // put your setup code here, to run once:
  pinMode(TRIGGER_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  myservo.attach(SERVO_PIN);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  static int MOTOR_ANGLE = STARTING_ANGLE;
  static int MOTOR_ROTATE_AMOUNT = ROTATION_SPEED;

  myservo.write(MOTOR_ANGLE);
  delay(10);
  SerialOutput(MOTOR_ANGLE, CalculateDistance());

  MOTOR_ANGLE += MOTOR_ROTATE_AMOUNT;
  if (MOTOR_ANGLE <= MINIMUM_ANGLE || MOTOR_ANGLE >= MAXIMUM_ANGLE) {
    MOTOR_ROTATE_AMOUNT = -MOTOR_ROTATE_AMOUNT;
  }
}

int CalculateDistance(void) {
  
  digitalWrite(TRIGGER_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIGGER_PIN, LOW);

  long duration = pulseIn(ECHO_PIN, HIGH);
  float distance = duration * 0.017F;
  return int(distance);
}

void SerialOutput(const int angle, const int distance) {
  String angleString = String(angle);
  String distanceString = String(distance);
  Serial.println(angleString + "," + distanceString);
}
