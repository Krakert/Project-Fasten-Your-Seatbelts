
import RPi.GPIO as GPIO
import time

#defines
SERVO_CHANNEL = 16
CENTER = 600
LEFT_MAX = 1150
RIGHT_MAX = 250

#variables
currentPosition = CENTER

#init the PWM
GPIO.setup(SERVO_CHANNEL, GPIO.OUT)
pwm = GPIO.PWM(SERVO_CHANNEL, 50)
pwm.start((CENTER/100))

def setBoardCenter():
    global CENTER
    global currentPosition

    currentPosition = CENTER
    pwm.ChangeDutyCycle((CENTER/100))

def rotateBoard(direction):
    global currentPosition
    global LEFT_MAX
    global RIGHT_MAX
    
    if direction == 1:
        currentPosition = currentPosition + 1
        if currentPosition > LEFT_MAX:
            currentPosition = LEFT_MAX

    elif direction == 2:
        currentPosition = currentPosition - 1
        if currentPosition < RIGHT_MAX:
            currentPosition = RIGHT_MAX

    pwm.ChangeDutyCycle((currentPosition/100))
