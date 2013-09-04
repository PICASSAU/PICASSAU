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
  serialSetup();
  plottingSetup();
  brushSetup();
  
  //debug();
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
    brushWiggle = false;
    removeBrush();
    totalDist += getDistFromPoint(cCur, cDest);
  }
  else if (command == 'L')
  {
    applyBrush();
    brushWiggle = true;
    float tempDist = getDistFromPoint(cCur, cDest);
    totalDist += tempDist;
    brushDist += tempDist;
    strokeDist += tempDist;
    //if you will have painted too much, AND you've gone far enough
    if ((strokeDist > PAINTING_DISTANCE) && (strokeDist - tempDist > PAINTING_DISTANCE / 16))
      ;//dipBrush();
  }
    
  moveToPoint(cDest);
}

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
  

  
  
