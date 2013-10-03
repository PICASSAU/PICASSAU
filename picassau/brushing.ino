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
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  rotateServo.write(0);
  
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
      if (brushOffset >= 5)
        dir = !dir;
    } else
    {
      brushOffset--;
      if (brushOffset <= -5)
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
    
    //slowly apply the brush to keep the carriage from bouncing
    //off the poster
    for (int i = 40; i >= 0; i--)
    {
      brushServo.write(BPOS_APPLY+i);
      delay(10);
    }
    
    brushSetting = BPOS_APPLY;
    brushOffset = 0;
    
    if (interruptFlag)
      brushWiggle = true; //re-enable wiggle
  }
}

//////////////////////////////////////////////////////////
////removeBrush
///removes the brush
void removeBrush()
{
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  brushOffset = 0;
  
  delay(100);
}

//////////////////////////////////////////////////////////
////dipBrush
///dips the brush into the paint
void dipBrush()
{
  brushWiggle = false;
  brushServo.write(BPOS_DIP);
  brushSetting = BPOS_DIP;
  brushOffset = 0;
  
  coord cReturn = cCur;
  
  delay(1000);
  //Serial.println("moving to paint coordinates...");
  delay(1000);
  
  moveToPoint(cPaint2);
  
  delay(1000);
  //Serial.println("dipping...");
  delay(1000);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(1);
    motorRStep(1);
    delay(MOTOR_DELAY);
  }
  
  delay(1000);
  //Serial.println("wiggling...");
  
  brushWiggle = true;
  delay(1000);
  brushWiggle = false;
  
  delay(1000);
  Serial.println("raising...");
  delay(1000);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    motorLStep(-1);
    motorRStep(-1);
    delay(MOTOR_DELAY);
  }
  
  delay(1000);
  Serial.println("returning...");
  delay(1000);
  
  removeBrush();
  
  moveToPoint(cReturn);
}

void rotateBrush(int deg)
{
  rotateServo.write(deg);
}


