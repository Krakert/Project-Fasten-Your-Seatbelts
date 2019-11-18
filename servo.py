import RPi.GPIO as GPIO
import time

# this library is used to generate a timer
# https://www.geeksforgeeks.org/timer-objects-python/
import threading

SERVO_PIN 16
SERVO_PWM_FREQ = 50 #frequentie in Hz

INTERVAL_SECONDS = 0.005 #5ms

START_POS_SERVO = 7.5 #can range between 5 and 10
SERVO_STEP_PER_DEGREE = 0.025
targetPosition = 0
currentPosition = 0

GPIO.setwarnings(False)

def timerCallback():
    global targetPosition
    print("Test\n")
    
    if targetPosition < currentPosition:
        servoPos += SERVO_STEP_PER_DEGREE
        pwm.ChangeDutyCycle(servoPos)

    if targetPosition > currentPosition:
        servoPos -= SERVO_STEP_PER_DEGREE
        pwm.ChangeDutyCycle(servoPos)
    

#start the timer
timer = threading.Timer(INTERVAL_SECONDS, timerCallback)

GPIO.setmode(GPIO.BOARD)
#use GPIO 16(PWM) for the servo
GPIO.setup(SERVO_PIN, GPIO.OUT)
#set PWM at 50Hz
pwm=GPIO.PWM(SERVO_PIN, SERVO_PWM_FREQ)



#start PWM
def startPWM():
    global currentPosition
    global targetPosition

    pwm.start(START_POS_SERVO)
    currentPosition = START_POS_SERVO
    targetPosition = START_POS_SERVO
    time.sleep(0.5)

#this function can start the timer used for controlling the servo
def startTimer():
    timer.start()

#this function can stop the timer used for controlling the servo
def stopTimer():
    timer.cancel()

#degrees must be a value between 0 and 200
#if the value is not valid the function will return False
def setServo(degrees):
    global targetPosition

    if degrees <= 200 and degrees >= 0:
        targetPosition = (degrees / 40) + 5
        return True
    
    else:
        print("Used a invalid value for setServo!\n")
        return False

