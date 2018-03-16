//Use existing packet check to reset watchdog
//Add jammed state/ check to hopper/ gun control
//Use PWM pin for gun motor
//Add current state comments to every state
//Add comments to everything else
//Send idle packet to Pi
//No hardcoded numbers. Define at top.
//Do all the Pi communication in one place
//Don't name communications "leg"
//Add manual aiming state and associated code
//Add packets for gimbal control from Pi
//Write the control loop for the camera to gimbal in a more standard form (regular PID?). Add optional low pass filter to sensor data
//Timer interrupts for running state machine at constant frequency; decouple control code

//communication defines for comms with Pi and remote control
#include <SBUS.h>
SBUS x8r(Serial1);
#define computer Serial
#define gimbal x8r
#define SERIAL1_PIN 0

// channel, fail safe, and lost frames data
float channels[16];
uint8_t failSafe;
uint16_t lostFrames = 0;
uint16_t gimbals[3];

//remote control channels
#define IDLE_SWITCH 0
#define GUN_CHANNEL 0
#define GUN_COMMAND 0
#define LEG_CHANNEL_START 0
#define AIM_CHANNEL 0
#define LIGHT_SENSOR 0
#define HOPPER_MOTOR 0

//Comms defines for comms with gun subsystems
int gunmotor = 6;
int laserpointer = 2;
int hoppermotor = 9;
int lightsensor = 14;

#define IDLE_THRESHOLD 1000
unsigned long idleTimer; // number of milliseconds without recieving data from the controller
void resetIdleTimer()
{
  idleTimer = millis();
}

void setup() {
  // begin the SBUS communication
  x8r.begin();
  Serial.begin(9600);
  pinMode(gunmotor, OUTPUT);
  pinMode(laserpointer, OUTPUT);
  pinMode(hoppermotor, OUTPUT);
  pinMode(lightsensor, INPUT);

  // attach an interrupt to the serial 1 reciever pin
  attachInterrupt(digitalPinToInterrupt(SERIAL1_PIN), resetIdleTimer, CHANGE);

  idleTimer = millis();
}

int stateAim = 0;
int stateGun = 0;
int stateLeg = 0;
//return condition for fire-idle
bool donefiring() {
}
// needs code
int gunState(int currState)
{
  switch (currState) {
    //idle state for gun
    case 0:
      analogWrite(hoppermotor, 0);
      digitalWrite(gunmotor, LOW);
      if (channels[GUN_CHANNEL] == GUN_COMMAND) {
        //if remote control sends fire signal
        return 1;
      }
      return 0;
    case 1:
    //load state
      //might need more complex code here for loading
      analogWrite(hoppermotor, HOPPER_MOTOR);
      //change number later
      if (analogRead(lightsensor) >= LIGHT_SENSOR) {
        //if gun is loaded, move to fire
        return 2;
      }
      return 1;
    case 2:
    //fire state
      digitalWrite(gunmotor, HIGH);
      if (donefiring()) {
        return 0;
      }
      return 2;
  }


}

//needs code
void legCode()
{
  //send remote control info to pi
  String baseString = "";
  for (int i = 0; i < 16; i++) {
    baseString = baseString + String(channels[i]) + ", ";
  }
  computer.print(baseString);
}

int legState(int currState)
{
  switch (currState) {
    case 0:
    //legs idle
      if (channels[IDLE_SWITCH] > 0) {
        return 1;
      }
      return 0;
    case 1:
    //legs active
      legCode();
      if (channels[IDLE_SWITCH] == 0) {
        return 0;
      }
      return 1;
  }
}
uint16_t converttospd(float n) {
  //This is a janky hack that is annoying. Sad.
  //conversion of within pi targeting data into gimbal ready data
  float x = 1020.0 + 500.0 * n;
  int y = (int) x;
  uint16_t z = (uint16_t) y;
  return z;
}

//initialization and description for the sweep function
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
/*
 * Sample usage of sweeper:
 * for (int i = 0; i < 16; i++) {
    gimbals[i] = 0;
  }
    spdnow = spdstep(spdnow, -100, 100, 1);
    float fltspd = ((float) spdnow) / 100.0;
    int spdsend = converttospd(fltspd);
    gimbals[0] = spdsend;
    gimbals[1]=spdsend;
    // write the SBUS packet to an SBUS compatible servo
    x8r.write(gimbals);
 */
//conversion of bytes from the Pi into -1 to 1 float values for internal calculations, with low precision near the center to avoid jittering
float bytetospd(int i, int bound) {
  int j = 127;
  if (abs(i - j) < bound) {
    i = 127;
  }
  float newspd = (((float) i) - 127.0) / 127.0;
  if (newspd > 1.0) {
    newspd = 1.00;
  }
  if (newspd < -1.00) {
    newspd = -1.00;
  }
  return newspd;
}

int bytesfound = 0;
float spd[16];
int convspds[16];
void aimCode() {
  //If in aim state, then take in byte-based targeting data from computer, then convert to float, then convert to gimbal commands
  bytesfound = 0;
  for (int i = 0; i < 16; i++) {
    gimbals[i] = 0;
    spd[i] = 0.0;
    convspds[i] = 0;
  }
  while (bytesfound < 2) {
    int center = 260 + bytesfound * 60;
    if (computer.available()) {
      spd[bytesfound] = bytetospd(computer.parseInt(), 10);
      //computer.println(bytesfound);
      //computer.println(spd[bytesfound]);
      bytesfound++;
    }
    else {

    }
  }
  /*
   * Here is where we'd put PID calculations--the output should go into the spd array, or something of similar structure: an array with up to 16 elements, with float values between -1 and 1.
   */
  while (bytesfound >= 0) {
    convspds[bytesfound] = converttospd(spd[bytesfound]);
    bytesfound--;
  }
  //write new data to the gimbals
  for (int i = 0; i < 2; i++) {
    gimbals[i] = convspds[i];
  }
  x8r.write(gimbals);
  //computer.println(gimbals[0]);
  //purging the input buffer
  while (computer.available()) {
    computer.read();
  }
  //computer.println(3);
  //computer.println(gimbals[0]);
  //computer.println(gimbals[1]);

}
int aimState(int currState)
{
  switch (currState) {
    //idle state
    case 0:
      if (channels[IDLE_SWITCH] > 0) {
        return 1;
      }
      return 0;
    case 1:
    //automatic state
      aimCode();
      if (channels[IDLE_SWITCH] == 0) {
        return 0;
      }
      return 1;
     //NEED TO IMPLEMENT MANUAL STATE
  }

}
//functions for converting target data packets into packets for gimbal commands


void loop() {
  // read from the remote controller
  if (x8r.readCal(&channels[0], &failSafe, &lostFrames)) {
    // detect whenever we send a command to fire the gun
    if (channels [AIM_CHANNEL] >= 0) {
      stateAim = aimState(stateAim);
    }
    if (channels[GUN_CHANNEL] == GUN_COMMAND) {
      stateGun = gunState(stateGun);
      // ...
    }
    if (channels[LEG_CHANNEL_START] >= 0) {
      stateLeg = legState(stateLeg);
    }
    else {
      // if it's been too long since we've recieved data from the controller...
      if (millis() - idleTimer > IDLE_THRESHOLD) {
        // make everything idle
        for (int i = 0; i < 16; i++) {
          channels[i] = 0;
        }
        stateAim = aimState(0);
        stateGun = gunState(0);
        stateLeg = legState(0);


      }
    }

  }
}
