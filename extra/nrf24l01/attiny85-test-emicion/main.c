#include <avr/io.h>
#include <stdio.h>
#include <util/delay.h>

#include "nRF24L01.h"
#include "main.h"

int main(void)
{
    // Configure SPI interface
    configurePortsForSPI();

    // Check if SPI interface is working properly
    ledCheck(STATUS, 0x0E, 1);
    //Delay
    // Configure nRF
    configureNRF();

    // Create dummy information to transmit
    uint8_t dummy[PAYLOAD_WIDTH] = {0x61, 0x6E, 0x64, 0x72, 0x65, 0x73, 0x20, 0x69,
                                    0x73, 0x20, 0x6D, 0x79, 0x20, 0x6D, 0x61, 0x73,
                                    0x74, 0x65, 0x72};
    //int i;
    //for(i = 0; i < PAYLOAD_WIDTH; ++i) {
    //    dummy[i] = 0x93;
    //}

    while(1) {
        transmitPayload(dummy);

        // Check sanity of transmission
        if((SPICommProbe(STATUS) & (1<<4)) != 0) {
            // Failed
            ledCheck(STATUS, SPICommProbe(STATUS), 1);
        }
        resetIRQ();

        _delay_ms(1000);
    }

    return 0;
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
    SETBIT(PORTB, CSN_PIN);
    CLEARBIT(PORTB, CE_PIN);
}

void configureNRF(void)
{
    // Allow radio to reach power down if shut down
    _delay_ms(100);

    uint8_t val[5];

    // Enable autoacknowledgement
    val[0]=0x01;
    WRNrf(W, EN_AA, val, 1);

    // Set number of retries to 15, with 750us in between
    val[0]=0x2F;
    WRNrf(W, SETUP_RETR, val, 1);

    // Choose number of enabled datapipes (1-5), enable datapipe 0
    val[0] = 0x01;
    WRNrf(W, EN_RXADDR, val, 1);

    // Set the receiver address to be of 5 bytes
    // it can be 3, 4 or 5. Write 3 to select 5.
    val[0] = 0x03;
    WRNrf(W, SETUP_AW, val, 1);

    // Choose the desired channel
    // (2400 + channel)NHz
    val[0] = 0x01;
    WRNrf(W, RF_CH, val, 1);

    // Choose power mode and data speed
    // 00000111 bit 3=0 for 1Mbps, bit 2,1=(11 for 0dB, 00 for -18dB)
    val[0] = 0x07;
    WRNrf(W, RF_SETUP, val, 1);

    // Setup the receiver address for communication, long and secure
    int i;
    for(i = 0; i < 5; ++i) {
        val[i] = 0x12;
    }
    // We chose pipe 0, so we write to that pipe
    WRNrf(W, RX_ADDR_P0, val, 5);

    // Setup the transmitter address for communication
    for(i = 0; i < 5; ++i) {
        val[i] = 0x12;
    }
    // We chose pipe 0, so we write to that pipe
    WRNrf(W, TX_ADDR, val, 5);

    // Setup payload width
    val[0] = PAYLOAD_WIDTH;
    WRNrf(W, RX_PW_P0, val, 1);

    // Configure nRF behavior, in this case:
    // boot up nRF, decide wether it will transmit or receive
    // and mask the irq signal
    // 0b0001 1110, bit 0=('0'->transmitter; '1'-> receiver)
    //              bit 1='1'->power up
    //              bit 2='1'->CRC is 2 bytes (for error checking)
    //              bit 3='1'->enable CRC
    //              bit 4='1'->mask IRQ interruption
    val[0] = 0x1E;
    WRNrf(W, CONFIG, val, 1);

    // Device needs 1.5ms to reach standby mode (CE=low)
    _delay_ms(100);
}

void resetIRQ(void)
{
    _delay_us(10);
    CLEARBIT(PORTB, CSN_PIN);
    _delay_us(10);
    writeReadByteSPI(W_REGISTER + STATUS);
    _delay_us(10);
    writeReadByteSPI(0x70);
    _delay_us(10);
    SETBIT(PORTB, CSN_PIN);
}

void transmitPayload(uint8_t *data_buffer)
{
    // Flush buffer from old data, here data_buffer is dummy, it is
    // passed only because the function requires such a parameter
    WRNrf(R, FLUSH_TX, data_buffer, 0);

    // Send the data in the buffer to the nRF
    // Used R because W_TX_PAYLOAD is on the highest byte-level
    WRNrf(R, W_TX_PAYLOAD, data_buffer, PAYLOAD_WIDTH);

    // Timeout after payload was loaded
    _delay_ms(10);

    // Transmit data
    SETBIT(PORTB, CE_PIN);
    _delay_us(20);
    CLEARBIT(PORTB, CE_PIN);
    _delay_ms(10);
}

uint8_t *WRNrf(uint8_t flag, uint8_t reg, uint8_t *val, uint8_t pkg_size)
{
    // Set read or write mode (Read mode is 0x0+reg) so skip that
    if(flag == W) {
        reg = W_REGISTER + reg;
    }

    // Array to be returned at the end
    static uint8_t ret[32];
    
    _delay_us(10);
    CLEARBIT(PORTB, CSN_PIN);
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

    SETBIT(PORTB, CSN_PIN);
    return ret;
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
    CLEARBIT(PORTB, CSN_PIN);
    _delay_us(10);

    // Set nRF to reading mode
    writeReadByteSPI(R_REGISTER + reg);
    _delay_us(10);

    // Write NOP to receive back reg
    reg = writeReadByteSPI(NOP);
    _delay_us(10);

    // Set CSN Hi - nRF goes back to doing nothing
    SETBIT(PORTB, CSN_PIN);

    return reg;
}

void ledCheck(uint8_t bt, uint8_t expected, int port)
{
    uint8_t prev_state = PORTB;
    if(SPICommProbe(bt) == expected) {
        // Enable PORTB for LED checking
        USICR &= ~(1<<USIWM0);
        SETBIT(PORTB, port);

        // Recover previous state
        _delay_ms(1000);
        PORTB = prev_state;
        USICR |= (1<<USIWM0);
    }
}