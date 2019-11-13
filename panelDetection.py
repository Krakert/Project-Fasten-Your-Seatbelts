#!/usr/bin/env python3

#import installed libraries
import RPi.GPIO as GPIO
import time

# Pin defines
GPIO.setmode(GPIO.BCM)
BOARD_PANEL_PINS = [4, 17, 27, 22, 14, 23]
GPIO.setup(BOARD_PANEL_PINS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


BOARD_PANEL_PIN_1 = 4
BOARD_PANEL_PIN_2 = 17
BOARD_PANEL_PIN_3 = 27
BOARD_PANEL_PIN_4 = 22
BOARD_PANEL_PIN_5 = 14
BOARD_PANEL_PIN_6 = 23

# variables
callbackValue = 0
iteration = 0

#defines
PANEL_BOUNCETIME = 500 # time in ms
CORRECT_SEQUENCE = 1
INVALID_SEQUENCE = 2

# can set an bit in a value
def setBit(number, pos): 
    return ((1 << pos) | number)

# can check an bit in a value
def check_bit(var, bitNumber):
    return ((1 << var) & bitNumber)

#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# setup an interrupt for all board panel pins
# all the panels use the same value and set the bits in the value to show they are set

# GPIO setup panel 1
GPIO.add_event_detect(BOARD_PANEL_PINS[0], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback1(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 1)
    print('Pushed 1: %d' % (callbackValue))
GPIO.add_event_callback(BOARD_PANEL_PINS[0], panelCallback1)

# GPIO setup panel 2
GPIO.add_event_detect(BOARD_PANEL_PINS[1], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback2(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 2)
    print('Pushed 2: %d' % (callbackValue))
GPIO.add_event_callback(BOARD_PANEL_PINS[1], panelCallback2)

# GPIO setup panel 3
GPIO.add_event_detect(BOARD_PANEL_PINS[2], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback3(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 3)
    print('Pushed 3: %d' % (callbackValue))
GPIO.add_event_callback(BOARD_PANEL_PINS[2], panelCallback3)

# GPIO setup panel 4
GPIO.add_event_detect(BOARD_PANEL_PINS[3], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback4(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 4)
    print('Pushed 4: %d' % (callbackValue))
GPIO.add_event_callback(BOARD_PANEL_PINS[3], panelCallback4)

# GPIO setup panel 5
GPIO.add_event_detect(BOARD_PANEL_PINS[4], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback5(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 5)
    print('Pushed 5: %d' % (callbackValue))  
GPIO.add_event_callback(BOARD_PANEL_PINS[4], panelCallback5)

# GPIO setup panel 6
GPIO.add_event_detect(BOARD_PANEL_PINS[5], GPIO.RISING, bouncetime= PANEL_BOUNCETIME)
def panelCallback6(self):
    global callbackValue
    callbackValue = setBit(callbackValue, 6)
    print('Pushed 6: %d' % (callbackValue))  
GPIO.add_event_callback(BOARD_PANEL_PINS[5], panelCallback6)

# this function checks if the correct panel is hit of the board
# it will return True if the sequence was correct
# if the player makes a mistake it will instantly retrun False
def guessSequence(newSequence):
    global callbackValue
    global iteration

    lengthOfArray = len(newSequence)            # lookup length of the sequence 
    currentIndex = newSequence[iteration]       # panelnumber you currently want to throw at
    positionSetBit = lookupSetBit()             # returns the panelnumber that was hit 

    # checks if the correct panel was hit
    if currentIndex == positionSetBit and positionSetBit != 0:
        iteration += 1                          # let's go to the next step!
                                                
        if lengthOfArray == iteration:          # check if the last panel was hit 
            iteration = 0                       # reset
            return CORRECT_SEQUENCE    
    
    # checks if the wrong panel was hit
    if currentIndex != positionSetBit and positionSetBit != 0:
        iteration = 0                           # reset
        return INVALID_SEQUENCE


                                                # this function looks which panel is hit
                                                # if a panel is hit it will make a bit high in a value
                                                # by checking which bit is set we can conclude which panel was hit in the interrupt
def lookupSetBit():
    global callbackValue
    temp = 0                                    # define temporary value
    
    for i in range(7):                          # check position of set bit
        temp = check_bit(i, callbackValue)      # returns value > 0 if bit is set
        if temp > 1:
            callbackValue = 0                   # clear all bits
            return i                            # return the found location of the set bit
    return 0                                    # if nothing is found