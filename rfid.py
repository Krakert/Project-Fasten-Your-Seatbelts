#!/usr/bin/env python3

# import installed libraries
import RPi.GPIO as GPIO
import signal
from mfrc522 import SimpleMFRC522
import sqlHandling as SQL

import config

# This function reads out the id from the tag
def read():
    while True:
        reader = SimpleMFRC522()
        id, name = reader.read()
        print(id)
        print(config.gameModeCase)
    # return id


def write(name):
    reader = SimpleMFRC522()
    reader.write(name)
