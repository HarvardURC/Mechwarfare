#include <PololuMaestro.h>
#include <SoftwareSerial.h>
SoftwareSerial maestroSerial(10, 11);
MiniMaestro maestro(maestroSerial);

int home1 = 6000;
int homecrouch = 5000;
int rotate = 4000;
int std_delay = 100;

// servo indicates which servo or -1 for delays
typedef struct rotation
{
  int servo;
  int degree;
};

// rotates bot right
rotation[22] turn = 
{
  {7, rotate},
  {1, rotate}.
  {-1, std_delay},
  {0, rotate},
  {6, rotate},
  {-1, std_delay},
  {7, homecrouch},
  {1, homecrouch},
  {-1, std_delay},
  {10, rotate},
  {4, rotate},
  {-1, std_delay},
  {3, rotate},
  {9, rotate},
  {-1, std_delay},
  {10, homecrouch},
  {4, homecrouch},
  {-1, std_delay},
  {3, home1},
  {9, home1},
  {0, home1},
  {6, home1}
}

// moves bot forward
rotation[22] walk = 
{
  {7, rotate},
  {1, rotate}.
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
  
}

// dir = 0 for forward, 1 for backwards.
void execute(rotation commands[], int dir)
{
  int start = 0
  int incrementor = 1;
  int fin = sizeof(commands);
  if (dir == 1)
  {
    start = fin;
    fin = 0;
    incrementor = -1;
  }
  for(int i = start; i < fin; i+=incrementor)
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

void turn_right()
{
  execute(turn, 0);
}

void turn_left()
{
  execute(turn, 1);
}

void move_forward()
{
  execute(walk, 0);
}

void move_back()
{
  execute(walk, 1);
}

void setup()
{
  
  // Set the serial port's baud rate
  maestroSerial.begin(9600);
  Serial.begin(9600);
  
}

void loop()
{
  turn_right();
  turn_left();
  move_forward();
  move_back();
}
