#include "Arduino.h"

int PIN = 12;

int main(void)
{
    pinMode(PIN, OUTPUT);
    while(1) {
        digitalWrite(PIN, HIGH);
        delay(1000);
        digitalWrite(PIN, LOW);
        delay(1000);
    }

    return 0;
}