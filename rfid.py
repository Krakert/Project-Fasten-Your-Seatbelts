#!/usr/bin/env python3

# import installed libraries
import RPi.GPIO as GPIO
import signal
from mfrc522 import SimpleMFRC522
import sqlite3

# import files from our own project
import sqlHandling as SQL
import config as C


# This function reads out the id from the tag
def main():
    while True:
        if C.gameModeCase == 0:
            reader = SimpleMFRC522()
            uidTag, name = reader.read()
            SQL.updateEmployees(uidTag)

def write(name):
    reader = SimpleMFRC522()
    reader.write(name)
