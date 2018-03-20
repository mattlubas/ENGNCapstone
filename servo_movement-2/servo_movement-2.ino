//This code programs a servo motor move a specified angle.This angle
//will then determine how much the piston cylinder needs to move.
//Author: Alfred Rwagaju, Matt Lubas, Eric Wirth
#include <Servo.h>

Servo myservo;
float x;
float max_d = 1.39; // maximum distance by the piston in cm. // May change based on actual angles used
float area = 452.25; // area of the piston cylinder in mm^2
float amp = max_d/2; //amplitude
float k = 0.02485; // slope of the linear part of the wave
int pos;
float deg; // 
int N = 180; //period in number of integer steps

float tidal_vol = max_d * area;

//// Initial Input for Freqency, Conversion to Time Delay

float f = 3 ;// frequency of the device. Units in Hz  // Integrate as a user function.
float pos_add = 3; //angle between each step
float step_total = N / pos_add;
float time_delay = 1000/(step_total*f); //number of steps 

//// Initial Bar Lengths and Angle Definitions for 4 Bar Crank and Slider
float a = 1.5; // cm. Length of Bar 1, the servo hub.
float b= 4.6  ; //cm. Length of Bar 2, the Pneumatic actuator bar.
float c = 0; //cm. The seperation horizontally between the servo motor and piston cylinder.
float theta3; //degrees or radians. The angle of the piston cylinder which calculates the volume.

void setup() {
  myservo.attach(9);
  Serial.begin(57600);
  Serial1.begin(57600);
  myservo.write(amp/k); // move the servo motor to that position.
  
}

void loop() {
  for (pos = 0; pos <= N; pos=pos+pos_add)
  {
  float time_initial = micros();  
  float theta = amp/k; //angle moved by the servo motor
  deg = 2*PI*pos/N;
  x = 90 + theta * sin (deg);

  theta3 = asin((-a*sin(theta) - c)/b) + PI;
  float deg_theta3 = theta3 *57296/1000;
  Serial.println(deg_theta3);
  //Serial.println(x);
  //Serial1.println(x);
  //Serial1.println("tv:");
  //Serial1.println(tidal_vol);
  float time_final =micros();
  float time_taken = time_final - time_initial;
  myservo.write (x);
  //Serial.println("Time Delay:");
  //Serial.println(time_delay);
  delay(time_delay);
  }
}
      
 