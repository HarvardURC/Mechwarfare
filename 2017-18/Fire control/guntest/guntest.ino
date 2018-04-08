
int gunmotor = A6;
int laserpointer = 2;
int hoppermotor = 9;
int hopperdir = 8;
int lightsensor = 14;
#define IDLE_SWITCH 0
#define GUN_CHANNEL 0
#define GUN_COMMAND 0
#define LEG_CHANNEL_START 0
#define AIM_CHANNEL 0
#define LIGHT_SENSOR 0
#define HOPPER_MOTOR 255
#define MANUAL_CHANNEL 0
#define GUN_DIR 100
#define computer Serial
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
  // put your setup code here, to run once:
  pinMode(gunmotor, OUTPUT);
  pinMode(laserpointer, OUTPUT);
  pinMode(hoppermotor, OUTPUT);
  pinMode(hopperdir, OUTPUT);
  pinMode(lightsensor, INPUT);
  computer.begin(9600);
}
int hol;
void loop() {
  // put your main code here, to run repeatedly:
 if(computer.available()){
   int a = computer.read();
   analogWrite(gunmotor, GUN_DIR);
   hopperDriver(1, HOPPER_MOTOR);
   delay(0);
   analogWrite(gunmotor, 0);
   delay(500);
   computer.print("hi");
 }
}
