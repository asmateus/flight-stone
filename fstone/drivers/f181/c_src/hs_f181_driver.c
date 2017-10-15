/*
 *
 * This is the driver code for the controller of the HolyStone F181 drone. The idea is for this
 * piece of code to be as general as possible. Hardware dependent configuration should be dealt
 * with in the libs files, specifically in the core_XX.h lib file and exposed to this with the
 * same name conventions.
 *
 * Basic functionality is as follows:
 * 1. Read the serial port for master instructions
 * 2. Perform the desired actions
 * 3. Keep track of synchronization
 *
*/

#include "libs/core_ard.h"
#include "libs/controller.h"
#include "libs/hwconfig.h"

int sync_status = N_SYNC;

int main(void)
{
    while(1) {
        sync_status = checkStatus();
        if(sync_status)
            pass();
        else
            pass();
    }

    return 0;
}
