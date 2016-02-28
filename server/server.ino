//: Include Arduino Libraries
#include <SoftwareSerial.h>
#include <Wire.h>

//: Include Macro Definitions
#include "server.h"

//: variable declarations
int pos_x;
int pos_y;

int acc_x;
int acc_y;
int acc_z;

int other;

int z_dwn;
int c_dwn;

SoftwareSerial xbee(RX, TX);

//: helper functions
void Wire_write(int data, bool begin, bool end) {
    if (begin) {
        Wire.beginTransmission(NUNCHUCK_ADDRESS);
    }

    Wire.write(data);

    if (end) {
        Wire.endTransmission();
    }
}

int decrypt(int b) {
    return (b ^ DECRYPT_BYTE) + DECRYPT_BYTE;
}

void transform_data() {
    pos_x = map(pos_x, MIN_POS_X, MAX_POS_X, MIN_VAL, MAX_VAL);
    pos_y = map(pos_y, MIN_POS_Y, MAX_POS_Y, MIN_VAL, MAX_VAL);

    acc_x = acc_x << 2 | bitRead(other, 2) | bitRead(other, 3);
    acc_y = acc_y << 2 | bitRead(other, 4) | bitRead(other, 5);
    acc_z = acc_z << 2 | bitRead(other, 6) | bitRead(other, 7);

    z_dwn = 1 - bitRead(other, 0);
    c_dwn = 1 - bitRead(other, 1);
}

void transmit_data() {
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

    xbee.print(pos_x);
    xbee.print(pos_y);
    xbee.print(acc_x);
    xbee.print(acc_y);
    xbee.print(acc_z);
    xbee.print(z_dwn);
    xbee.print(c_dwn);
}

//: Arduino functions
void setup() {
    Serial.begin(BAUD_RATE);
    Wire.begin();

    Wire_write(MEMORY_ADDRESS, true, false);
    Wire_write(NULL_BYTE, false, true);
}

void loop() {
    Wire.requestFrom(NUNCHUCK_ADDRESS, INPUT_SIZE);

    if (INPUT_SIZE <= Wire.available()) {
        pos_x = decrypt(Wire.read());
        pos_y = decrypt(Wire.read());

        acc_x = decrypt(Wire.read());
        acc_y = decrypt(Wire.read());
        acc_z = decrypt(Wire.read());

        other = decrypt(Wire.read());

        transform_data();
        transmit_data();
    }

    Wire_write(NULL_BYTE, true, true);

    delay(DELAY_TIME);
}
