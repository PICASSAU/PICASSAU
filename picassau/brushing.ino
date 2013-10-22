//////////////////////////////////////////////////////////
// brushing.ino
// 
// Made to control the servos moving the brush on the carriage.
//
// Primary author(s): Ben Straub
// Team members: David Toledo, Kayla Frost, Drew Kerr, Peter Gartland
//////////////////////////////////////////////////////////


//////////////////////////////////////////////////////////
////brushSetup
///sets up the brush servos and calls the timer setup
void brushSetup()
{
  brushServo.attach(PIN_BRUSH_SERVO);
  rotateServo.attach(PIN_ROTATE_SERVO);
  armServo.attach(PIN_ARM_SERVO);
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  rotateServo.write(ROTATE_SERVO_HOME);
  armServo.write(75);

  initTimer();
}

//////////////////////////////////////////////////////////
////initTimer
///sets up the timer interrupt (used for brush wiggle)
void initTimer()
{
  cli();
  
  TCCR2A = (1 << WGM21); //turn on CTC mode for timer 2
  TCCR2B = PRESCALER; //set up prescaler
  OCR2A = OCR_VALUE; //set up compare register
  TIMSK2 |= (1 << OCIE2A); //enable timer interrupt
  
  TCNT2 = 0;
  
  sei();
}

//////////////////////////////////////////////////////////
////ISR
///ISR for the timer interrupt (should be about 100Hz).
///  It should move the brush between -5 and +5 degrees
///  at a rate of about 5 full wiggles per second.
ISR(TIMER2_COMPA_vect)
{
  static boolean dir = true;
  if (brushWiggle)
  {
    if (dir)
    {
      brushOffset++;
      if (brushOffset >= wiggleDist)
        dir = !dir;
    } else
    {
      brushOffset--;
      if (brushOffset <= -wiggleDist)
        dir = !dir;
    }
    brushServo.write(brushSetting+brushOffset);
  }

}


//////////////////////////////////////////////////////////
////applyBrush
///applies the brush
void applyBrush()
{
  if (brushSetting != BPOS_APPLY)
  {
    boolean interruptFlag = brushWiggle;
    if ( interruptFlag )
      brushWiggle = false;
    
    for (int i = ARM_SERVO_UP; i >= ARM_SERVO_DOWN; i--)
    {
      armServo.write(i);
      delay(10);
    }
    
    //slowly apply the brush to keep the carriage from bouncing
    //off the poster
    for (int i = 40; i >= 0; i--)
    {
      brushServo.write(BPOS_APPLY+i);
      delay(20);
    }
    
    for (int i = ARM_SERVO_DOWN; i <= ARM_SERVO_UP; i++)
    {
      armServo.write(i);
      delay(10);
    }
    
    brushSetting = BPOS_APPLY;
    brushOffset = 0;
    
    delay(500);
    
    if (interruptFlag)
      brushWiggle = true; //re-enable wiggle
  }
}

//////////////////////////////////////////////////////////
////applyBrushWithRotate
///applies the brush and rotates just before lifting the arm back up
void applyBrushWithRotate(int deg)
{
  if (brushSetting != BPOS_APPLY)
  {
    boolean interruptFlag = brushWiggle;
    if ( interruptFlag )
      brushWiggle = false;
    
    for (int i = ARM_SERVO_UP; i >= ARM_SERVO_DOWN; i--)
    {
      armServo.write(i);
      delay(10);
    }
    
    //slowly apply the brush to keep the carriage from bouncing
    //off the poster
    for (int i = 40; i >= 0; i--)
    {
      brushServo.write(BPOS_APPLY+i);
      delay(20);
    }
    
    rotateBrush(deg);
    
    for (int i = ARM_SERVO_DOWN; i <= ARM_SERVO_UP; i++)
    {
      armServo.write(i);
      delay(10);
    }
    
    brushSetting = BPOS_APPLY;
    brushOffset = 0;
    
    delay(500);
    
    if (interruptFlag)
      brushWiggle = true; //re-enable wiggle
  }
  else
  {
    rotateBrush(deg);
  }
}

