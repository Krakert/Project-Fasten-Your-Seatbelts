import sqlite3

def read_alldata():
    with sqlite3.connect( "./databases/balldart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT * FROM game;'''
    cursor.execute(readData)
    scoreRecord = cursor.fetchall()
    print(scoreRecord)

read_alldata()
