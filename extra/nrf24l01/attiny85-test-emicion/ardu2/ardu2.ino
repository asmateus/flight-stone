/*
 * RF_Tranceiver.c
 *
 * Created: 2012-08-10 15:24:35
 *  Author: Kalle
 *  Atmega88
 */ 

#include <avr/io.h>
#include <stdio.h>

#include "nRF24L01.h"

#define CSN_PIN 0
#define CE_PIN 4
#define PAYLOAD_WIDTH 19

void initSPI(void);
char WriteByteSPI(unsigned char);
uint8_t GetReg(uint8_t);
uint8_t *WriteToNrf(uint8_t, uint8_t, uint8_t*, uint8_t);
void nrf24L01_init(void);
void receive_payload(void);
void reset(void);
void uglyPrint(void);
void receiver(void);
void sender(void);

uint8_t *data;
uint8_t dummy[PAYLOAD_WIDTH] = {0x61, 0x6E, 0x64, 0x72, 0x65, 0x73, 0x20, 0x69,
                                    0x73, 0x20, 0x6D, 0x79, 0x20, 0x6D, 0x61, 0x73,
                                      0x74, 0x65, 0x72};
    

void setup()
{
  Serial.begin(115200);
  delay(2000);
  
  initSPI();
  
  if(GetReg(STATUS) == 0x0E) {
     Serial.println("SPI initialization OK"); 
  }
  
  nrf24L01_init();
  uglyPrint();
  /*
  for(int i = 0; i < 5; ++i) {
      dummy[i] = 0x93;
  }
  */
}

void loop()
{
  delay(1000);
  //receiver();
  sender();
  
}

void sender(void)
{
  transmit_payload(dummy);
  if((GetReg(STATUS) & (1<<4)) != 0) {
    Serial.println("Failed");  
  }
  else {
    Serial.println("Success");
  }
  reset();
}

void receiver(void)
{
  receive_payload();
   
  if((GetReg(STATUS) & (1<<6)) == 0) {
    Serial.println(GetReg(STATUS));  
  }
  else {
    data = WriteToNrf(R, R_RX_PAYLOAD, data, 5);

    for(int i = 0; i < 5; ++i) {
      Serial.print(data[i]);
      Serial.print(" ");  
    }
    Serial.println("");
    reset();
  }
}

void uglyPrint(void)
{
  Serial.println("** Printing configuration **");
  Serial.print("EN_AA: ");
  Serial.println(GetReg(EN_AA));
  Serial.print("SETUP_RETR: ");
  Serial.println(GetReg(SETUP_RETR));
  Serial.print("EN_RXADDR: ");
  Serial.println(GetReg(EN_RXADDR));
  Serial.print("SETUP_AW: ");
  Serial.println(GetReg(SETUP_AW));
  Serial.print("RF_CH: ");
  Serial.println(GetReg(RF_CH));
  Serial.print("RF_SETUP: ");
  Serial.println(GetReg(RF_SETUP));
  data = WriteToNrf(R, RX_ADDR_P0, data, 5);
  Serial.print("RX_ADDR_P0: ");
  for(int i = 0; i < 5; ++i) {
    Serial.print(data[i]);  
  }
  Serial.println("");
  data = WriteToNrf(R, TX_ADDR, data, 5);
  Serial.print("TX_ADDR: ");
  for(int i = 0; i < 5; ++i) {
    Serial.print(data[i]);  
  }
  Serial.println("");
  Serial.print("RX_PW_P0: ");
  Serial.println(GetReg(RX_PW_P0));
  Serial.print("CONFIG: ");
  Serial.println(GetReg(CONFIG));
}

void initSPI(void)
{
  // Pins
  /*
  * CE   = PORTB4 10
  * CSN  = PORTB0 53
  * MOSI = PORTB2 51
  * SCK  = PORTB1 52
  * MISO = PORTB3 50
  *
  */
   DDRB |= (1 << DDB4) | (1 << DDB2) | (1 << DDB1) | (1 << DDB0);
   
   SPCR |= (1<<SPE) | (1<<MSTR) | (1<<SPR0);

   SETBIT(PORTB, CSN_PIN);
   CLEARBIT(PORTB, CE_PIN);
}

