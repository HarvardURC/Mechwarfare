#include <PololuMaestro.h>
#include <SoftwareSerial.h>

// servo indicates which servo or -1 for delays
typedef struct rotation
{
  int servo;
  int degree;
};

// function declarations (needed because parameter is of custom type)
void execute(rotation commands[], int dir, int len);

// Motor controller constants
SoftwareSerial maestroSerial(10, 11);
MiniMaestro maestro(maestroSerial);

// rotation and delay constants
int std_delay = 250;

// turning
int rotation_raise = 1000;
int rotate = 2000;

//walk
int w_raise = 600;
int w_rot = 750;
int w_lean = 250;
int w_araise = 400;

//creep
int c_small_rot = 200;
int c_small_ankle = 200;
int c_knee = 600;
int c_ankle = 600;
int c_rot = 3000;
int c_small_rot = 1000;


/*
  #####################
  # Servo assignments #
  #####################
*/

// legs
int flh = 0; // front left hip
int flk = 1; // front left knee
int fla = 2; // front left ankle
int frh = 3; // front right hip
int frk = 4; // front right knee
int fra = 5; // front right ankle
int brh = 6; // back right hip
int brk = 7; // back right knee
int bra = 8; // back right ankle
int blh = 9; // back left hip
int blk = 10; // back left knee
int bla = 11; // back left ankle

// shuffle movement
int servo_homes[12] = {7704,3676,8296,5794,3092,8620,7222,3074,7780,6088,3584,8072};

// turret
int tp = 12; // turret pan
int tt = 13; // turret tilt


/*
  ######################
  # movement sequences #
  ######################
*/

// rotates bot right
rotation turn[27] =
{
  {flk, rotation_raise},
  {brk, rotation_raise},
  {-1, std_delay},
  {flh, rotate},
  {brh, rotate},
  {-1, std_delay},
  {flk, 0},
  {brk, 0},
  {frh, rotate},
  {blh, rotate},
  {-1, std_delay},
  {frk, rotation_raise},
  {blk, rotation_raise},
  {-1, std_delay},
  {frh, 0},
  {blh, 0},
  {flh, rotate},
  {brh, rotate},
  {-1, std_delay},
  {frk, rotation_raise},
  {blk, rotation_raise},
  {-1, std_delay},
  {frh, 0},
  {blh, 0},
  {-1, std_delay},
  {frk, 0},
  {blk, 0}
};

// shuffles bot forward
rotation shuffle[32] =
{
  {-1, std_delay},
  {flk, w_raise},
  {fla, w_araise},
  {brk, w_raise},
  {bra, w_araise},
  {-1, std_delay},
  {flh, -w_rot},
  {brh, w_rot},
  {-1, std_delay},
  {flk, 0},
  {fla, 0},
  {brk, 0},
  {bra, 0},
  {-1, std_delay},
  {frk, w_raise},
  {fra, w_araise},
  {blk, w_raise},
  {bla, w_araise},
  {-1, std_delay},
  {frh, w_rot},
  {blh, -w_rot},
  {-1, std_delay},
  {frk, 0},
  {fra, 0},
  {blk, 0},
  {bla, 0},
  {-1, std_delay},
  {flh, 0},
  {frh, 0},
  {blh, 0},
  {brh, 0},
  {-1, std_delay}
};

// creeping move
rotation creep[24] =
{
  {flh, c_small_rot},
  {brh, -c_small_rot},
  {fra, c_small_ankle},
  {fla, c_small_ankle},
  {bra, -c_small_ankle},
  {blk, c_knee},
  {bla, c_ankle},
  {-1, std_delay},
  {blh, c_rot},
  {flh, -c_rot}
  {-1, std_delay},
  {blk, 0},
  {bla, 0},
  {-1, std_delay},
  {brh, 0},
  {blh, -c_small_rot},
  {flh, c_small_rot},
  {flk, c_knee},
  {fla, c_ankle},
  {-1, std_delay},
  {flh, 0},
  {-1, std_delay},
  {flk, 0},
  {fla, 0}
}


// legs down
rotation start_pos[13] =
{
  {frh, 0},
  {frk, 0},
  {fra, 0},
  {flh, 0},
  {flk, 0},
  {fla, 0},
  {brh, 0},
  {brk, 0},
  {bra, 0},
  {blh, 0},
  {blk, 0},
  {bla, 0},
  {-1, std_delay}
};

void calibrate()
{
  while (true)
  {
    Serial.print("Which servo?\n");
    Serial.setTimeout(3000);
    int inp = Serial.parseInt();
    if (inp > -1 && inp < 14)
    {
      Serial.setTimeout(200);
      Serial.print("tweaking servo: ");
      Serial.println(inp);
      while(true)
      {
        maestro.setTarget(inp, servo_homes[inp]);
        int contrl = Serial.parseInt();
        if (contrl == 2)
        {
          servo_homes[inp] += 50;
        }
        else if (contrl == 1)
        {
          servo_homes[inp] -= 50;
        }
        else if (contrl != 0)
        {
          Serial.print("final pos: ");
          Serial.println(servo_homes[inp]);
          break;
        }
      }
    }
    Serial.setTimeout(100);
    Serial.print("final position matrix: ");
    for(int i = 0; i < 13; i++)
    {
      Serial.print(servo_homes[i]);
      Serial.print(", ");
    }
    Serial.println(servo_homes[13]);
    Serial.setTimeout(1000);
    return;
  }
}


/*
  ######################
  # Movement functions #
  ######################
*/

// dir = 0 for forward, 1 for backwards.
void execute(rotation commands[], int dir, int len)
{
  if (dir == 1)
  {
    for(int i = len-1; i >= 0; i--)
    {
      if(commands[i].servo == -1)
      {
        delay(commands[i].degree);
      }
      else
      {
        maestro.setTarget(commands[i].servo, servo_homes[commands[i].servo] + commands[i].degree);
      }
    }
  }
  else
  {
    for(int i = 0; i < len; i++)
    {
      if(commands[i].servo == -1)
      {
        delay(commands[i].degree);
      }
      else
      {
        maestro.setTarget(commands[i].servo, servo_homes[commands[i].servo] + commands[i].degree);
      }
    }
  }
}

void turn_right()
{
  execute(turn, 0, 27);
}

void shuffle_walk()
{
  execute(shuffle, 0, 32);
}

void stand()
{
  execute(start_pos, 0, 13);
}

void creep_walk()
{
  execute(creep, 0, 24);
}


/*
  ##################
  # Main functions #
  ##################
*/

void setup()
{

  // Set the serial port's baud rate
  maestroSerial.begin(9600);
  Serial.begin(9600);
  stand();
  delay(3000);

}

void loop()
{
  //stand();
  //shuffle_walk();
  //creep_walk();
  calibrate();
}
