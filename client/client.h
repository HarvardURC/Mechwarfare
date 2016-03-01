#define MAESTRO_RX 8
#define MAESTRO_TX 9

#define XBEE_RX 10
#define XBEE_TX 9

#define INPUT_SIZE 7

#define BAUD_RATE 9600

#define SETUP_DELAY_TIME 3000
#define LOOP_DELAY_TIME 10

#define FRONT_LEFT_HIP_HOME_POS    6204
#define FRONT_LEFT_KNEE_HOME_POS   4826
#define FRONT_LEFT_ANKLE_HOME_POS  8596
#define FRONT_RIGHT_HIP_HOME_POS   5494
#define FRONT_RIGHT_KNEE_HOME_POS  3992 // formerly 3492
#define FRONT_RIGHT_ANKLE_HOME_POS 8370 // formerly 8720
#define BACK_RIGHT_HIP_HOME_POS    7122
#define BACK_RIGHT_KNEE_HOME_POS   4424
#define BACK_RIGHT_ANKLE_HOME_POS  8280
#define BACK_LEFT_HIP_HOME_POS     4588
#define BACK_LEFT_KNEE_HOME_POS    4334
#define BACK_LEFT_ANKLE_HOME_POS   9072
#define TURRET_PAN_HOME_POS        0
#define TURRET_TILT_HOME_POS       5850

#define EVENT_DELAY_TIME 150 // formerly 40

#define TURNING_RAISE_ANGLE  800
#define TURNING_ROTATE_ANGLE 2000
#define TURNING_LEAN_ANGLE   400

#define WALKING_RAISE_ANGLE             700
#define WALKING_ROTATE_ANGLE            1100
#define WALKING_LEAN_ANGLE             -300
#define WALKING_RAISE_ANKLE_ANGLE       450
#define WALKING_DROP_FRONT_ANKLE_ANGLE  0
#define WALKING_DROP_BACK_ANKLE_ANGLE   0
#define ZERO_ANGLE                      0

#define STAND_LENGTH      15
#define CREEP_LENGTH      43
#define CREEP_HOME_LENGTH 13

enum pservo_t {
    DELAY             = -1,
    FRONT_LEFT_HIP    = 0,
    FRONT_LEFT_KNEE   = 1,
    FRONT_LEFT_ANKLE  = 2,
    FRONT_RIGHT_HIP   = 3,
    FRONT_RIGHT_KNEE  = 4,
    FRONT_RIGHT_ANKLE = 5,
    BACK_RIGHT_HIP    = 6,
    BACK_RIGHT_KNEE   = 7,
    BACK_RIGHT_ANKLE  = 8,
    BACK_LEFT_HIP     = 9,
    BACK_LEFT_KNEE    = 10,
    BACK_LEFT_ANKLE   = 11,
    TURRET_PAN        = 12,
    TURRET_TILT       = 13,
    NUM_SERVOS        = 14
};

struct event_t {
    pservo_t servo;
    int value;
};

int HOME_POS[] = {
    [FRONT_LEFT_HIP]    = FRONT_LEFT_HIP_HOME_POS,
    [FRONT_LEFT_KNEE]   = FRONT_LEFT_KNEE_HOME_POS,
    [FRONT_LEFT_ANKLE]  = FRONT_LEFT_ANKLE_HOME_POS,
    [FRONT_RIGHT_HIP]   = FRONT_RIGHT_HIP_HOME_POS,
    [FRONT_RIGHT_KNEE]  = FRONT_RIGHT_KNEE_HOME_POS,
    [FRONT_RIGHT_ANKLE] = FRONT_RIGHT_ANKLE_HOME_POS,
    [BACK_RIGHT_HIP]    = BACK_RIGHT_HIP_HOME_POS,
    [BACK_RIGHT_KNEE]   = BACK_RIGHT_KNEE_HOME_POS,
    [BACK_RIGHT_ANKLE]  = BACK_RIGHT_ANKLE_HOME_POS,
    [BACK_LEFT_HIP]     = BACK_LEFT_HIP_HOME_POS,
    [BACK_LEFT_KNEE]    = BACK_LEFT_KNEE_HOME_POS,
    [BACK_LEFT_ANKLE]   = BACK_LEFT_ANKLE_HOME_POS,
    [TURRET_PAN]        = TURRET_PAN_HOME_POS,
    [TURRET_TILT]       = TURRET_TILT_HOME_POS,
};

event_t STAND[] = {
    {FRONT_RIGHT_HIP,   ZERO_ANGLE},
    {FRONT_RIGHT_KNEE,  ZERO_ANGLE},
    {FRONT_RIGHT_ANKLE, ZERO_ANGLE},
    {FRONT_LEFT_HIP,    ZERO_ANGLE},
    {FRONT_LEFT_KNEE,   ZERO_ANGLE},
    {FRONT_LEFT_ANKLE,  ZERO_ANGLE},
    {BACK_RIGHT_HIP,    ZERO_ANGLE},
    {BACK_RIGHT_KNEE,   ZERO_ANGLE},
    {BACK_RIGHT_ANKLE,  ZERO_ANGLE},
    {BACK_LEFT_HIP,     ZERO_ANGLE},
    {BACK_LEFT_KNEE,    ZERO_ANGLE},
    {BACK_LEFT_ANKLE,   ZERO_ANGLE},
    {TURRET_PAN,        ZERO_ANGLE},
    {TURRET_TILT,       ZERO_ANGLE},
    {DELAY,             EVENT_DELAY_TIME}
};

