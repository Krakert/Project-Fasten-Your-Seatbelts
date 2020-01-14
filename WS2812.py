#!/usr/bin/env python3

#import installed libraries
import time
from rpi_ws281x import PixelStrip, Color

#import files from our own project
import sqlHandling as SQL

#color code hexdecimal
COLORS = [  0x000000,   # black
            0x200000,   # red
			0x201000,   # orange
			#0x202000,  # yellow
			0x002000,   # green
			#0x002020,  # light-blue
			0x000020,   # blue
			0x100010,   # purple
			#0x200010,  # pink
            0x202020, ] # white

#this function will be used to test the leds of the board
def testPixel(strip, NUMBER_OF_BOARD_PANELS):
    for i in range(NUMBER_OF_BOARD_PANELS + 1):
            setPixelColor(strip, i, COLORS[6]) # set a pixel to white

            time.sleep(0.5)
            setPixelColor(strip, i, COLORS[0]) # turn the pixel off

# this function can be used to turn all the leds off
def colorWipe(strip):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, COLORS[0]) # set all colors to black aka off
        strip.show()
        #time.sleep(wait_ms / 1000.0)

# this function can be used to turn on a led with a wanted color
def setPixelColor(strip, pixelNum, color):
        """Set color for a pixel"""
        strip.setPixelColor(pixelNum, color)
        strip.show()

def showSequence(strip, newSequence, SEQUENCE_LED_ON_TIME, SEQUENCE_LED_OFF_TIME):
    print('show the sequence')
    for element in newSequence:
        print(element)
        setPixelColor(strip, element - 1, COLORS[element])                                          # turns the led on in the sequence
        time.sleep(SEQUENCE_LED_ON_TIME)
        setPixelColor(strip, element - 1, COLORS[0])                                                # turns the led on in the sequence
        time.sleep(SEQUENCE_LED_OFF_TIME)

# this function can be displayed if the sequence wass guessed wrong
def showWrongSequence(NUMBER_OF_BOARD_PANELS, strip, iterations = 3):
    for _ in range(iterations):
        for j in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, j, COLORS[1])                                                      # Set all pixels to red.

        strip.show()
        time.sleep(0.5)                                                                             # Needs fixing, dont use the sleep fuction!

        for j in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, j, COLORS[0])                                                      # Set all colors to black aka off.

        strip.show()
        time.sleep(0.5)                                                                             # Needs fixing, dont use the sleep fuction!

def showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip):
    for i in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, i, COLORS[3])                                                          # Set all pixels to green.
    strip.show()
    time.sleep(0.5)                                                                                 # Needs fixing, dont use the sleep fuction!
    for j in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, j, COLORS[0])                                                          # Set all colors to black aka off.
    strip.show()

def showPanelHit(strip, valid, SHOW_HIT_ON_TIME):
    setPixelColor(strip, valid - 1, COLORS[valid])                                                  # Turn on the led corresponding to the switch that was detected.
    time.sleep(SHOW_HIT_ON_TIME)
    setPixelColor(strip, valid - 1, COLORS[0])                                                      # Turn the led off.

def checkPlayerTooClose(NUMBER_OF_BOARD_PANELS, strip, distance, MIN_DISTANCE):
    if distance < MIN_DISTANCE:
        for i in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, i, COLORS[2])                                                      # Set all pixels to orange.
        strip.show()
        print('Distance must be greater than %dcm, distance= %dcm' % (MIN_DISTANCE, distance))
        time.sleep(1)                                                                               # Otherwise the led's will start flashing.
        return True
    else:
        for j in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, j, COLORS[0])                                                      # Set all colors to black aka off.
        strip.show()
        return False

def showWinnerPlayer1(NUMBER_OF_BOARD_PANELS, strip):
    for i in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, i, COLORS[1])                                                          # Set all pixels to purple.
    strip.show()                                                                                    # Contra of the player that needs
                                                                                                    # to play.
def showWinnerPlayer2(NUMBER_OF_BOARD_PANELS, strip):
    for i in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, i, COLORS[4])                                                          # Set all pixels to blue.
    strip.show()                                                                                    # Contra of the player that needs
                                                                                                    # to play.
def setCurrentPlayer(NUMBER_OF_BOARD_PANELS, strip, player):
    if player:
        setPixelColor(strip, NUMBER_OF_BOARD_PANELS, COLORS[4])                                     # Set all pixels to blue.
    else:
        setPixelColor(strip, NUMBER_OF_BOARD_PANELS, COLORS[1])                                     # Set all pixels to puple.

    strip.show()



#this can show a rainbow with the WS2812 LEDs
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(strip, wait_ms=15, iterations = 1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        if SQL.checkGameMode() != 0 or SQL.getTestData()[0] == 1:
            break
        time.sleep(wait_ms / 1000.0)
