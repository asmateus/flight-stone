/* Voltage Levels
 * 3.1 V  - 160
 * 1.7 V  - 87
 *   0 V  - 0
 */
/* Notes
 * Drone takes off with in channel 2 1.1v - 0.5v
 * El drone se desplaza hacia alante y derecha en estado estable  -  dron is not calibrated
 *
 * Drone always takes 20s to synchronize
 * Voltages need to be set to 1.7v in all four movement channels, or it wont Sync.
 *
 * When the controller is turned on and there is one long beed , it wont sync with the drone.
 * The drone wont sync to any controller if it stays idle for more than 20s
 * The drone is Synced when the Leds stop BLinking
 *
*/
// millis()
#include "Arduino.h"
#include "functions.h"

const int nChannel = 5;

int AN[nChannel] = {0,1,2,3,5};      // Analog Channels
Drone D1(2,3,4,5,6);

void setup()
{
    Serial.begin(9600);
    for(int i=0;i<D1.getSize();i++){
        pinMode(D1.getCHannel(i), OUTPUT);   // sets the pin as output
    }
    D1.reset();
}

int i=0;

void loop()
{
    printCH(nChannel);

    if(millis()>=23000){
        Serial.println("Synced");

        if(i==0){


            /*  Demo Up hold Down
             */
            D1.moveUp(40);
            delay(1000);
            D1.moveUp(0);
            delay(1000);
            D1.moveDown(80);
            /*
            */

            /* Demo Engine

            D1.switchEngine();

            */

            i++;
        }
    }
    delay(100);
}

