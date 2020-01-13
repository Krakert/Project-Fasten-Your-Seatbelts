#!/usr/bin/env python3

# import installed libraries
import RPi.GPIO as GPIO
import signal
import time
from mfrc522 import SimpleMFRC522
import sqlite3

# import files from our own project
import sqlHandling as SQL
import config as C
import servo
import WS2812

dataFormDatabases  = 0

C.strip.begin()

# This function reads out the id from the tag
def main():
    global dataFormDatabases
    while True:
        if C.gameModeCase == 0 and SQL.checkEmployees() != 1:
            reader = SimpleMFRC522()
            uidTag, name = reader.read()
            SQL.updateEmployees(uidTag)

        if SQL.checkEmployees() == 1:
            dataFormDatabases = SQL.getTestData()
            if dataFormDatabases[0] == 1:
                WS2812.colorWipe(C.strip)
                time.sleep(1)
                WS2812.testPixel(C.strip, 7)
                SQL.setTestToZero()
            elif dataFormDatabases[1] == 1:
                servo.testServo()
                SQL.setTestToZero()
def write(name):
    reader = SimpleMFRC522()
    reader.write(name)
