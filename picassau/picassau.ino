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


void setup()
{
  serialSetup();
  plottingSetup();
}

void loop()
{
  serialReady();
  do
  {
    receiveInstruction();
    if (!parseInstruction())
      serialError();
  } while (!verifyInstruction());
  
  if (command == 'M')
  {
    removeBrush();
    totalDist += getDistFromPoint(cCur, cDest);
  }
  else if (command == 'L')
  {
    applyBrush();
    float tempDist = getDistFromPoint(cCur, cDest);
    totalDist += tempDist;
    brushDist += tempDist;
    strokeDist += tempDist;
    //if you will have painted too much, AND you've gone far enough
    if ((strokeDist > PAINTING_DISTANCE) && (strokeDist - tempDist > PAINTING_DISTANCE / 16))
      dipBrush();
  }
    
  moveToPoint(cDest);
}


  
  
