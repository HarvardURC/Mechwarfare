#include <SBUS.h>
SBUS x8r(Serial1);
#define gimbal x8r;
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
  int j = 127;
  if (abs(i-j) < bound) {
    i = 127;
  }
  float newspd = (((float) i)-127.0) / 127.0;
  if(newspd>1.0){
    newspd=1.00;
  }
  if(newspd<-1.00){
    newspd=-1.00;
  }
  return newspd;
}
int bytesfound = 0;
int itemfound[2];
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
      int center = 260 + bytesfound*60;
      if (computer.available()) {
        spd[bytesfound] = bytetospd(computer.parseInt(), 10);
        computer.println(bytesfound);
        computer.println(spd[bytesfound]);
        bytesfound++;
      }
      else{
        
      }
    }
    while (bytesfound >= 0) {
      convspds[bytesfound] = converttospd(spd[bytesfound]);
      bytesfound--;
    }
    for (int i = 0; i < 2; i++) {
      gimbals[i] = convspds[i];
    }
    x8r.write(gimbals);
    //computer.println(gimbals[0]);
    delay(10);
    while (computer.available()) {
      computer.read();
    }
    computer.println(3);
    computer.println(gimbals[0]);
    computer.println(gimbals[1]);
  }
  else {

for (int i = 0; i < 16; i++) {
    gimbals[i] = 0;
  }
  // look for a good SBUS packet from the receiver
    spdnow = spdstep(spdnow, -100, 100, 1);
    float fltspd = ((float) spdnow) / 100.0;
    int spdsend = converttospd(fltspd);
    gimbals[0] = spdsend;
    gimbals[1]=spdsend;
    // write the SBUS packet to an SBUS compatible servo
    x8r.write(gimbals);
    computer.println(gimbals[0]);
    delay(10);
  }
}
