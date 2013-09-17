//////////////////////////////////////////////////////////
// picassau.ino
// 
// Main file for PICASSAU.  Has the higher-level structure for what to do.
//
// Primary author(s): Ben Straub
// Team members: David Toledo, Kayla Frost, Drew Kerr, Peter Gartland
//////////////////////////////////////////////////////////

#include "picassau.h"
#include <Stepper.h>
#include <Servo.h>

char command = 0;
coord cDest; //destination coordinates
coord cCur; //current coordinates

float brushDist = 0;
float totalDist = 0;
float strokeDist = 0;

Stepper stepperL(NSTEPS, PIN_STEP_L[0], PIN_STEP_L[1], PIN_STEP_L[2], PIN_STEP_L[3]);  
Stepper stepperR(NSTEPS, PIN_STEP_R[0], PIN_STEP_R[1], PIN_STEP_R[2], PIN_STEP_R[3]); 

Servo brushServo;
Servo rotateServo;

int brushSetting;
int brushOffset = 0;
boolean brushWiggle = false;


void setup()
{
  serialSetup();  //set up the serial stuff
  plottingSetup(); //set up the stepper motors
  brushSetup(); //set up the brushes
  debug();
}

void loop()
{
  serialReady(); //let the comp know that you're ready
  do
  {
    receiveInstruction(); //try to receive the instruction
    if (!parseInstruction()) //try to parse
      serialError(); //if there's an error, let the comp know
  } while (!verifyInstruction()); //try to verify the instruction with the comp
  
  if (command == 'M') //is it a move (no painting)?
  {
    brushWiggle = false;
    removeBrush();
    totalDist += getDistFromPoint(cCur, cDest); //add this distance to total tally
  }
  else if (command == 'L') //or is it a line (move with painting)?
  {
    applyBrush();
    brushWiggle = true;
    float tempDist = getDistFromPoint(cCur, cDest);
    totalDist += tempDist; //add to total distance
    brushDist += tempDist; // and total painted distance
    strokeDist += tempDist; // and to the current stroke distance
    //if you will have painted too much, AND you've gone far enough
    if ((strokeDist > PAINTING_DISTANCE) && (strokeDist - tempDist > PAINTING_DISTANCE / 16))
      ;//dipBrush();
  }
    
  moveToPoint(cDest); //and GO!
}

//I was using this to test stuff
void debug()
{
  Serial.println("DEBUGGING...");
//  while(1)
//  {
//    int reading = analogRead(PIN_IR_SENSOR);
//    Serial.print(reading);
//    double distance = double(reading) + 61.8322; //intermediate step
//    distance = pow(distance,-1.5281); //another intermediate step
//    distance = 141186.4*distance/2.54; //ok, now it's really the distance
//    Serial.print(" :\t");
//    Serial.println(distance);
//    delay(1000);
//  }
  

//  if (positionCalibration())
//    Serial.println("success!");
//  else
//    Serial.println("FAIL.");
//    
//  Serial.print("absolute coord: (");
//  Serial.print(cCur.x);
//  Serial.print(", ");
//  Serial.print(cCur.y);
//  Serial.print(")\ncanvas coord: (");
//  Serial.print(cCur.x-COORD_OFFSET_X);
//  Serial.print(", ");
//  Serial.println(cCur.y-COORD_OFFSET_Y);
  
  dipBrush();
  
  while(1);
}
  

  
  
