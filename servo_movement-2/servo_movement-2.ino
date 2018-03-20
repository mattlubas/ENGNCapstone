//This code programs a servo motor move a specified angle.This angle
//will then determine how much the piston cylinder needs to move.
//Author: Alfred Rwagaju
#include <Servo.h>

Servo myservo;
float x;
float max_d = 1.39; // maximum distance by the piston in cm. // May change based on actual angles used
float area = 452.25; // area of the piston cylinder in mm^2
float tidal_vol;
float amp = max_d/2; //amplitude  // may also calculate amplitude by difference from top point to bottom point as well
float k = 0.02485; // slope of the linear part of the wave
int pos;
float deg; // 
int N = 180; //period in number of integer steps

//// Initial Input for Freqency, Conversion to Time Delay

float f = 2 ;// frequency of the device. Units in Hz  // Integrate as a user function.
float pos_add = 3; //angle between each step
float step_total = N / pos_add;
float time_delay = 1000/(step_total*f); //number of steps 



void setup() {
  myservo.attach(9);
  Serial.begin(57600);
  Serial1.begin(57600);
  myservo.write(amp/k); // move the servo motor to that position.

  // Integrating desired frequency calculation
}

void loop() {
  for (pos = 0; pos <= N; pos=pos+pos_add)
  {
  float time_initial = micros();  
  float theta = amp/k; //angle moved by the servo motor
  deg = 2*PI*pos/N;
  x = 90 + theta * sin (deg);
  tidal_vol = max_d * area;
  
  Serial.println(x);
  //Serial1.println(x);
  //Serial1.println("tv:");
  //Serial1.println(tidal_vol);
  float time_final =micros();
  float time_taken = time_final - time_initial;
  //Serial1.println(time_taken);
  myservo.write (x);
  Serial.println("Time Delay:");
  Serial.println(time_delay);
  //Serial.println("Time Taken:");
  //Serial.println(time_taken);
  delay(time_delay);
  }
}
      
 
