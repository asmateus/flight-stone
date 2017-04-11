#define PAYLOAD_WIDTH 5

// Initialization function
void configurePortsForSPI(void);

// Send and receive from the nRF
uint8_t writeReadByteSPI(uint8_t);

// Check if SPI communication is working
uint8_t SPICommProbe(uint8_t);

// Led check of SPI communication
void ledCheck(uint8_t, uint8_t, int);

// Write and Read from nRF
uint8_t *WRNrf(uint8_t, uint8_t, uint8_t *, uint8_t);

// Configure the transmision of the nRF (search for ShockBurst packet
// configuration for more info)
void configureNRF(void);

// Transmit data to receiver
void transmitPayload(uint8_t *);

// Reset irq flag
void resetIRQ(void);