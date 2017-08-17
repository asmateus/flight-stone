#ifndef FUNCTIONS_H_
#define FUNCTIONS_H_

const int _3v3_  = 160;
const int _1v7_  = 87;

float getV(int index);

void printCH(int nChannel){
    for(int i=0;i<nChannel;i++){
        Serial.print("CH");
        Serial.print(i);
        Serial.print(": ");
        Serial.print(getV(i));
        if(i!=nChannel-1){
            Serial.print(", ");
        }
    }
    Serial.println("\n");
}

float mapfloat(float x, float in_min, float in_max, float out_min, float out_max)
{
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

float getV(int index)
{
    return mapfloat(analogRead(index), 0, 1023, 0, 5);
}





class Drone{
    /* Channels
     *
     * Channel 0: ID 2 - Blue    Y -> Syncronization
     * Channel 1: ID 2 - Green   X
     * Channel 2: ID 2 - Yellow  Z
     * Channel 3: ID 2 - Purple  Spin -> Not Used
     *
     * Drone
     *
     *          Y
     *          |
     *          |
     *      ---------
     *      |   F   |
     *      |  LZR  |---X
     *      |   B   |
     *      ---------
     *
     *
     * Se primero el drone, luego el microcontrolador y despues el control
     *
     */

    /* Voltage Levels
     * 3.1 V  - 160
     * 1.7 V  - 87
     *   0 V  - 0
     */

    public:
        Drone(int CHY,int CHX, int CHZ, int CHS, int CHE){
            CH[CH_Y] = CHY;
            CH[CH_X] = CHX;
            CH[CH_Z] = CHZ;
            CH[CH_S] = CHS;
            CH[CH_E] = CHE;
        }

        void setV(int channel,int voltage)
        {
            if((voltage<=160)||(voltage>=0)){
                analogWrite(channel,voltage);
            } else{
                Serial.print("Error");
            }
        }

        void reset(){
            for(int i=0;i<getSize()-1;i++){
                setV(CH[i],_1v7_);
            }
            setV(CH[CH_E],0);
        }

        int getSize(){
            return (sizeof(CH)/sizeof(*CH));
        }

        int getCHannel(int index){
            return CH[index];
        }



        void switchEngine(){
            Serial.println("Switching");
            Serial.println(CH[CH_E]);
            setV(CH[CH_E], _3v3_);
            delay(100);

            setV(CH[CH_E], 0);
            Serial.println("Done");
        }

        void moveUp(int level){
            setV(CH[CH_Z],_1v7_-level);
            Serial.println("Done");
        }

        void moveDown(int level){
            setV(CH[CH_Z],_1v7_+level);
            Serial.println("Done");
        }

        void moveLeft(int level){
            setV(CH[CH_X],_1v7_+level);
            Serial.println("Done");
        }

        void moveRight(int level){
            setV(CH[CH_X],_1v7_-level);
            Serial.println("Done");
        }

        void moveForward(int level){
            setV(CH[CH_Y],_1v7_+level);
            Serial.println("Done");
        }

        void moveBackwards(int level){
            setV(CH[CH_Y],_1v7_-level);
            Serial.println("Done");
        }



    private:
        int CH[5];
        const int _3v3_  = 160;
        const int _1v7_  = 87;
        const int CH_Y = 0;
        const int CH_X = 1;
        const int CH_Z = 2;
        const int CH_S = 3;
        const int CH_E = 4;

};

/*
int level = 0;
int cycle = 0;
int inc   = 10;

void Syncronize(int channel){


    setV(channel, level);

    if(!cycle){
        level = level + inc;
    }else{
        level = level - inc;
    }


    if(level>158){
        cycle = 1;
        level = 158;
    }else if(level <=0){
        cycle = 0;
        level = 0;
    }
}

*/

#endif
