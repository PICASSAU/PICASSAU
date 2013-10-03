//////////////////////////////////////////////////////////
// handshake.ino
// 
// Made to handle the communication between the Arduino and the computer.
//   Includes actual serial reading and writing, and parsing the received
//   commands.
//
// Primary author(s): Drew Kerr, Ben Straub
// Team members: David Toledo, Kayla Frost, Peter Gartland
//////////////////////////////////////////////////////////

char stringBuffer[25];
byte stringIndex = 0;

void serialSetup() //initialize serial port
{
  Serial.begin(9600); //open serial port, set data rate to 9600 bps
  stringBuffer[0] = '\0';
  stringIndex = 0;
}

void serialReady() //Send ready status to computer
{
  while(Serial.available()){Serial.read();} //Serial.flush
  Serial.print("R");    //when ready, inform computer
  stringBuffer[0] = '\0';
  stringIndex = 0;
}

void serialError()
{
  Serial.print("X");  //error in reading message
}
    
boolean receiveInstruction() //receive instruction from computer
{
  long t = millis();
  //Serial.println("receiving");
  char temp;
  //Serial.println(stringBuffer);
  do
  {
    while (!Serial.available()) //wait until data in serial buffer
    {
      if ((millis()-t) > SERIAL_TIMEOUT)
        return false;
    }
    temp = Serial.read();   //write buffer data into string
    Serial.print(temp);
    stringBuffer[stringIndex++] = temp;
  } while (temp != '\n');
  stringBuffer[stringIndex] = '\0';
  //Serial.print(stringBuffer[0]);
  //Serial.print(stringBuffer);
  return true;
}
    
boolean verifyInstruction()  //check if correct instr. received with computer and parse numbers out
{
  while(Serial.available()){Serial.read();} //Serial.flush - make sure there's nothing sitting in the Serial buffer
  Serial.print(stringBuffer); //send received instr. back to comp.
  while (!Serial.available()) {} //wait for verification
  stringBuffer[0] = Serial.read(); //write verification status to buffer
  stringIndex = 1;
  stringBuffer[1] = '\0';
  if(stringBuffer[0] != 'G') //if the instruction received isn't correct
    return false; 
  return true;
}

boolean parseInstruction()
{
  command = stringBuffer[0];
  if (command == 'D') //D for Done
    return true;
  if ((command != 'L') && (command != 'M') && (command != 'C'))
    return false;
  if (stringBuffer[1] != ' ')
    return false;
  
  char i = 2;
  int temp = 0; //used to hold the number as it comes in
  
  while (stringBuffer[i] != ',') //keep looping until you get to a comma
  {
    if ((stringBuffer[i] < 0x30) || (stringBuffer[i] > 0x39)) //make sure it's '0' to '9'
      return false; //not a number
    temp = temp*10 + stringBuffer[i] - 0x30; //the -0x30 converts the character to an integer
    if ((++i) > 12) //allows a max of 10 digits
      return false; //too long
  }
  
  //set this number as the x coordinate if it's a move/line command
  if (command != 'C')
    cDest.x = temp + COORD_OFFSET_X;
  else //otherwise, if it's a color command, make sure the color index is valid
    if (temp >= MAX_COLORS)
      return false;
      
  i++;
  temp = 0;
  while (stringBuffer[i] != '\n') //keep looping until you get to a comma
  {
    if ((stringBuffer[i] < 0x30) || (stringBuffer[i] > 0x39))
      return false; //not a number
    temp = temp*10 + stringBuffer[i] - 0x30;
    if ((++i) > 23) //allows a max of 10 digits
      return false; //too long
  }
  
  //set this number as the y coordinate if it's a move/line command
  if (command != 'C')
    cDest.y = temp + COORD_OFFSET_Y;
  else //otherwise, if it's a color command, make sure it's 0
    if (temp != 0)
      return false;
      
  //all done    
  return true;
}
        
        
