#import servo
import time
from rpi_ws281x import PixelStrip, Color
import WS2812
import RPi.GPIO as GPIO
import random

NUMBER_OF_BOARD_PANELS = 6
SEQUENCE_LED_ON_TIME = 1 #seconds
SEQUENCE_LED_OFF_TIME = 0.3 #seconds

BOARD_PANEL_PIN_1 = 4
BOARD_PANEL_PIN_2 = 0
BOARD_PANEL_PIN_3 = 0
BOARD_PANEL_PIN_4 = 0
BOARD_PANEL_PIN_5 = 0
BOARD_PANEL_PIN_BULL = 0

sequence = []
sequenseSize = 0

# LED strip configuration:
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

#color code hexdecimal
COLORS = [  0x000000,   #black
                0x200000,   # red
				0x201000,   # orange
				#0x202000,   # yellow
				0x002000,   # green
				#0x002020,   # lightblue
				0x000020,   # blue
				0x100010,   # purple
				#0x200010,   # pink
                0x202020, ] #white

GPIO.setmode(GPIO.BCM)

GPIO.setup(BOARD_PANEL_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(BOARD_PANEL_PIN_1, GPIO.RISING, bouncetime=500)
def panelCallback(self):
    print ('pushed!!!')
    panelOneHit()

GPIO.add_event_callback(BOARD_PANEL_PIN_1, panelCallback)

def panelOneHit():
    randomColor = random.randrange(0, 7)
    WS2812.setPixelColor(strip, 0, COLORS[randomColor])

def generateSequence():
    randomPanel = random.randrange(1, NUMBER_OF_BOARD_PANELS + 1)
    print('new number: %d' % (randomPanel))
    sequence.append(randomPanel)
    
    return sequence

def showSequence(newSequence):
    print('show the sequence')
    for element in newSequence:
        print(element)
        WS2812.setPixelColor(strip, element - 1, COLORS[element])
        time.sleep(SEQUENCE_LED_ON_TIME)
        WS2812.colorWipe(strip, COLORS[0])
        time.sleep(SEQUENCE_LED_OFF_TIME)

# Create NeoPixel object with appropriate configuration.
strip = PixelStrip(NUMBER_OF_BOARD_PANELS, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

while True:
    newSequence = generateSequence()

    showSequence(newSequence)

    time.sleep(0.5)
    
    # WS2812.rainbow(strip)


