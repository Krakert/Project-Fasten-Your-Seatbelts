#!/usr/bin/env python3

#import installed libraries
import smbus
import math

#defines
POWER_MGMT_1 = 0x6b         # See line 45.
BUS = smbus.SMBus(1)        # Make use of the I2C bus.
ADDRESS = 0x68              # The address where it IC can ben found.
SCALE_FACTOR = 16384.0      # See line 51.

#variables
threshold = 12              # The minimum angle.

# Get the two 8 bits and glue them together.
def readWord(reg):
    h = BUS.read_byte_data(ADDRESS, reg)
    l = BUS.read_byte_data(ADDRESS, reg+1)
    value = (h << 8) + l
    return value
 
def readWord2c(reg):
    val = readWord(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def getRotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    direction = math.degrees(radians)
    if direction <- threshold:
        return 1                                        # When the controller is held to the right.
    elif direction > threshold:
        return 2                                        # When the controller is held to the right.
    else:   
        return 0                                        # If controller is within the set threshold.
    
def main():
    try:                                                # I2C is not in the best condition over a long wire.
        BUS.write_byte_data(ADDRESS, POWER_MGMT_1, 0)   # Get the MPU6050 out of sleep mode, page 40, 4.28, Register 107.

        accelerationXout = readWord2c(0x3b)             # Read all the info off the accelerometer
        accelerationYout = readWord2c(0x3d)             # MPU-6000/MPU-6050 Register Map and Descriptions
        accelerationZout = readWord2c(0x3f)             # Page 29, 4.17, Registers 59 to 64.

        accelerationXoutScaled = accelerationXout / SCALE_FACTOR  # Scale al the data , Sensitivity Scale Factor
        accelerationYoutScaled = accelerationYout / SCALE_FACTOR  # MPU-6000/MPU-6050 Product Specification,
        accelerationZoutScaled = accelerationZout / SCALE_FACTOR  # Page 13, 6.2, Accelerometer Specifications.

        direction = (getRotation(accelerationXoutScaled, accelerationYoutScaled, accelerationZoutScaled))
        return direction                                # Return a 0, 1 or 2 back to the program.

    except OSError:
        print ("Can`t open bus I2C, ignore me")         # If the I2C data is not great


    
