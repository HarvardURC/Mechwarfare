//: Include Ardunio libraries
#include <SoftwareSerial.h>
#include <Servo.h>
#include <PololuMaestro.h>

//: Include Macro Definitions
#include "calibrate.h"

//: Global variable declarations
SoftwareSerial maestro_serial(8, 9);
MiniMaestro maestro(maestro_serial);

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
    Serial.begin(9600);
    maestro_serial.begin(9600);

    delay(3000);
    exec(HOME_STANCE, STANCE_LEN);
}

void loop() {
    calibrate();
}
