#
# TO DO: Add support for the little endian / big endian data
#

import pi_platform as Platform


def default_bus():
    plat = Platform.detect_platform()
    if plat == Platform.PI:
        if Platform.revision() == 1.0:
            return 0
        else:
            # busnum is 1 for Raspberry Pi B and above.
            return 1
    else:
        raise RuntimeError ("I2c Bus for the platform could not be detected.")

def i2c_device(address, busnum=None, i2c_interface=None, **kwargs):
    if busnum == None:
        busnum = default_bus()
    return Device(address, busnum, i2c_interface, **kwargs)  

class Device(object):
    def __init__(self, address, busnum, i2cinterface=None):
        self._address = address
        if i2cinterface is None:
            import smbus
            self._bus = smbus.SMBus(busnum)
        else:
            self._bus = i2cinterface(busnum)
    
    def writeRaw8bit(self,data):
        # Write 8-bit data on the bus.
        data = data & 0xFF
        self._bus.write_byte(self._address, data)

    def write8bit(self,register,data):
        # Write 8-bit data to the specified register.
        data = data & 0xFF
        self._bus.write_byte_data(self._address, register, data)

    def write16bit(self,register,data):
        # Write 16-bit data to the specified register.
        data = data & 0xFFFF
        self._bus.write_word_data(self._address, register, data)
    
    def writeBlock(self,register, data):
        # Write block of data to the specified register.
        self._bus.write_i2c_block_data(self._address, register, data)
    
    def readRaw8bit(self):
        # Read 8-bit data on the bus.
        data = self._bus.read_byte(self._address) & 0xFF
        return data
    
    def readU8bit(self, register):
        # Read unsigned  8-bit from the specified register.
        data = self._bus.read_byte_data(self._address, register) & 0xFF
        return data
    
    def readS8bit(self, register):
        # Read signed 8-bit from the specified register.
        data = self.readU8bit(register)
        if data > 127:
            data -= 256
        return data
    
    def readU16bit(self, register, little_endian = True):
        # Read Un
        data = self._bus.read_word_data(self._address, register) & 0xFFFF
        if not little_endian:
            data = ((data <<8) & 0xFF00) + (data >> 8)
        return data

    def readS16bit(self, register, little_endian=True):
        # Read signed 16-bit data from the specified register on the specified endianesss.
        data = self.readU16bit(register, little_endian)
        if data > 32767:
            data -= 65536
        return data

    def readBlock(self, register, length):
        # Read block of data of length from the register
        data = self._bus.read_i2c_block_data(self._address, register, length)
        return data
