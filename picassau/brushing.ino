

void brushSetup()
{
  brushServo.attach(PIN_BRUSH_SERVO);
  rotateServo.attach(PIN_ROTATE_SERVO);
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  rotateServo.write(0);
  cPaint.x = PAINT_X;
  cPaint.y = PAINT_Y;
  
  initTimer();
}

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

/// ISR for the timer interrupt (2.404kHz)
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

void applyBrush()
{
  if (brushSetting != BPOS_APPLY)
  {
    boolean interruptFlag = brushWiggle;
    if ( interruptFlag )
      brushWiggle = false;
    
    //slowly apply the brush
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

void removeBrush()
{
  brushServo.write(BPOS_LIFT);
  brushSetting = BPOS_LIFT;
  brushOffset = 0;
  
  delay(100);
}

void dipBrush()
{
  brushWiggle = false;
  brushServo.write(BPOS_DIP);
  brushSetting = BPOS_DIP;
  brushOffset = 0;
  
  coord cReturn = cCur;
  
  moveToPoint(cPaint);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    stepperL.step(1);
    stepperR.step(1);
    delay(MOTOR_DELAY);
  }
  
  brushWiggle = true;
  delay(1000);
  brushWiggle = false;
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    stepperL.step(-1);
    stepperR.step(-1);
    delay(MOTOR_DELAY);
  }
  
  removeBrush();
  
  moveToPoint(cReturn);
}

void rotateBrush(int deg)
{
  rotateServo.write(deg);
}


