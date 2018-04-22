//Use existing packet check to reset watchdog
//Add jammed state/ check to hopper/ gun control  DONE (with more code needed)
//Use PWM pin for gun motor
//Add current state comments to every state DONE
//Add comments to everything else DONE
//Send idle packet to Pi DONE
//No hardcoded numbers. Define at top. DONE
//Do all the Pi communication in one place
//Don't name communications "leg"
//Add manual aiming state and associated code DONE
//Add packets for gimbal control from Pi
//Write the control loop for the camera to gimbal in a more standard form (regular PID?). Add optional low pass filter to sensor data  DONE
//Timer interrupts for running state machine at constant frequency; decouple control code  DONE

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
#define LEG_CHANNEL_1 0
#define LEG_CHANNEL_2 0
#define LEG_CHANNEL_3 0
#define LEG_CHANNEL_4 0
#define LEG_CHANNEL_5 0
#define LEG_CHANNEL_6 0
#define LEG_CHANNEL_7 0
#define LEG_CHANNEL_8 0
#define HOPPER_MOTOR 255
#define MANUAL_CHANNEL 0
#define GUN_DIR 255
#define JAM_CHANNEL 0
#define JAM_COMMAND 255

//Comms defines for comms with gun subsystems
int gunmotor = 6;
int laserpointer = 2;
int hoppermotor = 9;
int hopperdir = 8;
int lightsensor = 14;

#define IDLE_THRESHOLD 1000
#define UPDATE_THRESHOLD 10
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
  pinMode(hopperdir, OUTPUT);
  pinMode(lightsensor, INPUT);
  pinMode(GUN_CHANNEL, INPUT);
  pinMode(IDLE_SWITCH, INPUT);
  pinMode(JAM_CHANNEL, INPUT);
  pinMode(LEG_CHANNEL_1, INPUT);
  pinMode(LEG_CHANNEL_2, INPUT);
  pinMode(LEG_CHANNEL_3, INPUT);
  pinMode(LEG_CHANNEL_4, INPUT);
  pinMode(LEG_CHANNEL_5, INPUT);
  pinMode(LEG_CHANNEL_6, INPUT);
  pinMode(LEG_CHANNEL_7, INPUT);
  pinMode(LEG_CHANNEL_8, INPUT);


  // attach an interrupt to the serial 1 reciever pin
  attachInterrupt(digitalPinToInterrupt(SERIAL1_PIN), resetIdleTimer, CHANGE);

  idleTimer = millis();
}

int stateGun = 0;
int stateLeg = 0;
//return condition for fire-idle
void hopperDriver(int inst, int power) {
  switch (inst) {
    case 0:
      //brake
      analogWrite(hoppermotor, 0);
      digitalWrite(hopperdir, LOW);
      break;
    case 1:
      //forward
      analogWrite(hoppermotor, power);
      digitalWrite(hopperdir, HIGH);
      break;
    case 2:
      //reverse
      analogWrite(hoppermotor, power);
      digitalWrite(hopperdir, LOW);
      break;
  }
}
void unjamcode() {
  hopperDriver(2, HOPPER_MOTOR);
}


// needs code
//int numCock = 150;
//int numLoad = 350;
int numCatchUp = 500;
int numFire = 150;
int numReload = 200;
int numUnjam = 200;
int stateHold = 0;
/*While fire button is help, alternate between running and not running gun.  When button is released, run hopper to ensure gun is loaded */
int gunState(int currState)
{
  switch (currState) {
    //idle state for gun
    case 0:
      hopperDriver(0, 0);
      analogWrite(gunmotor, 0);
      if (analogRead(IDLE_SWITCH) != 0) {
        //if no longer idle
        stateHold = 0;
        return 1;
      }
      return 0;
    case 1:
      //load state
      if (analogRead(IDLE_SWITCH) == 0) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (stateHold < numCatchUp) {
        //if not yet reloaded, reload
        hopperDriver(1, HOPPER_MOTOR);
      }
      else {
        //otherwise, wait for further commands
        hopperDriver(0, HOPPER_MOTOR);
      }
      analogWrite(gunmotor, 0);

      stateHold++;
      //change number later
      if (analogRead(GUN_CHANNEL) == GUN_COMMAND) {
        //move to fire
        stateHold = 0;
        return 2;
      }
      return 1;
    case 2:
      //fire state, active gun
      analogWrite(gunmotor, GUN_DIR);
      hopperDriver(1, HOPPER_MOTOR);
      stateHold++;
      if (analogRead(IDLE_SWITCH) == 0) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (analogRead(JAM_CHANNEL) == JAM_COMMAND) {
        //then unjam
        stateHold = 0;
        return 4;
      }
      if (analogRead(GUN_CHANNEL) != GUN_COMMAND) {
        //then enter quiet load state
        stateHold = 0;
        return 1;
      }
      if (stateHold > numFire) {
        //then enter active reload
        stateHold = 0;
        return 3;
      }

      return 2;
    case 3:
      //fire state, inactive gun
      analogWrite(gunmotor, 0);
      hopperDriver(1, HOPPER_MOTOR);
      stateHold++;
      if (analogRead(IDLE_SWITCH) == 0) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (analogRead(JAM_CHANNEL) == JAM_COMMAND) {
        //then unjam
        stateHold = 0;
        return 4;
      }
      if (analogRead(GUN_CHANNEL) != GUN_COMMAND) {
        //then enter quiet load state
        stateHold = 0;
        return 1;
      }
      if (stateHold > numCatchUp) {
        //then enter active fire
        stateHold = 0;
        return 2;
      }
      return 3;
    case 4:
      analogWrite(gunmotor, 0);
      hopperDriver(2, HOPPER_MOTOR);
      stateHold++;
      if (analogRead(IDLE_SWITCH) == 0) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (stateHold > numUnjam) {
        //then enter quiet load state
        stateHold = 0;
        return 1;
      }
      return 4;

  }


}


void legCode()
{
  //send remote control info to pi
  String baseString = "";
  baseString = baseString + String(analogRead(IDLE_SWITCH)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_1)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_2)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_3)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_4)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_5)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_6)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_7)) + ", ";
  baseString = baseString + String(analogRead(LEG_CHANNEL_8));
  computer.print(baseString);
}




void loop() {
  if (millis() - idleTimer > UPDATE_THRESHOLD) {
    // read from the remote controller
    if (x8r.readCal(&channels[0], &failSafe, &lostFrames)) {
      resetIdleTimer();
      // detect whenever we send a command to fire the gun
      stateGun = gunState(stateGun);
      // ...
      legCode();
    }
    else {
      // if it's been too long since we've recieved data from the controller...
      if (millis() - idleTimer > IDLE_THRESHOLD) {
        // make everything idle
        for (int i = 0; i < 16; i++) {
          channels[i] = 0;
        }
        stateGun = gunState(0);
        legCode();


      }
    }
  }


}
