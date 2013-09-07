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

Stepper stepperL(NSTEPS, 6,7,8,9);  
Stepper stepperR(NSTEPS, 10,11,12,13); 

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
  applyBrush();
  rotateBrush(0);
  while(1)
  {
    //BRUSH POSITIONS
//    Serial.println("applying");
//    applyBrush();
//    delay(2000);
//    Serial.println("removing");
//    removeBrush();
//    delay(2000);
//    //dipBrush();
//    Serial.println("dipping");
//    brushServo.write(BPOS_DIP);
//    delay(2000);

    //BRUSH ROTATION
//    for(int i = 0; i <= 150; i++)
//    {
//      rotateBrush(i);
//      delay(10);
//    }
//    delay(500);
//    for(int i = 150; i >= 0; i--)
//    {
//      rotateBrush(i);
//      delay(10);
//    }

//    for (int i = -5; i <= 5; i++)
//    {
//      brushServo.write(BPOS_APPLY + i);
//      delay(10);
//    }
//    for (int i = 5; i >= -5; i--)
//    {
//      brushServo.write(BPOS_APPLY + i);
//      delay(10);
//    }

    brushWiggle = true;
    delay(5000);
    brushWiggle = false;
    delay(2000);

  }
}
  

  
  
