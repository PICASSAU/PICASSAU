#include "header.h"

void setup()
{
  
}

void loop()
{
  
}


coord getCoord( float d1, float d2 )
{
  coord c;
  c.x = (d1*d1 - d2*d2 + X2*X2) / (2*X2);
  c.y = sqrt(d1*d1 - c.x*c.x);
  
  return c;
}

float getDistFromLine( coord line1, coord line2, coord point)
{
  float a = line1.y-line2.y;
  float b = line2.x-line1.x;
  float c = -b*line1.y + a*line1.x;
  float num = a*point.x + b*point.y + c;
  float d = abs(num)/(sqrt(a*a + b*b));
  return d;
}

float getDistFromPoint( coord p1, coord p2)
{
  float dx = p1.x - p2.x;
  float dy = p1.y - p2.y;
  return sqrt(dx*dx + dy*dy);
}


  
  