void reset(void)
{
  delayMicroseconds(10);
  CLEARBIT(PORTB, CSN_PIN);
  delayMicroseconds(10);
  WriteByteSPI(W_REGISTER + STATUS);  
  delayMicroseconds(10);
  WriteByteSPI(0b01110000); 
  delayMicroseconds(10);
  SETBIT(PORTB, CSN_PIN);
}

void transmit_payload(uint8_t * W_buff)
{
  WriteToNrf(R, FLUSH_TX, W_buff, 0);
    
  WriteToNrf(R, W_TX_PAYLOAD, W_buff, PAYLOAD_WIDTH); 

  delay(10);    
  SETBIT(PORTB, CE_PIN);
  delayMicroseconds(20);   
  CLEARBIT(PORTB, CE_PIN);
  delay(10); 

}


void receive_payload(void)
{
  SETBIT(PORTB, CE_PIN);
  delay(1000);  
  CLEARBIT(PORTB, CE_PIN);
}

void nrf24L01_init(void)
{
  delay(100);
  
  uint8_t val[5]; 

 
  val[0]=0x01; 
  WriteToNrf(W, EN_AA, val, 1); 
  
  //SETUP_RETR (the setup for "EN_AA")
  val[0]=0x2F; 
  WriteToNrf(W, SETUP_RETR, val, 1);
  
  
  val[0]=0x01;
  WriteToNrf(W, EN_RXADDR, val, 1); //enable data pipe 0

  
  val[0]=0x03;
  WriteToNrf(W, SETUP_AW, val, 1); 

  val[0]=0x01;
  WriteToNrf(W, RF_CH, val, 1); 
  
  val[0]=0x07;
  WriteToNrf(W, RF_SETUP, val, 1); 
  
  
  int i;
  for(i=0; i<5; i++)  
  {
    val[i]=0x12;  
  }
  WriteToNrf(W, RX_ADDR_P0, val, 5); 
  
  
  for(i=0; i<5; i++)  
  {
    val[i]=0x12;  
  }
  WriteToNrf(W, TX_ADDR, val, 5); 
 
  val[0]=5;
  WriteToNrf(W, RX_PW_P0, val, 1);
  
  val[0]=0x1E;
  WriteToNrf(W, CONFIG, val, 1);

  delay(100); 

  //sei();  
}


uint8_t *WriteToNrf(uint8_t ReadWrite, uint8_t reg, uint8_t *val, uint8_t antVal) 
{

  
  if (ReadWrite == W) 
  {
    reg = W_REGISTER + reg;  
  }
  
  static uint8_t ret[32]; 
  
  delayMicroseconds(10); 
  CLEARBIT(PORTB, CSN_PIN);
  delayMicroseconds(10);    
  WriteByteSPI(reg);    
  delayMicroseconds(10);    
  
  int i;
  for(i=0; i<antVal; i++)
  {
    if (ReadWrite == R && reg != W_TX_PAYLOAD)
    {
      ret[i]=WriteByteSPI(NOP);
      delayMicroseconds(10);      
    }
    else 
    {
      WriteByteSPI(val[i]);
      delayMicroseconds(10);
    }   
  }
  SETBIT(PORTB, CSN_PIN);
  

  
  return ret;
}

char WriteByteSPI(unsigned char cData)
{
  //Load byte to Data register
  SPDR = cData; 
    
  /* Wait for transmission complete */
  while(!(SPSR & (1<<SPIF)));
  
  return SPDR;
}

uint8_t GetReg(uint8_t reg)
{  
  delayMicroseconds(10);
  CLEARBIT(PORTB, CSN_PIN);
  delayMicroseconds(10);
  WriteByteSPI(R_REGISTER + reg);
  delayMicroseconds(10);
  reg = WriteByteSPI(NOP);
  delayMicroseconds(10);
  SETBIT(PORTB, CSN_PIN);
  return reg;
}

