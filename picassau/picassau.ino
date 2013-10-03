//////////////////////////////////////////////////////////
// picassau.ino
// 
// Main file for PICASSAU.  Has the higher-level structure for what to do.
//
// Primary author(s): Ben Straub
// Team members: David Toledo, Kayla Frost, Drew Kerr, Peter Gartland
//////////////////////////////////////////////////////////

#include "picassau.h"
//#include <Stepper.h>
#include <Servo.h>

char command = 0;
coord cDest; //destination coordinates
coord cCur; //current coordinates

float brushDist = 0;
float totalDist = 0;
float strokeDist = 0;

//Stepper stepperL(NSTEPS, PIN_STEP_L[0], PIN_STEP_L[1], PIN_STEP_L[2], PIN_STEP_L[3]);  
//Stepper stepperR(NSTEPS, PIN_STEP_R[0], PIN_STEP_R[1], PIN_STEP_R[2], PIN_STEP_R[3]); 

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
  //debug();
}

void loop()
{
  serialReady(); //let the comp know that you're ready
  
  do //get instruction and verify it
  {
    while(!receiveInstruction()) //try to receive the instruction
    { //if failed to receive anything (timed out)
      serialReady(); //resend ready and try again
    }
    if (!parseInstruction()) //try to parse
      serialError(); //if there's an error, let the comp know
  } while (!verifyInstruction()); //try to verify the instruction with the comp
  
  
  //decide how to position the brush:
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
  
  //and actually move
  if ((command == 'M') || (command == 'L'))
    moveToPoint(cDest); //and GO!
    
    
  //miscellaneous other commands
  if (command == 'D')
  {
    brushWiggle = false;
    removeBrush();
  }
  if (command == 'C')
  {
    //do some color changing stuff
  }
}

//I was using this to test stuff
void debug()
{
  Serial.println("asdlfkjhsa;glknsa;lgkasf");
  while(1)
  {
    motorLStep(200);
    motorRStep(200);
    motorLStep(-200);
    motorRStep(-200);
  }
   
}
  

  
  
