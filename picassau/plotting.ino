float lengthL, lengthR; //length from motor to platform 

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

void moveToPoint( coord cD )
{
  long t = millis();
  coord cStart = cCur;
  float curDist;
  signed char stateL;
  signed char stateR;
  
  float tempDL;
  float tempDR;
  coord cTempL;
  coord cTempR;
  
//  Serial.print("Start (");
//  Serial.print(cStart.x);
//  Serial.print(",");
//  Serial.print(cStart.y);
//  Serial.flush();
//  Serial.print("End (");
//  Serial.print(cD.x);
//  Serial.print(",");
//  Serial.print(cD.y);
//  Serial.flush();
  
  while(1)
  {
    curDist = getDistFromPoint( cCur, cD );
    stateL = 0; // 0 is none, 1 is move +, -1 is move -
    stateR = 0; //ditto
    cTempL = getCoord( lengthL+STEP_DIST, lengthR );
    if (getDistFromPoint( cTempL, cD ) < curDist)
    {
      tempDL = getDistFromLine( cStart, cD, cTempL );
      stateL = 1;
    } else
    {
      cTempL = getCoord( lengthL-STEP_DIST, lengthR );
      if (getDistFromPoint( cTempL, cD ) < curDist)
      {
        tempDL = getDistFromLine( cStart, cD, cTempL );
        stateL = -1;
      }
    }
    
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
    
    if ((stateR != 0) && (stateL != 0))
    {
      if (tempDL < tempDR) //left move gets closer than right move
      {
        stepperL.step( stateL ); //move +-1
        lengthL += stateL*STEP_DIST;
        cCur = cTempL;
        
        //Serial.print("L");
        //Serial.println(stateL);
      } else if (tempDR < tempDL)//right move gets closer than left move
      {
        stepperR.step( stateR ); //move +-1
        lengthR += stateR*STEP_DIST;
        cCur = cTempR;
        
        //Serial.print("R");
        //Serial.println(stateR);
      } else
      {
        stepperR.step( stateR );
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
      
      //Serial.print("R");
      //Serial.println(stateR);
    } else if (stateL != 0) //only left move gets closer
    {
      stepperL.step( stateL ); //move +-1
      lengthL += stateL*STEP_DIST;
      cCur = cTempL;
      
      //Serial.print("L");
      //Serial.println(stateL);
    } else //no moves get closer
    {
      break; //leave the loop
    }
    
    
    
    while(millis()-t < MOTOR_DELAY) {} //wait
    t = millis();
    
  } //end while(1) loop
    
    
}

coord getCoord( float d1, float d2 )
{
  coord c;
  c.x = (d1*d1 - d2*d2 + MOTOR_DIST2) / (DBL_MOTOR_DIST);
  c.y = sqrt(d1*d1 - c.x*c.x);
  return c;
}

float getDistFromLine( coord line1, coord line2, coord point)
{
  float a = line1.y-line2.y;
  float b = line2.x-line1.x;
  float c = -b*line1.y + a*line1.x;
  float num = a*point.x + b*point.y + c;
  float d = num/(sqrt(a*a + b*b));
  if (d>=0)
    return d;
  else
    return -d;
}

float getDistFromPoint( coord p1, coord p2)
{
  float dx = p1.x - p2.x;
  float dy = p1.y - p2.y;
  return sqrt(dx*dx + dy*dy);
}
