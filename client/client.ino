//: Include Ardunio libraries
#include <SoftwareSerial.h>
#include <Servo.h>
#include <PololuMaestro.h>

//: Include Macro Definitions
#include "client.h"

//: Global variable declarations
SoftwareSerial maestro_serial(MAESTRO_RX, MAESTRO_TX);
MiniMaestro maestro(maestro_serial);
SoftwareSerial xbee(XBEE_RX, XBEE_TX);

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
    // Serial1.begin(BAUD_RATE_XBEE);

     pinMode(5, OUTPUT);
     pinMode(6, OUTPUT);

     digitalWrite(6, HIGH);
     digitalWrite(5, HIGH);

     delay(3000);

     exec(HOME_STANCE, HOME_STANCE_LEN);
     current_stance = HOME;

     delay(SETUP_DELAY_TIME);

     //exec(HOME_TO_CREEP_R, HOME_TO_CREEP_R_LEN);

   // test_movements();

}

// void print_data() {
//     Serial.print("POS_X: ");
//     Serial.print(pos_x);
//     Serial.print(" ");
//
//     Serial.print("POS_Y: ");
//     Serial.print(pos_y);
//     Serial.print(" ");
//
//     Serial.print("ACC_X: ");
//     Serial.print(acc_x);
//     Serial.print(" ");
//
//     Serial.print("ACC_Y: ");
//     Serial.print(acc_y);
//     Serial.print(" ");
//
//     Serial.print("ACC_Z: ");
//     Serial.print(acc_z);
//     Serial.print(" ");
//
//     Serial.print("Z_DWN: ");
//     Serial.print(z_dwn);
//     Serial.print(" ");
//
//     Serial.print("C_DWN: ");
//     Serial.print(c_dwn);
//     Serial.print(" ");
//
//     Serial.println();
// }

int points_up(float theta) {
    return M_PI/4 <= theta && theta < 3 * M_PI/4;
}

int points_down(float theta) {
    return -3 * M_PI/4 <= theta && theta < -M_PI/4;
}

int points_left(float theta) {
    return 3 * M_PI/4 <= theta || theta < -3 * M_PI/4;
}

int points_right(float theta) {
    return -M_PI/4 <= theta && theta < M_PI/4;
}

