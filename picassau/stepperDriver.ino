void motorLStep(int steps)
{
  digitalWrite(PIN_MOTOR_L_STEP, LOW);
  
  if (steps < 0)
  {
    digitalWrite(PIN_MOTOR_L_DIR, LOW);
    steps = -steps;
  }
  else
  {
    digitalWrite(PIN_MOTOR_L_DIR, HIGH);
  }
  
  while( true )
  {
    digitalWrite(PIN_MOTOR_L_STEP, HIGH);
    if (--steps <= 0)
      break;
    digitalWrite(PIN_MOTOR_L_STEP, LOW);
    delay(MOTOR_DELAY);
  }
  digitalWrite(PIN_MOTOR_L_STEP, LOW);
}

void motorRStep(int steps)
{
  digitalWrite(PIN_MOTOR_R_STEP, LOW);
  
  if (steps < 0)
  {
    digitalWrite(PIN_MOTOR_R_DIR, HIGH);
    steps = -steps;
  }
  else
  {
    digitalWrite(PIN_MOTOR_R_DIR, LOW);
  }
  
  while( true )
  {
    digitalWrite(PIN_MOTOR_R_STEP, HIGH);
    if (--steps <= 0)
      break;
    digitalWrite(PIN_MOTOR_R_STEP, LOW);
    delay(MOTOR_DELAY);
  }
  digitalWrite(PIN_MOTOR_R_STEP, LOW);
}
