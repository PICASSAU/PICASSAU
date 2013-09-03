
typedef struct Coord { float x; float y; } coord;

const float MOTOR_DIST = 280; // how far are the motors apart?
const float DBL_MOTOR_DIST = 2*MOTOR_DIST;
const float MOTOR_DIST2 = MOTOR_DIST*MOTOR_DIST;

const int MOTOR_DELAY = 20; // in ms, time between stepping the motors

const float INITIAL_LENGTH_L = 330; //based on the starting position
const float INITIAL_LENGTH_R = 330; // of the platform

const float CIRCUM = 11.125; //in inches, circumference of the spindle
const int NSTEPS = 100; //number of steps per revolution of the stepper motors
const float STEP_DIST = 1;//CIRCUM/NSTEPS; //the change in distance between motor and platform when motor steps

// (0,0) is at the left spindle
const int COORD_OFFSET_X = 50; //so at what coordinates is the top left
const int COORD_OFFSET_Y = 150; // corner of the canvas?
