//This code programs a servo motor move a specified angle.This angle
//will then determine how much the piston cylinder needs to move.
//Author: Alfred Rwagaju
#include <Servo.h>


Servo myservo;
float x;
float max_d = 1.39; // maximum distance by the piston in cm
float area = 452.25; // area of the piston cylinder in mm^2
float tidal_vol;
float a = max_d/2; //amplitude
float k = 0.02485; // slope of the linear part of the wave
int pos;
float per;
int N = 180; //period in number of integer steps


void setup() {
  myservo.attach(9);
  Serial.begin(57600);
  Serial1.begin(57600);
  myservo.write(a/k); // move the servo motor to that position.

}

void loop() {
  for (pos = 0; pos <= N; pos=pos+3)
  {
  float time_initial = micros();  
  float theta = a/k; //angle moved by the servo motor
  per = 2*PI*pos/N;
  x = 90 + theta * sin (per);
  tidal_vol = max_d * area;
  Serial.println(x);
  Serial1.println(x);
  //Serial1.println("tv:");
  //Serial1.println(tidal_vol);
  float time_final =micros();
  float time_taken = time_final - time_initial;
  //Serial.println(time_taken);
  //Serial1.println(time_taken);
  myservo.write (x) ;
  delay(10);
  }
}
      
 
