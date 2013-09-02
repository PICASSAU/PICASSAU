String inputinstruction = "";
verificationbyte = 0;


void setup() //initialize serial port
    {
        Serial.begin(9600); //open serial port, set data rate to 9600 bps
        inputinstruction.reserve(25); //reserve 25 bytes for string
    }


void ready() //Send ready status to computer
    {
        Serial.print("R");    //when ready, inform computer
    }    
    
void receiveInstruction() //receive instruction from computer
    {
        while (!Serial.available()) {};  //wait until data in serial buffer
        inputinstruction = Serial.read();   //write buffer data into string
    }
    
boolean verifyInstruction()  //check if correct instr. received with computer
    {
        Serial.print(inputinstruction); //send received instr. back to comp.
        while (!Serial.available()) {}; //wait for verification
        verificationbyte = Serial.read(); //write verification status to variable
        return (verificationbyte != 'G') //if the instruction received isn't correct
    }
     
void ExecuteInstruction() //this program executes instruction received by Ard.      
    {
         /////////// ******execute instruction code;****///////////
         verificationbyte = 0; //reset verification bit
         inputinstruction = ""; //clear instruction string
       } 

//////////////////////////////MAIN//////////////////////////////////////////////
void loop()
{
    setup(); 
    while(1); 
       {
         status(); //Transmit status
         do 
         {
            receiveInstruction(); //Receive instruction
         } while ( !verifyInstruction() ) //verify instruction
         ExecuteInstruction(); // execute
       } //repeat until done painting
      
////////////////////////////////////////////////////////////////////////////////      
        
        
        
        