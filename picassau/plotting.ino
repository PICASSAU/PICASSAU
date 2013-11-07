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
//  lengthL = INITIAL_LENGTH_L;
//  lengthR = INITIAL_LENGTH_R;
//  cCur = getCoord(lengthL, lengthR);
  
  pinMode( PIN_MOTOR_L_STEP, OUTPUT );
  pinMode( PIN_MOTOR_R_STEP, OUTPUT );
  pinMode( PIN_MOTOR_L_DIR, OUTPUT );
  pinMode( PIN_MOTOR_R_DIR, OUTPUT );
  
  motorDelay = CALIB_MOTOR_DELAY;
  
  motorLStep(1);
  motorRStep(1);
  delay(motorDelay);
  motorLStep(-1);
  motorRStep(-1);
  
  if (!positionCalibration())
    while(1);
  
}

//////////////////////////////////////////////////////////
////moveToPoint
///moves from the current coordinates to destination cD.
void moveToPoint( coord cD )
{
//  Serial.println("moving");
  long t = millis(); //used to time motor delays / speed
  coord cStart = cCur; //start point
  float curDist, prevDist = 0;
  signed char stateL; //will be 0, 1, or -1
  signed char stateR; //ditto
  signed char stateB; //ditto
  
  float tempDL; //temporary holding variable for the distance from line for a left motor move
  float tempDR; //ditto but for right motor move
  float tempDB; //ditto but for moving both
  coord cTempL; //temp variable for holding the coordinates of a left motor move
  coord cTempR; //ditto for right
  coord cTempB; //both
  
  curDist = getDistFromPoint( cCur, cD );
  prevDist = curDist+1;
  
  while(1) //loop infinitely (until arriving at cD 
  {
    curDist = getDistFromPoint( cCur, cD ); //how far are we now from our destination?
    stateL = 0; // 0 is none, 1 is move +, -1 is move -
    stateR = 0; //ditto
    stateB = 0;
    
    if (((prevDist-curDist) < 0.01) && (curDist < 1.5))
    {
//      Serial.println("d change thresh");
      break;
    }
    
    if (curDist < 0.6)
    {
//      Serial.println("d thresh");
      break;
    }
      
    
    
    prevDist = curDist;
    
    cTempL = getCoord( lengthL+STEP_DIST, lengthR ); //what if we move left motor in + direction (let line out from spool)?
    if (getDistFromPoint( cTempL, cD ) < curDist - STEP_THRESH) //does it get us closer?
    {
      tempDL = getDistFromLine( cStart, cD, cTempL ); //how close to the line are we?
      stateL = 1; //means that moving the left motor in + direction is better than -
    } else
    {
      cTempL = getCoord( lengthL-STEP_DIST, lengthR ); //try - direction
      if (getDistFromPoint( cTempL, cD ) < curDist - STEP_THRESH) //does it get us closer?
      {
        tempDL = getDistFromLine( cStart, cD, cTempL ); //how close to the line are we?
        stateL = -1; //means - direction is better for left motor than + direction
      }
    }
    
    //this section does the same thing with the right motor that the above section does with the left motor
    cTempR = getCoord( lengthL, lengthR+STEP_DIST );
    if (getDistFromPoint( cTempR, cD ) < curDist - STEP_THRESH)
    {
      tempDR = getDistFromLine( cStart, cD, cTempR );
      stateR = 1;
    } else
    {
      cTempR = getCoord( lengthL, lengthR-STEP_DIST );
      if (getDistFromPoint( cTempR, cD ) < curDist - STEP_THRESH)
      {
        tempDR = getDistFromLine( cStart, cD, cTempR );
        stateR = -1;
      }
    }
    
    if ((stateL != 0) && (stateR != 0))
    {
      //this section does the same thing with the right motor that the above section does with the left motor
      cTempB = getCoord( lengthL+STEP_DIST*stateL, lengthR+STEP_DIST*stateR );
      if (getDistFromPoint( cTempB, cD ) < curDist - STEP_THRESH)
      {
        tempDB = getDistFromLine( cStart, cD, cTempB );
        stateB = 1;
      }
    }
    
    
    //ok, now let's see which move is better
    if ((stateL != 0) && (stateR != 0)) //means that moving either motor will get us closer to the destination
    { 
      if (stateB == 1)
      {
        if ((tempDL <= tempDR) && (tempDL <= tempDB)) //if left move gets closer than right move or both moves
        {
          motorLStep( stateL ); //move +-1
          lengthL += stateL*STEP_DIST; // change by +- STEP DIST
          cCur = cTempL; //update the current coordinates
          
        } else if ((tempDR <= tempDL) && (tempDR <= tempDB)) //right move gets closer than left move or both moves
        {
          motorRStep( stateR ); //move +-1
          lengthR += stateR*STEP_DIST; // change by +- STEP DIST
          cCur = cTempR; //update the current coordinates
          
        } else  //otherwise both moves gets closest (or they're tied)
        {
          motorRStep( stateR ); //move both
          motorLStep( stateL );
          lengthL += stateL*STEP_DIST;
          lengthR += stateR*STEP_DIST;
          cCur = getCoord( lengthL, lengthR);
        }
      }
      else
      {
        if (tempDL <= tempDR) //if left move gets closer than right move or both moves
        {
          motorLStep( stateL ); //move +-1
          lengthL += stateL*STEP_DIST; // change by +- STEP DIST
          cCur = cTempL; //update the current coordinates
          
        } else //right move gets closer than left move or both moves
        {
          motorRStep( stateR ); //move +-1
          lengthR += stateR*STEP_DIST; // change by +- STEP DIST
          cCur = cTempR; //update the current coordinates
          
        }
      }
        
    } else if (stateR != 0) //only right move gets closer
    {
      motorRStep( stateR ); //move +-1
      lengthR += stateR*STEP_DIST;
      cCur = cTempR;
      
    } else if (stateL != 0) //only left move gets closer
    {
      motorLStep( stateL ); //move +-1
      lengthL += stateL*STEP_DIST;
      cCur = cTempL;
      
    } else //no moves get closer
    {     //which means we're done!
      break; //leave the loop
    } 
    
    while(millis()-t < motorDelay) {} //wait for motor delay
    t = millis();
    
  } //end while(1) loop
  
  //Serial.println("done moving");
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

//////////////////////////////////////////////////////////
////positionCalibration
///Calibrates the position of the carriage by moving the platform
/// up until it gets detected by the IR sensor.
///Returns false if it fails.
boolean positionCalibration()
{
  
  //step one: make sure that the carriage isn't already in front of the sensor
  if (analogRead(PIN_IR_SENSOR) > IR_THRESHOLD) //if voltage is greater than threshold voltage
    //aka if distance is less than threshold distance
  {
//    Serial.println("saw it early");
    delay(500);
    for(int i = 0; i < DIP_STEPS; i++) //we're not dipping, but it's convenient to just go the same distance
    {
      motorLStep(1);
      motorRStep(1);
      delay(motorDelay);
    }
    delay(500);
    //now check again:
//    if (analogRead(PIN_IR_SENSOR) > IR_THRESHOLD)
//      return false; //calibration fails if sensor is still picking something up.
  }
  
  //ok, now we should be ready to start lifting the carriage
  int count = 0;  //counts the steps moved upwards
  int reading = 0; //will be used to store the sensor reading
//  Serial.println("scanning...");
//  delay(500);
  while(1)
  {
    motorLStep(-1); //pull both motors up a step
    motorRStep(-1);
    delay(motorDelay); //delay before reading sensor to give it time to finish moving
    
    
    if (analogRead(PIN_IR_SENSOR) > IR_THRESHOLD) //have we found it?
      break; //yes!
      
    if (++count >= MAX_CALIBRATION_STEPS) //have we moved too much (aka missed it?)
    {  //if so, move back down to where you started, and report a failure
      for(int i = 0; i < MAX_CALIBRATION_STEPS + CALIBRATION_Y_CORRECTION_STEPS; i++)
      {
        motorLStep(1);
        motorRStep(1);
        delay(motorDelay);
      }
      return positionCalibration();
    }
  } //end while loop
  
//  Serial.println("found it");
//    delay(500);
  //at this point we have found the carriage, now we just need to convert that voltage
  //reading into an x distance
  
  for(int i = 0; i < CALIBRATION_ADJUSTMENT_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(motorDelay);
  }
  
//  Serial.println("reading");
  delay(500); //let it settle slightly before reading
  reading = analogRead(PIN_IR_SENSOR);

  //this equation was made using line-fitting in excel with actual measurements
  double distance = pow(double(reading),-1.198);
  distance = distance * 169721.1;//62930.3;
//  Serial.print("distance: ");
//  Serial.println(distance);
//  delay(500);  
  
  //set the current coordinates based on where it is relative to the IR sensor
  cCur.x = IR_X + distance; //assumes it's mounted on the left side
  cCur.y = IR_Y;
  
  //calculate the lengths of the fishing line
  lengthL = getDistFromPoint(cCur, cMotorL);
  lengthR = getDistFromPoint(cCur, cMotorR);
  
  if ((distance > 121) || (distance < 73)) //are you in the ideal sensor range yet?
  {                  //if not, then move halfway from where you are to the center of the ideal range
    coord cAdjust;
    cAdjust.x = IR_X + 97 + (distance-97)/2;
    cAdjust.y = IR_Y;
    moveToPoint(cAdjust);
    return finePositionCalibration();
  }
  
  //at this point it has calibrated the y, and fine-tuned the x
  //for better precision, let's re-calibrate the y
  
  //send it back down below the sensor
  for(int i = 0; i < 2*CALIBRATION_ADJUSTMENT_STEPS; i++)
  {
    motorLStep(1);
    motorRStep(1);
    delay(motorDelay);
  }
  //now come back up
  delay(1000);
  while (analogRead(PIN_IR_SENSOR) <= IR_THRESHOLD) //while it's not seen
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(motorDelay);
  }
  
  for(int i = 0; i < CALIBRATION_ADJUSTMENT_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(motorDelay);
  }
  
  //now the y coord (IR_Y) should be more accurate
  
  return true;
} 
  
  
//////////////////////////////////////////////////////////
////positionCalibration
///Calibrates the position of the carriage by moving the platform
/// up until it gets detected by the IR sensor.
///Returns false if it fails.
boolean finePositionCalibration()
{
//  Serial.println("fine tuning...");

  //step one: make sure that the carriage IS already in front of the sensor
  if (analogRead(PIN_IR_SENSOR) <= IR_THRESHOLD) //if voltage is less than or equal to threshold voltage
    //aka if distance is greater than threshold distance
  {
//    Serial.println("missed it");
//    delay(500);
    for(int i = 0; i < DIP_STEPS; i++) //we're not dipping, but it's convenient to just go the same distance
    {
      motorLStep(1);
      motorRStep(1);
      delay(motorDelay);
    }
//    delay(1000);
    
      //ok, now we should be ready to start lifting the carriage
    int count = 0;  //counts the steps moved upwards
    int reading = 0; //will be used to store the sensor reading
//    Serial.println("scanning...");
//    delay(500);
    while(1)
    {
      motorLStep(-1); //pull both motors up a step
      motorRStep(-1);
      delay(motorDelay); //delay before reading sensor to give it time to finish moving
            
      if (analogRead(PIN_IR_SENSOR) > IR_THRESHOLD) //have we found it?
        break; //yes!
        
      if (++count >= MAX_CALIBRATION_STEPS) //have we moved too much (aka missed it?)
      {  //if so, move back down to where you started, and report a failure
        for(int i = 0; i < MAX_CALIBRATION_STEPS + CALIBRATION_Y_CORRECTION_STEPS; i++)
        {
          motorLStep(1);
          motorRStep(1);
          delay(motorDelay);
        }
        return positionCalibration();
      }
    } //end while loop
    
    for(int i = 0; i < CALIBRATION_ADJUSTMENT_STEPS; i++)
    {
      motorLStep(-1);
      motorRStep(-1);
      delay(motorDelay);
    }
  }
  
//  Serial.println("found it");
  delay(500); //let it settle slightly before reading
  int reading = analogRead(PIN_IR_SENSOR);

  //this equation was made using line-fitting in excel with actual measurements
  double distance = pow(double(reading),-1.198);
  distance = distance * 169721.1;//62930.3;
//  Serial.print("distance: ");
//  Serial.println(distance);
//  delay(500);  
  
  //set the current coordinates based on where it is relative to the IR sensor
  cCur.x = IR_X + distance; //assumes it's mounted on the left side
  cCur.y = IR_Y;
  
  //calculate the lengths of the fishing line
  lengthL = getDistFromPoint(cCur, cMotorL);
  lengthR = getDistFromPoint(cCur, cMotorR);
  
  if ((distance > 121) || (distance < 73)) //are you in the ideal sensor range yet?
  {                  //if not, then move halfway from where you are to the center of the ideal range
    coord cAdjust;
    cAdjust.x = IR_X + 97 + (distance-97)/2;
    cAdjust.y = IR_Y;
    moveToPoint(cAdjust);
    return finePositionCalibration();
  }
  
  //at this point it has calibrated the y, and fine-tuned the x
  //for better precision, let's re-calibrate the y
  
  //send it back down below the sensor
  for(int i = 0; i < 2*CALIBRATION_ADJUSTMENT_STEPS; i++)
  {
    motorLStep(1);
    motorRStep(1);
    delay(motorDelay);
  }
  delay(1000);
  //now come back up
  while (analogRead(PIN_IR_SENSOR) <= IR_THRESHOLD) //while it's not seen
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(motorDelay);
  }
  
  for(int i = 0; i < CALIBRATION_ADJUSTMENT_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(motorDelay);
  }
  
  //now the y coord (IR_Y) should be more accurate
  
  return true;
}

//////////////////////////////////////////////////////////
////getServoAngle
///Shoulddddd return the servo angle for the rotation servo
/// corresponding to the direction from start to dest (or dest to start).
/// Should hopefully come out between 0 to 180 deg.
///Returns the angle in deg [0,180]
int getServoAngle( coord start, coord dest )
{
  float deg = atan((dest.y-start.y)/(dest.x-start.x))*RAD_TO_DEG;
  deg = 90 - deg;
  return int(deg);
}
