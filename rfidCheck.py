# import RPi.GPIO as GPIO
# import sys
# import signal
import sqlite3

#
# from mfrc522 import SimpleMFRC522
rfid = "fakeID"
with sqlite3.connect("./databases/balldart.db") as db:
  cursor = db.cursor()
readData = '''SELECT * FROM employees WHERE id = ?'''
cursor.execute(readData, [rfid])
gameRecord = cursor.fetchall()
print(gameRecord[0][0])
if gameRecord[0][0] == "fakeID":
    active = 1
else:
    active = 0
print(active)
insertData = '''UPDATE employees SET active = ?, led = ?, servo = ? WHERE id = ?'''
row = (active,0,0,rfid)
cursor.execute(insertData,row)
db.commit()
# def read():
#     reader = SimpleMFRC522()
#     id, text = reader.read()
#     print(id)
#     print(text)
#     user_acces(id)
