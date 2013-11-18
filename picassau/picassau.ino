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
coord cPrev; //previous destination coordinates

int motorDelay = MOVE_MOTOR_DELAY;

float brushDist = 0;
float totalDist = 0;
float strokeDist = 0;

//Stepper stepperL(NSTEPS, PIN_STEP_L[0], PIN_STEP_L[1], PIN_STEP_L[2], PIN_STEP_L[3]);  
//Stepper stepperR(NSTEPS, PIN_STEP_R[0], PIN_STEP_R[1], PIN_STEP_R[2], PIN_STEP_R[3]); 

Servo armServo;
Servo brushServo;
Servo rotateServo;

int brushSetting; //the angle in deg that the brush is applied (like dipped, applied, removed)
int brushRotation = 0; //what angle in deg that the brush is rotated
int brushOffset = 0; //used in wiggling
boolean brushWiggle = false; //set true to wiggle
int wiggleDist = 5; //what range to wiggle brush; brush wiggles in arc of +/- [wiggleDist] degrees

int currentColor = 0;
int newColor = 0;

void setup()
{
  serialSetup();  //set up the serial stuff
  
  //controlGUI();
  
  brushSetup(); //set up the brushes
  plottingSetup(); //set up the stepper motors
//  washBrush();
  dipBrush();
}

void loop()
{
  serialReady(); //let the comp know that you're ready
  
  cPrev = cDest;
  
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
    motorDelay = MOVE_MOTOR_DELAY;
  }
  else if (command == 'L') //or is it a line (move with painting)?
  {
    float tempDist = getDistFromPoint(cCur, cDest);
    totalDist += tempDist; //add to total distance
    brushDist += tempDist; // and total painted distance
    strokeDist += tempDist; // and to the current stroke distance
    //if you will have painted too much, AND you've gone far enough
    if ((strokeDist > PAINTING_DISTANCE) && (strokeDist - tempDist > PAINTING_DISTANCE / 16))
    {
      motorDelay = MOVE_MOTOR_DELAY;
      dipBrush();
      motorDelay = PAINT_MOTOR_DELAY;
      strokeDist = 0;
    }
    //now apply the brush to get ready for painting
    applyBrushWithRotate(getServoAngle(cPrev, cDest));
    
    
    brushWiggle = true;
    wiggleDist = PAINT_WIGGLE_DIST;
    motorDelay = PAINT_MOTOR_DELAY;
  }
  
  //and actually move
  if ((command == 'M') || (command == 'L'))
    moveToPoint(cDest); //and GO!
    
    
  //miscellaneous other commands
  if (command == 'D') //d for done
  {
    brushWiggle = false;
    removeBrush();
    delay(500);
    washBrush();
  }
  if (command == 'C') //c for color change
  {
    if (newColor != currentColor)
    {
      currentColor = newColor;
      washBrushWithDip();
      strokeDist = PAINTING_DISTANCE / 2 ;
    }
    //otherwise it doesn't matter
  }
}

//I was using this to test stuff
void debug()
{
  dipBrush();
}
  

  
  
