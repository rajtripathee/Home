#define I2CADDR                 0X44
#define MEAS_HIGHREP_STRETCH    0x2C06
#define MEAS_MEDREP_STRETCH     0x2C0D
#define MEAS_LOWREP_STRETCH     0x2C10
#define MEAS_HIGHREP            0x2400
#define MEAS_MEDREP             0x240B
#define MEAS_LOWREP             0x2416
#define READSTATUS              0xF32D
#define CLEARSTATUS             0x3041
#define SOFTRESET               0x30A2
#define HEATER_ON               0x306D
#define HEATER_OFF              0x3066

class SHT31D {
public:
float readTemperature();
float readHumidity();
int begin(int i2c_address, uint8_t sht31_address);
int close(int file);
uint8_t crc8(const uint8_t *data, int len);

private:
float temp, humid;

 boolean readTempHum(void);
 void writeCommand(uint16_t cmd);
}