event_t TURN_LEFT[] = {
    {FRONT_LEFT_ANKLE,   TURNING_LEAN_ANGLE},
    {FRONT_RIGHT_ANKLE,  TURNING_LEAN_ANGLE},
    {BACK_LEFT_ANKLE,   -TURNING_LEAN_ANGLE},
    {BACK_RIGHT_ANKLE,  -TURNING_LEAN_ANGLE},

    {FRONT_LEFT_KNEE, TURNING_RAISE_ANGLE},
    {BACK_RIGHT_KNEE, TURNING_RAISE_ANGLE},
    {DELAY,           EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,  TURNING_ROTATE_ANGLE},
    {BACK_RIGHT_HIP,  TURNING_ROTATE_ANGLE},
    {DELAY,           EVENT_DELAY_TIME},
    {FRONT_LEFT_KNEE, ZERO_ANGLE},
    {BACK_RIGHT_KNEE, ZERO_ANGLE},
    {DELAY,           EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,  ZERO_ANGLE},
    {BACK_RIGHT_HIP,  ZERO_ANGLE},

    {FRONT_RIGHT_KNEE, TURNING_RAISE_ANGLE},
    {BACK_LEFT_KNEE,   TURNING_RAISE_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,  TURNING_ROTATE_ANGLE},
    {BACK_LEFT_HIP,    TURNING_ROTATE_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_RIGHT_KNEE, ZERO_ANGLE},
    {BACK_LEFT_KNEE,   ZERO_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,  ZERO_ANGLE},
    {BACK_LEFT_HIP,    ZERO_ANGLE},
};

event_t TURN_RIGHT[] = {
    {FRONT_LEFT_ANKLE,   TURNING_LEAN_ANGLE},
    {FRONT_RIGHT_ANKLE,  TURNING_LEAN_ANGLE},
    {BACK_LEFT_ANKLE,   -TURNING_LEAN_ANGLE},
    {BACK_RIGHT_ANKLE,  -TURNING_LEAN_ANGLE},

    {FRONT_LEFT_KNEE,  TURNING_RAISE_ANGLE},
    {BACK_RIGHT_KNEE,  TURNING_RAISE_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,  -TURNING_ROTATE_ANGLE},
    {BACK_RIGHT_HIP,  -TURNING_ROTATE_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_LEFT_KNEE,  ZERO_ANGLE},
    {BACK_RIGHT_KNEE,  ZERO_ANGLE},
    {DELAY,            EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,   ZERO_ANGLE},
    {BACK_RIGHT_HIP,   ZERO_ANGLE},

    {FRONT_RIGHT_KNEE,  TURNING_RAISE_ANGLE},
    {BACK_LEFT_KNEE,    TURNING_RAISE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,  -TURNING_ROTATE_ANGLE},
    {BACK_LEFT_HIP,    -TURNING_ROTATE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_RIGHT_KNEE,  ZERO_ANGLE},
    {BACK_LEFT_KNEE,    ZERO_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,   ZERO_ANGLE},
    {BACK_LEFT_HIP,     ZERO_ANGLE},
};

event_t SHUFFLE_FORWARD[] = {
    {FRONT_LEFT_KNEE,   WALKING_RAISE_ANGLE},
    {FRONT_LEFT_ANKLE,  WALKING_RAISE_ANKLE_ANGLE},
    {BACK_RIGHT_KNEE,   WALKING_RAISE_ANGLE},
    {BACK_RIGHT_ANKLE,  WALKING_RAISE_ANKLE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,   -WALKING_ROTATE_ANGLE},
    {BACK_RIGHT_HIP,    WALKING_ROTATE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_LEFT_KNEE,   ZERO_ANGLE},
    {BACK_RIGHT_KNEE,   ZERO_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},

    {FRONT_RIGHT_KNEE,   WALKING_RAISE_ANGLE},
    {FRONT_RIGHT_ANKLE,  WALKING_RAISE_ANKLE_ANGLE},
    {BACK_LEFT_KNEE,     WALKING_RAISE_ANGLE},
    {BACK_LEFT_ANKLE,    WALKING_RAISE_ANKLE_ANGLE},
    {DELAY,              EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,    WALKING_ROTATE_ANGLE},
    {BACK_LEFT_HIP,     -WALKING_ROTATE_ANGLE},
    {DELAY,              EVENT_DELAY_TIME},
    {FRONT_RIGHT_KNEE,   ZERO_ANGLE},
    {BACK_LEFT_KNEE,     ZERO_ANGLE},
    {DELAY,              EVENT_DELAY_TIME},

    {FRONT_LEFT_HIP,    ZERO_ANGLE},
    {FRONT_RIGHT_HIP,   ZERO_ANGLE},
    {BACK_LEFT_HIP,     ZERO_ANGLE},
    {BACK_RIGHT_HIP,    ZERO_ANGLE},
    {FRONT_RIGHT_ANKLE, ZERO_ANGLE},
    {FRONT_LEFT_ANKLE,  ZERO_ANGLE},
    {BACK_RIGHT_ANKLE,  WALKING_LEAN_ANGLE},
    {BACK_LEFT_ANKLE,   WALKING_LEAN_ANGLE},
    {DELAY,             EVENT_DELAY_TIME}
};

