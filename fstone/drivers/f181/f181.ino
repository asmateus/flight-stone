#include "libs/controller.h"

char cmd[9] = "00000000";
int intensity = 0;
long idle_time[4] = {0, 0, 0, 0};

  void setup()
{
    Serial.begin(115200);
    delay(100);
}

void loop()
{
    if (Serial.available() > 0) {
        Serial.readBytes(cmd, 8);

        if(cmd[0] == START_STOP_CMD_SIZE) {
            toogleEngine();
        }
        else if(cmd[0] == ACTION_CMD_SIZE) {
            intensity = (int)((cmd[3]-48)*100 + (cmd[4]-48)*10 + (cmd[5]-48)*1);
            Serial.print(idle_time[0]);
            Serial.print(idle_time[1]);
            Serial.print(idle_time[2]);
            Serial.println(idle_time[3]);

            if(cmd[2] == U_DIR) {
                if(cmd[1] == MOV_CMD) {
                    idle_time[0] = 0;
                    moveUp(intensity);
                }
            }
            else if (cmd[2] == D_DIR) {
                if(cmd[1] == MOV_CMD) {
                    idle_time[0] = 0;
                    moveDown(intensity);
                }
            }
            else if (cmd[2] == R_DIR) {
                if(cmd[1] == MOV_CMD) {
                    idle_time[1] = 0;
                    moveRight(intensity);
                }
                else if(cmd[1] == ROT_CMD) {
                    idle_time[2] = 0;
                    rotateRight(intensity);
                }
            }
            else if (cmd[2] == L_DIR) {
                if(cmd[1] == MOV_CMD) {
                    idle_time[1] = 0;
                    moveLeft(intensity);
                }
                else if(cmd[1] == ROT_CMD) {
                    idle_time[2] = 0;
                    rotateLeft(intensity);
                }
            }
        }
        else {
            Serial.println("Command not recognized");
        }
    }
    else {
        if(idle_time[0] < 30000) idle_time[0] += 1;
        else toogleIdle(0);
        if(idle_time[1] < 30000) idle_time[1] += 1;
        else toogleIdle(1);
        if(idle_time[2] < 30000) idle_time[2] += 1;
        else toogleIdle(3);
        if(idle_time[3] < 30000) idle_time[3] += 1;
    }
}

void toogleIdle(int ch)
{
    
}

void toogleEngine()
{
    Serial.println("Toogling Engine");
};

void moveUp(int intensity)
{
    Serial.print("Moving Up at: ");
    Serial.println(intensity);
}

void moveDown(int intensity)
{
    Serial.print("Moving Down at: ");
    Serial.println(intensity);
}

void moveRight(int intensity)
{
    Serial.print("Moving Right at: ");
    Serial.println(intensity);
}

void moveLeft(int intensity)
{
    Serial.print("Moving Left at: ");
    Serial.println(intensity);
}

void rotateRight(int intensity)
{
    Serial.print("Rotating Right at: ");
    Serial.println(intensity);
}

void rotateLeft(int intensity)
{
    Serial.print("Rotating Left at: ");
    Serial.println(intensity);
}
