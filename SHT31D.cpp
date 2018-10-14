#include <unistd.h>
#include <linux/i2c-dev.h>
#include <time.h>
#include "SHT31D.h"

int SHT31D::begin(int i2c_address, uint8_t sht31_address){
 char filename[20];
 int fp;

 snprintf(filename, 19, "/dev/i2c-%d", i2c_address);
 fp = open(filename, O_RDWR);
 if (fp < 0) {
  return fp;
 }

 if (ioctl(fp, I2C_SLAVE, I2CADDR ) < 0) {
  close(fp);
  return -1;
  }
  
	return fp;
}
	
int SHT31D::close(int fp){
  return close(fp);

}

unsigned int SHT31D:: readwriteCommand(int fp,uint16_t cmd, uint8_t *buffer, int readSize){
  int sts;
  int sendSize = 2;
  uint8_t send[sendSize];

  // big-endian : split the 16 bit word to two 8 bits that are flipped
  send[0] = (cmd >> 8) & 0xff;
  send[1] = cmd & 0xff;

  sts = write (fp, send, sendSize);
  if ( sendSize != sts){
    return -1;
  }
  if (readSize > 0){
    delay(10);
    sts = read(fp, buffer, readSize);
    if (sta < readSize){
      return -1;
    }
  }
  return 0;
}

unsigned int SHT31D:: getSerialNum(int file, uint32_t * serialNum){
  uint8_t buffer[10];
  int id;

  id = writeandread(file, READ_SERIALNUM, buffer, 6);
  if( 0 !=  id)
    return id;
  else {
    *serialNum = ((uint32_t)buffer[0]<< 24)
                | ((uint32_t)buffer[1] << 16)
                | ((uint32_t)buffer[3] << 8)
                | (uint32_t)buffer[4];
    if (buffer[2] != crc8(buffer,2) || buffer[5] != crc8(buffer +3,2))
      return -1;
    
  }
  return 1;
}
uint8_t SHT31D::crc8(const uint8_t *data, int len)
{
/*
*
 * CRC-8 formula from page 14 of SHT spec pdf
 *
 * Test data 0xBE, 0xEF should yield 0x92
 *
 * Initialization data 0xFF
 * Polynomial 0x31 (x8 + x5 +x4 +1)
 * Final XOR 0x00
 */

  const uint8_t POLYNOMIAL(0x31);
  uint8_t crc(0xFF);
  
  for ( int j = len; j; --j ) {
      crc ^= *data++;

      for ( int i = 8; i; --i ) {
	crc = ( crc & 0x80 )
	  ? (crc << 1) ^ POLYNOMIAL
	  : (crc << 1);
      }
  }
  return crc;
}
