//: Include Ardunio libraries
#include <SoftwareSerial.h>
#include <Servo.h>
#include <PololuMaestro.h>

//: Include Macro Definitions
#include "client.h"

//: Global variable declarations
SoftwareSerial maestro_serial(MAESTRO_RX, MAESTRO_TX);
MiniMaestro maestro(maestro_serial);

stance_t current_stance;

String str;
int pos_x;
int pos_y;
int acc_x;
int acc_y;
int acc_z;
int z_dwn;
int c_dwn;

unsigned long previousMillis = 0;        // will store last time LED was updated

// constants won't change :
const long interval = 100;


 void calibrate() {
     while (true) {
         Serial.println("Which servo?");
         Serial.setTimeout(3000);

         int servo = Serial.parseInt();

         if (0 <= servo && servo < NUM_SERVOS) {
             Serial.setTimeout(200);

             Serial.print("Tweaking servo: ");
             Serial.println(servo);

             while (true) {
                 maestro.setTarget(servo, HOME_POS[servo]);

                 int ctrl = Serial.parseInt();

                 if (ctrl == 2) {
                     HOME_POS[servo] += 50;
                 } else if (ctrl == 1) {
                     HOME_POS[servo] -= 50;
                 } else if (ctrl == 0) {
                     continue;
                 } else {
                     Serial.print("Final position: ");
                     Serial.println(HOME_POS[servo]);

                     break;
                 }
             }
         } else {
             break;
         }
     }

     Serial.setTimeout(100);

     Serial.print("Final Positions: ");

     for (int servo = 0; servo < NUM_SERVOS; servo++) {
         Serial.print(HOME_POS[servo]);
         Serial.print(" ");
     }

     Serial.setTimeout(1000);
 }

void exec(event_t events[], int len) {

    for (int idx = 0; idx < len; idx++) {
        int servo = events[idx].servo;
        int value = events[idx].value;

        if (servo == DELAY) {
            delay(value);
        } else {
            maestro.setTarget(servo, HOME_POS[servo] + value);
        }
    }
}


void setup() {
    Serial.begin(BAUD_RATE_XBEE);
    maestro_serial.begin(BAUD_RATE_SERVO);
   delay(SETUP_DELAY_TIME);
     exec(HOME_STANCE, HOME_STANCE_LEN);

}

void loop() {

    calibrate();


}
