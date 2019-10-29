import smbus
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    value = read_word(reg)
    if value >= 0x8000:
        return -((65535 - value) + 1)
    else:
        return value
    
bus = smbus.SMBus(1) 
# Used Adress via i2c Detect
address = 0x68
 
# Activate, to approach the model
bus.write_byte_data(address, power_mgmt_1, 0)
 
print "Gyroscope Data"
while True:
    SCALED_TO_USEFUL_DATA = 128.0
    gyroscope_xout = read_word_2c(0x43)
    gyroscope_yout = read_word_2c(0x45)
    gyroscope_zout = read_word_2c(0x47)
    print gyroscope_xout
    print "--------"
    print "GyroscopeX: %5d Scaled Data: %.2f" % (gyroscope_xout, gyroscope_xout / SCALED_TO_USEFUL_DATA)
    print "GyroscopeY: %5d Scaled Data: %.2f" % (gyroscope_yout, gyroscope_yout / SCALED_TO_USEFUL_DATA)
    print "GyroscopeZ: %5d Scaled Data: %.2f" % (gyroscope_zout, gyroscope_zout / SCALED_TO_USEFUL_DATA)
    time.sleep(1)