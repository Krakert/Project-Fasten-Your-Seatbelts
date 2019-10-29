#!/usr/bin/env python3

#import installed libraries
import time
from rpi_ws281x import PixelStrip, Color
import RPi.GPIO as GPIO
import random

#import files from our own project
import WS2812
import panelDetection
#import servo

#defines
NUMBER_OF_BOARD_PANELS = 6
SEQUENCE_LED_ON_TIME = 1 #seconds
SEQUENCE_LED_OFF_TIME = 0.3 #seconds

#variables
sequence = []
sequenseSize = 0
previousRandomNumber = 0

#enumeratie of 'switch case'
GEN_SEQUENCE = 1
SHOW_SEQUENCE = 2
DETECT_SEQUENCE = 3
CORRECT_SEQUENCE = 4
WRONG_SEQUENCE = 5

case = GEN_SEQUENCE

# LED strip configuration:
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53


def addToSequence(previousRandomNumber):
    randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    while randomPanel == previousRandomNumber:
        randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)

    print('new number: %d' % (randomPanel))
    sequence.append(randomPanel)

    return sequence, randomPanel

def showSequence(newSequence):
    print('show the sequence')
    for element in newSequence:
        print(element)
        WS2812.setPixelColor(strip, element - 1, WS2812.COLORS[element]) # turns the led on in the sequence
        time.sleep(SEQUENCE_LED_ON_TIME)
        WS2812.colorWipe(strip) #turns the leds off
        time.sleep(SEQUENCE_LED_OFF_TIME)

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(NUMBER_OF_BOARD_PANELS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

try:
    while True:

        if case == GEN_SEQUENCE:
            #case 1
            newSequence, randomPanel = addToSequence(previousRandomNumber)  # add random number (1 t/m 6) to sequence
            previousRandomNumber = randomPanel                              # prevents generating the same number
            case = SHOW_SEQUENCE

        if case == SHOW_SEQUENCE:
            # case 2
            showSequence(newSequence)                                       # show sequence to the player
            case = DETECT_SEQUENCE

        if case == DETECT_SEQUENCE:
            # case 3
            valid = panelDetection.guessSequence(newSequence)               # returns 1 if the sequence was correct, 2 if incorrect

            if valid == 1:
                case = CORRECT_SEQUENCE
            if valid == 2:
                case = WRONG_SEQUENCE

        if case == CORRECT_SEQUENCE:
            print("Correct!\n")
            time.sleep(3)       # Needs fixing, dont use the sleep fuction!
            case = GEN_SEQUENCE                                             # if the sequence was correct, add one to the sequence

        if case == WRONG_SEQUENCE:
            print("Incorrect! jammer joh...\n")
            newSequence.clear()                                             # clear array
            WS2812.showWrongSequence(NUMBER_OF_BOARD_PANELS, strip)         # show blinking red LEDs                    
            case = GEN_SEQUENCE                                             # if the sequence was incorrect, generate new sequence

        # WS2812.rainbow(strip)

except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
