//////////////////////////////////////////////////////////
// picassau.h
// 
// Header file for storing useful constants, pin numbers, structs, etc.
//
// Primary author(s): Ben Straub
// Team members: David Toledo, Kayla Frost, Drew Kerr, Peter Gartland
//////////////////////////////////////////////////////////

#include "Arduino.h"

typedef struct Coord { float x; float y; } coord;

//// miscellaneous
const int MAX_COLORS = 3; //how many paint colors?
const int PAINT_MOTOR_DELAY = 80;//30; // in ms, time between stepping the motors
const int MOVE_MOTOR_DELAY = 20; //moving, including going to the dipping checkpoint
const int DIP_MOTOR_DELAY = 30; //just for the straight-down move while dipping
const int CALIB_MOTOR_DELAY = 40; //used during calibration
const long SERIAL_TIMEOUT = 1000; //serial time out in ms (aka how long to wait before sending another 'R')
//const float RAD_TO_DEG = (180/3.14159265358979); //apparently this is already a thing

const float INITIAL_LENGTH_L = 314.6; //based on the starting position
const float INITIAL_LENGTH_R = 322.5; // of the platform

//// physical measures
const float CIRCUM = 8.25; //in inches, circumference of the spindle
const int NSTEPS = 200; //number of steps per revolution of the stepper motors
const float STEP_DIST = 1; //the change in distance between motor and platform when motor steps
  //we normalize all coordinates from inches to "step-units" (aka "Peters") on the Python side
  //to make plotting and such easier
const float MOTOR_DIST = 727.3; // how far are the motors apart?
const float DBL_MOTOR_DIST = 2*MOTOR_DIST; //used in plotting math. I pre-calculate to save calculation time.
const float MOTOR_DIST2 = MOTOR_DIST*MOTOR_DIST; //ditto
const int STEP_THRESH = 0;

// (0,0) is at the left spindle guide in absolute coordinates
const int COORD_OFFSET_X = 115; //so at what coordinates is the top left
const int COORD_OFFSET_Y = 250;//194; // corner of the canvas?

//// calibration and sensor stuff
const int IR_X = 85; //3.5 inches
const int IR_Y = 733; //30.25 inches
const int IR_THRESHOLD = 150; //the ADC reading threshold to decide whether or not it sees anything during calibration
const int MAX_CALIBRATION_STEPS = 558; //max upward movement during calib. before assuming you started above
const int CALIBRATION_ADJUSTMENT_STEPS = 35; //how much to move slightly up to center itself on the sensor in calibration
const int CALIBRATION_Y_CORRECTION_STEPS = 270; //if the carriage started above, how far down to go to correct it

//// brush position and paint distance
const float PAINTING_DISTANCE = 500; //how far (in step-units) you can go before needing to redip brush
const int BPOS_APPLY = 70; //angle of the brush servo when the brush is applied
const int BPOS_DIP = 160; //angle of the brush servo when dipping in paint
const int BPOS_LIFT = 135; //angle of the brush servo when lifted
const int PAINT_WIGGLE_DIST = 10;
const int DIP_WIGGLE_DIST = 5;
const int ROTATE_SERVO_HOME = 1;
const int ARM_SERVO_UP = 80;
const int ARM_SERVO_DOWN = 45;

//// constants for the timer interrupt (used for brush wiggling)
const unsigned char PRESCALER = (1 << CS22) | (1 << CS21) | (1 << CS20); //aka prescaler of 1024 to get 15.625kHz
const unsigned char OCR_VALUE = 156; //156 @ 15.625kHz = 100 Hz

//// coordinates for the paint containers
    //this first set used relative coordintates.  I changed it to use absolute coordinates (so that
    // changing the canvas location wouldn't affect the paint locations)
  //const float PAINT_X1 = 72.4; //4.5
  //const float PAINT_X2 = 193.6; //9.5
  //const float PAINT_X3 = 314.8; //14.5
  //const float PAINT_Y = 810; //40 - dipsteps
  //const coord cPaint1 = {PAINT_X1+COORD_OFFSET_X, PAINT_Y+COORD_OFFSET_Y};
  //const coord cPaint2 = {PAINT_X2+COORD_OFFSET_X, PAINT_Y+COORD_OFFSET_Y};
  //const coord cPaint3 = {PAINT_X3+COORD_OFFSET_X, PAINT_Y+COORD_OFFSET_Y};
const float PAINT_X1 = 172.4; //4.5
const float PAINT_X2 = 293.6; //9.5
const float PAINT_X3 = 414.8; //14.5
const float PAINT_Y = 1030; //40 - dipsteps //945+194
const coord cPaint1 = {PAINT_X1, PAINT_Y};
const coord cPaint2 = {PAINT_X2, PAINT_Y};
const coord cPaint3 = {PAINT_X3, PAINT_Y};
const int DIP_STEPS = 100; //number of steps down from cPaint to move to dip brush

//// coordinates of motors (useful when calculating line lengths)
const float MOTOR_L_X = 0;
const float MOTOR_L_Y = 0;
const coord cMotorL = {MOTOR_L_X, MOTOR_L_Y};
const float MOTOR_R_X = MOTOR_DIST;
const float MOTOR_R_Y = 0;
const coord cMotorR = {MOTOR_R_X, MOTOR_R_Y};

//// pin numbers
const int PIN_BRUSH_SERVO = 2;
const int PIN_ARM_SERVO = 3;
const int PIN_ROTATE_SERVO = 8;
//const int PIN_STEP_L[4] = {6,7,8,9};
//const int PIN_STEP_R[4] = {10,11,12,13};
const int PIN_MOTOR_L_STEP = 11;
const int PIN_MOTOR_L_DIR = 10;
const int PIN_MOTOR_R_STEP = 12;
const int PIN_MOTOR_R_DIR = 13;
const int PIN_IR_SENSOR = A0;

