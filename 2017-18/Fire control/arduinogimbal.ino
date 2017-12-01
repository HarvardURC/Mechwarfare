#include <SBUS.h>
SBUS x8r(Serial2);
SBUS gimbal(Serial3);
// channel, fail safe, and lost frames data
float channels[16];
uint8_t failSafe;
uint16_t lostFrames = 0;
uint16_t gimbals[16];
bool serialread = false;
#define computer Serial
void setup() {
  // begin the SBUS communication
  x8r.begin();
  gimbal.begin();
  computer.begin(9600);
}
uint16_t converttospd(float n) {
  float x = 1020.0 + 500.0 * n;
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
  int j = (int) 10 * bound / 1000
  if (abs(i) < j) {
    i = 0;
  }
  float newspd = (float) i / 1000.0;
  return newspd;
}
int bytesfound = 0;
float spd[16];
int convspds[16];
void loop() {
  bytesfound = 0;
  for (int i = 0; i < 16; i++) {
    gimbals[i] = 0;
    spd[i] = 0.0;
    convspds[i] = 0;
  }
  if (serialread) {
    while (bytesfound < 2) {
      int center = 240 + bytesfound;
      if (computer.available()) {
        spd[bytesfound] = bytetospd(computer.parseInt(), center);
        bytesfound++;
      }
    }
    while (bytesfound > 0) {
      convspds[bytesfound] = converttospd(spd[bytesfound]);
      bytesfound--;
    }
    for (int l = 0; i < 2; i++) {
      gimbals[i] = convspds[i];
    }
    gimbal.write(gimbals);
    computer.println(gimbals[0]);
    delay(5);
    while (computer.available()) {
      computer.read();
    }
    computer.write(1);
  }
  else {


    // look for a good SBUS packet from the receiver
    /*if(x8r.readCal(&channels[0], &failSafe, &lostFrames)){

      // write the SBUS packet to an SBUS compatible servo
      for(int i=0; i<2; i++){
        //computer.println(channels[i]);
        gimbals[i]=converttospd(channels[i]);
      }
      }*/
    //else{
    spdnow = spdstep(spdnow, -100, 100, 1);
    float fltspd = ((float) spdnow) / 100.0;
    int spdsend = converttospd(fltspd);
    gimbals[0] = spdsend;
    //}
    gimbal.write(gimbals);
    computer.println(gimbals[0]);
    delay(5);
    computer.write(10);
  }
}
