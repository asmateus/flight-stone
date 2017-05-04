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

#define CSN_PIN 2
#define CE_PIN 0
#define PAYLOAD_WIDTH 19

void initSPI(void);
char WriteByteSPI(unsigned char);
uint8_t GetReg(uint8_t);
uint8_t *WriteToNrf(uint8_t, uint8_t, uint8_t*, uint8_t);
void nrf24L01_init(void);
void receive_payload(void);
void reset(void);

uint8_t *data;
unsigned long i = 0;
unsigned long e = 0;
unsigned long l = 0;
void setup()
{
  Serial.begin(115200);
  delay(2000);
  
  initSPI();
  
  if(GetReg(STATUS) == 0x0E) {
     Serial.println("SPI initialization OK"); 
  }
  
  nrf24L01_init();
  i = micros();
  //Serial.println(PORTB);
}

void loop()
{
  receive_payload();
   
  if((GetReg(STATUS) & (1<<6)) == 0) {
    Serial.println("NOP");  
  }
  else {
    Serial.print("He contado: ");
    e = micros();
    l = e - i;
    i = micros();
    Serial.print(l);
    Serial.println(", Amo.");
    data = WriteToNrf(R, R_RX_PAYLOAD, data, PAYLOAD_WIDTH);
    //Serial.println((char*) data);
    /*for(int i = 0; i < 5; ++i) {
      Serial.print(data[i]);
      Serial.print(" ");  
    }
    Serial.println("");*/
    reset();
  }
}

void initSPI(void)
{
   DDRB |= (1 << DDB5) | (1 << DDB3) | (1 << DDB2) | (1 << DDB0);
   
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


void receive_payload(void)
{
  SETBIT(PORTB, CE_PIN);
  delay(20);  
  CLEARBIT(PORTB, CE_PIN);
}

void nrf24L01_init(void)
{
  delay(100);
  
  uint8_t val[5]; 

  val[0]=0x01; 
  WriteToNrf(W, EN_AA, val, 1); 
  
  val[0]=0x06;
  WriteToNrf(W, FEATURE, val, 1); //Seteo Feature DPL
  
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
 
  val[0]=PAYLOAD_WIDTH;
  WriteToNrf(W, RX_PW_P0, val, 1);
  
  val[0]=0x1F;
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


