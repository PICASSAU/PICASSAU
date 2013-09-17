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

const float MOTOR_DIST = 245; // how far are the motors apart?
const float DBL_MOTOR_DIST = 2*MOTOR_DIST;
const float MOTOR_DIST2 = MOTOR_DIST*MOTOR_DIST;

const int MOTOR_DELAY = 30; // in ms, time between stepping the motors

const float INITIAL_LENGTH_L = 314.6; //based on the starting position
const float INITIAL_LENGTH_R = 322.5; // of the platform

const float CIRCUM = 11.125; //in inches, circumference of the spindle
const int NSTEPS = 100; //number of steps per revolution of the stepper motors
const float STEP_DIST = 1;//CIRCUM/NSTEPS; //the change in distance between motor and platform when motor steps

// (0,0) is at the left spindle
const int COORD_OFFSET_X = 50;//47; //so at what coordinates is the top left
const int COORD_OFFSET_Y = 200;//117; // corner of the canvas?

const int IR_X = 45; //5 inches
const int IR_Y = 296; //32.875 inches
const int IR_THRESHOLD = 150;
const int MAX_CALIBRATION_STEPS = 207;
const int CALIBRATION_ADJUSTMENT_STEPS = 14;
const int CALIBRATION_Y_CORRECTION_STEPS = 100; //if the carriage started above

const float PAINTING_DISTANCE = 400;
const int BPOS_APPLY = 70; //angle of the brush servo when the brush is applied
const int BPOS_DIP = 160; //angle of the brush servo when dipping in paint
const int BPOS_LIFT = 135; //angle of the brush servo when lifted

const unsigned char PRESCALER = (1 << CS22) | (1 << CS21) | (1 << CS20); //aka prescaler of 1024 to get 15.625kHz
const unsigned char OCR_VALUE = 156; //156 @ 15.625kHz = 100 Hz

const float PAINT_X = 148;
const float PAINT_Y = 413;
coord cPaint;

const float MOTOR_L_X = 0;
const float MOTOR_L_Y = 0;
coord cMotorL;
const float MOTOR_R_X = MOTOR_DIST;
const float MOTOR_R_Y = 0;
coord cMotorR;






const int DIP_STEPS = 49; //number of steps down from cPaint to move to dip brush

const int PIN_BRUSH_SERVO = 2;
const int PIN_ROTATE_SERVO = 3;
const int PIN_STEP_L[4] = {6,7,8,9};
const int PIN_STEP_R[4] = {10,11,12,13};
const int PIN_IR_SENSOR = A0;

