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

/*NOTES ON SWITCH INTERPRETATION:  IDLESWITCH ON:  GO IDLE.  GUNSWITCH ON:  ACTIVE FIRE/RELOAD.  JAMSWITCH ON:  UNJAM.*/


/*
  GENERAL STATE DIAGRAM:

  IDLE STATE:  REMAIN IN UNTIL THE IDLE SWITCH IS FLIPPED, AT WHICH POINT TRANSITION TO LOAD STATE.  OTHERWISE DO NOTHING.
  ALL BELOW STATES TRANSITION TO IDLE IF IDLE SWITCH IS FLIPPED:
  QUIET LOAD STATE:  IF THE HOPPER HASN'T CAUGHT UP TO THE GUN (LOADED NEW ROUNDS) RUN THE HOPPER, OTHERWISE WAIT FOR GUN COMMAND TO TRANSITION TO ACTIVE FIRE
  ACTIVE FIRE STATE: RUN GUNMOTOR AND HOPPER MOTOE, TRANSITIONING TO QUIET LOAD IF FIRE BUTTON RELEASED, TRANSITION TO UNJAM IF JAM COMMAND SENT OTHERWISE RUN GUNMOTOR AND HOPPER UNTIL TIME COMES FOR ACTIVE RELOAD
  ACTIVE RELOAD: SHUT OFF GUN MOTOR TO ALLOW CATCHUP TIME FOR HOPPER, TRANSITION TO QUIET LOAD IF FIRE BUTTON RELEASED, TRANSITION TO UNJAM IF JAM COMMAND SENT, OTHERWISE KEEP GUNMOTOR OFF AND RUN HOPPER UNTIL TIME COMES FOR ACTIVE FIRE
  UNJAM:  SHUT OFF GUN MOTOR, RUN HOPPER MOTOR BACKWARDS UNTIL TIME FOR UNJAM RUNS OUT, THEN GO TO QUIET LOAD
*/


#define computer Serial


// Defines for retrieving remote control signals

volatile uint16_t state[8];

volatile unsigned long timers[8];

#define CH1 23
#define CH2 22
#define CH3 21
#define CH4 19
#define CH5 18
#define CH6 17
#define CH7 16
#define CH8 15

//remote control channels
#define IDLE_SWITCH 7
#define GUN_CHANNEL 4
#define SWITCH_BOUND 1200
#define SWITCH_BOUND_JAM 1200
#define JAM_CHANNEL 0


//Comms defines for comms with gun subsystems
int gunmotor = 6;
int laserpointer = 2;
int hoppermotor = 9;
int hopperdir = 8;

#define HOPPER_MOTOR 255
#define GUN_DIR 255

#define IDLE_THRESHOLD 1000
#define UPDATE_THRESHOLD 10
unsigned long idleTimer; //  hold milliseconds since last state update
void resetIdleTimer()
{
  idleTimer = millis();
}

void setup() {
  // begin the SBUS communication

  Serial.begin(9600);
  pinMode(gunmotor, OUTPUT);
  pinMode(laserpointer, OUTPUT);
  pinMode(hoppermotor, OUTPUT);
  pinMode(hopperdir, OUTPUT);
  pinMode(lightsensor, INPUT);
   pinMode(CH1,INPUT);
  pinMode(CH2,INPUT);
  pinMode(CH3,INPUT);
  pinMode(CH4,INPUT);
  pinMode(CH5,INPUT);
  pinMode(CH6,INPUT);
  pinMode(CH7,INPUT);
  pinMode(CH8,INPUT);
  attachInterrupt(CH1,interrupt1,CHANGE);
  attachInterrupt(CH2,interrupt2,CHANGE);
  attachInterrupt(CH3,interrupt3,CHANGE);
  attachInterrupt(CH4,interrupt4,CHANGE);
  attachInterrupt(CH5,interrupt5,CHANGE);
  attachInterrupt(CH6,interrupt6,CHANGE);
  attachInterrupt(CH7,interrupt7,CHANGE);
  attachInterrupt(CH8,interrupt8,CHANGE);

  idleTimer = millis();
}
//Reads Pulse length manually -- basically softPWM
void interrupt1(){
    if(digitalReadFast(CH1) == 1){         
      timers[1] = micros();
    }
    else {
      state[1] = micros() - timers[1];
   }
}
void interrupt2(){
    if(digitalReadFast(CH2) == 1){         
      timers[2] = micros();
    }
    else {
      state[2] = micros() - timers[2];
   }
}
void interrupt3(){
    if(digitalReadFast(CH3) == 1){         
      timers[3] = micros();
    }
    else {
      state[3] = micros() - timers[3];
   }
}
void interrupt4(){
    if(digitalReadFast(CH4) == 1){         
      timers[4] = micros();
    }
    else {
      state[4] = micros() - timers[4];
   }
}
void interrupt5(){
    if(digitalReadFast(CH5) == 1){         
      timers[5] = micros();
    }
    else {
      state[5] = micros() - timers[5];
   }
}
void interrupt6(){
    if(digitalReadFast(CH6) == 1){         
      timers[6] = micros();
    }
    else {
      state[6] = micros() - timers[6];
   }
}
void interrupt7(){
    if(digitalReadFast(CH7) == 1){         
      timers[7] = micros();
    }
    else {
      state[7] = micros() - timers[7];
   }
}
void interrupt8(){
    if(digitalReadFast(CH8) == 1){         
      timers[8] = micros();
    }
    else {
      state[8] = micros() - timers[8];
   }
}
int stateGun = 0;

//Hopper controller
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


// needs code
//int numCock = 150;
//int numLoad = 350;
int numCatchUp = 500;
int numFire = 150;
int numReload = 200;
int numUnjam = 200;
int stateHold = 0;



int gunState(int currState)
{
  switch (currState) {
    //idle state for gun
    case 0:
      hopperDriver(0, 0);
      analogWrite(gunmotor, 0);
      if (state[IDLE_SWITCH] > SWITCH_BOUND) {
        //if no longer idle
        stateHold = 0;
        return 1;
      }
      return 0;
    case 1:
      //load state
      if (state[IDLE_SWITCH] < SWITCH_BOUND) {
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
      if (state[GUN_CHANNEL] > SWITCH_BOUND) {
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
      if (state[IDLE_SWITCH] < SWITCH_BOUND) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (state[JAM_CHANNEL] > SWITCH_BOUND_JAM) {
        //then unjam
        stateHold = 0;
        return 4;
      }
      if (state[GUN_CHANNEL] < SWITCH_BOUND) {
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
      if (state[IDLE_SWITCH] == 0) {
        //if idle
        stateHold = 0;
        return 0;
      }
      if (state[JAM_CHANNEL] > SWITCH_BOUND_JAM) {
        //then unjam
        stateHold = 0;
        return 4;
      }
      if (state[GUN_CHANNEL] < SWITCH_BOUND) {
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
      if (state[IDLE_SWITCH] > SWITCH_BOUND) {
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
  //send remote control info to pi, load in channel by channel
  String baseString = "";
  for (int i = 0; i < 10; i++){
  baseString = baseString + String(state[i]) + ", ";
  }
  baseString = baseString + String(state[10]);
  computer.print(baseString);
}




void loop() {
  //timed interrupt on gun and leg state
  if (millis() - idleTimer > UPDATE_THRESHOLD) {
    
    resetIdleTimer();
    stateGun = gunState(stateGun);
    legCode();

  }
  

}
