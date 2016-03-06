//: Include Ardunio libraries
#include <SoftwareSerial.h>
#include <Servo.h>
#include <PololuMaestro.h>

//: Include Macro Definitions
#include "client.h"

#include "math.h"

//: variable declarations
SoftwareSerial maestro_serial(MAESTRO_RX, MAESTRO_TX);
MiniMaestro maestro(maestro_serial);

SoftwareSerial xbee(XBEE_RX, XBEE_TX);

stance_t current_stance;

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
    Serial.begin(BAUD_RATE);
    maestro_serial.begin(BAUD_RATE);
    xbee.begin(BAUD_RATE);

    exec(TO_HOME, TO_HOME_LEN);

    delay(SETUP_DELAY_TIME);

    exec(HOME_TO_CREEP_R, HOME_TO_CREEP_LEN);
}

void test() {
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_R_TO_HOME,      CREEP_R_TO_HOME_LEN);
    exec(TURRET_V,             TURRET_V_LEN);
    exec(TURRET_H,             TURRET_H_LEN);
    exec(TURN_LEFT,            TURN_LEFT_LEN);
    exec(TURN_LEFT,            TURN_LEFT_LEN);
    exec(TURN_LEFT,            TURN_RIGHT_LEN);
    exec(TURN_LEFT,            TURN_RIGHT_LEN);
    exec(HOME_TO_CREEP_R,      HOME_TO_CREEP_R_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_LEN);
    exec(CREEP_L_TO_HOME,      HOME_TO_CREEP_LEN);
    exec(TURRET_V,             TURRET_V_LEN);
    exec(TURRET_H,             TURRET_H_LEN);
    exec(TURN_RIGHT,           TURN_LEN);
    exec(TURN_RIGHT,           TURN_LEN);
    exec(TURN_RIGHT,           TURN_LEN);
    exec(TURN_RIGHT,           TURN_LEN);
    exec(HOME_TO_CREEP_R,      HOME_TO_CREEP_R_LEN);
}

void print_data(int pos_x, int pos_y, int acc_x, int acc_y, int acc_z, int z_dwn, int c_dwn) {
    Serial.print("POS_X: ");
    Serial.print(pos_x);
    Serial.print(" ");

    Serial.print("POS_Y: ");
    Serial.print(pos_y);
    Serial.print(" ");

    Serial.print("ACC_X: ");
    Serial.print(acc_x);
    Serial.print(" ");

    Serial.print("ACC_Y: ");
    Serial.print(acc_y);
    Serial.print(" ");

    Serial.print("ACC_Z: ");
    Serial.print(acc_z);
    Serial.print(" ");

    Serial.print("Z_DWN: ");
    Serial.print(z_dwn);
    Serial.print(" ");

    Serial.print("C_DWN: ");
    Serial.print(c_dwn);
    Serial.print(" ");

    Serial.println();
}

void points_up(float theta) {
    return pi/4 <= theta && theta < 3 * pi/4;
}

void points_down(float theta) {
    return -3 * pi/4 <= theta && theta < -pi/4;
}

void points_left(float theta) {
    return 3 * pi/4 <= theta || theta < -3 * pi/4;
}

void points_right(float theta) {
    return -pi/4 <= theta && theta < pi/4;
}

void loop() {
    if (INPUT_SIZE <= xbee.available()) {
        int pos_x = xbee.read();
        int pos_y = xbee.read();

        int acc_x = xbee.read();
        int acc_y = xbee.read();
        int acc_z = xbee.read();

        int z_dwn = xbee.read();
        int c_dwn = xbee.read();

        print_data(pos_x, pos_y, acc_x, acc_y, acc_z, z_dwn, c_dwn);

        float radius = sqrt(pos_x * pos_x, pos_y * pos_y);

        if (MOVEMENT_THRESHOLD < radius) {
            float theta = atan2(pos_y, pos_x);

            /*
            There are three current movements. Creep, shuffle, and rotate. If
            no buttons are pressed, default movement is creep and strafe. Meaning, joystick
            turned forward moves robot forward (in creep mode), joystick to the right
            makes robot strafe to the right. Joystick back strafes back, etc.

            If z is pressed, then robots movements will be shuffle instead of creep.

            If c is pressed, then joystick left or right rotates the robot clockwise
            or counterclockwise respectively -- Robot WILL NOT strafe left or right.
            Joystick forward or backward will shuffle robot forward and backward.

            If c and z are pressed, joystick left or right still rotates the robot,
            but joystick forward and backward will shuffle robot forward and backward.
            */
            if (points_up(theta)) {
                if (z_dwn) {
                    exec(SHUFFLE_FORWARD, SHUFFLE_FORWARD_LEN);
                } else {
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
                }
            } else if (points_down(theta)) {
                if (z_dwn) {
                    exec(SHUFFLE_BACKWARD, SHUFFLE_BACKWARD_LEN);
                } else {
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
                } else if (z_dwn) {
                    exec(SHUFFLE_LEFT, SHUFFLE_LEFT_LEN);
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
                } else if (z_dwn) {
                    exec(SHUFFLE_RIGHT, SHUFFLE_RIGHT_LEN);
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
}