event_t CREEP_HOME[] = {
    {FRONT_RIGHT_HIP,    ZERO_ANGLE},
    {FRONT_RIGHT_KNEE,   ZERO_ANGLE},
    {FRONT_RIGHT_ANKLE,  ZERO_ANGLE},
    {FRONT_LEFT_HIP,     ZERO_ANGLE},
    {FRONT_LEFT_KNEE,    ZERO_ANGLE},
    {FRONT_LEFT_ANKLE,   ZERO_ANGLE},
    {BACK_RIGHT_HIP,    -WALKING_ROTATE_ANGLE * 2.4},
    {BACK_RIGHT_KNEE,    ZERO_ANGLE},
    {BACK_RIGHT_ANKLE,   ZERO_ANGLE},
    {BACK_LEFT_HIP,      WALKING_ROTATE_ANGLE * 2.4},
    {BACK_LEFT_KNEE,     ZERO_ANGLE},
    {BACK_LEFT_ANKLE,    ZERO_ANGLE},
    {DELAY,              EVENT_DELAY_TIME}
};

event_t CREEP_FORWARD[] = {
    {DELAY, EVENT_DELAY_TIME},

    {BACK_RIGHT_KNEE,   TURNING_RAISE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {BACK_RIGHT_HIP,    TURNING_ROTATE_ANGLE * .1},
    {DELAY,             EVENT_DELAY_TIME},
    {BACK_RIGHT_ANKLE,  WALKING_LEAN_ANGLE * 1.5},
    {BACK_RIGHT_KNEE,  -TURNING_RAISE_ANGLE / 2.0},

    {DELAY,             EVENT_DELAY_TIME},
    {DELAY,             EVENT_DELAY_TIME},

    //push off front left leg
    {FRONT_LEFT_ANKLE,  WALKING_LEAN_ANGLE * 1.5},

    {BACK_RIGHT_ANKLE,  ZERO_ANGLE},
    {BACK_RIGHT_KNEE,   ZERO_ANGLE},
    {FRONT_RIGHT_HIP,   TURNING_ROTATE_ANGLE * 1.4},
    {BACK_LEFT_HIP,    -TURNING_ROTATE_ANGLE * .3},
    // {BACK_RIGHT_HIP,    ZERO_ANGLE},

    {DELAY,             EVENT_DELAY_TIME},

    {FRONT_LEFT_KNEE,   TURNING_RAISE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_LEFT_HIP,   -TURNING_ROTATE_ANGLE * 1.4},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_LEFT_ANKLE,  ZERO_ANGLE},
    {FRONT_LEFT_KNEE,   ZERO_ANGLE},



    {DELAY,             EVENT_DELAY_TIME},

    // alternate creep
    {FRONT_RIGHT_KNEE,  TURNING_RAISE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_RIGHT_HIP,   TURNING_ROTATE_ANGLE * .1},
    {DELAY,             EVENT_DELAY_TIME},
    {FRONT_RIGHT_ANKLE, WALKING_LEAN_ANGLE * 2},
    {FRONT_RIGHT_KNEE, -TURNING_RAISE_ANGLE / 2.0},

    {DELAY,             EVENT_DELAY_TIME},
    {DELAY,             EVENT_DELAY_TIME},

    //push off back left leg
    {BACK_LEFT_ANKLE,   WALKING_LEAN_ANGLE * 1.5},

    {FRONT_RIGHT_ANKLE, ZERO_ANGLE},
    {FRONT_RIGHT_KNEE,  ZERO_ANGLE},
    {BACK_RIGHT_HIP,   -TURNING_ROTATE_ANGLE * 1.4},
    {FRONT_LEFT_HIP,    TURNING_ROTATE_ANGLE * .3},
    // {FRONT_RIGHT_HIP,   ZERO_ANGLE},

    {DELAY,             EVENT_DELAY_TIME},

    {BACK_LEFT_KNEE,    TURNING_RAISE_ANGLE},
    {DELAY,             EVENT_DELAY_TIME},
    {BACK_LEFT_HIP,     TURNING_ROTATE_ANGLE * 1.4},
    {DELAY,             EVENT_DELAY_TIME},
    {BACK_LEFT_ANKLE,   ZERO_ANGLE},
    {BACK_LEFT_KNEE,    ZERO_ANGLE},

    {DELAY,             EVENT_DELAY_TIME},
};
