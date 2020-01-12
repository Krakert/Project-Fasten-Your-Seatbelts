# This file is used to share the gamemode
# The RFID uses this variable to check the tag.
# if gameModeCase != the program wont have to look at the tag.
gameModeCase = 0


# LED strip configuration:
L_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
L_HZ = 800000       # LED signal frequency in hertz (usually 800khz)
L_DMA = 10          # DMA channel to use for generating signal (try 10)
L_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
L_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
L_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
