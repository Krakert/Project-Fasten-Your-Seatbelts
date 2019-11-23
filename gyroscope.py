import smbus
import math
import time
 
# Register
# power_mgmt_1 = 0x6b
# power_mgmt_2 = 0x6c
 
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

# Variables for scaling data
SCALED_TO_USEFUL_DATA = 128
MAX_SCALED_DATA = 255
MIN_SCALED_DATA = -256
DELTA_SCALED_DATA = 510
MAX_SERVO_POS = 200 
 
print "Gyroscope Data"
while True:
    
    gyroscope_xout = read_word_2c(0x43)
    gyroscope_yout = read_word_2c(0x45)
    gyroscope_zout = read_word_2c(0x47)
    
    scaled_datax = gyroscope_xout / SCALED_TO_USEFUL_DATA
    scaled_datay = gyroscope_yout / SCALED_TO_USEFUL_DATA
    scaled_dataz = gyroscope_zout / SCALED_TO_USEFUL_DATA
    
    print scaled_datax
    servo_compatible_x = ((scaled_datax + MAX_SCALED_DATA) * MAX_SERVO_POS) / DELTA_SCALED_DATA
    servo_compatible_y = ((scaled_datay + MAX_SCALED_DATA) * MAX_SERVO_POS) / DELTA_SCALED_DATA
    servo_compatible_z = ((scaled_dataz + MAX_SCALED_DATA) * MAX_SERVO_POS) / DELTA_SCALED_DATA

    print "--------"
    print "GyroscopeX: %5d Scaled Data: %.2f" % (gyroscope_xout, servo_compatible_x)
    print "GyroscopeY: %5d Scaled Data: %.2f" % (gyroscope_yout, servo_compatible_y)
    print "GyroscopeZ: %5d Scaled Data: %.2f" % (gyroscope_zout, servo_compatible_z)
    time.sleep(1)