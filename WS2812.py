#!/usr/bin/env python3

import time
from rpi_ws281x import PixelStrip, Color

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

# this function can be displayed if the sequence wass guessed wrong
def showWrongSequence(NUMBER_OF_BOARD_PANELS, strip, iterations=3):
    for i in range(iterations):
        for j in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, j, COLORS[1]) # set all pixels to red

        strip.show()
        time.sleep(0.5) # Needs fixing, dont use the sleep fuction!

        for j in range(NUMBER_OF_BOARD_PANELS):
            setPixelColor(strip, j, COLORS[0]) # set all colors to black aka off

        strip.show()
        time.sleep(0.5) # Needs fixing, dont use the sleep fuction!

def showCorrectSequence(NUMBER_OF_BOARD_PANELS, strip):
    for i in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, i, COLORS[3]) # set all pixels to green
    strip.show()
    time.sleep(0.5) # Needs fixing, dont use the sleep fuction!
    for j in range(NUMBER_OF_BOARD_PANELS):
        setPixelColor(strip, j, COLORS[0]) # set all colors to black aka off
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


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)
