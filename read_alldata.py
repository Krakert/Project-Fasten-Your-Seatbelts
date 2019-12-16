import sqlite3

read_alldata()

def read_alldata():
    with sqlite3.connect( "./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT * FROM account;'''
    cursor.execute(readData)
    scoreRecord = cursor.fetchall()
    print(scoreRecord)
