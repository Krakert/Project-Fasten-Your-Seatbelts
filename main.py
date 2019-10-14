import servo
import time

SLEEPTIME = 3

servo.setServo(200)
time.sleep(SLEEPTIME)

servo.setServo(100)
time.sleep(SLEEPTIME)

servo.setServo(150)
time.sleep(SLEEPTIME)

servo.setServo(50)
time.sleep(SLEEPTIME)

servo.setServo(0)
time.sleep(SLEEPTIME)

print ('Done executing program!')
