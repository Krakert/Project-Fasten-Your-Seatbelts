import smbus
import math

power_mgmt_1 = 0x6b
bus = smbus.SMBus(1)
address = 0x68
threshold = 12
  
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    direction = math.degrees(radians)
    if direction <- threshold:
        return 1
    elif direction > threshold:
        return 2
    else:   
        return 0
    
def main():    

    bus.write_byte_data(address, power_mgmt_1, 0) 

    acceleration_xout = read_word_2c(0x3b)
    acceleration_yout = read_word_2c(0x3d)
    acceleration_zout = read_word_2c(0x3f)
    
    acceleration_xout_scaled = acceleration_xout / 16384.0
    acceleration_yout_scaled = acceleration_yout / 16384.0
    acceleration_zout_scaled = acceleration_zout / 16384.0
    
    direction = (get_rotation(acceleration_xout_scaled, acceleration_yout_scaled, acceleration_zout_scaled))
    return direction

    
