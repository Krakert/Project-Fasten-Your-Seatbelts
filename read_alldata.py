import sqlite3


def read_alldata():
    with sqlite3.connect("dbballdart.db") as db:
        cursor = db.cursor()
    readData = '''SELECT * FROM User;'''
    cursor.execute(readData)
    scoreRecord = cursor.fetchall()
    print(scoreRecord)


read_alldata()
