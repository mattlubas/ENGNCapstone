//This code programs a servo motor move a specified angle.This angle
//will then determine how much the piston cylinder needs to move.
//Author: Alfred Rwagaju, Matt Lubas, Eric Wirth

#include <Servo.h>

Servo myservo;

// Constants
static const float area = 452.25; 			// cross sectional area of the piston cylinder in mm^2
static const float k = 0.2485; 				// slope of the linear part of the wave // mm / degrees
//static const float k = -0.2635; 			// mm/degree (mm per degree)
static const int N = 180; 				// period in number of integer steps
static const float deg_add = 3; 			// angle between each step
static const float theta_i = 0;  // Initial theta angle for writing servo ... theta_i is in degrees.
//static const float a = 1.5; // cm. Length of Bar 1, the servo hub.
//static const float b= 4.6  ; //cm. Length of Bar 2, the Pneumatic actuator bar.
//static const float c = 0.5; //cm. NEW OFFSET. The seperation horizontally between the servo motor and piston cylinder.

// Values computed directly from constants
static float x_i = k*theta_i;
static float step_total = N / deg_add; 

// User-modifiable parameters
static float tidal_vol = 2; //mL units.
static float f = 2 ;// frequency of the device. Units in Hz  // Integrate as a user function.

//Time of Study to be used as a global variable.
static unsigned long time_initial;

void setup() {

	myservo.attach(9);
	Serial.begin(57600);
	Serial1.begin(57600); //Bluetooth 9600 assuredly
	time_initial = micros();
}

void loop() {

	// Update values that depend on user input tidal_vol, f --------------------------------------
	//converting tidal_vol to mm^3
	float tidal_vol_mm3 = tidal_vol *1000;

	//finding change in distance that the piston cylinder will move through
	float delta_x = tidal_vol_mm3 / area;

	float x_f = delta_x + x_i;
	float theta_f = x_f /k; //theta_f units in degrees.
	float delta_theta = theta_f - theta_i;

	float FRC_initial = 60 + delta_theta/2 ; //angle, placeholder for finding the FRC of the device
	//desired FRC around 4 mL, should be 8.844 mm away from front of PA. This can be estimated for 
	//validation, and calibrated easily later by increasing/ decreasing angle.
	//This should be the smallest the motor ever goes.


	// Check for new params input by user in serial monitor ---------------------------------------
	static char message[100];
	static int messageIndex;
	if (Serial.available()) {

		while (Serial.available()) {
			message[messageIndex] = Serial.read();
			messageIndex++;
		}
	}
	else if (messageIndex > 0) {
		sscanf(message, "%f %f", &tidal_vol, &f); 
		Serial.printf("Tidal volume: %f   Frequency: %f\n", tidal_vol, f);
		message[0] = 0;
		messageIndex = 0;
	}

	// Run the motors based on our computations ----------------------------------------------------
	for (float step_index = 0; step_index <= N; step_index=step_index+deg_add) {

		float AMP = (theta_f - theta_i)*k; //angle moved by the servo motor
		float rad = step_index * 2000 / 57296; // converting angle deg to radians through approximation
		//its 2000 in order to incorporate negative and positive outputs from the below sine function

		// x is starting from mid-point, 90, and is the angle used to write the servo motor.
		float angle_servo = FRC_initial + 2*AMP * sin (rad); 

		// theta_i is initial positioneeds to be replaced by the cacluated FRC
		//Amplitude is doubled to reach the amplitude desired.

		float distance = angle_servo*k;

		//Serial.println("angle servo");
		//Serial.println(angle_servo);

		myservo.write (angle_servo);

		float time_delay = 1000/(step_total*f);

		//Serial.println("Time Delay:");
		//Serial.println(time_delay);
		unsigned long time_final = micros() - time_initial;

		Serial.printf("%f,%d\n", distance, time_final);

		delay(time_delay);
	}
}


