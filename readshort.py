import RPi.GPIO as GPIO
import sys
import signal

#sys.path.append('/home/pi/MFRC522-python')
from mfrc522 import SimpleMFRC522

#This function tests if the id of the scanned tag is similar to the id of the admin tag and returns true or false based on the id.
def acces(check):
        id = check
        value = True
        if id == int(154162618071):
            print("TRUE")
            print(value)
            return value
        else:
            value = not value
            print("False")
            print(value)
        return value

#This function reads out the id from the tag
def read():
    id, text = reader.read()
    print(id)
    print(text)
    acces(id)


reader = SimpleMFRC522()


print("Hold a tag near the reader")
#continue_reading = True
#while continue_reading:
try:
    read()
finally:
    GPIO.cleanup()