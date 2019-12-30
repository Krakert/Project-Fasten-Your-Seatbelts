import RPi.GPIO as GPIO
import sys
import signal
import sqlite3


from mfrc522 import SimpleMFRC522


def user_access(check):
    id = check
    with sqlite3.connect("./databases/balldart.db") as db:
        cursor = db.cursor()
    readData =('SELECT * FROM employees WHERE id = %(id)s', {'id': id})
    cursor.exectute(readData)
    if readData(True):
        active = 1
    else:
        active = 0
    insertData = '''UPDATE employees SET ACTIVE = ? WHERE id = ?'''
    cursor.exectute(insertData, active, id)

def read():
    reader = SimpleMFRC522()
    id, text = reader.read()
    print(id)
    print(text)
    user_acces(id)