//This code programs a servo motor move a specified angle.This angle
//will then determine how much the piston cylinder needs to move.
//Author: Alfred Rwagaju, Matt Lubas, Eric Wirth

#include <Servo.h>

Servo myservo;
float angle_servo;
float max_d = 1.39; // maximum distance by the piston in cm. // May change based on actual angles used
float area = 452.25; // area of the piston cylinder in mm^2
float amp = max_d/2; //amplitude
float k = 0.2485; // slope of the linear part of the wave //
//float k = -0.2635; // mm/degree (mm per degree)
float pos;
float rad; // 
int N = 180; //period in number of integer steps

//float tidal_vol = max_d * area;

////////////////////////////////////////////////////////////////
//// Initial Input for Tidal Volume, through converting distance.
////////////////////////////////////////////////////////////////
float tidal_vol = 2; //mL units.

//converting tidal_vol to mm^3
float tidal_vol_mm3 = tidal_vol *1000;

//finding change in distance that the piston cylinder will move through
float delta_x = tidal_vol_mm3 / area;

//DO NOT DELETE THIS COMMENT -set theta_i to zero, forcing x_i to be equal to zero.  
//Setting theta_i to a non-zero value will be important for finding and setting the 
// functional residual capacity (FRC) of the device.
// This can be done by finding the distance from most extended linear point 
// (whether from low bound or high bound

float theta_i = 0;  //theta_i is in degrees.
float x_i = k*theta_i;

float x_f = delta_x + x_i;
float theta_f = x_f /k; //theta_f units in degrees.
float delta_theta = theta_f - theta_i;


float FRC_initial = 60; //angle, placeholder for finding the FRC of the device


//////////////////////////////////////////////////////////
//// Initial Input for Freqency, Conversion to Time Delay
//////////////////////////////////////////////////////////

float f = 1.5 ;// frequency of the device. Units in Hz  // Integrate as a user function.
float deg_add = 3; //angle between each step

float step_total = N / deg_add;  // delta_theta used to be N
//The frequency is off because the number of steps is greater than it should be. Change N 

float time_delay = 1000/(step_total*f); //number of steps 

//// Initial Bar Lengths and Angle Definitions for 4 Bar Crank and Slider
float a = 1.5; // cm. Length of Bar 1, the servo hub.
float b= 4.6  ; //cm. Length of Bar 2, the Pneumatic actuator bar.
float c = 0; //cm. Will put in an offset soon. The seperation horizontally between the servo motor and piston cylinder.
float theta3; //degrees or radians. The angle of the piston cylinder which calculates the volume.

void setup() {
  myservo.attach(9);
  Serial.begin(57600);
  Serial1.begin(57600);
  myservo.write(FRC_initial); // move the servo motor to that position.
  
}

void loop() {
  for (pos = 0; pos <= 180; pos=pos+deg_add)
  { 
  float AMP = (theta_f - theta_i)*k; //angle moved by the servo motor
  rad = pos * 2000 / 57296; // converting angle deg to radians for the below sine function
  //its 2000 in order to incorporate negative and positive outputs from the below sine function

  
  float sine = sin(rad);
  angle_servo = FRC_initial + 2*AMP * sin (rad); // x is starting from mid-point, 90, and is the angle used to write the servo motor.
  // theta_i is initial positioneeds to be replaced by the cacluated FRC
  //Amplitude is doubled to reach the amplitude desired.

  
  //Serial.println(x);
  float distance = angle_servo*k;
  //Serial.println(distance); //position of the motor over time.
  //Serial1.println(x);
  //Serial.println("Theta_f");
  //Serial.println(sine);

  Serial.println("angle servo");
  Serial.println(angle_servo);

  Serial.println("distance");
  Serial.println(distance);

  //Serial.println("time delay");
  //Serial.println(time_delay);
  
  myservo.write (angle_servo);
  //Serial.println("Time Delay:");
  //Serial.println(time_delay);
  delay(time_delay);
  }
}
      
 
