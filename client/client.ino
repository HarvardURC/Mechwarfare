#include <SoftwareSerial.h>
#include <Servo.h>
#include <PololuMaestro.h>

#include "client.h"

SoftwareSerial maestro_serial(8, 9);
MiniMaestro maestro(maestro_serial);

stance_t current_stance;

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

void shoot() {
    digitalWrite(6, LOW);
}

void no_shoot() {
    digitalWrite(6, HIGH);
}

void reload() {
    digitalWrite(5, LOW);
}

void no_reload() {
    digitalWrite(5, HIGH);
}

void setup() {
    Serial.begin(9600);
    maestro_serial.begin(9600);

    pinMode(6, OUTPUT);
    pinMode(5, OUTPUT);

    no_shoot();
    no_reload();

    delay(3000);

    exec(HOME_STANCE, STANCE_LEN);

    current_stance = HOME;

    delay(500);
}

bool in_range(float begin, float theta, float end) {
    return begin <= theta && theta < end;
}

bool points_up(float theta) {
    return in_range(M_PI/4, theta, 3 * M_PI/4);
}

bool points_down(float theta) {
    return in_range(-3 * M_PI/4, theta, -M_PI/4);
}

bool points_right(float theta) {
    return in_range(-M_PI/4, theta, M_PI/4);
}

bool points_left(float theta) {
    return in_range(3 * M_PI/4, theta, M_PI) || in_range(-M_PI, theta, -3 * M_PI/4);
}

void process(int pos_x, int pos_y, int acc_x, int acc_y, int acc_z, int z_dwn, int c_dwn) {
    float radius = sqrt(pos_x * pos_x + pos_y * pos_y);
    float theta = atan2(pos_y, pos_x);

    if (30 < radius) {
        if (z_dwn && c_dwn) {
            if (points_up(theta)) {
                shoot();
            } else if (points_down(theta)) {
                reload();
            } else {
                no_shoot();
                no_reload();
            }
        } else if (z_dwn) {
            if (points_right(theta)) {
                maestro.setTarget(TURRET_PAN, TURRET_PAN_RIGHT);
            } else if (points_left(theta)) {
                maestro.setTarget(TURRET_PAN, TURRET_PAN_LEFT);
            } else {
                maestro.setTarget(TURRET_PAN, TURRET_PAN_CENTER);
            }

            maestro.setTarget(TURRET_TILT, HOME_POS[TURRET_TILT] += pos_y/2);

            no_shoot();
            no_reload();
        } else {
            no_shoot();
            no_reload();

            if (points_up(theta)) {
                switch (current_stance) {
                    case FRONT:
                        exec(CREEP_F_TO_HOME, CREEP_TO_HOME_LEN);
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_FORWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case BACK:
                        exec(CREEP_B_TO_HOME, CREEP_TO_HOME_LEN);
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_FORWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case LEFT:
                        exec(CREEP_FORWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case RIGHT:
                        exec(CREEP_FORWARD_FROM_R, CREEP_LEN);

                        current_stance = LEFT;
                    break;
                    case HOME:
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_FORWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                }
            } else if (points_down(theta)) {
                switch (current_stance) {
                    case FRONT:
                        exec(CREEP_F_TO_HOME, CREEP_TO_HOME_LEN);
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_BACKWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case BACK:
                        exec(CREEP_B_TO_HOME, CREEP_TO_HOME_LEN);
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_BACKWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case LEFT:
                        exec(CREEP_BACKWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;
                    break;
                    case RIGHT:
                        exec(CREEP_BACKWARD_FROM_R, CREEP_LEN);

                        current_stance = LEFT;
                    break;
                    case HOME:
                        exec(HOME_TO_CREEP_L, HOME_TO_CREEP_LEN);
                        exec(CREEP_BACKWARD_FROM_L, CREEP_LEN);

                        current_stance = RIGHT;

                    break;
                }
            } else if (points_right(theta)) {
                if (c_dwn) {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_F_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case BACK:
                            exec(CREEP_B_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case LEFT:
                            exec(CREEP_L_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case RIGHT:
                            exec(CREEP_R_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                    }

                    exec(TURN_R, TURN_LEN);
                } else {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_RIGHT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case BACK:
                            exec(CREEP_RIGHT_FROM_B, CREEP_LEN);

                            current_stance = FRONT;
                        break;
                        case LEFT:
                            exec(CREEP_L_TO_HOME, CREEP_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_RIGHT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case RIGHT:
                            exec(CREEP_R_TO_HOME, CREEP_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_RIGHT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case HOME:
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_RIGHT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                    }
                }
            } else /* if (points_left(theta)) */ {
                if (c_dwn) {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_F_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case BACK:
                            exec(CREEP_B_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case LEFT:
                            exec(CREEP_L_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                        case RIGHT:
                            exec(CREEP_R_TO_HOME, CREEP_TO_HOME_LEN);

                            current_stance = HOME;
                        break;
                    }

                    exec(TURN_L, TURN_LEN);
                } else {
                    switch (current_stance) {
                        case FRONT:
                            exec(CREEP_LEFT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case BACK:
                            exec(CREEP_LEFT_FROM_B, CREEP_LEN);

                            current_stance = FRONT;
                        break;
                        case LEFT:
                            exec(CREEP_L_TO_HOME, CREEP_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_LEFT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case RIGHT:
                            exec(CREEP_R_TO_HOME, CREEP_TO_HOME_LEN);
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_RIGHT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                        case HOME:
                            exec(HOME_TO_CREEP_F, HOME_TO_CREEP_LEN);
                            exec(CREEP_LEFT_FROM_F, CREEP_LEN);

                            current_stance = BACK;
                        break;
                    }
                }
            }
        }

    } else {
        no_shoot();
        no_reload();
        maestro.setTarget(TURRET_PAN, TURRET_PAN_CENTER);
    }
}

void loop() {
    Serial.readStringUntil('[');

    String str = Serial.readStringUntil(']');

    int begin = 0;
    int end = str.indexOf(",");
    int pos_x = str.substring(begin, end).toInt();

    begin = end + 1;
    end = str.indexOf(",", begin);
    int pos_y = str.substring(begin, end).toInt();

    begin = end + 1;
    end = str.indexOf(",", begin);
    int acc_x = str.substring(begin, end).toInt();

    begin = end + 1;
    end = str.indexOf(",", begin);
    int acc_y = str.substring(begin, end).toInt();

    begin = end + 1;
    end = str.indexOf(",", begin);
    int acc_z = str.substring(begin, end).toInt();

    begin = end + 1;
    end = str.indexOf(",", begin);
    int z_dwn = str.substring(begin, end).toInt();

    int c_dwn = str.substring(end + 1).toInt();

    process(pos_x, pos_y, acc_x, acc_y, acc_z, z_dwn, c_dwn);
}
