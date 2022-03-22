// Marshall Sullivan
// Assignment 3
// ENGN4080 - Robotics & Automation II

#include <Braccio.h>
#include <Servo.h>

int sensor = 0;
int sensor2 = 0;
int sensor3 = 0;
int sensor4 = 0;
int sensor5 = 0;

// PINS FOR HALL SENSORS
#define pinHall 3  
#define pinHall2 5
#define pinHall3 7
#define pinHall4 11
#define pinHall5 A5


Servo base;
Servo shoulder;
Servo elbow;
Servo wrist_rot;
Servo wrist_ver;
Servo gripper;

const byte numChars = 32;
char receivedChars[numChars];
char tempChars[numChars];
char messageFromPC[numChars] = {0};

int m1 = 0;
int m2 = 0;
int m3 = 0;
int m4 = 0;
int m5 = 0;
int m6 = 0;

boolean newData = false;

//============

void setup() {
    Serial.begin(115200);
    pinMode(13, OUTPUT);
    pinMode(pinHall, INPUT);  // sets the digital pin as input
    pinMode(pinHall2, INPUT);
    pinMode(pinHall3, INPUT);
    pinMode(pinHall4, INPUT);
    pinMode(pinHall5, INPUT);
    Braccio.begin();
    Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);

}

//============

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        showParsedData();
        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");    // get the first part - the string
    strcpy(messageFromPC, strtokIndx);    // copy it to messageFromPC

    strtokIndx = strtok(NULL, ",");
    m1 = atoi(strtokIndx);
    
    strtokIndx = strtok(NULL, ",");
    m2 = atoi(strtokIndx);     

    strtokIndx = strtok(NULL, ",");
    m3 = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    m4 = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    m5 = atoi(strtokIndx);

    strtokIndx = strtok(NULL, ",");
    m6 = atoi(strtokIndx);

}

//============

void showParsedData() {

    if (strcmp("i", messageFromPC) == 0) {
      Serial.println("Ready!");
      Serial.println(m1);
      Serial.println(m2);
      Serial.println(m3);
      Serial.println(m4);
      Serial.println(m5);
      Serial.println(m6);
    }

    if (strcmp("M_O1", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 33, 85, 98, 82, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 33, 44, 0, 45, 50, 73);
      delay(1000);
      Braccio.ServoMovement(20, 33, 44, 0, 45, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 0, 50, 12, 31, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 0, 50, 12, 31, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
     }
   
    if (strcmp("M_O2", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 145, 85, 98, 82, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 145, 55, 12, 22, 40, 73);
      delay(1000);
      Braccio.ServoMovement(20, 145, 55, 12, 22, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 180, 55, 12, 22, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 180, 55, 12, 22, 40, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
   }

    if (strcmp("M_O3", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 81, 42, 0, 46, 55, 73);
      delay(1000);
      Braccio.ServoMovement(20, 81, 42, 0, 46, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 81, 70, 0, 46, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 112, 36, 0, 86, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 112, 18, 0, 86, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 112, 18, 0, 86, 55, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
    }

    if (strcmp("P_O1", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 0, 85, 98, 82, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 0, 50, 12, 31, 50, 73);
      delay(1000);
      Braccio.ServoMovement(20, 0, 50, 12, 31, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 40, 44, 0, 45, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 40, 44, 0, 45, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
    }

    if (strcmp("P_O2", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 180, 85, 98, 82, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 180, 55, 12, 22, 40, 73);
      delay(1000);
      Braccio.ServoMovement(20, 180, 55, 12, 22, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 140, 55, 12, 22, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 140, 55, 12, 22, 40, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
    }

    if (strcmp("P_O3", messageFromPC) == 0) {
      Braccio.ServoMovement(20, 112, 85, 98, 82, 50, 73);
      delay(500);
      Braccio.ServoMovement(20, 112, 18, 0, 86, 55, 73);
      delay(1000);
      Braccio.ServoMovement(20, 112, 18, 0, 86, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 112, 36, 0, 86, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 81, 70, 0, 46, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 81, 42, 0, 46, 85, 73);
      delay(500);
      Braccio.ServoMovement(20, 81, 42, 0, 46, 55, 73);
      delay(500);
      Braccio.ServoMovement(20, 90, 85, 98, 82, 90, 73);
    }
}
