# This file only needs to run once
import sqlite3

def create_connection(db_file):
    """ Create a database connection to the SQLite database """
    conn = None
    conn = sqlite3.connect(db_file)
    print(sqlite3.version)
    if conn:
        conn.close()

def create_table(conn, create_table_sql):
    c = conn.cursor()
    c.execute(create_table_sql)

def account():
    database = "./databases/balldart.db"
    sql_create_account_table = '''CREATE TABLE IF NOT EXISTS account (
                                        id varchar(255) PRIMARY KEY,
                                        password varchar(255),
                                        totalPoints integer,
                                        highestPoints integer,
                                        numberOfRounds integer,
                                        latestRound integer
                                    );'''
    conn = create_connection(database)                                          # create a database connection
    create_table(conn, sql_create_account_table)                                # create account table

def game():
    with sqlite3.connect("./databases/balldart.db") as db:                      # create connection to database
        cursor = db.cursor()
    sql_create_game_table = '''CREATE TABLE IF NOT EXISTS game (
                                        id varchar(255) PRIMARY KEY,
                                        mode integer
                                    );'''
    cursor.execute(sql_create_game_table)
    sql_insertData = '''INSERT INTO game(id, mode) VALUES(?,?)'''
    cursor.execute(sql_insertData, [('board1'), (0)])
    db.commit()

if __name__ == '__main__':
    create_connection(r"./databases/balldart.db")
    account()
    game()
