

/*NOTES ON SWITCH INTERPRETATION:  IDLESWITCH ON:  GO IDLE.  GUNSWITCH ON:  ACTIVE FIRE/RELOAD.  JAMSWITCH ON:  UNJAM.*/


/*
  GENERAL STATE DIAGRAM:

  IDLE STATE:  REMAIN IN UNTIL THE IDLE SWITCH IS FLIPPED, AT WHICH POINT TRANSITION TO LOAD STATE.  OTHERWISE DO NOTHING.
  ALL BELOW STATES TRANSITION TO IDLE IF IDLE SWITCH IS FLIPPED:
  QUIET LOAD STATE, CATCHUP:  RUN THE HOPPER TIL CAUGHT UP, AT WHICH POINT TRANSITION TO QUIET LOAD: IDLE, WAIT FOR GUN COMMAND TO TRANSITION TO ACTIVE FIRE
  QUIET LOAD STATE, IDLE:  STAY IDLE IN GUN AND HOPPER, WAIT FOR GUN COMMAND TO TRANSITION TO ACTIVE FIRE
  ACTIVE FIRE STATE: RUN GUNMOTOR AND HOPPER MOTOE, TRANSITIONING TO QUIET LOAD IF FIRE BUTTON RELEASED, TRANSITION TO UNJAM IF JAM COMMAND SENT OTHERWISE RUN GUNMOTOR AND HOPPER UNTIL TIME COMES FOR ACTIVE RELOAD
  ACTIVE RELOAD: SHUT OFF GUN MOTOR TO ALLOW CATCHUP TIME FOR HOPPER, TRANSITION TO QUIET LOAD IF FIRE BUTTON RELEASED, TRANSITION TO UNJAM IF JAM COMMAND SENT, OTHERWISE KEEP GUNMOTOR OFF AND RUN HOPPER UNTIL TIME COMES FOR ACTIVE FIRE
  UNJAM:  SHUT OFF GUN MOTOR, RUN HOPPER MOTOR BACKWARDS UNTIL TIME FOR UNJAM RUNS OUT, THEN GO TO QUIET LOAD
*/


#define computer Serial
#define SERIAL_RATE 9600 // baud rate for comms with pi

// Defines for retrieving remote control signals
volatile uint16_t state[9];
volatile unsigned long timers[9];

//CHANNELS FOR PWM COMMS
#define CH1 23
#define CH2 22
#define CH3 21
#define CH4 19
#define CH5 18
#define CH6 17
#define CH7 16
#define CH8 15

//remote control channels and switch bounds for parsing
#define IDLE_SWITCH 8
#define GUN_CHANNEL 5
#define SWITCH_BOUND 1200
#define GUN_BOUND 1800
#define SWITCH_BOUND_JAM 1200 
#define JAM_CHANNEL 1


//Comms defines for comms with gun subsystems
int gunmotor = A6; 
int hoppermotor = 6;
int hopperdir = 7;

#define HOPPER_POWER 65 //PWM POWER TO RUN HOPPER
#define GUN_POWER 255 //PWM POWER TO RUN GUNMOTOR

#define STATE_DELAY 10 //DELAY BETWEEN STATE UPDATES

//times for state transitions
//ALL NUM INTS ARE IN UNITS OF MS (REAL TIME IS THE NUMBER, DIVISION BY STATE_DELAY IS FOR NUMBER OF STATE UPDATES
int numCatchUp = 500 / STATE_DELAY; //TIME FOR HOPPER TO CATCH UP TO GUN (WHEN WE TRANSITION TO QUIET LOAD FROM ACTIVE FIRE)
int numFire = 100 / STATE_DELAY; //TIME FOR GUN TO ACTIVELY FIRE
int numReload = 200 / STATE_DELAY; //TIME FOR GUN TO ACTIVELY RELOAD
int numUnjam = 200 / STATE_DELAY; //TIME FOR GUN TO UNJAM

int stateHold = 0; //HOLDS THE NUMBER OF TIMES WE'VE REMAINED ON A PARTICULAR STATE, USED FOR SCHEDULING

unsigned long idleTimer; //  hold milliseconds since last state update
void resetIdleTimer()
{
  idleTimer = millis();
}

