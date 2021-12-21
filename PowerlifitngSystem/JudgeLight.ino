/*
  Button

  Turns on and off a light emitting diode(LED) connected to digital pin 13,
  when pressing a pushbutton attached to pin 2.

  The circuit:
  - LED attached from pin 13 to ground
  - pushbutton attached to pin 2 from +5V
  - 10K resistor attached to pin 2 from ground

  - Note: on most Arduinos there is already an LED on the board
    attached to pin 13.

  created 2005
  by DojoDave <http://www.0j0.org>
  modified 30 Aug 2011
  by Tom Igoe

  This example code is in the public domain.

  http://www.arduino.cc/en/Tutorial/Button
*/

// constants won't change. They're used here to set pin numbers:
const int buttonPinWhite = 8;
const int buttonPinRed = 12;
const int buttonPinOff = 13;
const int redPin = 7;
const int greenPin = 4;
const int bluePin = 2;


// variables will change:
int buttonStateWhite = 0;         // variable for reading the pushbutton status
int buttonStateRed = 0;
int buttonStateOff = 0;


void setup() {
  // initialize the LED pin as an output:
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
  // initialize the pushbutton pin as an input:
  pinMode(buttonPinWhite, INPUT);
  pinMode(buttonPinRed, INPUT);
  pinMode(buttonPinOff, INPUT);
  
}

void loop() {
  // read the state of the pushbutton value:
  buttonStateWhite = digitalRead(buttonPinWhite);
  buttonStateRed = digitalRead(buttonPinRed);
  buttonStateOff = digitalRead(buttonPinOff);

  // check if the pushbutton is pressed. If it is, the buttonState is HIGH:
  if (buttonStateWhite == HIGH) {
    // turn LED on white:
    RGB_color(255, 255, 255);
  } else if (buttonStateRed == HIGH) {
    // turn LED on red:
    RGB_color(255, 0, 0);
  }
  else if (buttonStateOff == HIGH) {
    RGB_color(0, 0, 0);
  }
}

void RGB_color(int red, int green, int blue)
{
  analogWrite(redPin, red);
  analogWrite(greenPin, green);
  analogWrite(bluePin, blue);
}
