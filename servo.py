
import RPi.GPIO as GPIO
import time

#defines
SERVO_CHANNEL = 16
CENTER = 600
LEFT_MAX = 1150
RIGHT_MAX = 250

#variables
currentPosition = CENTER
runTimeServo = 0

timeNow = time.time()
#init the PWM
GPIO.setup(SERVO_CHANNEL, GPIO.OUT)
pwm = GPIO.PWM(SERVO_CHANNEL, 50)
pwm.start((CENTER/100))

def testServo():
    global CENTER
    global LEFT_MAX
    global RIGHT_MAX
    global currentPosition

    pwm.ChangeDutyCycle((LEFT_MAX/100))
    time.sleep(10)

    pwm.ChangeDutyCycle((RIGHT_MAX/100))
    time.sleep(10)

    pwm.ChangeDutyCycle((CENTER/100))
    currentPosition = CENTER
    time.sleep(10)

    
#this function will set the board to the center
def setBoardCenter():
    global CENTER
    global currentPosition

    currentPosition = CENTER
    pwm.ChangeDutyCycle((CENTER/100))

#this function rotates the board. Direction is collected from the MPU6050
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


def timerServo():
    global timeNow
    global runTimeServo
    if time.time() - timeNow > 1:
        runTimeServo = runTimeServo + 1
        timeNow = time.time()
    return runTimeServo