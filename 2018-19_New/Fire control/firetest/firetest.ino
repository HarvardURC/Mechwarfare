#include <SBUS.h>
#include <SoftPWM.h>
int gunmotor = A6;
int laserpointer = 2;
int hoppermotor = 7;
int hopperdir = 6;
int lightsensor = 14;
#define IDLE_SWITCH 0
#define GUN_CHANNEL 0
#define GUN_COMMAND 0
#define LEG_CHANNEL_START 0
#define AIM_CHANNEL 0
#define LIGHT_SENSOR 0
#define HOPPER_MOTOR 255
#define MANUAL_CHANNEL 0
#define GUN_DIR 255
SBUS x8r(Serial1);
// channel, fail safe, and lost frames data
float channels[16];
uint8_t failSafe;
uint16_t lostFrames = 0;
uint16_t gimbals[16];
bool serialread = false;
#define computer Serial
void hopperDriver(int inst, int power) {
  switch (inst) {
    case 0:
      //brake
      SoftPWMSet(hoppermotor, 0);
      digitalWrite(hopperdir, LOW);
      break;
    case 1:
      //forward
      SoftPWMSet(hoppermotor, power);
      digitalWrite(hopperdir, HIGH);
      break;
    case 2:
      //reverse
      SoftPWMSet(hoppermotor, power);
      digitalWrite(hopperdir, LOW);
      break;
  }
}
bool donefiring() {
  return true;
}
//needs to be filled in
bool isjammed() {
  return true;
}
void unjamcode() {
  hopperDriver(2, HOPPER_MOTOR);
}
int gunState(int currState)
{
  switch (currState) {
    //idle state for gun
    case 0:
      hopperDriver(0, 0);
      analogWrite(gunmotor, 0);
      if (true) {
        //if remote control sends fire signal
        return 1;
      }
      return 0;
    case 1:
      //load state
      //might need more complex code here for loading
      hopperDriver(1, HOPPER_MOTOR);
      //change number later
      if (analogRead(lightsensor) >= LIGHT_SENSOR) {
        //if gun is loaded, move to fire
        return 2;
      }
      return 1;
    case 2:
      //fire state
      analogWrite(gunmotor, GUN_DIR);
      hopperDriver(0, 0);
      if (donefiring()) {
        return 0;
      }
      if (isjammed()) {
        return 3;
      }
      return 2;
    case 3:
      unjamcode();
      if (!isjammed()) {
        return 1;
      }
      else {
        return 3;
      }
  }


}
void setup() {
  // begin the SBUS communication
  x8r.begin();
  pinMode(gunmotor, OUTPUT);
  pinMode(laserpointer, OUTPUT);
  pinMode(hoppermotor, OUTPUT);
  pinMode(hopperdir, OUTPUT);
  pinMode(lightsensor, INPUT);
  computer.begin(9600);
  SoftPWMBegin(SOFTPWM_NORMAL);
}
uint16_t converttospdyaw(float n) {
  float x = 1020.0 + 500.0 * n;
  int y = (int) x;
  uint16_t z = (uint16_t) y;
  return z;
}
uint16_t converttospdpitch(float n) {
  float x = 1020.0 + 200.0 * n;
  int y = (int) x;
  uint16_t z = (uint16_t) y;
  return z;
}
int spdnow = 0;
bool dir = true;
int spdstep(int i, int bound1, int bound2, int stepsize) {
  if (dir) {
    if (i >= bound2) {
      dir = false;
      return i;
    }
    else {
      i += stepsize;
      return i;
    }
  }
  else {
    if (i <= bound1) {
      dir = true;
      return i;
    }
    else {
      i -= stepsize;
      return i;
    }
  }
}
float bytetospd(int i, int bound) {
  int j = abs(i);
  if (j < bound) {
    i = 0;
  }
  float newspd = (float) i / 127.0;
  return newspd;
}
int bytesfound = 0;
float spd[16];
int convspds[16];
bool sweepormove = false;
bool testgun = true;
void loop() {
  for (int i = 0; i < 16; i++) {
    gimbals[i] = 0;
    spd[i] = 0.0;
    convspds[i] = 1020;
  }
  if (sweepormove) {
    if (x8r.readCal(&channels[0], &failSafe, &lostFrames)) {

      // write the SBUS packet to an SBUS compatible servo
      for (int i = 0; i < 3; i++) {
        //computer.println(channels[i]);
        gimbals[i] = (channels[i]);
        computer.println(channels[i]);
      }
      //x8r.write(gimbals);
      //computer.print(gimbals);
    }
    else {
      computer.println("no packet");
    }
    /*while (computer.available()) {
      computer.read();
      }*/

  }
  else {


    // look for a good SBUS packet from the receiver
    /**/
    //else{
    //spdnow = spdstep(spdnow, -100, 100, 1);
    //float fltspd = ((float) spdnow) / 100.0;
    float fltspd = 0.0;
    int spdsend = converttospdpitch(fltspd);
    gimbals[0] = spdsend;
    spdsend = converttospdyaw(fltspd);
    gimbals[1] = spdsend;
    // gimbals[1] = spdsend;
    //}
    x8r.write(gimbals);
    computer.println(gimbals[0]);
    delay(30);
  }
  if (computer.available() && testgun) {
    int a = computer.read();
    //computer.print(a);
    analogWrite(gunmotor, GUN_DIR);
    delay(550);
    hopperDriver(1, HOPPER_MOTOR);
    analogWrite(gunmotor, 0);
    delay(2500);
    hopperDriver(0, HOPPER_MOTOR);
    analogWrite(gunmotor, GUN_DIR);
    delay(1700);
    analogWrite(gunmotor, 0);
    hopperDriver(2, HOPPER_MOTOR);
    delay(500);
    hopperDriver(0, HOPPER_MOTOR);
  }
}
