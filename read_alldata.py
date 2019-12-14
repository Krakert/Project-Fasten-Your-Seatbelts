import sqlite3

def read_alldata():
    with sqlite3.connect("/dev/sqlite3/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT * FROM account;'''
    cursor.execute(readData)
    scoreRecord = cursor.fetchall()
    print(scoreRecord)

read_alldata()
