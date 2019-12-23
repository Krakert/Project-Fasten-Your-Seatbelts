
import RPi.GPIO as GPIO
import time

#defines
SERVO_CHANNEL = 16
CENTER = 60
LEFT_MAX = 115
RIGHT_MAX = 25

#variables
currentPosition = CENTER

#init the PWM
GPIO.setup(SERVO_CHANNEL, GPIO.OUT)
pwm = GPIO.PWM(SERVO_CHANNEL, 50)
pwm.start((CENTER/10))

def setBoardCenter():
    global CENTER
    global currentPosition

    currentPosition = CENTER
    pwm.ChangeDutyCycle((CENTER/10))
    time.sleep(2)
 
def rotateBoard(direction):
    global currentPosition
    global LEFT_MAX
    global RIGHT_MAX
    
    DELAY = 0.25
    
    if direction == 1:
        currentPosition = currentPosition + 1
        if currentPosition > LEFT_MAX:
            currentPosition = LEFT_MAX

    elif direction == 2:
        currentPosition = currentPosition - 1
        if currentPosition < RIGHT_MAX:
            currentPosition = RIGHT_MAX
        
    #print(currentPosition)
    pwm.ChangeDutyCycle((currentPosition/10))
    #time.sleep(DELAY)
 