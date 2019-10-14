import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

GPIO.setmode(GPIO.BOARD)
#gebruik pin 11 voor de servo
GPIO.setup(11,GPIO.OUT)
#zet de pwm op pin 11 op 50Hz
pwm=GPIO.PWM(11,50)

#start PWM
pwm.start(5)
time.sleep(0.2)

#degrees moeten tussen 0 en 200 zijn
def setServo(degrees):
    servoPos = (degrees / 40) + 5
    pwm.ChangeDutyCycle(servoPos)

# pwm.ChangeDutyCycle(7.5)
# time.sleep(2)

# pwm.ChangeDutyCycle(10)
# time.sleep(2)
# print ('Done executing program!')
