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
int homeankle = 8000;
int homeknee = 3600;
int homehip = 6800;
int home1 = 6000;
int homecrouch = 5000;
int rotate = 4000;
int std_delay = 300;


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

// turret
int tp = 12; // turret pan
int tt = 13; // turret tilt


/*
  ######################
  # movement sequences #
  ######################
*/

// rotates bot right
rotation turn[22] =
{
  {flk, rotate},
  {brk, rotate},
  {-1, std_delay},
  {flh, rotate},
  {brh, rotate},
  {-1, std_delay},
  {flk, homecrouch},
  {brk, homecrouch},
  {-1, std_delay},
  {frk, rotate},
  {blk, rotate},
  {-1, std_delay},
  {frh, rotate},
  {blh, rotate},
  {-1, std_delay},
  {frk, homecrouch},
  {blk, homecrouch},
  {-1, std_delay},
  {flh, home1},
  {frh, home1},
  {blh, home1},
  {brh, home1}
};

// moves bot forward
rotation walk[36] =
{
  {7, rotate},
  {1, rotate},
  {-1, std_delay},
  {6, rotate},
  {0, 2*home1 - rotate},
  {-1, std_delay},
  {7, homecrouch},
  {1, homecrouch},
  {-1, std_delay},
  {10, homecrouch - (homecrouch - rotate)/2.0},
  {4, homecrouch - (homecrouch - rotate)/2.0},
  {0, home1},
  {6, home1},
  {-1, std_delay},
  {10, homecrouch},
  {4, homecrouch},
  {-1, std_delay},
  {10, rotate},
  {4, rotate},
  {-1, std_delay},
  {10, rotate},
  {4, rotate},
  {-1, std_delay},
  {9, rotate},
  {3, 2*home1 - rotate},
  {-1, std_delay},
  {10, homecrouch},
  {4, homecrouch},
  {-1, std_delay},
  {7, homecrouch - (homecrouch - rotate)/2.0},
  {1, homecrouch - (homecrouch - rotate)/2.0},
  {3, home1},
  {9, home1},
  {-1, std_delay},
  {7, homecrouch},
  {1, homecrouch}
};

// legs down
rotation start_pos[13] =
{
  {frh, homehip},
  {frk, homeknee},
  {fra, homeankle},
  {flh, homehip},
  {flk, homeknee},
  {fla, homeankle},
  {brh, homehip},
  {brk, homeknee},
  {bra, homeankle},
  {blh, homehip},
  {blk, homeknee},
  {bla, homeankle},
  {-1, 1000}
};


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
        maestro.setTarget(commands[i].servo, commands[i].degree);
      }
    }
  }

  for(int i = 0; i < len; i++)
  {
    if(commands[i].servo == -1)
    {
      delay(commands[i].degree);
    }
    else
    {
      maestro.setTarget(commands[i].servo, commands[i].degree);
    }
  }
}

void turn_right()
{
  execute(turn, 0, 22);
}

void turn_left()
{
  execute(turn, 1, 22);
}

void move_forward()
{
  execute(walk, 0, 36);
}

void move_back()
{
  execute(walk, 1, 36);
}

void stand()
{
  execute(start_pos, 0, 13);
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
  turn_right();
  turn_right();
  Serial.print("LOL");
  turn_left();
  turn_left();
  stand();
  
}

void loop()
{
  stand();
}
