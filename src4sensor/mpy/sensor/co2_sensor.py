import machine
import time
from micropython import const

class SCD4X:
    
    # ref. 3.4 SCD4x Command Overview
    RESISTER_ADDRESS=0x62 # p7 3 Digital Interface Description
    START_PERIODIC_MEASUREMENT=const(0x21B1) #p9 3.5.1 start_periodic_measurement
    READ_MEASUREMENT = const(0xEC05) #p9 3.5.2 read_measurement 
    STOP_PERIODIC_MEASUREMENT = const(0x3F86)#p10 3.5.3 stop_periodic_measurement
    DATA_READY_STATUS = const(0xE4B8)

    def __init__(self, i2c_bus, address=RESISTER_ADDRESS):
        
        # sensor properties
        # ref. "3.3 Command Sequence Types" in Data Sheet.
        self.i2c = i2c_bus
        self.address = address # bytearray([0x62])
        self._buffer = bytearray(18) # 18byte is 144bit, data 0xXX(16bit)*9
        self._cmd = bytearray(2) # 16bit, address MSB + LSB
        self._crc_buffer = bytearray(2)

        # numerical data
        self._temp = 0
        self._humi = 0
        self._co2 = 0

    def __del__(self):
        # for forgetting stop_periodic_measurement
        self.stop_periodic_measurement()

    @property
    def temp(self):
        # returns the current temp in degrees celsius
        if self.data_ready_status:
            self._read_data()
        return self._temp

    @property
    def humi(self):
        # return the current humi in %rH
        if self.data_ready_status:
            self._read_data()
        return self._humi

    @property
    def co2(self):
        # return the current co2 in parts per million
        if self.data_ready_status:
            self._read_data()
        return self._co2

    @property
    def data_ready_status(self):
        # check the sensor to read if new data is available
        self._send_cmd(self.DATA_READY_STATUS, cmd_delay=0.01)
        #self._read_reply(self._buffer, 3)
        self._read_reply(3)
        #return not ((self._buffer[0] & 0x03 == 0) and (self._buffer[1] == 0))
        return not ((self._buffer[0] & 0x07 == 0) and (self._buffer[1] == 0))

    def _send_cmd(self, command, cmd_delay=0.0):
        self._cmd[0] = (command >> 8) & 0xFF # MSB
        self._cmd[1] = command & 0xFF # LSB
        self.i2c.writeto(self.address, self._cmd)
        time.sleep(cmd_delay)

    def _read_data(self):
        # read temp/humi/co2
        self._send_cmd(self.READ_MEASUREMENT, cmd_delay=0.001)
        #self._read_reply(self._buffer, 9)
        self._read_reply(9)
        # analysis
        self._co2 = (self._buffer[0] << 8) | self._buffer[1]
        temp = (self._buffer[3] << 8) | self._buffer[4]
        self._temp = -45 + 175 * (temp/(2**16))
        humi = (self._buffer[6] << 8) | self._buffer[7]
        self._humi = 100 * (humi/(2**16))

    def _read_reply(self, num):
        self._buffer = self.i2c.readfrom(self.address, num)
        self._check_buffer_crc(self._buffer[0:num])

    """
    def _read_reply(self, buffer, num):
        self.i2c.readfrom_into(self.address, buffer, num) # read data
        self._check_buffer_crc(self._buffer[0:num])
    """

    def start_periodic_measurement(self):
        # Starts periodic measurements mode, every 5 seconds
        # Available CMD:
        # read_measurement,
        # stop_periodic_measurement,
        # set_ambient_pressure
        # get_data_ready_status
        self._send_cmd(self.START_PERIODIC_MEASUREMENT, cmd_delay=0.01)

    def stop_periodic_measurement(self):
        # stop measurement mode
        self._send_cmd(self.STOP_PERIODIC_MEASUREMENT, cmd_delay=0.5)

    def _check_buffer_crc(self, buffer):
        # check sum by crc8
        for i in range(0, len(buffer), 3):
            self._crc_buffer[0] = buffer[i] # Data MSB
            self._crc_buffer[1] = buffer[i + 1] # Data LSB
            if self._calc_crc8(self._crc_buffer) != buffer[i + 2]:
                raise RuntimeError("CRC check faild because reading now")
        return True


    def _calc_crc8(self, crc_buffer):
        # ref. p18 3.11 CHecksum Calculation
        # crc is Cyclic Redundancy Check
        result_crc = 0xFF # 255(int)
        for crc_byte in crc_buffer:
            result_crc ^= crc_byte
            for _ in range(8):
                if result_crc & 0x80:
                    result_crc = (result_crc << 1) ^ 0x31
                else:
                    result_crc = result_crc << 1
        return result_crc & 0xFF