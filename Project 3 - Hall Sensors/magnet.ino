int sensor = 0;
int sensor2 = 0;
int sensor3 = 0;
int sensor4 = 0;
int sensor5 = 0;

#define pinHall 3  // Pin for the Hall sensor
#define pinHall2 5
#define pinHall3 7
#define pinHall4 11
#define pinHall5 A5





void setup()
{
  Serial.begin(9600);
  pinMode(pinHall, INPUT);  // sets the digital pin as input
  pinMode(pinHall2, INPUT);
  pinMode(pinHall3, INPUT);
  pinMode(pinHall4, INPUT);
  pinMode(pinHall5, INPUT);


}

void loop()
{
  sensor = digitalRead(pinHall); // If a magnet is near the Hall sensor
  sensor2 = digitalRead(pinHall2);
  sensor3 = digitalRead(pinHall3);
  sensor4 = digitalRead(pinHall4);
  sensor5 = digitalRead(pinHall5);
  Serial.println(sensor);
  Serial.println(sensor2);
  Serial.println(sensor3);
  Serial.println(sensor4);
  Serial.println(sensor5);
  delay(500);

}
