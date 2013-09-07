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
    
void receiveInstruction() //receive instruction from computer
{
  //Serial.println("receiving");
  char temp;
  //Serial.println(stringBuffer);
  do
  {
    while (!Serial.available()) {};  //wait until data in serial buffer
    temp = Serial.read();   //write buffer data into string
    Serial.print(temp);
    stringBuffer[stringIndex++] = temp;
  } while (temp != '\n');
  stringBuffer[stringIndex] = '\0';
  //Serial.print(stringBuffer[0]);
  //Serial.print(stringBuffer);
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
  if ((command != 'L') && (command != 'M'))
    return false;
  if (stringBuffer[1] != ' ')
    return false;
  
  char i = 2;
  int temp = 0;
  while (stringBuffer[i] != ',') //keep looping until you get to a comma
  {
    if ((stringBuffer[i] < 0x30) || (stringBuffer[i] > 0x39))
      return false; //not a number
    temp = temp*10 + stringBuffer[i] - 0x30;
    if ((++i) > 12) //allows a max of 10 digits
      return false; //too long
  }
  cDest.x = temp + COORD_OFFSET_X;
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
  cDest.y = temp + COORD_OFFSET_Y;
  return true;
}
        
        
