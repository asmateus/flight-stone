#define N_SYNC 0
#define Y_SYNC 1

#define ACTION_CMD_SIZE '5'
#define START_STOP_CMD_SIZE '4'
#define MOV_CMD 'm'
#define ROT_CMD 'r'
#define U_DIR 'u'
#define R_DIR 'r'
#define D_DIR 'd'
#define L_DIR 'l'

void moveUp(int);
void moveDown(int);
void moveRight(int);
void moveLeft(int);

void rotateRight(int);
void rotateLeft(int);

void toogleIdle(int);
void toogleEngline(void);