void process_data() {

    float radius = sqrt(pos_x * pos_x + pos_y * pos_y);
    float theta = atan2(pos_y, pos_x);

      //GUN AND RELOAD
//    if (z_dwn)
//    {
//      digitalWrite(6, LOW);
//    }
//    else
//    {
//      digitalWrite(6, HIGH);
//    }
//    if (c_dwn)
//    {
//      digitalWrite(5, LOW);
//    }
//    else
//    {
//      digitalWrite(5, HIGH);
//    }


    if (MOVEMENT_THRESHOLD < radius) {
          
          if (z_dwn)
          {
            // CONTROL PAN
            if (points_left(theta))
            {
              maestro.setTarget(12,5500);
            }
            else if (points_right(theta))
            {
              maestro.setTarget(12,6500);
            }
            else
            {
              maestro.setTarget(12,6000);
            }
            // CONTROL TILT
            HOME_POS[TURRET_TILT] += pos_y/2;
            maestro.setTarget(13,HOME_POS[TURRET_TILT]); // changing angle of tilt depending on joystick displacement
          }
          else
          {
            if (points_up(theta)) {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_F_TO_HOME, CREEP_F_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case BACK:
                            exec(CREEP_B_TO_HOME, CREEP_B_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case LEFT:
                            exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case RIGHT:
                            exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);

                            current_stance = LEFT;
                        break;
                        case HOME:
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                    }
                } else if (points_down(theta)) {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_F_TO_HOME, CREEP_F_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_BACKWARD_FROM_L, CREEP_BACKWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case BACK:
                            exec(CREEP_B_TO_HOME, CREEP_B_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_BACKWARD_FROM_L, CREEP_BACKWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case LEFT:
                            exec(CREEP_BACKWARD_FROM_L, CREEP_BACKWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                        case RIGHT:
                            exec(CREEP_BACKWARD_FROM_R, CREEP_BACKWARD_FROM_R_LEN);

                            current_stance = LEFT;
                        break;
                        case HOME:
                            exec(HOME_TO_CREEP_L, HOME_TO_CREEP_L_LEN);
                            exec(CREEP_BACKWARD_FROM_L, CREEP_BACKWARD_FROM_L_LEN);

                            current_stance = RIGHT;
                        break;
                    }
                } else if (points_left(theta)) {
                    if (c_dwn) {
                        switch (current_stance) {
                            case FRONT:
                                exec(CREEP_F_TO_HOME, CREEP_F_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case BACK:
                                exec(CREEP_B_TO_HOME, CREEP_B_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case LEFT:
                                exec(CREEP_L_TO_HOME, CREEP_L_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case RIGHT:
                                exec(CREEP_R_TO_HOME, CREEP_R_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                        }

                        exec(TURN_LEFT, TURN_LEFT_LEN);
                    } else {
                        switch (current_stance) {
                            case FRONT:
                                exec(CREEP_LEFT_FROM_F, CREEP_LEFT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case BACK:
                                exec(CREEP_LEFT_FROM_B, CREEP_LEFT_FROM_B_LEN);

                                current_stance = FRONT;
                            break;
                            case LEFT:
                                exec(CREEP_L_TO_HOME, CREEP_L_TO_HOME_LEN);
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_LEFT_FROM_F, CREEP_LEFT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case RIGHT:
                                exec(CREEP_R_TO_HOME, CREEP_R_TO_HOME_LEN);
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_RIGHT_FROM_F, CREEP_RIGHT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case HOME:
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_LEFT_FROM_F, CREEP_LEFT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                        }
                    }
                } else {
                    if (c_dwn) {
                        switch (current_stance) {
                            case FRONT:
                                exec(CREEP_F_TO_HOME, CREEP_F_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case BACK:
                                exec(CREEP_B_TO_HOME, CREEP_B_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case LEFT:
                                exec(CREEP_L_TO_HOME, CREEP_L_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                            case RIGHT:
                                exec(CREEP_R_TO_HOME, CREEP_R_TO_HOME_LEN);

                                current_stance = HOME;
                            break;
                        }

                        exec(TURN_LEFT, TURN_LEFT_LEN);
                    } else {
                        switch (current_stance) {
                            case FRONT:
                                exec(CREEP_RIGHT_FROM_F, CREEP_RIGHT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case BACK:
                                exec(CREEP_RIGHT_FROM_B, CREEP_RIGHT_FROM_B_LEN);

                                current_stance = FRONT;
                            break;
                            case LEFT:
                                exec(CREEP_L_TO_HOME, CREEP_L_TO_HOME_LEN);
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_RIGHT_FROM_F, CREEP_RIGHT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case RIGHT:
                                exec(CREEP_R_TO_HOME, CREEP_R_TO_HOME_LEN);
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_RIGHT_FROM_F, CREEP_RIGHT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                            case HOME:
                                exec(HOME_TO_CREEP_F, HOME_TO_CREEP_F_LEN);
                                exec(CREEP_RIGHT_FROM_F, CREEP_RIGHT_FROM_F_LEN);

                                current_stance = BACK;
                            break;
                        }
                    }
                }
          }
      }
      else
      {
        maestro.setTarget(12,6000);
      }
}

void loop() {

    // Get data using the string method
    
    Serial.readStringUntil('[');
    str = Serial.readStringUntil(']');
    int begin = 0;
    int end = str.indexOf(",");
    pos_x = str.substring(begin, end).toInt();
    begin = end + 1;
    end = str.indexOf(",", begin);
    pos_y = str.substring(begin, end).toInt();
    begin = end + 1;
    end = str.indexOf(",", begin);
    acc_x = str.substring(begin, end).toInt();
    begin = end + 1;
    end = str.indexOf(",", begin);
    acc_y = str.substring(begin, end).toInt();
    begin = end + 1;
    end = str.indexOf(",", begin);
    acc_z = str.substring(begin, end).toInt();
    begin = end + 1;
    end = str.indexOf(",", begin);
    z_dwn = str.substring(begin, end).toInt();
    c_dwn = str.substring(end + 1).toInt();

    //print_data();
    process_data();



}


