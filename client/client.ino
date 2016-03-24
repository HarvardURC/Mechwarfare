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
String pos_x;
String pos_y;
String acc_x;
String acc_y;
String acc_z;
String z_dwn;
String c_dwn;

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

void test_movements() {
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

    /*
    digitalWrite(6, LOW);
    delay(1000);
    digitalWrite(6, HIGH);
    digitalWrite(7, LOW);
    delay(1000);
    digitalWrite(7, HIGH);
    */

    exec(TURN_LEFT,            TURN_LEFT_LEN);
    exec(TURN_LEFT,            TURN_LEFT_LEN);
    exec(TURN_LEFT,            TURN_RIGHT_LEN);
    exec(TURN_LEFT,            TURN_RIGHT_LEN);
    exec(HOME_TO_CREEP_R,      HOME_TO_CREEP_R_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_FORWARD_FROM_L, CREEP_FORWARD_FROM_L_LEN);
    exec(CREEP_FORWARD_FROM_R, CREEP_FORWARD_FROM_R_LEN);
    exec(CREEP_L_TO_HOME,      CREEP_L_TO_HOME_LEN);
    exec(TURRET_V,             TURRET_V_LEN);
    exec(TURRET_H,             TURRET_H_LEN);

    /*
    digitalWrite(6, HIGH);
    delay(1000);
    digitalWrite(6, LOW);
    digitalWrite(7, HIGH);
    delay(1000);
    digitalWrite(7, LOW);
    */

    exec(TURN_RIGHT,           TURN_RIGHT_LEN);
    exec(TURN_RIGHT,           TURN_RIGHT_LEN);
    exec(TURN_RIGHT,           TURN_RIGHT_LEN);
    exec(TURN_RIGHT,           TURN_RIGHT_LEN);
    exec(HOME_TO_CREEP_R,      HOME_TO_CREEP_R_LEN);
}

void setup() {
    Serial.begin(BAUD_RATE_XBEE);
    maestro_serial.begin(BAUD_RATE_SERVO);
    Serial1.begin(BAUD_RATE_XBEE);

    // pinMode(7, OUTPUT);
    // pinMode(6, OUTPUT);

    // digitalWrite(6, HIGH);
    // digitalWrite(7, HIGH);

    // delay(3000);

    // exec(HOME_STANCE, HOME_STANCE_LEN);

    // delay(SETUP_DELAY_TIME);

    // exec(HOME_TO_CREEP_R, HOME_TO_CREEP_R_LEN);

    //test_movements();
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

void process_data(int pos_x, int pos_y, int acc_x, int acc_y, int acc_z, int z_dwn, int c_dwn) {
    print_data(pos_x, pos_y, acc_x, acc_y, acc_z, z_dwn, c_dwn);

    float radius = sqrt(pos_x * pos_x + pos_y * pos_y);
    float theta = atan2(pos_y, pos_x);

    Serial.print("points_up ");
    Serial.println(points_up(theta));

    Serial.print("points_left ");
    Serial.println(points_left(theta));

    Serial.print("points_right ");
    Serial.println(points_right(theta));

    Serial.print("points_down ");
    Serial.println(points_down(theta));

    if (MOVEMENT_THRESHOLD < radius) {
        if (points_up(theta)) {
            HOME_POS[TURRET_TILT] += TURRET_TILT_ANGLE; // should it be plus or minus, what should tilt angle be?
        } else if (points_down(theta)) {
            HOME_POS[TURRET_TILT] -= TURRET_TILT_ANGLE;
        } else if (points_left(theta)) {
            HOME_POS[TURRET_PAN] = TURRET_PAN_LEFT;
            delay(TURRET_PAN_DELAY);
            HOME_POS[TURRET_PAN] = TURRET_PAN_HOME_POS;
        } else {
            HOME_POS[TURRET_PAN] = TURRET_PAN_RIGHT;
            delay(TURRET_PAN_DELAY);
            HOME_POS[TURRET_PAN] = TURRET_PAN_HOME_POS;
        }
    }

    exec(HOME_STANCE, HOME_STANCE_LEN);
}

void loop() {
    Serial1.readStringUntil('[');

    str = Serial1.readStringUntil(']');

    int begin = 0;
    int end = str.indexOf(",");

    pos_x = str.substring(begin, end);

    begin = end + 1;
    end = str.indexOf(",", begin);

    pos_y = str.substring(begin, end);

    begin = end + 1;
    end = str.indexOf(",", begin);

    acc_x = str.substring(begin, end);

    begin = end + 1;
    end = str.indexOf(",", begin);

    acc_y = str.substring(begin, end);

    begin = end + 1;
    end = str.indexOf(",", begin);

    acc_z = str.substring(begin, end);

    begin = end + 1;
    end = str.indexOf(",", begin);

    z_dwn = str.substring(begin, end);

    c_dwn = str.substring(end + 1);

    process_data(
        pos_x.toInt(), pos_y.toInt(), acc_x.toInt(), acc_y.toInt(),
        acc_z.toInt(), z_dwn.toInt(), c_dwn.toInt()
    );
}

void oldloop() {
    if (INPUT_SIZE <= Serial1.available()) {
        int pos_x = Serial1.read();
        int pos_y = Serial1.read();

        int acc_x = Serial1.read();
        int acc_y = Serial1.read();
        int acc_z = Serial1.read();

        int z_dwn = Serial1.read();
        int c_dwn = Serial1.read();

        // int shoot  = Serial1.read();
        // int reload = Serial1.read();

        print_data(pos_x, pos_y, acc_x, acc_y, acc_z, z_dwn, c_dwn);

        float radius = sqrt(pos_x * pos_x + pos_y * pos_y);

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
            if (z_dwn) {
                if (points_up(theta)) {
                    HOME_POS[TURRET_TILT] += TURRET_TILT_ANGLE; // should it be plus or minus, what should tilt angle be?
                } else if (points_down(theta)) {
                    HOME_POS[TURRET_TILT] -= TURRET_TILT_ANGLE;
                } else if (points_left(theta)) {
                    HOME_POS[TURRET_PAN] = TURRET_PAN_LEFT;
                    delay(TURRET_PAN_DELAY);
                    HOME_POS[TURRET_PAN] = TURRET_PAN_HOME_POS;
                } else {
                    HOME_POS[TURRET_PAN] = TURRET_PAN_RIGHT;
                    delay(TURRET_PAN_DELAY);
                    HOME_POS[TURRET_PAN] = TURRET_PAN_HOME_POS;
                }
            } else {
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
        } else {
            switch(current_stance) {
              case FRONT:
                  exec(FRONT_STANCE, FRONT_STANCE_LEN);
              break;
              case BACK:
                  exec(BACK_STANCE, BACK_STANCE_LEN);
              break;
              case LEFT:
                  exec(LEFT_STANCE, LEFT_STANCE_LEN);
              break;
              case RIGHT:
                  exec(RIGHT_STANCE, RIGHT_STANCE_LEN);
              break;
              case HOME:
                  exec(HOME_STANCE, HOME_STANCE_LEN);
              break;
            }
        }
    }
}
