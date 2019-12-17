import sqlite3


def update_score(score, username):
    with sqlite3.connect("balldart.db") as db:  # create connection to database
        cursor = db.cursor()
    updateData = '''UPDATE User
                    SET score = ?
                    WHERE username = ?;'''
    cursor.execute(updateData, [(score), (username)])
    db.commit()
