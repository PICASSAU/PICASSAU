const int CGUI_SER_TIMEOUT = 10000; //in ms
const char CGUI_QUEUE_SIZE = 8;    //needs to be a power of two
const char CGUI_QUEUE_MOD = CGUI_QUEUE_SIZE - 1;
const long CGUI_KNOB_SEND_TIME = 500; //in ms
const long CGUI_BTN_DEBOUNCE = 500; //in ms

volatile char cgQueue[CGUI_QUEUE_SIZE];
unsigned char firstIndex = 0;
volatile unsigned char lastIndex = 0;

long tTP = 0;
long tCon = 0;

char cgBuf[28];
char cgBufIndex = 0;

int knobA, knobB, knobC = 0;

void controlGUI()
{
  controlGUIInit();
  controlGUILoop();
  controlGUIDeInit(); //deinitialize
}

void controlGUIDeInit()
{
  detachInterrupt(INT_BTN_TP);
  detachInterrupt(INT_BTN_CON);
  Serial.println("ending GUI");
}

void controlGUIInit()
{
  //set buttons as inputs
  pinMode(PIN_BTN_TP, INPUT);
  pinMode(PIN_BTN_CON, INPUT);
  
  //init the queue
  for (int i = 0; i < CGUI_QUEUE_SIZE; i++)
  {
    cgQueue[i] = '\n'; //default value that won't confuse the other end
  }
  
  //attach button interrupts
  attachInterrupt(INT_BTN_TP, cgTPInt, RISING);
  attachInterrupt(INT_BTN_CON, cgConInt, RISING);
  
  //flush serial port
  Serial.flush();
}

void controlGUILoop()
{
  char blah = 1;
  char ret = 0; //for the return value
  long t = 0;
  
  while (true)
  {
    //check serial (for end condition)
      //return if end condition
    
    while (firstIndex != lastIndex)
    {
      ret = cgSendChar( cgQueue[firstIndex] );
      if (ret == 2) //X
        return;
      if (ret == 1) //timeout
        continue; //retry
      firstIndex = (firstIndex+1)&(CGUI_QUEUE_MOD);
    }
    
    if (millis()-t > CGUI_KNOB_SEND_TIME )
    {
      cgReadKnobs();
      ret = cgSendKnobs();
      if (ret == 2) //X
          return;
      //if it timed out, we can just try again later.
      t = millis();
    }
    
  }
}

//button interrupts
void cgTPInt()
{
  if (millis()-tTP > CGUI_BTN_DEBOUNCE)
  {
    cgQueue[lastIndex] = 'T';
    lastIndex = (lastIndex+1)&(CGUI_QUEUE_MOD);
    tTP = millis();
  }
}
void cgConInt()
{
  if (millis()-tCon > CGUI_BTN_DEBOUNCE)
  {
    cgQueue[lastIndex] = 'C';
    lastIndex = (lastIndex+1)&(CGUI_QUEUE_MOD);
    tCon = millis();
  }
}

void cgReadKnobs()
{
  knobA = analogRead(PIN_KNOB_A);
  knobB = analogRead(PIN_KNOB_B);
  knobC = analogRead(PIN_KNOB_C);
}

char cgSendKnobs()
{
  //divide knobs by 4 (to get 0-255 range) and convert to string
  String strA = String((knobA >> 2),DEC);
  String strB = String((knobB >> 2),DEC);
  String strC = String((knobC >> 2),DEC);
  String strSend = "D," + strA + "," + strB + "," + strC;
  return cgSendString(strSend);
}

//returns 0 = success,  1 = timeout,  2 = X received
char cgSendString( String s )
{
  long t;
  char temp;
  //Serial.println( s );
  
  String s2;
  t = millis();
  s = s + "\n"; //add new line
  
  do
  {
    Serial.print( s );
    s2 = "";
    do
    {
      while (!Serial.available()) //wait for serial input
      {
        if ( (millis()-t) > CGUI_SER_TIMEOUT ) //check for timeout
          return 1;  //return timeout code
      }
      temp = Serial.read();
      s2 += temp;
      
      if (temp == 'X') //check for X
      {
        if (handleX())
          return 2;
      }
      
    } while (temp != '\n'); //keep going until you reach 
    //Serial.println("newline");
  } while (!s.equals(s2)); //if they don't match, try again
  
  Serial.println("G");
  
  return 0;
}

//returns 0 = success,  1 = timeout,  2 = X received
char cgSendChar( char c )
{
  long t;
  
  char c2, c3;
  t = millis();
  
  do
  {
    Serial.println( c );
    
    while (!Serial.available()) //wait for input
    {
      if ( (millis()-t) > CGUI_SER_TIMEOUT ) //check for timeout
        return 1;
    }
    c2 = Serial.read();
    
    if (c2 == 'X') //make sure its not an X
    {
      if (handleX())
        return 2;
    }
    
    while (!Serial.available()) //wait for input
    {
      if ( (millis()-t) > CGUI_SER_TIMEOUT ) //check for timeout
        return 1;
    }
    c3 = Serial.read();
    
    if (c3 == 'X') //make sure its not an X
    {
      if (handleX())
        return 2;
    }
    
  } while ((c != c2) || (c3 != '\n'));
  Serial.println("G");
  return 0;
}

//checks to see if it's really an X (true) or not (false)
boolean handleX()
{
  long t = millis();
  char temp;
  while(Serial.available()){Serial.read();} //flush
  Serial.println('X');
  while(1)
  {
    while (!Serial.available()) //wait for input
    {
      if ( (millis()-t) > CGUI_SER_TIMEOUT ) //check for timeout
        return false;
    }
    if (Serial.peek() == 'G')
    {
      temp = Serial.read(); //get it out of the buffer
      return true;
    }
    else
      temp = Serial.read();
  }
  return false;
}
