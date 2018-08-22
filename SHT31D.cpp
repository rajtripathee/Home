#include <unistd.h>
#include <linux/i2c-dev.h>
#include "SHT31D.h"

int SHT31D::begin(int i2c_address, uint8_t sht31_address){
 char filename[20];
 int fp;

 snprintf(filename, 19, "/dev/i2c-%d", i2c_address);
 fp = open(filename, O_RDWR);
 if (fp < 0) {
  return fp;
 }

 if (ioctl(fp, I2C_SLAVE, sht31_address) < 0) {
  close(fp);
  return -1;
  }
  
	return fp;
}
	
int SHT31D::close(int fp){
  return close(fp);
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
