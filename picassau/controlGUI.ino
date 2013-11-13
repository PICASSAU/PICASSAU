const int CGUI_SER_TIMEOUT = 1000; //in ms
const char CGUI_QUEUE_SIZE = 8;    //needs to be a power of two
const char CGUI_QUEUE_MOD = CGUI_QUEUE_SIZE - 1;

volatile char cgQueue[CGUI_QUEUE_SIZE];
unsigned char firstIndex = 0;
volatile unsigned char lastIndex = 0;

char cgBuf[28]
char cgBufIndex = 0;

void controlGUI()
{
  controlGUIInit();
  controlGUILoop();
}

void controlGUIInit()
{
  //set btns as inputs
  //init queue
  //attach interrupts
  //flush serial port
}

void controlGUILoop()
{
  char blah = 1;
  blah = (blah+1) % 10;
  while (true)
  {
    //check serial (for end condition)
      //return if end condition
    
    while (firstIndex != lastIndex)
    {
      cgSend( cgQueue[firstIndex] );
      firstIndex = (firstIndex-1)&(CGUI_QUEUE_MOD);
    }
      
    //read knobs
    //send knobs
  }
}

char cgSendString( String s )
{
  long t;
  
  Serial.println( s );
  
  String s2;
  t = millis();
  
  do
  {
    Serial.println( s );
    s2 = "";
    do
    {
      while (!Serial.available()) //wait for serial input
      {
        if ( (millis()-t) > CGUI_SER_TIMEOUT ) //check for timeout
          return 1;  //return timeout code
      }
      s2 += Serial.read();
      
      if (s2.endsWith('X')) //check for X
      {
        if (handleX())
          return 2;
      }
      
    } while (!s2.endsWith("\n")); //keep going until you reach 
  } while (!s.equals(s2)); //if they don't match, try again
  
  Serial.println("G\n");
  
  return 0;
}

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
}
  
boolean handleX()
{
  //confirm an X command
  //return true if confirmed
}