//////////////////////////////////////////////////////////
////removeBrush
///removes the brush
void removeBrush()
{
  boolean armFlag = (brushSetting == BPOS_APPLY);
  
  if (armFlag)
  {
    for (int i = ARM_SERVO_UP; i >= ARM_SERVO_DOWN; i--)
    {
      armServo.write(i);
      delay(10);
    }
  }
  
  rotateBrush(ROTATE_SERVO_HOME);
  
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  brushOffset = 0;
  
  delay(100);
  
  if (armFlag)
  {
    for (int i = ARM_SERVO_DOWN; i <= ARM_SERVO_UP; i++)
    {
      armServo.write(i);
      delay(10);
    }
  }
  
}

//////////////////////////////////////////////////////////
////dipBrush
///dips the brush into the paint
void dipBrush()
{
  int brushPrevSetting = brushSetting;
  int prevWiggleDist = wiggleDist;
  boolean brushPrevWiggle = brushWiggle;
  int prevBrushRotation = brushRotation;
  
  rotateBrush(ROTATE_SERVO_HOME);
  motorDelay = MOVE_MOTOR_DELAY;
  
  removeBrush(); //go to removed position first (includes pushing away from canvas if needed)
  
  brushWiggle = false;
  brushServo.write(BPOS_DIP);
  brushSetting = BPOS_DIP;
  brushOffset = 0;
  
  coord cReturn = cCur;
  
//  delay(1000);
//  Serial.println("moving to paint coordinates...");
//  delay(1000);
  if (currentColor == 0)
    moveToPoint(cPaint1);
  else if (currentColor == 1)
    moveToPoint(cPaint2);
  else if (currentColor == 2)
    moveToPoint(cPaint3);
  
//  delay(1000);
  //Serial.println("dipping...");
//  delay(1000);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(1);
    motorRStep(1);
    delay(DIP_MOTOR_DELAY);
  }
  
//  delay(1000);
  //Serial.println("wiggling...");
  
  brushWiggle = true;
  wiggleDist = DIP_WIGGLE_DIST;
  delay(1000);
//  Serial.println("raising...");
  delay(1000);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(DIP_MOTOR_DELAY);
  }
  
  brushWiggle = false;
//  delay(500);
//  Serial.println("returning...");
  delay(500);
  
  removeBrush();
  
  moveToPoint(cReturn);
  
  if (brushPrevSetting == BPOS_APPLY)
  {
    applyBrushWithRotate(prevBrushRotation);
    motorDelay = PAINT_MOTOR_DELAY;
  }
  brushWiggle = brushPrevWiggle;
  wiggleDist = prevWiggleDist;
//  brushServo.write(brushPrevSetting);
//  brushSetting = brushPrevSetting;
}

//////////////////////////////////////////////////////////
////washBrush
///washes the brush in the water
void washBrush()
{
  int brushPrevSetting = brushSetting;
  int prevWiggleDist = wiggleDist;
  boolean brushPrevWiggle = brushWiggle;
  int prevBrushRotation = brushRotation;
  
  rotateBrush(ROTATE_SERVO_HOME);
  motorDelay = MOVE_MOTOR_DELAY;
  
  removeBrush(); //go to removed position first (includes pushing away from canvas if needed)
  
  brushWiggle = false;
  brushServo.write(BPOS_DIP);
  brushSetting = BPOS_DIP;
  brushOffset = 0;
  
  coord cReturn = cCur;
  
  moveToPoint(cWater);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(1);
    motorRStep(1);
    delay(DIP_MOTOR_DELAY);
  }
  
//  delay(1000);
  //Serial.println("wiggling...");
  
  brushWiggle = true;
  wiggleDist = DIP_WIGGLE_DIST;
  delay(1000);
//  Serial.println("raising...");
  delay(1000);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(DIP_MOTOR_DELAY);
  }
  
  brushWiggle = false;
//  delay(500);
//  Serial.println("returning...");
  delay(500);
  
  removeBrush();
  
  moveToPoint(cReturn);
  
  if (brushPrevSetting == BPOS_APPLY)
  {
    applyBrushWithRotate(prevBrushRotation);
    motorDelay = PAINT_MOTOR_DELAY;
  }
  brushWiggle = brushPrevWiggle;
  wiggleDist = prevWiggleDist;
}

void rotateBrush(int deg)
{
  int dRot = brushRotation - deg;
  brushRotation = deg;
  rotateServo.write(deg);
  if (dRot > 5) //if we move more than 5 degrees
    delay( dRot*3 );
  //Serial.print("deg: ");
  //Serial.println(deg);
}


