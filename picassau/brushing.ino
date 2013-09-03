Servo brushServo;
Servo rotateServo;

void brushSetup()
{
  brushServo.attach(PIN_BRUSH_SERVO);
  rotateServo.attach(PIN_ROTATE_SERVO);
  cPaint.x = PAINT_X;
  cPaint.y = PAINT_Y;
}

void applyBrush()
{
  brushServo.write(BPOS_APPLY);
  delay(100);
}

void removeBrush()
{
  brushServo.write(BPOS_LIFT);
  delay(100);
}

void dipBrush()
{
  dipBrush();
  coord cReturn = cCur;
  
  moveToPoint(cPaint);
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    stepperL.step(1);
    stepperR.step(1);
    delay(MOTOR_DELAY);
  }
  
  //maybe wiggle the brush around here?
  
  for(int i = 0; i < DIP_STEPS; i++)
  {
    stepperL.step(-1);
    stepperR.step(-1);
    delay(MOTOR_DELAY);
  }
  
  liftBrush();
  
  moveToPoint(cReturn);
}
