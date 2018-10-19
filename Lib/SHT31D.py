import smbus
import time
from time import sleep

# Default address
I2CADDR = 0X44

# Registers
MEAS_HIGHREP_STRETCH = 0x2C06
MEAS_MEDREP_STRETCH = 0x2C0D
MEAS_LOWREP_STRETCH = 0x2C10
MEAS_HIGHREP = 0x2400
MEAS_MEDREP = 0x240B
MEAS_LOWREP = 0x2416
READSTATUS = 0xF32D
CLEARSTATUS = 0x3041
SOFTRESET = 0x30A2
HEATER_ON = 0x306D
HEATER_OFF = 0x3066
    


class SHT31D:
    def __init__(self, address = I2CADDR, i2c=None, **kwargs):
        if i2c is None:
            import I2C
            i2c = I2C
        self._device = i2c.i2c_device(address, **kwargs)
        self.write(SOFTRESET)
        sleep(0.05)
        #self.command(SOFTRESET);

    def write(self,cmd):
        self._device.write8bit(cmd >> 8, cmd & 0xFF)
    
    def read(self):
        self.write(READSTATUS)
        temp = self._device.readBlock(0,3)
        stat = temp[0] << 8 | temp[1]
        if temp[2] != self._crc8(temp[0:2]):
            return None
        return stat
    
    def clear(self):
        self.write(CLEARSTATUS)
    
    def reset(self):
        self.write(SOFTRESET)
        sleep(0.2)

    def temperature_humidity(self):
        self.write(MEAS_HIGHREP)
        sleep(0.02)
        temp = self._device.readBlock(0, 6)
        
        if temp[2] != self._crc8(temp[0:2]):
            return(float("NAN"),float("NAN"))

        rawTemperature = temp[0] << 8 | temp[1]
        temperature = 175.0 * rawTemperature / 0xFFFF - 45.0

        if temp[5] != self._crc8(temp[3:5]):
            return(float("NAN"),float("NAN"))
        
        rawHumidity = temp[3] << 8 | temp[4]
        humidity = 100.0 * rawHumidity / 0xFFFF

        return (temperature, humidity)

    def temperature(self):
        (temperature, humidity) = self.temperature_humidity()
        return temperature
    
    def humidity(self):
        (temperature, humidity) = self.temperature_humidity()
        return humidity
    
    def heater(self, value = False):
        if value:
            self.write(HEATER_ON)
        else:
            self.write(HEATER_OFF)


    def _crc8(self, buffer):
        """ Polynomial 0x31 (x8 + x5 +x4 +1) """

        polynomial = 0x31
        crc = 0xFF
  
        index = 0
        for index in range(0, len(buffer)):
            crc ^= buffer[index]
            for i in range(8, 0, -1):
                if crc & 0x80:
                    crc = (crc << 1) ^ polynomial
                else:
                    crc = (crc << 1)
        return crc & 0xFF
        


