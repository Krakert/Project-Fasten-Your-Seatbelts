import RPi.GPIO as GPIO
import sys
from mfrc522 import SimpleMFRC522

#Calling the SimpleMfrc522 library and assigning it to the variable 'reader'
reader = SimpleMFRC522()

try:
    while True:
        text = raw_input('Your Name: ')
        print("Now place tag next to the scanner to write")
        id, text = reader.write(text) 
        print("recorded")
        print(id)
        print(text)
        break
        
finally:
     GPIO.cleanup()
