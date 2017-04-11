/*
 * RF_Tranceiver.c
 *
 * Created: 2012-08-10 15:24:35
 *  Author: Kalle
 *  Atmega88
 */ 

#include <SPI.h>
#include <avr/io.h>
#include <stdio.h>
#define F_CPU 8000000UL  // 8 MHz
#include <util/delay.h>
#include <avr/interrupt.h>

#include "nRF24L01.h"

#define CSN_PIN 10
#define CE_PIN 8

void initSPI(void);
char WriteByteSPI(unsigned char);
uint8_t GetReg(uint8_t);
uint8_t *WriteToNrf(uint8_t, uint8_t, uint8_t*, uint8_t);
void nrf24L01_init(void);
void receive_payload(void);
void reset(void);

uint8_t *data;

void setup()
{
  Serial.begin(115200);
  
  initSPI();
  //Serial.println(GetReg(STATUS));
  
  nrf24L01_init();
}

void loop()
{
  _delay_us(100);
  receive_payload();
  
  Serial.println(GetReg(STATUS));  
  if((GetReg(STATUS) & (1<<6)) == 0) {
    //Serial.println("No data");  
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

void initSPI(void)
{
   pinMode(8,  OUTPUT);
   pinMode(10, OUTPUT);
   pinMode(11, OUTPUT);
   pinMode(13, OUTPUT);
   
   SPCR |= (1<<SPE) | (1<<MSTR) | (1<<SPR0);

   digitalWrite(CSN_PIN, HIGH);
   digitalWrite(CE_PIN, LOW);
}

void reset(void)
{
  _delay_us(10);
  digitalWrite(CSN_PIN, LOW);
  _delay_us(10);
  WriteByteSPI(W_REGISTER + STATUS);  
  _delay_us(10);
  WriteByteSPI(0b01110000); 
  _delay_us(10);
  digitalWrite(CSN_PIN, HIGH);
}


void receive_payload(void)
{
  digitalWrite(CE_PIN, HIGH);
  _delay_ms(1000);  
  digitalWrite(CE_PIN, LOW);
}

void nrf24L01_init(void)
{
  _delay_ms(100);
  
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
  
  val[0]=0x1F;
  WriteToNrf(W, CONFIG, val, 1);

  _delay_ms(100); 

  //sei();  
}


uint8_t *WriteToNrf(uint8_t ReadWrite, uint8_t reg, uint8_t *val, uint8_t antVal) 
{

  
  if (ReadWrite == W) 
  {
    reg = W_REGISTER + reg;  
  }
  
  static uint8_t ret[32]; 
  
  _delay_us(10); 
  digitalWrite(CSN_PIN, LOW);
  _delay_us(10);    
  WriteByteSPI(reg);    
  _delay_us(10);    
  
  int i;
  for(i=0; i<antVal; i++)
  {
    if (ReadWrite == R && reg != W_TX_PAYLOAD)
    {
      ret[i]=WriteByteSPI(NOP);
      _delay_us(10);      
    }
    else 
    {
      WriteByteSPI(val[i]);
      _delay_us(10);
    }   
  }
  digitalWrite(CSN_PIN, HIGH);
  

  
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
  _delay_us(10);
  CLEARBIT(PORTB, 2); //CSN low
  _delay_us(10);
  WriteByteSPI(R_REGISTER + reg);
  _delay_us(10);
  reg = WriteByteSPI(NOP);
  _delay_us(10);
  SETBIT(PORTB, 2); //CSN IR_High
  return reg;
}

