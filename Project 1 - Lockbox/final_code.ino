#include <Keypad.h>
#include <Servo.h>
Servo myservo;
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
LiquidCrystal_I2C lcd(0x27, 16, 2); // looks for address, columns, and rows

#define Pass_Length 7 // enough room for six chars + null char

int pos = 0;  // variable to store servo position

char Data[Pass_Length]; // 6 is the number of chars it can hold + the null char = 7
char Master[Pass_Length] = "123ABC";
byte data_count = 0;
char customKey;
bool door = true;


const byte ROWS = 4; // num of rows on the matrix keypad
const byte COLS = 4; // num of columns on the matrix keypad

char keys[ROWS][COLS] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte rowPins[ROWS] = {9, 8, 7, 6}; //connect to the row pinouts of the keypad
byte colPins[COLS] = {5, 4, 3, 2}; //connect to the column pinouts of the keypad

Keypad keypad = Keypad( makeKeymap(keys), rowPins, colPins, ROWS, COLS );

void setup() {  // splash screen
  
  myservo.attach(12); // pin 12 is dedicated to the servo motor
  ServoClose(); // servo motor will go into it's locked state upon startup
  lcd.init();
  lcd.backlight();
  lcd.print("Woah!!!");
  lcd.setCursor(0, 1);
  lcd.print("My lockbox!");
  delay(3000);
  lcd.clear();
}

void loop() {
  
  if (door == 0) {
    customKey = keypad.getKey();  // makes sure a key is actually pressed

    if (customKey == '#') { // pound sign will lock the door, this goes into effect after the user successfully guesses the passcode 
      lcd.clear();
      ServoClose();
      lcd.print("Closing...");
      delay(2000);
      door = 1;
    }
  }

  else Open();
}

void clearData() {
  while (data_count != 0) {
    Data[data_count--] = 0; // clears the array for new data
  }
  return;
}

void ServoOpen() {
  for (pos = 100; pos >= 0; pos -= 5) {
    myservo.write(pos); // tells the servo to go to the position in variable 'pos'
    delay(15);  // waits 15 milliseconds for the servo to reach said position
  }
}

void ServoClose() {
  for (pos = 0; pos <= 100; pos += 5) { // ditto but this tells the servo to go back to the initial lock position
    myservo.write(pos);
    delay(15);
  }
}

void Open() {
  lcd.setCursor(0, 0);
  lcd.print("Enter passcode:");

  customKey = keypad.getKey();  // makes sure a key is actually pressed

  // the next six if statements make sure the key that is pressed 
  // matches with any of the six chars from the Master array
  // yup, hardcoded - I wanted to implement this better but didn't have a clear way to do so
   
  if (customKey == Master[0]) {
    Data[data_count] = customKey; // store char into the data array
    lcd.setCursor(data_count, 1); // moves the cursor over to show each new char
    lcd.print(Data[data_count]);  // print char at said cursor position
    data_count++; // increments data array by 1 to store a new char/keeps track of the num of chars entered
  }

  if (customKey == Master[1]) {
    Data[data_count] = customKey; 
    lcd.setCursor(data_count, 1); 
    lcd.print(Data[data_count]);  
    data_count++; 
  }

  if (customKey == Master[2]) {
    Data[data_count] = customKey; 
    lcd.setCursor(data_count, 1); 
    lcd.print(Data[data_count]);  
    data_count++; 
  }

  if (customKey == Master[3]) {
    Data[data_count] = customKey; 
    lcd.setCursor(data_count, 1); 
    lcd.print(Data[data_count]);  
    data_count++; 
  }

  if (customKey == Master[4]) {
    Data[data_count] = customKey; 
    lcd.setCursor(data_count, 1); 
    lcd.print(Data[data_count]);  
    data_count++; 
  }

  if (customKey == Master[5]) {
    Data[data_count] = customKey; 
    lcd.setCursor(data_count, 1); 
    lcd.print(Data[data_count]); 
    data_count++; 
  }

  // the rest of the keys pressed will report to the lcd
  // that the user inputted an incorrect character
  // yes unfortunately this is hardcoded

  if (customKey == '4') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();  // this function clears the Data array and resets the data_count to zero
  }

  if (customKey == '5') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '6') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '7') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '8') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '9') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '0') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '*') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == '#') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (customKey == 'D') {
    lcd.clear();
    lcd.print("Wrong char.");
    delay(1000);
    door = 1;
    clearData();
  }

  if (data_count == Pass_Length - 1) {  // if the array index is equal to the number of expected chars, compare that data to master
    Compare();
  }
}

void Compare() {
  if (!strcmp(Data, Master)) {  // checks if the string of characters in the Data array matches the Master array
    lcd.clear();
    ServoOpen();
    lcd.print("Access Granted!");
    door = 0;
  }

  else
  {
    lcd.clear();
    lcd.print("Access Denied.");
    delay(1000);
    door = 1;
  }
  clearData();
}
