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
    # SQL.setupConnection()
    while True:
        if C.gameModeCase == 0:
            reader = SimpleMFRC522()
            uidTag, name = reader.read()
            print("UID given: %10d" % int(uidTag))

            with sqlite3.connect("./databases/balldart.db") as db:
                cursor = db.cursor()

            readData = '''SELECT id FROM employees WHERE id = ?'''
            cursor.execute(readData, [uidTag])
            databaseInfo = cursor.fetchall()
            print(len(databaseInfo))
            if len(databaseInfo) != 0:
                print("UID From database: %10d" % int(databaseInfo[0][0]))
                if int(databaseInfo[0][0]) == int(uidTag):
                    active = 1
                else:
                    active = 0
                print("Access: %s" % active)
                insertData = '''UPDATE employees SET active = ?, led = ?, servo = ? WHERE id = ?'''
                row = (active, 0, 0, int(uidTag))
                cursor.execute(insertData, row)
                db.commit()
        print("gamemode: %1d" % C.gameModeCase)


def write(name):
    reader = SimpleMFRC522()
    reader.write(name)
