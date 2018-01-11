/******************************************************************************
  This is example sketch for Arduino.
  Shows how to control SimpleBGC-driven gimbal via Serial API.
  API specs are available at http://www.basecamelectronics.com/serialapi/

  Demo:  control camera angles by Serial API direct control and by
  emulating various RC input methods;

  Arduino hardware:
  - analog joystick on the pins A1, A2  (connect GND, +5V to the side outputs of its potentiometers)

  Gimbal settings:
  - RC control in SPEED mode, RC signal should come from active RC source
  - RC SPEED is set to about 30..100

  Copyright (c) 2014-2015 Aleksey Moskalenko
*******************************************************************************/
#include <inttypes.h>
#include <SBGC.h>
#include <SBGC_Arduino.h>


// Serial baud rate should match with the rate, configured for the SimpleBGC controller
#define SERIAL_SPEED 115200

// delay between commands, ms
#define SBGC_CMD_DELAY 20

/*****************************************************************************/

// Set serial port where SBGC32 is connected
#define serial Serial2
#define computer Serial

void setup() {
  serial.begin(SERIAL_SPEED);
  SBGC_Demo_setup(&serial);

  // Take a pause to let gimbal controller to initialize
  delay(3000);
  SBGC_cmd_control_t c = { 0, 0, 0, 0, 0, 0, 0 };


  // Move camera to initial position (all angles are zero)
  // Set speed 30 degree/sec
  c.mode = SBGC_CONTROL_MODE_ANGLE;
  c.speedROLL = c.speedPITCH = c.speedYAW = 30 * SBGC_SPEED_SCALE;
  SBGC_cmd_control_send(c, sbgc_parser);
}
void setto0(SBGC_cmd_control_t c){
  
  c.mode = SBGC_CONTROL_MODE_ANGLE;
  c.speedROLL = c.speedPITCH = c.speedYAW = 30 * SBGC_SPEED_SCALE;
  SBGC_cmd_control_send(c, sbgc_parser);
  delay(10);
}
void speedcontrol(int pitch, int yaw, int t, SBGC_cmd_control_t c){
  c.mode = SBGC_CONTROL_MODE_SPEED;
  c.speedPITCH=pitch * SBGC_SPEED_SCALE;
  c.speedYAW=yaw * SBGC_SPEED_SCALE;
  SBGC_cmd_control_send(c, sbgc_parser);
  delay(t);
  c.mode = SBGC_CONTROL_MODE_NO;
  SBGC_cmd_control_send(c, sbgc_parser);
}
int anglecontrol(int pitch, int yaw, SBGC_cmd_control_t c){
  c.mode = SBGC_CONTROL_MODE_ANGLE;
  c.anglePITCH = SBGC_DEGREE_TO_ANGLE(pitch);
  c.angleYAW = SBGC_DEGREE_TO_ANGLE(yaw);
  int t=abs(pitch/10);
  SBGC_cmd_control_send(c, sbgc_parser);
  delay(t*1000);
  c.mode = SBGC_CONTROL_MODE_NO;
  SBGC_cmd_control_send(c, sbgc_parser);
  speedcontrol(0, 0, 10, c);
  return c.anglePITCH;
}

bool runonce=false;
void loop() {
  if(!runonce){
    serial.begin(SERIAL_SPEED);
    computer.begin(9600);
    computer.println("port open");
  SBGC_Demo_setup(&serial);
  runonce=true;
  }
  SBGC_cmd_control_t c = { 0, 0, 0, 0, 0, 0, 0 };
  /*speedcontrol(10, 10, 100,  c);
  computer.print("speed 1");
  speedcontrol(-10, -10, 100, c);
  computer.print("speed 2");*/
  
  computer.print("angle 1 " );
  computer.println(anglecontrol(40, 40, c));
  delay(500);
  computer.print("angle 2 " );
  computer.println(anglecontrol(-40, -40, c));
  delay(500);
  //anglecontrol(0, 0, c);
  //computer.print("0 point.");
  
}
