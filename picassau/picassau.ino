#include "picassau.h"
#include <Stepper.h>

char command = 0;
coord cDest; //destination coordinates
coord cCur; //current coordinates

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
  {//don't use brush
  }
  else if (command == 'L')
  {//use brush
  }
    
  moveToPoint(cDest);
}


  
  