void setup() {
  // begin the SBUS communication

  Serial.begin(SERIAL_RATE); //HAVE SERIAL RATE DEFINE
  pinMode(gunmotor, OUTPUT);
  pinMode(hoppermotor, OUTPUT);
  pinMode(hopperdir, OUTPUT);
  pinMode(CH1, INPUT);
  pinMode(CH2, INPUT);
  pinMode(CH3, INPUT);
  pinMode(CH4, INPUT);
  pinMode(CH5, INPUT);
  pinMode(CH6, INPUT);
  pinMode(CH7, INPUT);
  pinMode(CH8, INPUT);
  attachInterrupt(CH1, interrupt1, CHANGE);
  attachInterrupt(CH2, interrupt2, CHANGE);
  attachInterrupt(CH3, interrupt3, CHANGE);
  attachInterrupt(CH4, interrupt4, CHANGE);
  attachInterrupt(CH5, interrupt5, CHANGE);
  attachInterrupt(CH6, interrupt6, CHANGE);
  attachInterrupt(CH7, interrupt7, CHANGE);
  attachInterrupt(CH8, interrupt8, CHANGE);

  idleTimer = millis();
}
//Reads Pulse length
void interrupt1() {
  if (digitalReadFast(CH1) == 1) {
    timers[1] = micros();
  }
  else {
    state[1] = micros() - timers[1];
  }
}
void interrupt2() {
  if (digitalReadFast(CH2) == 1) {
    timers[2] = micros();
  }
  else {
    state[2] = micros() - timers[2];
  }
}
void interrupt3() {
  if (digitalReadFast(CH3) == 1) {
    timers[3] = micros();
  }
  else {
    state[3] = micros() - timers[3];
  }
}
void interrupt4() {
  if (digitalReadFast(CH4) == 1) {
    timers[4] = micros();
  }
  else {
    state[4] = micros() - timers[4];
  }
}
void interrupt5() {
  if (digitalReadFast(CH5) == 1) {
    timers[5] = micros();
  }
  else {
    state[5] = micros() - timers[5];
  }
}
void interrupt6() {
  if (digitalReadFast(CH6) == 1) {
    timers[6] = micros();
  }
  else {
    state[6] = micros() - timers[6];
  }
}
void interrupt7() {
  if (digitalReadFast(CH7) == 1) {
    timers[7] = micros();
  }
  else {
    state[7] = micros() - timers[7];
  }
}
void interrupt8() {
  if (digitalReadFast(CH8) == 1) {
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

int gunState(int currState)
{
  //Serial.println(currState);
  //Serial.println(state[GUN_CHANNEL]);
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
      //load state, catchup
      if (state[IDLE_SWITCH] < SWITCH_BOUND) {
        //if idle
        stateHold = 0;
        return 0;
      } 
      if (stateHold > numCatchUp) {
        //if caught up, move to idle quiet load
        stateHold = 0;
        return 5;
      }

      hopperDriver(1, HOPPER_POWER);

      analogWrite(gunmotor, 0);

      stateHold++;
     
      if (state[GUN_CHANNEL] > GUN_BOUND) {
        //move to fire
        stateHold = 0;
        return 2;
      }
      return 1;
    case 5:
      //load state, idle
      if (state[IDLE_SWITCH] < SWITCH_BOUND) {
        //if idle
        stateHold = 0;
        return 0;
      }
      hopperDriver(0, HOPPER_POWER);
      analogWrite(gunmotor, 0);
      stateHold++;

      if (state[GUN_CHANNEL] > GUN_BOUND) {
        //move to fire
        stateHold = 0;
        return 2;
      }
      return 5;
    case 2:
      //fire state, active gun
      analogWrite(gunmotor, GUN_POWER);
      hopperDriver(1, HOPPER_POWER);
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
      if (state[GUN_CHANNEL] < GUN_BOUND) {
        //then enter quiet load: catchup state
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
      hopperDriver(1, HOPPER_POWER);
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
      if (state[GUN_CHANNEL] < GUN_BOUND) {
        //then enter quiet load: catchup state
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
      computer.println("Unjam");
      analogWrite(gunmotor, 0);
      hopperDriver(2, HOPPER_POWER);
      stateHold++;
      if (state[IDLE_SWITCH] < SWITCH_BOUND) {
        //if idle
        computer.println("idle");
        stateHold = 0;
        return 0;
      }
      if (stateHold > numUnjam) {
        //then enter quiet load: catchup state
        computer.println("done unjam");
        stateHold = 0;
        return 1;
      }
      return 4;

  }


}

int numChannels = 8;
void forwardChannels()
{
  //send remote control info to pi, load in channel by channel
  String baseString = "";
  for (int i = 0; i < numChannels; i++) {
    baseString = baseString + String(state[i]) + ", ";
  }
  baseString = baseString + String(state[numChannels]);
  //computer.println(baseString);
}




void loop() {
  //timed interrupt on gun and leg state
  if (millis() - idleTimer > STATE_DELAY) {

    resetIdleTimer();
    stateGun = gunState(stateGun);
    forwardChannels();

  }


}
