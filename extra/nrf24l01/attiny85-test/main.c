// main.c
//
// A simple blinky program for ATtiny85
// Connect red LED at pin 2 (PB3)
//
// electronut.in

#include <avr/io.h>
#include <stdio.h>
#include <util/delay.h>

#include "nRF24L01.h"
#include "main.h"

int main(void)
{
    configurePortsForSPI();

    // Check if interface is working properly
    ledCheck(STATUS, 1);

    while(1) {

    }

    return 1;
}

void configurePortsForSPI(void)
{
    /*  Set these pins as output
        SCK : PB2
        MISO: PB1 (to nRF MOSI)
        CSN : PB4
        CE  : PB3
        
        The line below is basically:
        DDRB OR= 10 OR 100 OR 1000 OR 10000
        That is: DDRB = DDRB OR 00011110
     */
    DDRB |= (1<<PB1) | (1<<PB2) | (1<<PB3) | (1<<PB4);

    // Set MOSI (PB0) as input. Connect to nRF MISO
    DDRB &= ~(1<<PB0); // DDRB = DDRB AND NOT(00000001)
    PORTB |= (1<<PB0);

    // Set USI in three-wire mode: SPI (This disables PORTB D0, D1 and SCK pins)
    // USI configuration register
    USICR |= (1<<USIWM0) | (1<<USICS1) | (1<<USICLK);

    // Nothing to send/receive yet. CSN to high, CE to low
    SETBIT(PORTB, 4);
    CLEARBIT(PORTB, 3);
}

uint8_t *WRNrf(uint8_t flag, uint8_t reg, uint8_t *val, uint8_t pkg_size)
{
    // Set read or write mode (Read mode is 0x0+reg) so skip that
    if(flag == W)
        reg = W_REGISTER + reg;

    // Array to be returned at the end
    static uint8_t ret[32];
    _delay_us(10);
    CLEARBIT(PORTB, 4);
    _delay_us(10);
    writeReadByteSPI(reg);
    _delay_us(10);

    int i = 0;
    for(i = 0; i < pkg_size; ++i) {
        if(flag == R && reg != W_TX_PAYLOAD) {
            ret[i] = writeReadByteSPI(NOP);
            _delay_us(10);
        }
        else {
            writeReadByteSPI(val[i]);
            _delay_us(10);
        }
    }

    CLEARBIT(PORTB, 4);
    return reg;
}

uint8_t writeReadByteSPI(uint8_t cData)
{
    // Load data to the USI Data register
    USIDR = cData;

    /* 
        USIOIF is the counter Overflow Interrupt Flag. The
        overflow interruption holds the transmission.
        Write 1 in this bit to clear it.
     */
    USISR |= (1<<USIOIF);
    
    // Wait for transmission to complete. When USIOIF flag is set
    while((USISR & (1<<USIOIF)) == 0) {
        // Write 1 to the USITC bit. This will toggle the counter
        // this bit is read as zero always
        USICR |= (1<<USITC);
    }
    
    return USIDR;
}

uint8_t SPICommProbe(uint8_t reg)
{
    // Make sure last command was a while ago
    _delay_us(10);

    // Drive CSN low so that nRF starts to listen for command
    CLEARBIT(PORTB, 4);
    _delay_us(10);

    // Set nRF to reading mode
    writeReadByteSPI(R_REGISTER + reg);
    _delay_us(10);

    // Write NOP to receive back reg
    reg = writeReadByteSPI(NOP);
    _delay_us(10);

    // Set CSN Hi - nRF goes back to doing nothing
    SETBIT(PORTB, 4);

    return reg;
}

void ledCheck(uint8_t bt, int port)
{
    uint8_t prev_state = PORTB;
    if(SPICommProbe(bt) == 0x0E) {
        // Enable PORTB for LED checking
        USICR &= ~(1<<USIWM0);
        SETBIT(PORTB, port);

        // Recover previous state
        _delay_ms(100);
        PORTB = prev_state;
        USICR |= (1<<USIWM0);
    }
}





