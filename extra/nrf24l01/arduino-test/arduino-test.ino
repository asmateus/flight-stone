// Client and Server code
// OPERATION_MODE = 0 for client, 1 for server

#include <SPI.h>
#include <RH_NRF24.h>

#define CHANNEL 1
#define OPERATION_MODE 0
#define CE_PIN 8
#define CSN_PIN 10

void performServerLoop();
void performClientLoop();

// Instance of the radio driver. For leonardo SS pin (pin 10) needs to be explicity defined
RH_NRF24 nrf24(CE_PIN, CSN_PIN);

void setup()
{  
    Serial.begin(115200);
    delay(1000);
    Serial.println("INIT");
    // Try to init nrf24 radio driver
    while(!nrf24.init())
        ;

    // Try to set communication channel
    while(!nrf24.setChannel(CHANNEL))
        ;

    // Try to set data rate and transmission intensity
    while(!nrf24.setRF(RH_NRF24::DataRate2Mbps, RH_NRF24::TransmitPower0dBm))
        ;
    Serial.println("OK");
}

void loop()
{
    if(OPERATION_MODE == 1)
        performServerLoop();
    else
        performClientLoop();

    delay(1000);
}

void performServerLoop()
{
    if(nrf24.available())
    {
        // Message received
        uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
        uint8_t len = sizeof(buf);

        if(nrf24.recv(buf, &len))
        { 
          Serial.println((char*)buf);
          // Send reply
          uint8_t data[] = "Hi Misaka, Enomoto here!";
          nrf24.send(data, sizeof(data));
          nrf24.waitPacketSent();
        } 
    }
}

void performClientLoop()
{
    // Data to send
    uint8_t data[] = "Misaka here!";
    nrf24.send(data, sizeof(data));

    nrf24.waitPacketSent();
  
    // Wait for reply
    uint8_t buf[RH_NRF24_MAX_MESSAGE_LEN];
    uint8_t len = sizeof(buf);

    if(nrf24.waitAvailableTimeout(500))
    {
        // Message received
        if(nrf24.recv(buf, &len))
            Serial.println((char*)buf);
    }
}
