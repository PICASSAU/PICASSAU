//////////////////////////////////////////////////////////
// plotting.ino
// 
// Made to control the stepper motors and movement math for the PICASSAU
//   project.
//
// Primary author(s): Ben Straub
// Team members: David Toledo, Kayla Frost, Drew Kerr, Peter Gartland
//////////////////////////////////////////////////////////

float lengthL, lengthR; //length from motor to platform 

//////////////////////////////////////////////////////////
////plottingSetup
///sets up the stepper motors and plotting functions
void plottingSetup()
{
  lengthL = INITIAL_LENGTH_L;
  lengthR = INITIAL_LENGTH_R;
  cCur = getCoord(lengthL, lengthR);
  stepperL.step(1);
  stepperR.step(1);
  delay(MOTOR_DELAY);
  stepperL.step(-1);
  stepperR.step(-1);
  
}

//////////////////////////////////////////////////////////
////moveToPoint
///moves from the current coordinates to destination cD.
void moveToPoint( coord cD )
{
  long t = millis(); //used to time motor delays / speed
  coord cStart = cCur; //start point
  float curDist;
  signed char stateL; //will be 0, 1, or -1
  signed char stateR; //ditto
  
  float tempDL; //temporary holding variable for the distance from line for a left motor move
  float tempDR; //ditto but for right motor move
  coord cTempL; //temp variable for holding the coordinates of a left motor move
  coord cTempR; //ditto for right
  
  while(1) //loop infinitely (until arriving at cD 
  {
    curDist = getDistFromPoint( cCur, cD ); //how far are we now from our destination?
    stateL = 0; // 0 is none, 1 is move +, -1 is move -
    stateR = 0; //ditto
    
    
    cTempL = getCoord( lengthL+STEP_DIST, lengthR ); //what if we move left motor in + direction (let line out from spool)?
    if (getDistFromPoint( cTempL, cD ) < curDist) //does it get us closer?
    {
      tempDL = getDistFromLine( cStart, cD, cTempL ); //how close to the line are we?
      stateL = 1; //means that moving the left motor in + direction is better than -
    } else
    {
      cTempL = getCoord( lengthL-STEP_DIST, lengthR ); //try - direction
      if (getDistFromPoint( cTempL, cD ) < curDist) //does it get us closer?
      {
        tempDL = getDistFromLine( cStart, cD, cTempL ); //how close to the line are we?
        stateL = -1; //means - direction is better for left motor than + direction
      }
    }
    
    //this section does the same thing with the right motor that the above section does with the left motor
    cTempR = getCoord( lengthL, lengthR+STEP_DIST );
    if (getDistFromPoint( cTempR, cD ) < curDist)
    {
      tempDR = getDistFromLine( cStart, cD, cTempR );
      stateR = 1;
    } else
    {
      cTempR = getCoord( lengthL, lengthR-STEP_DIST );
      if (getDistFromPoint( cTempR, cD ) < curDist)
      {
        tempDR = getDistFromLine( cStart, cD, cTempR );
        stateR = -1;
      }
    }
    
    //ok, now let's see which move is better
    if ((stateR != 0) && (stateL != 0)) //means that moving either motor will get us closer to the destination
    {
      if (tempDL < tempDR) //if left move gets closer than right move
      {
        stepperL.step( stateL ); //move +-1
        lengthL += stateL*STEP_DIST; // change by +- STEP DIST
        cCur = cTempL; //update the current coordinates
        
      } else if (tempDR < tempDL)//right move gets closer than left move
      {
        stepperR.step( stateR ); //move +-1
        lengthR += stateR*STEP_DIST; // change by +- STEP DIST
        cCur = cTempR; //update the current coordinates
        
      } else  //otherwise they're exactly the same? (unlikely)
      {
        stepperR.step( stateR ); //move both
        stepperL.step( stateL );
        lengthL += stateL*STEP_DIST;
        lengthR += stateR*STEP_DIST;
        cCur = getCoord( lengthL, lengthR);
      }
        
    } else if (stateR != 0) //only right move gets closer
    {
      stepperR.step( stateR ); //move +-1
      lengthR += stateR*STEP_DIST;
      cCur = cTempR;
      
    } else if (stateL != 0) //only left move gets closer
    {
      stepperL.step( stateL ); //move +-1
      lengthL += stateL*STEP_DIST;
      cCur = cTempL;
      
    } else //no moves get closer
    {     //which means we're done!
      break; //leave the loop
    } 
    
    while(millis()-t < MOTOR_DELAY) {} //wait for motor delay
    t = millis();
    
  } //end while(1) loop
}

//////////////////////////////////////////////////////////
////getCoord
///gets the coordinate that is a distance d1 from motor 1/L (0,0) and
/// d2 from motor 2/R (MOTOR_DIST,0)
coord getCoord( float d1, float d2 )
{
  coord c;
  c.x = (d1*d1 - d2*d2 + MOTOR_DIST2) / (DBL_MOTOR_DIST);
  c.y = sqrt(d1*d1 - c.x*c.x);
  return c;
}

//////////////////////////////////////////////////////////
////getDistFromLine
///calculates the distance from point to the line between line1 and line2
float getDistFromLine( coord line1, coord line2, coord point)
{
  float num = ((line2.x-line1.x)*(line1.y-point.y))-((line1.x-point.x)*(line2.y-line1.y));
  num = abs(num);
  float den = getDistFromPoint(line1,line2);
  return num/den;
}

//////////////////////////////////////////////////////////
////getDistFromPoint
///calculates the distance between points p1 and p2
float getDistFromPoint( coord p1, coord p2)
{
  float dx = p1.x - p2.x;
  float dy = p1.y - p2.y;
  return sqrt(dx*dx + dy*dy);
}
