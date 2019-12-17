import sqlite3

def new_board():
    with sqlite3.connect("./databases/balldart.db") as db:                      # create connection to database
        cursor = db.cursor()
    sql_create_account_table = '''CREATE TABLE IF NOT EXISTS game (
                                        id varchar(255) PRIMARY KEY,
                                        mode integer
                                    );'''

    cursor.execute(sql_create_account_table)

    sql_insertData = '''INSERT INTO game(id, mode) VALUES(?,?)'''
    cursor.execute(sql_insertData, [('board1'), (0)])
    db.commit()

def main():
    new_board()

if __name__ == '__main__':
    main()
