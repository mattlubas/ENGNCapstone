# Respir-Rat Capstone Project
Capstone Design Project by Matt Lubas , Eric Wirth and Alfred Rwajagu

##Getting Started

The Device here mimic rodent respiration in a device by controlling for speed, volume moved, and airway resistance.

### Prerequisites
The device runs and exports data using Python3 and Arduino. Using a Teensy micro-controller the device is compatible with Arduino.
You can download python at the following link:
https://www.python.org/
You can download Arduino at the following link:
https://www.arduino.cc/en/Main/Software

To use Teensy with the Arduino setup, use the following link and directions to install and run a teensy:
https://www.pjrc.com/teensy/td_download.html


To run the entire Python Code with ability to visualize plots and export data to excel, the following import packages are needed for python.

pandas
matplotlib
numpy
scipy
threading
time
serial

To install these packages on Terminal for  Mac OSX/ Linux, use the following code lines in Terminal:


```
pip3 install pandas
pip3 install matplotlib
pip3 install numpy
pip3 install threading
pip3 install serial
pip3 install time
pip3 install scipy
pip3 install xlrd
pip3 install xlwt
pip3 install decimal
```

To use on Command Prompt on Windows, copy and paste the following lines:

```
pip install pandas
pip install matplotlib
pip install numpy
pip install threading
pip install serial
pip install time
pip install scipy
pip install xlrd
pip install xlwt
pip install decimal
```

### Installing

To download the Repository, open Terminal/ Command Prompt to the desired location, and run the following line:

```
git clone https://github.com/mattlubas/ENGNCapstone
```
If you are having trouble navigating around Terminal, you can use the following as a resource. https://www.tbi.univie.ac.at/~ronny/Leere/270038/tutorial/node8.html


Once dowloaded, upload and run servo_movement-3 in order to use the Respir-Rat.




## Built With

* Python 3 [https://www.python.org/]
* Arduino 
* Teensy

## Authors

See also the list of [contributors](https://github.com/mattlubas/ENGNCapstone) who participated in this project.

## License

